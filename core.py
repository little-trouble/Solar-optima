import math
import random
import requests

def manhattan_distance_m(lat1, lon1, lat2, lon2):
    return abs(lat1 - lat2) * 111000 + abs(lon1 - lon2) * 111000

def calc_energy(A_panel, eff, H_sun, PR):
    return A_panel * eff * H_sun * PR

def calc_loss(dist, total_I, rho, wire_area, hours_use):
    R = rho * dist / wire_area
    P_loss = total_I**2 * R
    E_loss = P_loss * hours_use / 1000
    return E_loss, P_loss

def find_best_location(users, solar_lat, solar_lon, mode, total_I, rho, wire_area, hours_use, V_source, forbidden_zones=None):
    best_score = float('inf')
    best = None
    total_weight = sum([u[2] for u in users])

    for dlat in [i * 0.0001 for i in range(-50, 51)]:
        for dlon in [i * 0.0001 for i in range(-50, 51)]:
            test_lat, test_lon = solar_lat + dlat, solar_lon + dlon

            is_forbidden = False
            if forbidden_zones:
                for zone in forbidden_zones:
                    if zone[0] <= test_lat <= zone[1] and zone[2] <= test_lon <= zone[3]:
                        is_forbidden = True
                        break
            if is_forbidden:
                continue

            dist_source = manhattan_distance_m(test_lat, test_lon, solar_lat, solar_lon)
            R = rho * dist_source / wire_area
            v_drop = total_I * R
            if (v_drop / V_source) * 100 > 5:
                continue

            E_loss, P_loss = calc_loss(dist_source, total_I, rho, wire_area, hours_use)

            if mode == "efficiency":
                score = P_loss
            elif mode == "equity":
                score = sum([u[2] * manhattan_distance_m(test_lat, test_lon, u[0], u[1]) for u in users]) / total_weight

            if score < best_score:
                best_score = score
                best = (test_lat, test_lon, E_loss, P_loss, dist_source)
    return best

def run_monte_carlo(trials, sigma, H_base, users, solar_lat, solar_lon, mode, total_I, rho, wire_area, hours_use, V_source, forbidden_zones, eff, PR, a_panel_limit):
    areas = []
    failures = 0
    eff = 0.18
    PR = 0.75
    total_E_demand = sum([u[2] for u in users]) * 0.05
    for _ in range(trials):
        uncertainty = random.gauss(1.0, sigma)
        H_sim = H_base * uncertainty

        res = find_best_location(users, solar_lat, solar_lon, mode, total_I, rho, wire_area, hours_use, V_source, forbidden_zones)
        if res is None:
            failures += 1
            continue

        E_loss = res[2]
        A_req = (total_E_demand + E_loss) / (eff * H_sim * PR)
        areas.append(A_req)

        if A_req > a_panel_limit:
            failures += 1

    reliability = (1 - (failures / trials)) * 100
    return areas, reliability

def calc_carbon_reduction(E_produced_daily, wire_saved_m):
    direct = E_produced_daily * 365 * 0.4991
    indirect = wire_saved_m * 0.022 * 4
    return direct, indirect

def get_nasa_solar_data(lat, lon):
    url = f'https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={lon}&latitude={lat}&format=JSON'
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        h_sun_nasa = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']['ann']
        return float(h_sun_nasa)
    except:
        return 5.0