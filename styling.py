import streamlit as st

def inject_custom_css():
    """
    Injects a high-fidelity, premium CSS theme into the Streamlit application.
    This replaces standard Streamlit styles with a gorgeous glassmorphic dark UI.
    """
    css_content = """
    <style>
    /* Import modern Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Background and Layout Overrides */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #171a25 0%, #08090d 100%) !important;
        font-family: 'Outfit', sans-serif !important;
        color: #f1f5f9 !important;
    }
    
    /* Remove default Streamlit header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Main container card */
    .calc-card {
        background: rgba(22, 28, 41, 0.45);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 28px;
        padding: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5),
                    0 0 40px rgba(0, 242, 254, 0.03);
        margin: 20px auto;
        max-width: 580px;
    }

    /* Screen display */
    .led-screen {
        background: #06070a;
        border: 1px solid rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 22px 26px;
        box-shadow: inset 0 4px 12px rgba(0, 0, 0, 0.8),
                    0 0 1px rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
        text-align: right;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
    }
    
    .screen-formula {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        color: #64748b;
        overflow-x: auto;
        white-space: nowrap;
        min-height: 28px;
        letter-spacing: 0.5px;
    }
    
    .screen-result {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #00f2fe;
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.4);
        overflow-x: auto;
        white-space: nowrap;
        margin-top: 10px;
        letter-spacing: 1px;
    }

    .screen-error {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.3rem;
        color: #ef4444 !important;
        text-shadow: 0 0 8px rgba(239, 68, 68, 0.3) !important;
        margin-top: 15px;
    }

    /* Streamlit input custom styles */
    .stTextInput input {
        background-color: #090b10 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #e2e8f0 !important;
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
    }
    .stTextInput input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.2) !important;
    }

    /* Streamlit Button Customization */
    div.stButton > button {
        width: 100% !important;
        height: 62px !important;
        border-radius: 16px !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        background: rgba(30, 41, 59, 0.45) !important;
        color: #f1f5f9 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                    0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    
    /* Secondary/standard Button Hover */
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.025) !important;
        border-color: rgba(0, 242, 254, 0.35) !important;
        background: rgba(30, 41, 59, 0.75) !important;
        color: #00f2fe !important;
        box-shadow: 0 10px 15px -3px rgba(0, 242, 254, 0.15),
                    0 4px 6px -2px rgba(0, 242, 254, 0.05) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(1px) scale(0.97) !important;
    }

    /* Primary buttons (equal sign) */
    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #040508 !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(0, 242, 254, 0.25) !important;
    }
    
    div.stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #33f6ff 0%, #66b5ff 100%) !important;
        box-shadow: 0 12px 25px rgba(0, 242, 254, 0.45) !important;
        color: #040508 !important;
    }

    /* Scientific / Math Constants Buttons logic inside layout columns */
    .sci-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        font-weight: 600;
    }

    /* Sidebar glassmorphism */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 12, 18, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Interactive History panel styling */
    .history-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .history-item:hover {
        background: rgba(0, 242, 254, 0.04);
        border-color: rgba(0, 242, 254, 0.2);
    }
    
    .history-formula {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #94a3b8;
        word-break: break-all;
    }
    
    .history-result {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        color: #00f2fe;
        margin-top: 4px;
        text-align: right;
    }
    
    /* Info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.01);
        border-left: 3px solid #00f2fe;
        padding: 12px 16px;
        border-radius: 0 12px 12px 0;
        margin-bottom: 15px;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.1);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 242, 254, 0.3);
    }
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)
