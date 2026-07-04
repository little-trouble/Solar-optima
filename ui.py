import streamlit as st

def init_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&family=Inter:wght@400;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
                
    .stApp {
        background: linear-gradient(180deg, #DAD7CD 0%, #D4DCB9 100%) !important;
    }
                
    html, body, [class*="css"], .stText, label, p, h1, h2, h3, input, select, button, textarea {
        font-family: 'Kanit', 'Inter', sans-serif !important;
    }
                
    .main-title {
        background: linear-gradient(90deg, #0A3323, #105666) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 700;
        font-size: 3rem;
    }
                
    .logo-text, h1, h2, h3, [data-testid="stHeader"] {
        color: #1A4D38 !important;
        -webkit-text-fill-color: #1A4D38 !important;
        font-weight: 700;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        background-color: #FFFDF0 !important;
        border: 1px solid #839958 !important;
        border-radius: 8px !important;
    } 
                
    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea,
    input[type="text"],
    input[type="number"],
    textarea {
        background-color: transparent !important;
        color: #1A4D38 !important;
        border: none !important;
    }
                
    div[data-testid="stNumberInput"] button {
        display: none !important;
    }
                
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        border: none !important; 
        box-shadow: none !important;
        background-color: #FFFDF0 !important;
    }
                
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 248, 0.75) !important;
        backdrop-filter: blur(8px);
        border: 1px solid #839958;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 6px 20px rgba(10, 51, 35, 0.04);
    }
                
    section[data-testid="stSidebar"] {
        background-color: #0A3323 !important;
        border-right: 1px solid #839958;
    }
                
    section[data-testid="stSidebar"] .stText,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #FFFDF0 !important;
    }

    .stButton>button {
        border: none;
        border-radius: 12px;
        background: #3A5A40 !important;
        color: #FFFDF0 !important;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(10, 51, 35, 0.18);
    }

    .stButton>button:hover {
        background: #588157 !important;
        transform: scale(1.03);
        box-shadow: 0 8px 20px rgba(16, 86, 102, 0.32);
    }

    .sus-card {
        background-color: rgba(255, 255, 248, 0.8) !important;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #839958;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    } 

    .sus-label { font-size: 1.1rem; font-weight: bold; color: #0A3323; }
    .sus-value { font-size: 2.8rem; font-weight: 800; color: #105666; line-height: 1; }
    .sus-unit { font-size: 1rem; color: #839958; margin-left: 5px; }
    .sus-desc { font-size: 0.9rem; color: #555555; margin-top: 8px; }
    </style>
    """, unsafe_allow_html=True)              

def draw_sus_card(label, value, unit, desc):
    st.markdown(f"""
    <div class="sus-card">
        <div class="sus-label">{label}</div>
        <div>
            <span class="sus-value">{value}</span>
            <span class="sus-unit">{unit}</span>
        </div>
        <div class="sus-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

init_styles()
