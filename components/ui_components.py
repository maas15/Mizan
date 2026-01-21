"""
Sentinel GRC - UI Components
Reusable Streamlit UI components.
"""

import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime


def load_css():
    """Load custom CSS styles."""
    st.markdown(
        """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #F8FAFC; 
        color: #1E293B; 
    }
    
    section[data-testid="stSidebar"] { 
        background-color: #FFFFFF; 
        border-right: 1px solid #E2E8F0; 
    }
    
    .metric-card { 
        background: #FFFFFF; 
        padding: 24px; 
        border-radius: 12px; 
        border: 1px solid #E2E8F0; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); 
        text-align: center; 
    }
    
    .metric-value { 
        font-size: 28px; 
        font-weight: 800; 
        color: #2563EB; 
        margin: 8px 0; 
    }
    
    .metric-label { 
        font-size: 12px; 
        color: #64748B; 
        text-transform: uppercase; 
        font-weight: 600; 
    }
    
    .stButton > button { 
        width: 100%; 
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); 
        color: white; 
        border: none; 
        padding: 12px; 
        border-radius: 8px; 
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        transform: translateY(-1px);
    }
    
    .policy-paper { 
        background-color: #FFFFFF; 
        color: #0F172A; 
        padding: 50px; 
        border-radius: 4px; 
        border: 1px solid #E2E8F0; 
        font-family: 'Times New Roman', serif; 
        line-height: 1.8; 
    }
    
    .disclaimer-box { 
        background-color: #EFF6FF; 
        border: 1px solid #BFDBFE; 
        border-radius: 8px; 
        padding: 20px; 
        margin-bottom: 30px; 
        color: #1E3A8A; 
        font-size: 14px; 
    }
    
    .disclaimer-split { 
        display: flex; 
        gap: 20px; 
    }
    
    .disclaimer-en { 
        width: 50%; 
        border-right: 1px solid #BFDBFE; 
        padding-right: 20px; 
    }
    
    .disclaimer-ar { 
        width: 50%; 
        direction: rtl; 
        text-align: right; 
    }
    
    .login-footer { 
        text-align: center; 
        margin-top: 50px; 
        color: #64748B; 
        font-size: 14px; 
        font-weight: 600; 
        border-top: 1px solid #E2E8F0; 
        padding-top: 20px; 
    }
    
    .success-banner {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .warning-banner {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .error-banner {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
    }
    
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #2563EB;
    }
</style>
""",
        unsafe_allow_html=True,
    )


def load_rtl_css():
    """Load RTL-specific CSS for Arabic interface."""
    st.markdown(
        """<style>
.element-container, .stMarkdown, .stButton, .stSelectbox, .stTextInput, .stTextArea, .stSlider { 
    direction: rtl; 
    text-align: right; 
}
.stTabs [data-baseweb="tab-list"] { direction: rtl; }
h1, h2, h3, h4, p { text-align: right; }
.metric-card { direction: rtl; }
div.block-container { direction: rtl; text-align: right; }
</style>""",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: Any, color: str = "#2563EB"):
    """
    Render a metric card.
    
    Args:
        label: Metric label
        value: Metric value
        color: Value color (hex)
    """
    st.markdown(
        f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value" style="color: {color}">{value}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def disclaimer_box(translations: Dict[str, str]):
    """
    Render the disclaimer box.
    
    Args:
        translations: Translation dictionary
    """
    disclaimer_html = f"""
    <div class='disclaimer-box'>
        <div style="text-align: center; margin-bottom: 10px; color: #DC2626; font-weight: bold;">
            ⚠️ {translations.get('disclaimer_title', 'Important Disclaimer')}
        </div>
        <div class="disclaimer-split">
            <div class="disclaimer-en">
                <strong>AI-Driven Assistant:</strong> Outputs require expert review.<br>
                <strong>Data Privacy:</strong> Uploads are transient (RAM-only) and never saved.<br>
                <span style="color: #DC2626;"><strong>Do not use critical/PII data during testing.</strong></span>
            </div>
            <div class="disclaimer-ar">
                <strong>المستشار الذكي:</strong> مساعدك المدعوم بالذكاء الاصطناعي، ولا يستغني عن رأيك بالتأكيد.<br>
                <strong>خصوصية البيانات:</strong> الملفات المرفقة تُعالج مؤقتاً ولا تُحفظ.<br>
                <span style="color: #DC2626;"><strong>يرجى عدم استخدام بيانات حساسة أثناء الاختبار.</strong></span>
            </div>
        </div>
    </div>
    """
    st.markdown(disclaimer_html, unsafe_allow_html=True)


def login_footer(creator_name: str):
    """
    Render the login footer with creator info.
    
    Args:
        creator_name: Creator's name
    """
    st.markdown(
        f"<div class='login-footer'>Created by: {creator_name}</div>",
        unsafe_allow_html=True
    )


def section_header(title: str):
    """
    Render a section header.
    
    Args:
        title: Section title
    """
    st.markdown(f"<div class='section-header'>{title}</div>", unsafe_allow_html=True)


def info_banner(message: str, banner_type: str = "info"):
    """
    Render an info banner.
    
    Args:
        message: Banner message
        banner_type: Type (info, success, warning, error)
    """
    class_map = {
        "success": "success-banner",
        "warning": "warning-banner",
        "error": "error-banner",
        "info": "disclaimer-box"
    }
    css_class = class_map.get(banner_type, "disclaimer-box")
    st.markdown(f"<div class='{css_class}'>{message}</div>", unsafe_allow_html=True)


def render_validation_errors(errors: list):
    """
    Render validation errors.
    
    Args:
        errors: List of error messages
    """
    if errors:
        error_html = "<div class='error-banner'><strong>Validation Errors:</strong><ul>"
        for error in errors:
            error_html += f"<li>{error}</li>"
        error_html += "</ul></div>"
        st.markdown(error_html, unsafe_allow_html=True)


def api_status_indicator(is_connected: bool):
    """
    Render API connection status.
    
    Args:
        is_connected: Whether API is connected
    """
    if is_connected:
        st.success("✅ Connected to AI Core")
    else:
        st.warning("⚠️ AI Core unavailable - Simulation Mode active")


def lockout_warning(remaining_seconds: int, remaining_attempts: int = None):
    """
    Render account lockout warning.
    
    Args:
        remaining_seconds: Seconds until lockout expires
        remaining_attempts: Remaining login attempts (if not locked)
    """
    if remaining_seconds:
        minutes = remaining_seconds // 60
        st.error(f"🔒 Account locked. Try again in {minutes} minute(s).")
    elif remaining_attempts is not None and remaining_attempts <= 2:
        st.warning(f"⚠️ {remaining_attempts} login attempt(s) remaining before lockout.")


def password_strength_indicator(score: int):
    """
    Render password strength indicator.
    
    Args:
        score: Password strength score (0-100)
    """
    if score >= 80:
        color = "#10B981"
        label = "Strong"
    elif score >= 50:
        color = "#F59E0B"
        label = "Medium"
    else:
        color = "#EF4444"
        label = "Weak"
    
    st.markdown(
        f"""
        <div style="margin-top: 8px;">
            <div style="background: #E2E8F0; border-radius: 4px; height: 8px; overflow: hidden;">
                <div style="background: {color}; width: {score}%; height: 100%;"></div>
            </div>
            <div style="font-size: 12px; color: {color}; margin-top: 4px;">Password Strength: {label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
