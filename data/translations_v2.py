"""
Sentinel GRC - Enhanced Translations
Multi-language support with complete Arabic translations for all UI elements.
"""

from typing import Dict, Any, List


# =============================================================================
# TECHNOLOGY STACK OPTIONS BY DOMAIN
# =============================================================================

TECH_STACK_OPTIONS: Dict[str, Dict[str, List[str]]] = {
    "cyber": {
        "Security Operations": [
            "SIEM (Splunk/QRadar/Sentinel)",
            "SOAR Platform",
            "EDR/XDR Solution",
            "24/7 SOC",
            "Threat Intelligence Platform",
            "Vulnerability Scanner"
        ],
        "Identity & Access": [
            "IAM Solution (Okta/Azure AD/SailPoint)",
            "PAM Solution (CyberArk/BeyondTrust)",
            "MFA Deployed",
            "SSO Implemented",
            "Identity Governance"
        ],
        "Network Security": [
            "Next-Gen Firewall",
            "Web Application Firewall (WAF)",
            "Zero Trust Network Access (ZTNA)",
            "Network Segmentation",
            "DDoS Protection",
            "VPN/Remote Access"
        ],
        "Data Protection": [
            "DLP Solution",
            "Encryption (At Rest)",
            "Encryption (In Transit)",
            "Key Management (KMS/HSM)",
            "Backup & Recovery",
            "Data Classification Tool"
        ],
        "Governance": [
            "GRC Platform",
            "Policy Management Tool",
            "Risk Register",
            "Compliance Dashboard",
            "Audit Management"
        ]
    },
    "data": {
        "Data Platform": [
            "Data Warehouse (Snowflake/Databricks/BigQuery)",
            "Data Lake",
            "Master Data Management (MDM)",
            "Data Integration/ETL Tools",
            "Real-time Streaming"
        ],
        "Data Governance": [
            "Data Catalog (Collibra/Alation)",
            "Data Quality Platform",
            "Data Lineage Tool",
            "Metadata Management",
            "Business Glossary"
        ],
        "Analytics & BI": [
            "BI Platform (Power BI/Tableau/Qlik)",
            "Self-Service Analytics",
            "Advanced Analytics/ML",
            "Reporting Automation"
        ],
        "Privacy & Compliance": [
            "Privacy Management Platform",
            "Consent Management",
            "Data Subject Request Automation",
            "Data Masking/Anonymization"
        ]
    },
    "ai": {
        "AI/ML Platform": [
            "ML Platform (Azure ML/SageMaker/Vertex AI)",
            "MLOps Pipeline",
            "Feature Store",
            "Model Registry",
            "Experiment Tracking"
        ],
        "GenAI & LLM": [
            "LLM API Integration (OpenAI/Azure OpenAI/Claude)",
            "RAG Implementation",
            "Vector Database",
            "Prompt Management",
            "Fine-tuned Models"
        ],
        "AI Governance": [
            "AI Model Inventory",
            "Bias Detection Tools",
            "Explainability (XAI) Tools",
            "AI Risk Assessment Framework",
            "Model Monitoring"
        ],
        "AI Security": [
            "Input/Output Guardrails",
            "Content Filtering",
            "Red Teaming Program",
            "AI Firewall"
        ]
    },
    "dt": {
        "Digital Platforms": [
            "Cloud Platform (AWS/Azure/GCP)",
            "Low-Code/No-Code Platform",
            "API Management Platform",
            "Integration Platform (iPaaS)",
            "Digital Experience Platform"
        ],
        "Enterprise Systems": [
            "ERP System (SAP/Oracle)",
            "CRM Platform (Salesforce/Dynamics)",
            "HCM System",
            "Supply Chain Management",
            "Document Management"
        ],
        "Automation": [
            "RPA Platform (UiPath/Automation Anywhere)",
            "Workflow Automation",
            "Process Mining",
            "Intelligent Automation"
        ],
        "Digital Channels": [
            "Customer Portal",
            "Mobile Applications",
            "Chatbot/Virtual Assistant",
            "E-commerce Platform"
        ]
    },
    "global": {
        "Management Systems": [
            "Quality Management System (QMS)",
            "Environmental Management System (EMS)",
            "Information Security Management System (ISMS)",
            "Business Continuity Management System (BCMS)",
            "IT Service Management (ITSM)"
        ],
        "Tools & Platforms": [
            "Document Control System",
            "Audit Management Software",
            "ITSM Platform (ServiceNow/BMC)",
            "Project Management Tools",
            "Risk Management Software"
        ],
        "Monitoring": [
            "Performance Dashboards",
            "SLA Monitoring",
            "Customer Feedback System",
            "Continuous Improvement Tracking"
        ]
    }
}


# =============================================================================
# ORGANIZATIONAL STRUCTURE OPTIONS
# =============================================================================

ORG_STRUCTURE_OPTIONS: Dict[str, Dict[str, List[str]]] = {
    "cyber": {
        "en": [
            "CISO reports to CEO",
            "CISO reports to CIO",
            "CISO reports to CRO",
            "Security team under IT",
            "Dedicated Security Department",
            "Virtual/Part-time Security Team",
            "Outsourced Security (MSSP)"
        ],
        "ar": [
            "مدير الأمن السيبراني يتبع الرئيس التنفيذي",
            "مدير الأمن السيبراني يتبع مدير تقنية المعلومات",
            "مدير الأمن السيبراني يتبع مدير المخاطر",
            "فريق الأمن ضمن تقنية المعلومات",
            "إدارة أمن مستقلة",
            "فريق أمن جزئي/افتراضي",
            "أمن مُدار خارجياً (MSSP)"
        ]
    },
    "data": {
        "en": [
            "CDO reports to CEO",
            "CDO reports to CIO",
            "Data team under IT",
            "Dedicated Data Office",
            "Federated Data Governance",
            "Centralized Data Team",
            "Data Mesh Model"
        ],
        "ar": [
            "مدير البيانات يتبع الرئيس التنفيذي",
            "مدير البيانات يتبع مدير تقنية المعلومات",
            "فريق البيانات ضمن تقنية المعلومات",
            "مكتب بيانات مستقل",
            "حوكمة بيانات موزعة",
            "فريق بيانات مركزي",
            "نموذج شبكة البيانات"
        ]
    },
    "ai": {
        "en": [
            "Chief AI Officer",
            "AI under CDO",
            "AI under CTO",
            "AI Center of Excellence",
            "Distributed AI Teams",
            "AI Lab/Innovation Team",
            "Outsourced AI Development"
        ],
        "ar": [
            "مدير الذكاء الاصطناعي",
            "الذكاء الاصطناعي تحت إدارة البيانات",
            "الذكاء الاصطناعي تحت الإدارة التقنية",
            "مركز تميز الذكاء الاصطناعي",
            "فرق ذكاء اصطناعي موزعة",
            "مختبر/فريق ابتكار",
            "تطوير خارجي للذكاء الاصطناعي"
        ]
    },
    "dt": {
        "en": [
            "Chief Digital Officer",
            "Digital under CEO",
            "Digital under CIO",
            "Digital Transformation Office",
            "Business Unit Digital Teams",
            "Agile Transformation Team",
            "External Digital Partner"
        ],
        "ar": [
            "مدير التحول الرقمي",
            "الرقمنة تحت الرئيس التنفيذي",
            "الرقمنة تحت إدارة تقنية المعلومات",
            "مكتب التحول الرقمي",
            "فرق رقمية في وحدات الأعمال",
            "فريق التحول الرشيق",
            "شريك رقمي خارجي"
        ]
    },
    "global": {
        "en": [
            "Quality Manager reports to CEO",
            "Quality under Operations",
            "Integrated Management System Team",
            "Dedicated Compliance Team",
            "Distributed Quality Representatives",
            "External Quality Consultant"
        ],
        "ar": [
            "مدير الجودة يتبع الرئيس التنفيذي",
            "الجودة ضمن العمليات",
            "فريق نظام إدارة متكامل",
            "فريق امتثال مخصص",
            "ممثلي جودة موزعين",
            "مستشار جودة خارجي"
        ]
    }
}


# =============================================================================
# UI TRANSLATIONS
# =============================================================================

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "English": {
        "download_strat_pdf": "📥 Export Strategy Pack (PDF)",
        "download_audit_pdf": "📥 Export Audit Report (PDF)",
        "sidebar_title": "Mizan",
        "sidebar_caption": "Enterprise GRC Operating System",
        "logout": "Log Out",
        "settings": "Settings",
        "clear_hist": "Clear History",
        "clear_confirm": "History cleared",
        "func_tabs": ["Strategy", "Policy Lab", "Audit", "Risk Radar", "Roadmap"],
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
        "org_sizes": ["Small (<100 employees)", "Medium (100-1000 employees)", "Large (1000+ employees)"],
        "disclaimer_title": "⚠️ Important Disclaimer",
        "disclaimer_text": "**AI-Driven Assistant:** Outputs require expert review.<br> **Data Privacy:** Files are processed in-memory.",
        "policy_name": "Policy Title",
        "audit_target": "Audit Standard",
        "upload_ev": "Upload Evidence (PDF)",
        "doc_lang": "Document Language",
        "doc_opts": ["English", "Arabic"],
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
        # Strategy output section titles
        "strategy_sections": {
            "vision": "Executive Vision & Strategic Objectives",
            "gaps": "Current State Assessment (Gap Analysis)",
            "pillars": "Strategic Pillars & Initiatives",
            "roadmap": "Implementation Roadmap",
            "kpis": "Measuring Success (KPIs & KRIs)",
            "confidence": "Confidence Score"
        },
        "ui_form": {
            "org_name": "Organization Name",
            "sector": "Sector",
            "reg": "Regulatory Frameworks",
            "size": "Organization Size",
            "budget": "Budget Range (SAR)",
            "horizon": "Strategic Horizon (Months)",
            "current_state": "Current State Assessment",
            "tech_stack": "Current Technology Stack",
            "tech_select": "Select Implemented Technologies",
            "org_structure": "Current Organizational Structure",
            "challenges": "Key Challenges & Pain Points",
            "ai_use": "Key AI Use Cases",
            "data_org": "Data Organization Structure",
            "cyber_org": "Cybersecurity Organization Structure",
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
        "sidebar_title": "ميزان (Mizan)",
        "sidebar_caption": "نظام تشغيل الحوكمة المؤسسية",
        "logout": "تسجيل خروج",
        "settings": "الإعدادات",
        "clear_hist": "مسح السجل",
        "clear_confirm": "تم المسح",
        "func_tabs": ["الاستراتيجية", "معمل السياسات", "التدقيق", "رادار المخاطر", "خارطة الطريق"],
        "domains": ["الأمن السيبراني", "إدارة البيانات", "الذكاء الاصطناعي", "التحول الرقمي", "المعايير العالمية"],
        "step1": "المرحلة 1: السياق والنطاق",
        "step2": "المرحلة 2: التحليل والاستراتيجية",
        "step3": "المرحلة 3: المخرجات التنفيذية",
        "btn_start": "بدء خط العمل",
        "btn_gen": "تنفيذ الاستراتيجية",
        "btn_reset": "جلسة جديدة",
        "btn_draft": "صياغة السياسة",
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
        "org_sizes": ["صغيرة (أقل من 100 موظف)", "متوسطة (100-1000 موظف)", "كبيرة (أكثر من 1000 موظف)"],
        "disclaimer_title": "⚠️ إخلاء مسؤولية هام",
        "disclaimer_text": "**المستشار الذكي:** المخرجات تتطلب مراجعة الخبراء.<br> **خصوصية البيانات:** تتم المعالجة في الذاكرة فقط.",
        "policy_name": "عنوان السياسة",
        "audit_target": "معيار التدقيق",
        "upload_ev": "رفع الإثبات (PDF)",
        "doc_lang": "لغة الوثيقة",
        "doc_opts": ["الإنجليزية", "العربية"],
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
        # Strategy output section titles in Arabic
        "strategy_sections": {
            "vision": "الرؤية التنفيذية والأهداف الاستراتيجية",
            "gaps": "تقييم الوضع الراهن (تحليل الفجوات)",
            "pillars": "الركائز الاستراتيجية والمبادرات",
            "roadmap": "خارطة طريق التنفيذ",
            "kpis": "قياس النجاح (مؤشرات الأداء والمخاطر)",
            "confidence": "درجة الثقة والتحقق"
        },
        "ui_form": {
            "org_name": "اسم المنشأة",
            "sector": "القطاع",
            "reg": "الأطر التنظيمية",
            "size": "حجم المنشأة",
            "budget": "نطاق الميزانية (ريال)",
            "horizon": "الأفق الاستراتيجي (أشهر)",
            "current_state": "تقييم الوضع الحالي",
            "tech_stack": "البنية التقنية الحالية",
            "tech_select": "اختر التقنيات المطبقة حالياً",
            "org_structure": "الهيكل التنظيمي الحالي",
            "challenges": "أهم التحديات ونقاط الألم",
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
    """Get translations for a specific language."""
    return TRANSLATIONS.get(language, TRANSLATIONS["English"])


def is_rtl_language(language: str) -> bool:
    """Check if language is RTL."""
    return language == "العربية"


def get_tech_options(domain_code: str) -> Dict[str, List[str]]:
    """Get technology stack options for a domain."""
    return TECH_STACK_OPTIONS.get(domain_code, TECH_STACK_OPTIONS["cyber"])


def get_org_structure_options(domain_code: str, language: str = "en") -> List[str]:
    """Get organizational structure options for a domain."""
    lang_key = "ar" if language in ["العربية", "Arabic"] else "en"
    domain_options = ORG_STRUCTURE_OPTIONS.get(domain_code, ORG_STRUCTURE_OPTIONS["cyber"])
    return domain_options.get(lang_key, domain_options["en"])


def get_section_title(section_key: str, language: str) -> str:
    """Get translated section title."""
    translations = get_translation(language)
    sections = translations.get("strategy_sections", {})
    
    # Fallback to English if not found
    if section_key not in sections:
        sections = TRANSLATIONS["English"].get("strategy_sections", {})
    
    return sections.get(section_key, section_key)

# Additional UI translations for pipeline status messages
PIPELINE_MESSAGES = {
    "English": {
        "generating_strategy": "Generating strategy...",
        "generating_policy": "Generating policy document...",
        "analyzing_audit": "Analyzing audit evidence...",
        "analyzing_risk": "Analyzing risk scenario...",
        "download_options": "Download Options",
        "export_pdf": "Export as PDF",
        "export_docx": "Export as Word",
        "export_pptx": "Export as PowerPoint",
        "processing": "Processing...",
        "complete": "Complete!",
        "error_occurred": "An error occurred",
        "invalid_document": "Invalid document for this domain",
        "document_mismatch": "The uploaded document does not appear to be related to {domain}. Please upload a relevant document.",
        "validating_document": "Validating document relevance..."
    },
    "العربية": {
        "generating_strategy": "جاري إنشاء الاستراتيجية...",
        "generating_policy": "جاري إنشاء وثيقة السياسة...",
        "analyzing_audit": "جاري تحليل أدلة التدقيق...",
        "analyzing_risk": "جاري تحليل سيناريو المخاطر...",
        "download_options": "خيارات التنزيل",
        "export_pdf": "تصدير كـ PDF",
        "export_docx": "تصدير كـ Word",
        "export_pptx": "تصدير كـ PowerPoint",
        "processing": "جاري المعالجة...",
        "complete": "اكتمل!",
        "error_occurred": "حدث خطأ",
        "invalid_document": "وثيقة غير صالحة لهذا المجال",
        "document_mismatch": "الوثيقة المرفوعة لا تبدو متعلقة بمجال {domain}. يرجى رفع وثيقة ذات صلة.",
        "validating_document": "جاري التحقق من صلة الوثيقة..."
    }
}

def get_pipeline_message(key: str, language: str = "English", **kwargs) -> str:
    """Get a pipeline status message in the specified language."""
    lang_key = "العربية" if language in ["Arabic", "العربية"] else "English"
    messages = PIPELINE_MESSAGES.get(lang_key, PIPELINE_MESSAGES["English"])
    message = messages.get(key, key)
    
    # Format with any provided kwargs
    if kwargs:
        try:
            message = message.format(**kwargs)
        except KeyError:
            pass
    
    return message
