"""
Mizan GRC - Premium UI Components
Beautifully designed Streamlit UI components with modern aesthetics.
Created by: Eng. Mohammad Abbas Alsaadon
"""

import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime


def load_css():
    """Load premium custom CSS styles with modern design."""
    st.markdown(
        """
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Root Variables for Premium Theme */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --accent-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --gold-gradient: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
        --emerald-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #4facfe;
        --gold-color: #f5af19;
        --emerald-color: #11998e;
        
        --bg-primary: #0f0f23;
        --bg-secondary: #1a1a2e;
        --bg-card: #16213e;
        --bg-elevated: #1f3460;
        
        --text-primary: #ffffff;
        --text-secondary: #a8b2d1;
        --text-muted: #8892b0;
        
        --border-color: rgba(255, 255, 255, 0.1);
        --shadow-color: rgba(0, 0, 0, 0.3);
        
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
    }
    
    /* Global Styles */
    html, body, [class*="css"] { 
        font-family: 'Inter', 'Noto Sans Arabic', sans-serif;
        background: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Main Container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Sidebar Premium Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }
    
    /* Premium Headers */
    h1 {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-weight: 700;
        color: var(--text-primary);
        border-bottom: 2px solid;
        border-image: var(--primary-gradient) 1;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    
    h3 {
        font-weight: 600;
        color: var(--accent-color);
    }
    
    /* Premium Buttons */
    .stButton > button {
        width: 100%;
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 14px 28px;
        border-radius: var(--radius-md);
        font-weight: 600;
        font-size: 15px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: var(--emerald-gradient);
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
    }
    
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.6);
    }
    
    /* Premium Cards */
    .metric-card {
        background: var(--bg-card);
        padding: 28px;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 32px var(--shadow-color);
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px var(--shadow-color);
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 12px 0;
    }
    
    .metric-label {
        font-size: 13px;
        color: var(--text-muted);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-radius: var(--radius-md);
        padding: 6px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: var(--radius-sm);
        padding: 12px 20px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-elevated);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient) !important;
        color: white !important;
    }
    
    /* Form Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-sm);
        color: var(--text-primary);
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Premium Policy Paper */
    .policy-paper {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        color: #1a1a2e;
        padding: 50px;
        border-radius: var(--radius-lg);
        border: none;
        font-family: 'Georgia', serif;
        line-height: 1.9;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        position: relative;
    }
    
    .policy-paper::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: var(--gold-gradient);
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }
    
    /* Disclaimer Box */
    .disclaimer-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: var(--radius-md);
        padding: 24px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
    }
    
    /* Success/Warning/Error Banners */
    .success-banner {
        background: var(--emerald-gradient);
        color: white;
        padding: 18px 24px;
        border-radius: var(--radius-md);
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(17, 153, 142, 0.3);
    }
    
    .warning-banner {
        background: var(--gold-gradient);
        color: white;
        padding: 18px 24px;
        border-radius: var(--radius-md);
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(245, 175, 25, 0.3);
    }
    
    .error-banner {
        background: var(--secondary-gradient);
        color: white;
        padding: 18px 24px;
        border-radius: var(--radius-md);
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(245, 87, 108, 0.3);
    }
    
    /* Premium Login Card */
    .login-card {
        background: var(--bg-card);
        border-radius: var(--radius-xl);
        padding: 48px;
        border: 1px solid var(--border-color);
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .login-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: var(--primary-gradient);
    }
    
    /* Brand Header */
    .brand-header {
        text-align: center;
        padding: 32px 24px;
        background: var(--bg-card);
        border-radius: var(--radius-xl);
        border: 1px solid var(--border-color);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    .brand-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .brand-name {
        font-family: 'Playfair Display', serif;
        font-size: 48px;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        position: relative;
    }
    
    .brand-tagline {
        color: var(--text-secondary);
        font-size: 14px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 8px;
        font-weight: 500;
    }
    
    .brand-version {
        color: var(--text-muted);
        font-size: 12px;
        margin-top: 12px;
    }
    
    /* Creator Footer */
    .creator-footer {
        text-align: center;
        margin-top: 40px;
        padding: 24px;
        background: var(--bg-secondary);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
    }
    
    .creator-name {
        font-weight: 600;
        background: var(--gold-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 16px;
    }
    
    .creator-title {
        color: var(--text-muted);
        font-size: 13px;
        margin-top: 4px;
    }
    
    .copyright {
        color: var(--text-muted);
        font-size: 11px;
        margin-top: 12px;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: var(--radius-md);
        overflow: hidden;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border-radius: var(--radius-sm);
        font-weight: 600;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background: var(--primary-gradient);
        border-radius: var(--radius-sm);
    }
    
    /* Spinners */
    .stSpinner > div {
        border-color: var(--primary-color) transparent transparent transparent;
    }
    
    /* Sidebar Logo Container */
    .sidebar-logo {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
    }
    
    .sidebar-brand {
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Domain Cards */
    .domain-card {
        background: var(--bg-card);
        border-radius: var(--radius-lg);
        padding: 24px;
        border: 1px solid var(--border-color);
        margin-bottom: 16px;
        transition: all 0.3s ease;
    }
    
    .domain-card:hover {
        border-color: var(--primary-color);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
</style>
""",
        unsafe_allow_html=True,
    )


def load_rtl_css():
    """Load comprehensive RTL-specific CSS for Arabic interface."""
    st.markdown(
        """<style>
/* Global RTL Direction */
.element-container, .stMarkdown, .stButton, .stSelectbox, .stTextInput, .stTextArea, .stSlider { 
    direction: rtl; 
    text-align: right; 
}

/* Tabs RTL */
.stTabs [data-baseweb="tab-list"] { 
    direction: rtl; 
    flex-direction: row-reverse;
}

/* Headers & Text */
h1, h2, h3, h4, h5, h6, p, li, span { 
    text-align: right; 
    direction: rtl;
}

/* Metric Cards */
.metric-card { 
    direction: rtl; 
    text-align: right;
}

/* Main Container */
div.block-container { 
    direction: rtl; 
    text-align: right; 
}

/* Arabic Content Styling */
.arabic-content {
    direction: rtl;
    text-align: right;
    font-family: 'Noto Sans Arabic', 'Segoe UI', 'Arial', sans-serif;
    line-height: 2.0;
    font-size: 16px;
}

.arabic-content h1, .arabic-content h2, .arabic-content h3, 
.arabic-content h4, .arabic-content h5 {
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 16px;
}

.arabic-content h2 {
    font-size: 22px;
    border-bottom: 2px solid;
    border-image: var(--primary-gradient, linear-gradient(135deg, #667eea 0%, #764ba2 100%)) 1;
    padding-bottom: 8px;
}

.arabic-content h3 {
    font-size: 18px;
    color: #4facfe;
}

.arabic-content p {
    margin-bottom: 12px;
    line-height: 2.0;
}

.arabic-content ul, .arabic-content ol {
    padding-right: 24px;
    padding-left: 0;
    margin-bottom: 16px;
}

.arabic-content li {
    margin-bottom: 8px;
    line-height: 1.8;
}

/* Arabic Tables */
.arabic-content table {
    width: 100%;
    direction: rtl;
    text-align: right;
    border-collapse: collapse;
    margin: 16px 0;
}

.arabic-content th, .arabic-content td {
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 12px;
    text-align: right;
}

.arabic-content th {
    background: rgba(102, 126, 234, 0.2);
    font-weight: 700;
}

/* Policy Paper Arabic */
.policy-paper-ar {
    direction: rtl;
    text-align: right;
    font-family: 'Noto Sans Arabic', 'Traditional Arabic', serif;
    line-height: 2.2;
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    color: #1a1a2e;
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

/* Strategy Output Arabic */
.strategy-output-ar {
    direction: rtl;
    text-align: right;
    font-family: 'Noto Sans Arabic', 'Segoe UI', sans-serif;
    line-height: 2.0;
}

.strategy-output-ar strong, .strategy-output-ar b {
    font-weight: 700;
    color: #4facfe;
}

/* Form elements RTL */
.stSelectbox > div, .stMultiSelect > div {
    direction: rtl;
}

/* Sidebar RTL */
section[data-testid="stSidebar"] {
    direction: rtl;
    text-align: right;
}

/* Expander RTL */
.streamlit-expanderHeader {
    direction: rtl;
    text-align: right;
}

/* Numbered lists Arabic */
.arabic-content ol {
    list-style: arabic-indic;
}

/* Brand elements RTL */
.brand-header, .creator-footer {
    direction: rtl;
}
</style>""",
        unsafe_allow_html=True,
    )


def render_brand_header(app_name: str, tagline: str, version: str, icon: str = "⚖️"):
    """Render a premium brand header."""
    st.markdown(f"""
    <div class="brand-header">
        <div style="font-size: 64px; margin-bottom: 16px;">{icon}</div>
        <h1 class="brand-name">{app_name}</h1>
        <p class="brand-tagline">{tagline}</p>
        <p class="brand-version">Version {version}</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_brand(app_name: str, icon: str = "⚖️"):
    """Render brand in sidebar."""
    st.markdown(f"""
    <div class="sidebar-logo">
        <div style="font-size: 40px; margin-bottom: 8px;">{icon}</div>
        <div class="sidebar-brand">{app_name}</div>
    </div>
    """, unsafe_allow_html=True)


def render_creator_footer(creator_name: str, creator_title: str = "GRC Solutions Architect", copyright_year: str = "2025"):
    """Render a premium creator footer."""
    st.markdown(f"""
    <div class="creator-footer">
        <div style="font-size: 11px; color: #8892b0; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px;">Created By</div>
        <div class="creator-name">{creator_name}</div>
        <div class="creator-title">{creator_title}</div>
        <div class="copyright">© {copyright_year} All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)


def metric_card(label: str, value: Any, color: str = "#667eea"):
    """Render a premium metric card."""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="background: linear-gradient(135deg, {color} 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def disclaimer_box(txt: dict):
    """Render a premium bilingual disclaimer box."""
    en_text = txt.get("disc_en", "AI-generated content. Verify with professionals.")
    ar_text = txt.get("disc_ar", "محتوى مُنشأ بالذكاء الاصطناعي. يُرجى التحقق مع المختصين.")
    
    st.markdown(f"""
    <div class="disclaimer-box">
        <div style="display: flex; gap: 24px;">
            <div style="flex: 1; padding-right: 24px; border-right: 1px solid rgba(102, 126, 234, 0.3);">
                <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #667eea; margin-bottom: 8px; font-weight: 600;">⚠️ Disclaimer</div>
                <p style="color: #a8b2d1; font-size: 13px; margin: 0; line-height: 1.6;">{en_text}</p>
            </div>
            <div style="flex: 1; direction: rtl; text-align: right;">
                <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #667eea; margin-bottom: 8px; font-weight: 600;">⚠️ إخلاء مسؤولية</div>
                <p style="color: #a8b2d1; font-size: 13px; margin: 0; line-height: 1.6; font-family: 'Noto Sans Arabic', sans-serif;">{ar_text}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def login_footer(creator_name: str):
    """Render premium login page footer."""
    st.markdown(f"""
    <div class="creator-footer">
        <div style="font-size: 11px; color: #8892b0; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px;">Designed & Developed By</div>
        <div class="creator-name">{creator_name}</div>
        <div class="creator-title">GRC Solutions Architect</div>
        <div class="copyright">© 2025 All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, icon: str = ""):
    """Render a premium section header."""
    icon_html = f'<span style="margin-right: 8px;">{icon}</span>' if icon else ""
    st.markdown(f"""
    <div style="margin: 24px 0 16px 0;">
        <h2 style="font-size: 22px; font-weight: 700; margin: 0; padding-bottom: 12px; border-bottom: 2px solid; border-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%) 1;">
            {icon_html}{title}
        </h2>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, icon: str = "ℹ️"):
    """Render an info card."""
    st.markdown(f"""
    <div style="background: rgba(102, 126, 234, 0.1); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 12px; padding: 20px; margin: 16px 0;">
        <div style="font-size: 20px; margin-bottom: 8px;">{icon}</div>
        <div style="font-weight: 600; color: #fff; margin-bottom: 8px;">{title}</div>
        <div style="color: #a8b2d1; font-size: 14px; line-height: 1.6;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def success_message(message: str):
    """Render a success message."""
    st.markdown(f"""
    <div class="success-banner">
        <span style="margin-right: 8px;">✅</span> {message}
    </div>
    """, unsafe_allow_html=True)


def warning_message(message: str):
    """Render a warning message."""
    st.markdown(f"""
    <div class="warning-banner">
        <span style="margin-right: 8px;">⚠️</span> {message}
    </div>
    """, unsafe_allow_html=True)


def error_message(message: str):
    """Render an error message."""
    st.markdown(f"""
    <div class="error-banner">
        <span style="margin-right: 8px;">❌</span> {message}
    </div>
    """, unsafe_allow_html=True)


def password_strength_indicator(strength_score: int):
    """Render a password strength indicator."""
    colors = ["#f5576c", "#f5af19", "#f5af19", "#38ef7d", "#11998e"]
    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    
    color = colors[min(strength_score, 4)]
    label = labels[min(strength_score, 4)]
    percentage = (strength_score + 1) * 20
    
    st.markdown(f"""
    <div style="margin: 12px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="font-size: 12px; color: #8892b0;">Password Strength</span>
            <span style="font-size: 12px; color: {color}; font-weight: 600;">{label}</span>
        </div>
        <div style="background: rgba(255,255,255,0.1); border-radius: 4px; height: 6px; overflow: hidden;">
            <div style="width: {percentage}%; height: 100%; background: linear-gradient(90deg, {color}, {colors[min(strength_score+1, 4)]}); border-radius: 4px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def api_status_indicator(is_connected: bool, message: str = ""):
    """Render an API connection status indicator."""
    if is_connected:
        st.markdown(f"""
        <div style="padding: 12px 16px; background: rgba(17, 153, 142, 0.15); border-radius: 8px; border: 1px solid rgba(56, 239, 125, 0.3); margin: 8px 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background: #38ef7d; border-radius: 50%; animation: pulse-green 2s infinite;"></div>
                <span style="color: #38ef7d; font-weight: 500; font-size: 14px;">✅ {message or 'AI Core Connected'}</span>
            </div>
        </div>
        <style>
            @keyframes pulse-green {{
                0%, 100% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.6; transform: scale(1.1); }}
            }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="padding: 12px 16px; background: rgba(245, 175, 25, 0.15); border-radius: 8px; border: 1px solid rgba(245, 175, 25, 0.3); margin: 8px 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 8px; height: 8px; background: #f5af19; border-radius: 50%;"></div>
                <span style="color: #f5af19; font-weight: 500; font-size: 14px;">⚠️ {message or 'Simulation Mode'}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_validation_errors(errors: list):
    """Render a list of validation errors."""
    if not errors:
        return
    
    error_items = "".join([f"<li style='margin-bottom: 4px;'>{error}</li>" for error in errors])
    
    st.markdown(f"""
    <div style="padding: 16px; background: rgba(245, 87, 108, 0.15); border-radius: 8px; border: 1px solid rgba(245, 87, 108, 0.3); margin: 12px 0;">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 20px;">❌</span>
            <div>
                <div style="color: #f5576c; font-weight: 600; margin-bottom: 8px;">Validation Errors</div>
                <ul style="color: #ffa0b4; font-size: 13px; margin: 0; padding-left: 16px; line-height: 1.6;">
                    {error_items}
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
