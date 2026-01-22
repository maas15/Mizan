"""
Sentinel GRC - Main Application (Enhanced)
Enterprise GRC Operating System with Big4-level AI-powered strategy generation.

Author: Eng. Mohammad Abbas Alsaadon
Version: 2.1.0 (Enhanced)

Fixes:
1. Big4-level strategy output quality
2. Technology dropdown menus for easier selection
3. Arabic policy context improved
4. Domain-specific risk radars for DT and Global Standards
5. Arabic translation for strategy section titles
"""

import streamlit as st
import time
import logging
import pandas as pd
from datetime import datetime
from io import BytesIO
import sys
import os
from pathlib import Path

# =============================================================================
# PATH SETUP & ENVIRONMENT LOADING
# =============================================================================

APP_DIR = Path(__file__).parent.absolute()

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

try:
    from dotenv import load_dotenv
    env_file = APP_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded .env from: {env_file}")
    else:
        load_dotenv()
except ImportError:
    print("⚠️ python-dotenv not installed")

_api_key = os.getenv("OPENAI_API_KEY")
if _api_key:
    print(f"✅ OPENAI_API_KEY found: {_api_key[:8]}...{_api_key[-4:]}")
else:
    print("❌ OPENAI_API_KEY not found")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =============================================================================
# IMPORTS - Each import block separated for better error handling
# =============================================================================

# Core config
try:
    from config import config, security_config, domain_config
except ImportError as e:
    print(f"❌ Config import error: {e}")
    raise

# Database services
try:
    from services.db_service import db_service, user_repo, risk_repo, project_repo, audit_log, stats_service
except ImportError as e:
    print(f"❌ Database service import error: {e}")
    raise

# Security utilities
try:
    from utils.security import password_hasher, password_validator, rate_limiter, input_sanitizer
except ImportError as e:
    print(f"❌ Security utils import error: {e}")
    raise

# Text processing
try:
    from utils.text_processing import pdf_extractor, text_processor, roadmap_parser
except ImportError as e:
    print(f"❌ Text processing import error: {e}")
    raise

# Validation
try:
    from utils.validation import InputValidator, FormValidator, DataValidator, FileValidator
except ImportError as e:
    print(f"❌ Validation import error: {e}")
    raise

# Frameworks
try:
    from data.frameworks import get_framework_pack
except ImportError as e:
    print(f"❌ Frameworks import error: {e}")
    raise

# UI Components
try:
    from components.ui_components import (
        load_css, load_rtl_css, metric_card, disclaimer_box,
        login_footer, api_status_indicator, password_strength_indicator, render_validation_errors
    )
except ImportError as e:
    print(f"❌ UI components import error: {e}")
    raise

# AI Service - try enhanced first
try:
    from services.ai_service_v2 import ai_service, ResponseType
    print("✅ Using enhanced AI service")
except ImportError:
    try:
        from services.ai_service import ai_service, ResponseType
        print("⚠️ Using standard AI service")
    except ImportError as e:
        print(f"❌ AI service import error: {e}")
        raise

# Risk Data - try enhanced first
try:
    from data.risk_data_v2 import get_risk_data
    print("✅ Using enhanced risk data")
except ImportError:
    try:
        from data.risk_data import get_risk_data
        print("⚠️ Using standard risk data")
    except ImportError as e:
        print(f"❌ Risk data import error: {e}")
        raise

# Translations - try enhanced first
try:
    from data.translations_v2 import (
        get_translation, is_rtl_language, get_tech_options, 
        get_org_structure_options, get_section_title, TRANSLATIONS
    )
    HAS_ENHANCED_TRANSLATIONS = True
    print("✅ Using enhanced translations")
except ImportError:
    try:
        from data.translations import get_translation, is_rtl_language, TRANSLATIONS
        HAS_ENHANCED_TRANSLATIONS = False
        print("⚠️ Using standard translations")
        
        def get_tech_options(domain_code):
            return {}
        def get_org_structure_options(domain_code, lang):
            return ["Standard Structure"]
        def get_section_title(key, lang):
            return key
    except ImportError as e:
        print(f"❌ Translations import error: {e}")
        raise

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON, layout="wide")
load_css()

# =============================================================================
# SESSION MANAGER
# =============================================================================

class SessionManager:
    PREFIX = "sentinel_"
    
    @classmethod
    def get(cls, key: str, default=None):
        return st.session_state.get(f"{cls.PREFIX}{key}", default)
    
    @classmethod
    def set(cls, key: str, value):
        st.session_state[f"{cls.PREFIX}{key}"] = value
    
    @classmethod
    def is_logged_in(cls) -> bool:
        return cls.get("logged_in", False)
    
    @classmethod
    def get_username(cls) -> str:
        return cls.get("username", "")
    
    @classmethod
    def login(cls, username: str):
        cls.set("logged_in", True)
        cls.set("username", username)
    
    @classmethod
    def logout(cls):
        cls.set("logged_in", False)
        cls.set("username", "")

# =============================================================================
# AUTHENTICATION
# =============================================================================

def handle_login(username: str, password: str) -> tuple:
    username = input_sanitizer.sanitize_username(username)
    is_locked, remaining = rate_limiter.is_locked(username)
    if is_locked:
        return False, f"Account locked. Try again in {remaining // 60} minute(s)."
    
    success, user_data = user_repo.verify_password(username, password)
    now_locked = rate_limiter.record_attempt(username, success)
    
    if success:
        audit_log.log(action="LOGIN_SUCCESS", username=username)
        return True, None
    else:
        remaining_attempts = rate_limiter.get_remaining_attempts(username)
        if now_locked:
            return False, "Too many failed attempts. Account locked."
        return False, f"Invalid credentials. {remaining_attempts} attempt(s) remaining."

def handle_registration(username: str, password: str) -> tuple:
    username_result = InputValidator.validate_username(username)
    if not username_result.is_valid:
        return False, username_result.errors[0]
    
    password_result = password_validator.validate(password)
    if not password_result.is_valid:
        return False, password_result.errors[0]
    
    if user_repo.create(username_result.sanitized_value, password):
        audit_log.log(action="USER_REGISTERED", username=username_result.sanitized_value)
        return True, None
    return False, "Username already exists."

# =============================================================================
# LOGIN PAGE
# =============================================================================

def render_login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Display logo if available
        logo_path = APP_DIR / "logo.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            # Fallback to text header
            st.markdown(
                f"""<div style="background-color: #FFFFFF; padding: 40px; border-radius: 12px; 
                    border: 1px solid #E2E8F0; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #2563EB; margin-bottom: 0;">{config.APP_ICON} {config.APP_NAME}</h1>
                    <p style="color: #64748B;">Enterprise GRC Operating System</p>
                    <p style="color: #94A3B8; font-size: 12px;">v{config.APP_VERSION}</p>
                </div>""", unsafe_allow_html=True)
        
        st.markdown(
            f"""<div style="text-align: center; padding: 10px;">
                <p style="color: #64748B; margin: 0;">Enterprise GRC Operating System</p>
                <p style="color: #94A3B8; font-size: 12px;">v{config.APP_VERSION}</p>
            </div>""", unsafe_allow_html=True)
        
        lang_opt = st.radio("language", ["English", "العربية"], horizontal=True, label_visibility="collapsed")
        txt = get_translation(lang_opt)
        disclaimer_box(txt)
        
        tab_login, tab_register = st.tabs([txt.get("login_title", "Sign In"), txt.get("register_title", "Register")])
        
        with tab_login:
            with st.form("login_form"):
                username = st.text_input(txt.get("username", "Username"))
                password = st.text_input(txt.get("password", "Password"), type="password")
                if st.form_submit_button(txt.get("login_btn", "Enter")):
                    if username and password:
                        success, error = handle_login(username, password)
                        if success:
                            SessionManager.login(username)
                            st.rerun()
                        else:
                            st.error(error)
                    else:
                        st.warning("Please enter username and password")
        
        with tab_register:
            with st.form("register_form"):
                new_username = st.text_input(txt.get("new_user", "New Username"))
                new_password = st.text_input(txt.get("new_pass", "New Password"), type="password")
                if new_password:
                    strength = password_validator.validate(new_password)
                    password_strength_indicator(strength.strength_score)
                if st.form_submit_button(txt.get("register_btn", "Create Account")):
                    if new_username and new_password:
                        success, error = handle_registration(new_username, new_password)
                        if success:
                            st.success("Account created! You can now login.")
                        else:
                            st.error(error)
        
        login_footer(config.CREATOR_NAME)

# =============================================================================
# ADMIN DASHBOARD
# =============================================================================

def render_admin_dashboard():
    st.markdown("## 🛠️ Admin Command Center")
    stats = stats_service.get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Total Users", stats["user_count"], "#3B82F6")
    with col2:
        metric_card("Total Risks", stats["risk_count"], "#F59E0B")
    with col3:
        metric_card("Total Projects", stats["project_count"], "#10B981")
    
    st.markdown("### User Management")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(stats["users"], use_container_width=True)
    with col2:
        user_list = stats["users"]["username"].tolist()
        user_to_delete = st.selectbox("Select User to Delete", user_list)
        if st.button("❌ Delete User", type="primary"):
            if user_to_delete != security_config.ADMIN_USERNAME:
                if user_repo.delete(user_to_delete):
                    st.success(f"Deleted: {user_to_delete}")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Cannot delete admin")
    
    if st.button("Logout"):
        SessionManager.logout()
        st.rerun()

# =============================================================================
# STRATEGY HELPERS
# =============================================================================

def build_roadmap(domain_code: str, org_inputs: dict, gap_summary: dict) -> pd.DataFrame:
    size = org_inputs.get("size", "Small")
    size_factor = 1.0
    if "Medium" in size or "متوسطة" in size:
        size_factor = 1.6
    elif "Large" in size or "كبيرة" in size:
        size_factor = 2.5
    
    initiatives = [
        ["0–3 months", "Establish governance framework", 3 * size_factor, 300000 * size_factor, "GRC Lead", "Policy coverage %"],
        ["0–3 months", "Implement IAM/MFA baseline", 4 * size_factor, 800000 * size_factor, "IAM Lead", "MFA coverage %"],
        ["3–12 months", "Deploy SIEM & monitoring", 6 * size_factor, 1200000 * size_factor, "SOC Lead", "MTTD"],
        ["3–12 months", "Third-party risk program", 3 * size_factor, 350000 * size_factor, "Vendor Risk", "Vendor coverage %"],
        ["12–36 months", "Zero Trust architecture", 12 * size_factor, 2000000 * size_factor, "Security Arch", "Segmentation %"],
    ]
    
    df = pd.DataFrame(initiatives, columns=["Phase", "Initiative", "Duration", "Cost", "Role", "KPI"])
    df["Duration"] = df["Duration"].round(1)
    df["Cost"] = df["Cost"].round(0)
    
    start = datetime.today()
    df["Start"] = [start + pd.DateOffset(months=i * 3) for i in range(len(df))]
    df["Finish"] = [s + pd.DateOffset(months=int(d)) for s, d in zip(df["Start"], df["Duration"])]
    
    return df

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def render_main_application():
    username = SessionManager.get_username()
    
    if username == security_config.ADMIN_USERNAME:
        render_admin_dashboard()
        return
    
    with st.sidebar:
        # Display logo in sidebar
        logo_path = APP_DIR / "logo.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        
        lang_opt = st.radio("Language", ["English", "العربية"], horizontal=True, label_visibility="collapsed")
        txt = get_translation(lang_opt)
        
        if is_rtl_language(lang_opt):
            load_rtl_css()
        
        st.markdown("---")
        st.markdown(f"## {txt['sidebar_title']}")
        st.caption(txt['sidebar_caption'])
        st.markdown(f"**{config.CREATOR_NAME}**")
        st.caption(f"👤 {username}")
        
        with st.expander(txt.get("settings", "Settings")):
            if st.button(txt.get("clear_hist", "Clear History")):
                risk_repo.delete_by_owner(username)
                project_repo.delete_by_owner(username)
                st.success("Cleared!")
                st.rerun()
        
        if st.button(txt["logout"]):
            SessionManager.logout()
            st.rerun()
        
        st.markdown("---")
        if ai_service.is_available:
            st.success("✅ Connected to AI Core")
        else:
            st.warning("⚠️ AI Core unavailable - Simulation Mode")
            with st.expander("Debug Info"):
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    st.code(f"Key: {api_key[:8]}...{api_key[-4:]}")
                else:
                    st.error("No OPENAI_API_KEY")
    
    st.title(f"{config.APP_ICON} {txt['sidebar_title']}")
    
    # Metrics
    df_projects = project_repo.get_by_owner(username)
    df_risks = risk_repo.get_by_owner(username)
    total_budget = df_projects["Cost"].sum() if not df_projects.empty and "Cost" in df_projects.columns else 0
    critical_risks = len(df_risks[df_risks["risk_level"] == "CRITICAL"]) if not df_risks.empty and "risk_level" in df_risks.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card(txt["metrics"][0], f"{config.DEFAULT_COMPLIANCE_SCORE}%", "#10B981")
    with col2:
        metric_card(txt["metrics"][1], len(df_projects), "#3B82F6")
    with col3:
        metric_card(txt["metrics"][2], f"{total_budget:,.0f}", "#F59E0B")
    with col4:
        metric_card(txt["metrics"][3], critical_risks, "#EF4444")
    
    st.markdown("---")
    
    # Domain tabs
    domain_labels = txt["domains"]
    main_tabs = st.tabs(domain_labels)
    
    for i, domain_name in enumerate(domain_labels):
        logic_code = domain_config.get_domain_code(domain_name)
        
        with main_tabs[i]:
            st.markdown(f"## {domain_name}")
            func_tabs = st.tabs(txt["func_tabs"])
            
            with func_tabs[0]:
                render_strategy_tab(username, domain_name, logic_code, txt, lang_opt)
            with func_tabs[1]:
                render_policy_tab(username, domain_name, logic_code, txt, lang_opt)
            with func_tabs[2]:
                render_audit_tab(username, domain_name, logic_code, txt)
            with func_tabs[3]:
                render_risk_tab(username, domain_name, logic_code, txt)
            with func_tabs[4]:
                render_roadmap_tab(username, domain_name, logic_code, txt)


def render_strategy_tab(username: str, domain_name: str, logic_code: str, txt: dict, lang_opt: str):
    """Render strategy pipeline with technology dropdowns and download options."""
    step_key = f"step_{logic_code}"
    current_step = SessionManager.get(step_key, 1)
    reg_list = domain_config.get_domain_regulations(domain_name)
    
    # Get section titles based on language
    section_titles = txt.get("strategy_sections", {
        "vision": "Vision", "gaps": "Gaps", "pillars": "Pillars", 
        "roadmap": "Roadmap", "kpis": "KPIs", "confidence": "Confidence"
    })
    
    if current_step == 1:
        st.info(f"{txt['step1']} - {domain_name}")
        
        with st.form(f"scope_{logic_code}"):
            col1, col2 = st.columns(2)
            
            org_name = col1.text_input(txt["ui_form"]["org_name"], value="My Organization")
            sector = col2.selectbox(txt["ui_form"]["sector"], 
                ["Government", "Banking/Finance", "Healthcare", "Energy", "Telecom", "Retail", "Manufacturing"])
            
            sel_reg = col1.multiselect(txt["ui_form"]["reg"], reg_list, 
                default=reg_list[:2] if len(reg_list) >= 2 else reg_list)
            
            # Use translated org sizes if available
            org_sizes = txt.get("org_sizes", ["Small (<100)", "Medium (100-1000)", "Large (1000+)"])
            size = col2.selectbox(txt["ui_form"]["size"], org_sizes)
            
            budget = col1.selectbox(txt["ui_form"]["budget"], ["< 1M", "1M-5M", "5M-20M", "20M+"])
            horizon = col2.slider(txt["ui_form"]["horizon"], 12, 60, 36)
            
            st.markdown(f"### {txt['ui_form']['current_state']}")
            
            # Organizational structure dropdown
            if HAS_ENHANCED_TRANSLATIONS:
                org_structures = get_org_structure_options(logic_code, lang_opt)
                org_structure = st.selectbox(
                    txt["ui_form"].get("org_structure", "Organization Structure"), 
                    org_structures
                )
                
                # Technology stack multi-select by category
                st.markdown(f"#### {txt['ui_form'].get('tech_select', 'Select Technologies')}")
                tech_options = get_tech_options(logic_code)
                selected_tech = []
                
                if tech_options:
                    tech_cols = st.columns(2)
                    col_idx = 0
                    for category, technologies in tech_options.items():
                        with tech_cols[col_idx % 2]:
                            selected = st.multiselect(category, technologies, key=f"tech_{logic_code}_{category}")
                            selected_tech.extend(selected)
                        col_idx += 1
                    tech_stack = ", ".join(selected_tech) if selected_tech else "Not specified"
                else:
                    tech_stack = st.text_input(txt["ui_form"]["tech_stack"])
                    org_structure = "Standard"
            else:
                tech_stack = st.text_input(txt["ui_form"]["tech_stack"])
                org_structure = "Standard"
            
            # Challenges
            pain = st.text_area(txt["ui_form"]["challenges"], 
                placeholder="Describe key challenges, pain points, and current gaps...")
            
            if st.form_submit_button(txt["btn_start"]):
                SessionManager.set(f"inputs_{logic_code}", {
                    "org": org_name, "sec": sector, "reg": sel_reg, "size": size,
                    "bud": budget, "time": horizon, 
                    "tech": tech_stack,
                    "org_structure": org_structure,
                    "pain": pain
                })
                SessionManager.set(step_key, 2)
                st.rerun()
    
    elif current_step == 2:
        st.info(txt["step2"])
        inputs = SessionManager.get(f"inputs_{logic_code}", {})
        
        doc_lang = st.selectbox(txt["doc_lang"], txt["doc_opts"], key=f"lang_{logic_code}")
        
        # Show language instruction
        if doc_lang in ["Arabic", "العربية"]:
            st.caption("📝 Strategy will be generated entirely in Arabic (الاستراتيجية ستكون باللغة العربية بالكامل)")
        elif doc_lang in ["Bilingual", "ثنائي اللغة"]:
            st.caption("📝 Strategy will be bilingual - English followed by Arabic translation")
        
        if st.button(txt["btn_gen"], key=f"gen_{logic_code}"):
            with st.spinner("🚀 Generating Big4-Level Strategy..."):
                gap_summary = {"compliance_score": 75, "gap_count": 5, "top_gap_controls": {"Unified.GOV": 2}}
                roadmap_df = build_roadmap(logic_code, inputs, gap_summary)
                
                # Map UI language to actual language
                lang_map = {"الإنجليزية": "English", "العربية": "Arabic", "ثنائي اللغة": "Bilingual"}
                actual_lang = lang_map.get(doc_lang, doc_lang)
                
                ai_context = {
                    "org_name": inputs.get("org"), 
                    "sector": inputs.get("sec"),
                    "size": inputs.get("size"), 
                    "domain": domain_name,
                    "frameworks": inputs.get("reg", []), 
                    "tech": inputs.get("tech"),
                    "org_structure": inputs.get("org_structure"),
                    "challenges": inputs.get("pain"), 
                    "budget": inputs.get("bud"),
                    "horizon": inputs.get("time"), 
                    "language": actual_lang,
                    "gap_data": gap_summary
                }
                
                ai_response = ai_service.generate_strategy(ai_context)
                
                sections = text_processor.extract_sections(ai_response.content, "|||")
                while len(sections) < 6:
                    sections.append("N/A")
                
                out_sections = {
                    "vision": sections[0],
                    "gaps": sections[1],
                    "pillars": sections[2],
                    "roadmap": sections[3],
                    "kpis": sections[4],
                    "confidence": sections[5],
                }
                
                SessionManager.set(f"out_{logic_code}", out_sections)
                SessionManager.set(f"roadmap_{logic_code}", roadmap_df)
                SessionManager.set(f"doc_lang_{logic_code}", actual_lang)
                SessionManager.set(f"org_name_{logic_code}", inputs.get("org", "Organization"))
                
                project_repo.save_roadmap(username, domain_name, roadmap_df)
                
                SessionManager.set(step_key, 3)
                st.rerun()
    
    elif current_step == 3:
        st.success("✅ Strategy Generated")
        
        out = SessionManager.get(f"out_{logic_code}", {})
        roadmap_df = SessionManager.get(f"roadmap_{logic_code}", pd.DataFrame())
        doc_lang = SessionManager.get(f"doc_lang_{logic_code}", "English")
        org_name = SessionManager.get(f"org_name_{logic_code}", "Organization")
        
        # Download buttons row
        st.markdown("### 📥 Download Options")
        dl_col1, dl_col2, dl_col3 = st.columns(3)
        
        with dl_col1:
            # Strategy DOCX download
            try:
                from utils.export_utils import generate_strategy_docx
                strategy_docx = generate_strategy_docx(org_name, domain_name, out, roadmap_df, doc_lang)
                if strategy_docx:
                    st.download_button(
                        label="📄 Strategy (Word)",
                        data=strategy_docx,
                        file_name=f"strategy_{logic_code}_{datetime.now().strftime('%Y%m%d')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_strat_{logic_code}"
                    )
            except Exception as e:
                st.caption(f"Word export unavailable: {e}")
        
        with dl_col2:
            # Roadmap Excel download
            try:
                from utils.export_utils import generate_roadmap_excel
                roadmap_excel = generate_roadmap_excel(roadmap_df, org_name, domain_name)
                st.download_button(
                    label="📊 Roadmap (Excel)",
                    data=roadmap_excel,
                    file_name=f"roadmap_{logic_code}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"dl_road_{logic_code}"
                )
            except Exception as e:
                st.caption(f"Excel export unavailable: {e}")
        
        with dl_col3:
            # Combined strategy as markdown/text
            full_strategy = f"# Strategic Roadmap: {org_name}\n\n"
            full_strategy += f"**Domain:** {domain_name}\n"
            full_strategy += f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
            for key in ["vision", "gaps", "pillars", "roadmap", "kpis", "confidence"]:
                full_strategy += f"## {section_titles.get(key, key)}\n\n{out.get(key, 'N/A')}\n\n"
            
            st.download_button(
                label="📝 Strategy (Text)",
                data=full_strategy,
                file_name=f"strategy_{logic_code}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                key=f"dl_md_{logic_code}"
            )
        
        st.markdown("---")
        
        # Use translated section titles
        tab_labels = [
            section_titles.get("vision", "Vision"),
            section_titles.get("gaps", "Gaps"),
            section_titles.get("pillars", "Pillars"),
            section_titles.get("roadmap", "Roadmap"),
            section_titles.get("kpis", "KPIs")
        ]
        
        tabs = st.tabs(tab_labels)
        section_keys = ["vision", "gaps", "pillars", "roadmap", "kpis"]
        
        # Apply RTL styling for Arabic
        rtl_style = "direction: rtl; text-align: right;" if doc_lang == "Arabic" else ""
        
        for tab, key in zip(tabs, section_keys):
            with tab:
                content = out.get(key, "N/A")
                if rtl_style:
                    st.markdown(f"<div style='{rtl_style}'>{content}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(content)
        
        if not roadmap_df.empty:
            st.markdown("### Implementation Timeline")
            st.dataframe(roadmap_df[["Phase", "Initiative", "Duration", "Cost", "Role", "KPI"]], use_container_width=True)
        
        if st.button(txt["btn_reset"], key=f"reset_{logic_code}"):
            SessionManager.set(step_key, 1)
            st.rerun()


def render_policy_tab(username: str, domain_name: str, logic_code: str, txt: dict, lang_opt: str):
    """Render policy lab with improved Arabic support and download option."""
    reg_list = domain_config.get_domain_regulations(domain_name)
    
    col1, col2 = st.columns(2)
    framework = col1.selectbox(txt.get("lbl_reg", "Framework"), reg_list, key=f"pol_fw_{logic_code}")
    policy_name = col2.text_input(txt.get("policy_name", "Policy Name"), key=f"pol_name_{logic_code}")
    
    doc_lang = st.selectbox(txt["doc_lang"], txt["doc_opts"], key=f"pol_lang_{logic_code}")
    
    # Map UI language to actual language for API
    lang_map = {"الإنجليزية": "English", "العربية": "Arabic", "ثنائي اللغة": "Bilingual"}
    actual_lang = lang_map.get(doc_lang, doc_lang)
    
    # Show language instruction
    if actual_lang == "Arabic":
        st.caption("📝 Policy will be generated entirely in Arabic (السياسة ستكون باللغة العربية بالكامل)")
    
    if st.button(txt["btn_draft"], key=f"draft_{logic_code}"):
        if policy_name:
            with st.spinner("Drafting policy..."):
                response = ai_service.generate_policy(policy_name, domain_name, framework, actual_lang)
                SessionManager.set(f"policy_{logic_code}", response.content)
                SessionManager.set(f"policy_name_{logic_code}", policy_name)
                SessionManager.set(f"policy_fw_{logic_code}", framework)
                SessionManager.set(f"policy_lang_{logic_code}", actual_lang)
    
    policy = SessionManager.get(f"policy_{logic_code}")
    if policy:
        # Download buttons
        st.markdown("### 📥 Download Options")
        dl_col1, dl_col2 = st.columns(2)
        
        stored_policy_name = SessionManager.get(f"policy_name_{logic_code}", "Policy")
        stored_framework = SessionManager.get(f"policy_fw_{logic_code}", "Framework")
        stored_lang = SessionManager.get(f"policy_lang_{logic_code}", "English")
        
        with dl_col1:
            try:
                from utils.export_utils import generate_policy_docx
                policy_docx = generate_policy_docx(stored_policy_name, domain_name, stored_framework, policy, stored_lang)
                if policy_docx:
                    st.download_button(
                        label="📄 Policy (Word)",
                        data=policy_docx,
                        file_name=f"policy_{logic_code}_{datetime.now().strftime('%Y%m%d')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_pol_docx_{logic_code}"
                    )
            except Exception as e:
                st.caption(f"Word export unavailable: {e}")
        
        with dl_col2:
            st.download_button(
                label="📝 Policy (Text)",
                data=f"# {stored_policy_name}\n\nFramework: {stored_framework}\nDomain: {domain_name}\nGenerated: {datetime.now().strftime('%Y-%m-%d')}\n\n{policy}",
                file_name=f"policy_{logic_code}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                key=f"dl_pol_md_{logic_code}"
            )
        
        st.markdown("---")
        
        # Apply RTL styling for Arabic
        rtl_style = "direction: rtl; text-align: right;" if stored_lang == "Arabic" else ""
        st.markdown(f"<div class='policy-paper' style='{rtl_style}'>{policy}</div>", unsafe_allow_html=True)


def render_audit_tab(username: str, domain_name: str, logic_code: str, txt: dict):
    """Render audit tab with language selection and download options."""
    reg_list = domain_config.get_domain_regulations(domain_name)
    
    col1, col2, col3 = st.columns(3)
    audit_std = col1.selectbox(txt.get("audit_target", "Standard"), reg_list, key=f"aud_std_{logic_code}")
    
    # Language selection for audit
    doc_lang = col2.selectbox(txt["doc_lang"], txt["doc_opts"], key=f"aud_lang_{logic_code}")
    lang_map = {"الإنجليزية": "English", "العربية": "Arabic", "ثنائي اللغة": "Bilingual"}
    actual_lang = lang_map.get(doc_lang, doc_lang)
    
    uploaded = col3.file_uploader(txt.get("upload_ev", "Upload PDF"), type=["pdf"], key=f"aud_file_{logic_code}")
    
    # Language hint
    if actual_lang == "Arabic":
        st.caption("📝 Audit report will be generated entirely in Arabic (تقرير التدقيق سيكون باللغة العربية بالكامل)")
    elif actual_lang == "Bilingual":
        st.caption("📝 Audit report will be bilingual - English followed by Arabic translation")
    
    if uploaded and st.button(txt["btn_audit"], key=f"audit_{logic_code}"):
        with st.spinner("Analyzing evidence and generating audit report..."):
            evidence = pdf_extractor.extract_text(uploaded)
            if evidence:
                response = ai_service.generate_audit_report(audit_std, evidence, actual_lang)
                SessionManager.set(f"audit_{logic_code}", response.content)
                SessionManager.set(f"audit_std_{logic_code}", audit_std)
                SessionManager.set(f"audit_lang_{logic_code}", actual_lang)
            else:
                st.error("Could not extract text from PDF")
    
    audit = SessionManager.get(f"audit_{logic_code}")
    if audit:
        stored_std = SessionManager.get(f"audit_std_{logic_code}", audit_std)
        stored_lang = SessionManager.get(f"audit_lang_{logic_code}", "English")
        
        # Download buttons
        st.markdown("### 📥 Download Audit Report")
        dl_col1, dl_col2 = st.columns(2)
        
        with dl_col1:
            try:
                from utils.export_utils import generate_audit_docx
                audit_docx = generate_audit_docx(stored_std, audit, stored_lang)
                if audit_docx:
                    st.download_button(
                        label="📄 Audit Report (Word)",
                        data=audit_docx,
                        file_name=f"audit_report_{logic_code}_{datetime.now().strftime('%Y%m%d')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"dl_aud_docx_{logic_code}"
                    )
            except Exception as e:
                st.caption(f"Word export unavailable: {e}")
        
        with dl_col2:
            # Full audit report as markdown
            report_header = f"# تقرير التدقيق: {stored_std}\n\n" if stored_lang == "Arabic" else f"# Audit Report: {stored_std}\n\n"
            report_header += f"Generated: {datetime.now().strftime('%Y-%m-%d')}\n"
            report_header += f"Language: {stored_lang}\n\n---\n\n"
            
            st.download_button(
                label="📝 Audit Report (Text)",
                data=report_header + audit,
                file_name=f"audit_report_{logic_code}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                key=f"dl_aud_md_{logic_code}"
            )
        
        st.markdown("---")
        
        # Apply RTL styling for Arabic
        rtl_style = "direction: rtl; text-align: right;" if stored_lang == "Arabic" else ""
        st.markdown(f"<div class='policy-paper' style='{rtl_style}'>{audit}</div>", unsafe_allow_html=True)


def render_risk_tab(username: str, domain_name: str, logic_code: str, txt: dict):
    """Render domain-specific risk radar with download option."""
    # Get domain-specific risk data
    risk_data = get_risk_data(logic_code)
    
    # Download button for risk register at the top
    df_risks = risk_repo.get_by_owner(username, domain_name)
    if not df_risks.empty:
        st.markdown("### 📥 Download Risk Register")
        try:
            from utils.export_utils import generate_risk_register_excel
            risk_excel = generate_risk_register_excel(df_risks, domain_name)
            st.download_button(
                label="📊 Risk Register (Excel)",
                data=risk_excel,
                file_name=f"risk_register_{logic_code}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"dl_risk_{logic_code}"
            )
        except Exception as e:
            st.caption(f"Excel export unavailable: {e}")
        st.markdown("---")
    
    with st.form(f"risk_{logic_code}"):
        col1, col2 = st.columns(2)
        
        # Risk category dropdown with domain-specific options
        categories = list(risk_data.keys())
        category = col1.selectbox(txt["ui_form"]["risk_cat"], categories)
        
        # Risk scenarios for selected category
        risks = risk_data.get(category, {}).get("risks", ["Generic Risk"])
        threat = col2.selectbox(txt["ui_form"]["risk_scen"], risks)
        
        # Show recommended mitigations
        mitigations = risk_data.get(category, {}).get("mitigations", "Standard controls")
        st.caption(f"🛡️ **Recommended Mitigations:** {mitigations}")
        
        # Asset details
        asset = st.text_input(txt["ui"]["asset_name"], 
            placeholder="e.g., Customer Database, Core Banking System, ERP Module...")
        
        context = st.text_area(txt["ui"]["custom_ctrl"], 
            placeholder="Describe specific context, existing controls, or concerns...")
        
        if st.form_submit_button(txt["ui_form"]["analyze_btn"]):
            if asset:
                with st.spinner("Analyzing risk..."):
                    response = ai_service.generate_risk_analysis(
                        domain_name, threat, asset, {"notes": context}
                    )
                    
                    risk_repo.create(
                        owner=username, domain=domain_name, asset_name=asset,
                        field1=category, field2="", field3="", field4="",
                        threat=threat, probability=3, impact=3,
                        risk_score=9, risk_level="HIGH", mitigation=response.content
                    )
                    
                    st.success(txt["risk_saved"])
                    SessionManager.set(f"risk_analysis_{logic_code}", response.content)
                    time.sleep(1)
                    st.rerun()
    
    # Display last analysis
    analysis = SessionManager.get(f"risk_analysis_{logic_code}")
    if analysis:
        st.markdown("### Risk Analysis Results")
        st.markdown(analysis)
    
    # Show existing risks
    if not df_risks.empty:
        st.markdown("### Registered Risks")
        display_cols = [c for c in ["asset_name", "threat", "risk_level", "created_at"] if c in df_risks.columns]
        st.dataframe(df_risks[display_cols], use_container_width=True)


def render_roadmap_tab(username: str, domain_name: str, logic_code: str, txt: dict):
    """Render roadmap tab with download option."""
    projects = project_repo.get_by_owner(username, domain_name)
    
    if not projects.empty:
        # Download button
        st.markdown("### 📥 Download Roadmap")
        try:
            from utils.export_utils import generate_roadmap_excel
            roadmap_excel = generate_roadmap_excel(projects, username, domain_name)
            st.download_button(
                label="📊 Roadmap (Excel)",
                data=roadmap_excel,
                file_name=f"roadmap_{logic_code}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"dl_roadmap_{logic_code}"
            )
        except Exception as e:
            st.caption(f"Excel export unavailable: {e}")
        
        st.markdown("---")
        
        # Gantt chart
        try:
            import plotly.express as px
            fig = px.timeline(projects, x_start="Start", x_end="Finish", y="Initiative", color="Phase",
                             title="Implementation Timeline")
            fig.update_layout(xaxis_title="Timeline", yaxis_title="Initiative")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            logger.warning(f"Gantt chart error: {e}")
        
        # Data table
        cols = [c for c in ["Phase", "Initiative", "Duration", "Cost", "Role", "Kpi"] if c in projects.columns]
        st.dataframe(projects[cols], use_container_width=True)
    else:
        st.info(txt["ui"]["no_data"])


# =============================================================================
# MAIN
# =============================================================================

def main():
    if "sentinel_logged_in" not in st.session_state:
        st.session_state["sentinel_logged_in"] = False
    
    if SessionManager.is_logged_in():
        render_main_application()
    else:
        render_login_page()

if __name__ == "__main__":
    main()
