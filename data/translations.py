"""
Sentinel GRC - Translations
Multi-language support for UI elements.
"""

from typing import Dict, Any


# =============================================================================
# UI TRANSLATIONS
# =============================================================================

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "English": {
        "download_strat_pdf": "📥 Export Strategy Pack (PDF)",
        "download_audit_pdf": "📥 Export Audit Report (PDF)",
        "sidebar_title": "Sentinel",
        "sidebar_caption": "Enterprise GRC Operating System",
        "logout": "Log Out",
        "settings": "Settings",
        "clear_hist": "Clear History",
        "clear_confirm": "History cleared",
        "func_tabs": ["Strategy", "Policy Lab", "Audit", "Risk Radar"],
        "domains": ["Cyber Security", "Data Management", "Artificial Intelligence", "Digital Transformation", "Global Standards"],
        "step1": "Phase 1: Context & Scope",
        "step2": "Phase 2: Analysis & Strategy",
        "step3": "Phase 3: Executive Output",
        "btn_start": "Initialize Pipeline",
        "btn_gen": "Execute Strategy Pipeline",
        "btn_reset": "New Pipeline Run",
        "btn_draft": "Draft Policy Document",
        "btn_audit": "Run Compliance Audit",
        "btn_risk": "Analyze & Register Risk",
        "download_strat": "📥 Export Strategy Pack",
        "download_pol": "📥 Export Policy",
        "download_audit": "📥 Export Audit Report",
        "master_btn": "📥 Executive Summary PDF",
        "download_excel": "📥 Download Roadmap (Excel)",
        "risk_new": "➕ Add New Risk",
        "risk_saved": "Risk Registered Successfully!",
        "metrics": ["Compliance Score", "Active Initiatives", "Est. Budget (SAR)", "Critical Risks"],
        "auth_error": "🚨 Authentication Failed: Contact Admin.",
        "org_sizes": ["Small", "Medium", "Large"],
        "disclaimer_title": "⚠️ Important Disclaimer",
        "disclaimer_text": "**AI-Driven Assistant:** Outputs require expert review.<br> **Data Privacy:** Files are processed in-memory.",
        "policy_name": "Policy Title",
        "audit_target": "Audit Standard",
        "upload_ev": "Upload Evidence (PDF)",
        "doc_lang": "Document Language",
        "doc_opts": ["English", "Arabic", "Bilingual"],
        "doc_fmt": "Format",
        "lbl_reg": "Regulation / Standard",
        "login_title": "Sign In",
        "login_btn": "Enter",
        "register_title": "Register",
        "register_btn": "Create Account",
        "username": "Username",
        "password": "Password",
        "new_user": "New Username",
        "new_pass": "New Password",
        "login_failed": "Login failed. Please check your credentials.",
        "register_success": "Account created successfully!",
        "register_failed": "Username already exists.",
        "ui_form": {
            "org_name": "Organization Name",
            "sector": "Sector",
            "reg": "Regulatory Frameworks",
            "size": "Organization Size",
            "budget": "Budget Range (SAR)",
            "horizon": "Strategic Horizon (Months)",
            "current_state": "Current State Assessment",
            "tech_stack": "Key Technologies",
            "challenges": "Key Challenges & Current Infrastructure",
            "ai_use": "Key AI Use Cases",
            "data_org": "Data Org Structure",
            "cyber_org": "Cyber Org Structure",
            "controls": "Existing Controls",
            "analyze_btn": "Analyze Risk",
            "risk_cat": "Risk Category",
            "risk_scen": "Risk Scenario"
        },
        "ui": {
            "asset_name": "Asset Name",
            "threat": "Threat / Vulnerability",
            "asset_type": "Asset Type",
            "zone": "Network Zone",
            "controls": "Current Controls",
            "custom_ctrl": "Additional Context",
            "no_data": "No Roadmap Data Available"
        },
    },
    "العربية": {
        "download_strat_pdf": "📥 تحميل حزمة الاستراتيجية (PDF)",
        "download_audit_pdf": "📥 تحميل تقرير التدقيق (PDF)",
        "sidebar_title": "الحارس (Sentinel)",
        "sidebar_caption": "نظام تشغيل الحوكمة المؤسسية",
        "logout": "تسجيل خروج",
        "settings": "الإعدادات",
        "clear_hist": "مسح السجل",
        "clear_confirm": "تم المسح",
        "func_tabs": ["الاستراتيجية", "معمل السياسات", "التدقيق", "رادار المخاطر"],
        "domains": ["الأمن السيبراني", "إدارة البيانات", "الذكاء الاصطناعي", "التحول الرقمي", "المعايير العالمية"],
        "step1": "المرحلة 1: السياق والنطاق",
        "step2": "المرحلة 2: التحليل والاستراتيجية",
        "step3": "المرحلة 3: المخرجات التنفيذية",
        "btn_start": "بدء خط العمل",
        "btn_gen": "تنفيذ استراتيجية",
        "btn_reset": "جلسة جديدة",
        "btn_draft": "صياغة الوثيقة",
        "btn_audit": "تشغيل التدقيق",
        "btn_risk": "تحليل وتسجيل الخطر",
        "download_strat": "📥 تحميل حزمة الاستراتيجية",
        "download_pol": "📥 تحميل السياسة",
        "download_audit": "📥 تحميل تقرير التدقيق",
        "master_btn": "📥 الملخص التنفيذي (PDF)",
        "download_excel": "📥 تحميل خارطة الطريق (Excel)",
        "risk_new": "➕ إضافة خطر جديد",
        "risk_saved": "تم تسجيل الخطر بنجاح!",
        "metrics": ["نسبة الامتثال", "المبادرات النشطة", "الميزانية (ريال)", "مخاطر حرجة"],
        "auth_error": "🚨 فشل المصادقة: اتصل بالمسؤول.",
        "org_sizes": ["صغيرة", "متوسطة", "كبيرة"],
        "disclaimer_title": "⚠️ إخلاء مسؤولية هام",
        "disclaimer_text": "**المستشار الذكي:** المخرجات تتطلب مراجعة الخبراء.<br> **خصوصية البيانات:** تتم المعالجة في الذاكرة فقط.",
        "policy_name": "عنوان السياسة",
        "audit_target": "معيار التدقيق",
        "upload_ev": "رفع الإثبات (PDF)",
        "doc_lang": "لغة الوثيقة",
        "doc_opts": ["الإنجليزية", "العربية", "ثنائي اللغة"],
        "doc_fmt": "الصيغة",
        "lbl_reg": "المرجع التنظيمي / المعيار",
        "login_title": "تسجيل الدخول",
        "login_btn": "دخول",
        "register_title": "إنشاء حساب",
        "register_btn": "إنشاء",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "new_user": "اسم مستخدم جديد",
        "new_pass": "كلمة مرور جديدة",
        "login_failed": "فشل تسجيل الدخول. يرجى التحقق من البيانات.",
        "register_success": "تم إنشاء الحساب بنجاح!",
        "register_failed": "اسم المستخدم موجود مسبقاً.",
        "ui_form": {
            "org_name": "اسم المنشأة",
            "sector": "القطاع",
            "reg": "الأطر التنظيمية",
            "size": "حجم المنشأة",
            "budget": "نطاق الميزانية (ريال)",
            "horizon": "الأفق الاستراتيجي (أشهر)",
            "current_state": "تقييم الوضع الحالي",
            "tech_stack": "التقنيات الحالية",
            "challenges": "أهم التحديات والبنية التحتية",
            "ai_use": "حالات استخدام الذكاء الاصطناعي",
            "data_org": "هيكل إدارة البيانات",
            "cyber_org": "هيكل الأمن السيبراني",
            "controls": "الضوابط الحالية",
            "analyze_btn": "تحليل الخطر",
            "risk_cat": "فئة الخطر",
            "risk_scen": "سيناريو الخطر"
        },
        "ui": {
            "asset_name": "اسم الأصل",
            "threat": "التهديد / الثغرة",
            "asset_type": "نوع الأصل",
            "zone": "المنطقة بالشبكة",
            "controls": "الضوابط الحالية",
            "custom_ctrl": "سياق إضافي",
            "no_data": "لا توجد بيانات لخارطة الطريق"
        },
    },
}


def get_translation(language: str) -> Dict[str, Any]:
    """
    Get translations for a specific language.
    
    Args:
        language: Language key ("English" or "العربية")
        
    Returns:
        Translation dictionary
    """
    return TRANSLATIONS.get(language, TRANSLATIONS["English"])


def is_rtl_language(language: str) -> bool:
    """Check if language is RTL."""
    return language == "العربية"
