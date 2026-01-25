"""
Mizan GRC - Comprehensive Domain-Specific Content
All content for Strategy, Policy, Audit, and Risk across all 5 domains.
Aligned with relevant frameworks and regulations.
"""

from typing import Dict, Any, List

# =============================================================================
# DOMAIN CONFIGURATIONS
# =============================================================================

DOMAIN_CONFIG = {
    "Cyber Security": {
        "primary_frameworks": ["NCA ECC", "NCA CCC", "SAMA CSF", "ISO 27001", "NIST CSF"],
        "key_regulations": ["NCA Essential Cybersecurity Controls", "SAMA Cyber Security Framework"],
        "policy_types": [
            "Information Security Policy",
            "Access Control Policy",
            "Incident Response Policy",
            "Data Protection Policy",
            "Network Security Policy",
            "Acceptable Use Policy"
        ],
        "risk_categories": [
            "Ransomware & Malware",
            "Data Breach",
            "Insider Threat",
            "Phishing & Social Engineering",
            "Third-Party/Supply Chain",
            "DDoS & Availability"
        ],
        "audit_areas": [
            "Access Control & IAM",
            "Network Security",
            "Endpoint Protection",
            "Security Monitoring",
            "Incident Response",
            "Data Protection"
        ]
    },
    "Artificial Intelligence": {
        "primary_frameworks": ["SDAIA AI Ethics", "NIST AI RMF", "EU AI Act", "ISO 42001"],
        "key_regulations": ["SDAIA AI Ethics Principles", "PDPL (AI provisions)"],
        "policy_types": [
            "AI Governance Policy",
            "AI Ethics Policy",
            "Model Risk Management Policy",
            "AI Data Usage Policy",
            "Algorithmic Accountability Policy",
            "AI Transparency Policy"
        ],
        "risk_categories": [
            "Model Bias & Fairness",
            "AI Security & Adversarial Attacks",
            "Privacy & Data Misuse",
            "Lack of Explainability",
            "Model Drift & Performance",
            "Regulatory Non-Compliance"
        ],
        "audit_areas": [
            "AI Governance Framework",
            "Model Development Lifecycle",
            "Bias & Fairness Testing",
            "Model Documentation",
            "AI Ethics Compliance",
            "Model Monitoring"
        ]
    },
    "Data Management": {
        "primary_frameworks": ["PDPL", "NDMO", "DAMA DMBOK", "ISO 8000"],
        "key_regulations": ["Personal Data Protection Law (PDPL)", "NDMO Data Governance"],
        "policy_types": [
            "Data Governance Policy",
            "Data Classification Policy",
            "Data Retention Policy",
            "Data Privacy Policy",
            "Data Quality Policy",
            "Data Sharing Policy"
        ],
        "risk_categories": [
            "Data Privacy Breach",
            "Data Quality Issues",
            "Regulatory Non-Compliance",
            "Data Loss/Corruption",
            "Unauthorized Data Access",
            "Consent Management Failure"
        ],
        "audit_areas": [
            "Data Governance Framework",
            "PDPL Compliance",
            "Data Quality Management",
            "Data Classification",
            "Consent Management",
            "Data Retention"
        ]
    },
    "Digital Transformation": {
        "primary_frameworks": ["COBIT 2019", "TOGAF", "DGA Digital Policy", "SAFe"],
        "key_regulations": ["DGA Digital Government Policy", "Vision 2030 Digital Initiatives"],
        "policy_types": [
            "Digital Transformation Policy",
            "Cloud Adoption Policy",
            "API Management Policy",
            "Agile Governance Policy",
            "Technology Innovation Policy",
            "Digital Customer Experience Policy"
        ],
        "risk_categories": [
            "Digital Project Failure",
            "Technology Obsolescence",
            "Integration Failures",
            "Change Resistance",
            "Vendor Lock-in",
            "Digital Skills Gap"
        ],
        "audit_areas": [
            "Digital Strategy Alignment",
            "Cloud Governance",
            "Digital Project Delivery",
            "Technology Architecture",
            "Change Management",
            "Digital KPIs"
        ]
    },
    "Global Standards": {
        "primary_frameworks": ["ISO 27001", "ISO 22301", "ISO 9001", "ITIL 4", "ISO 31000"],
        "key_regulations": ["ISO Certification Requirements", "Management System Standards"],
        "policy_types": [
            "Integrated Management System Policy",
            "Quality Management Policy",
            "Business Continuity Policy",
            "Information Security Policy",
            "Risk Management Policy",
            "Continual Improvement Policy"
        ],
        "risk_categories": [
            "Certification Loss",
            "Non-Conformity",
            "Audit Failure",
            "Process Deviation",
            "Documentation Gaps",
            "Competency Shortfall"
        ],
        "audit_areas": [
            "Management System Effectiveness",
            "Process Compliance",
            "Documentation Control",
            "Internal Audit Program",
            "Management Review",
            "Corrective Actions"
        ]
    }
}


# =============================================================================
# STRATEGY CONTENT - ARABIC
# =============================================================================

STRATEGY_ARABIC = {
    "Cyber Security": {
        "vision": "تأسيس منظومة أمن سيبراني متكاملة ومرنة تحمي الأصول الحيوية وتضمن الامتثال لمتطلبات الهيئة الوطنية للأمن السيبراني وتمكّن الابتكار الرقمي الآمن.",
        "objectives": [
            "تحقيق امتثال ٩٥٪+ لضوابط الهيئة الوطنية للأمن السيبراني خلال ١٨ شهر",
            "تقليل متوسط وقت اكتشاف التهديدات إلى أقل من ٤ ساعات",
            "تطبيق بنية انعدام الثقة عبر الأنظمة الحيوية",
            "بناء مركز عمليات أمنية يعمل على مدار الساعة",
            "تحقيق جاهزية التأمين السيبراني"
        ],
        "pillars": [
            {"name": "حوكمة الأمن والمخاطر", "initiatives": ["تأسيس لجنة الأمن السيبراني", "تطبيق إطار السياسات الأمنية", "نشر منصة الحوكمة والمخاطر والامتثال"]},
            {"name": "كشف التهديدات والاستجابة", "initiatives": ["نشر نظام SIEM/SOAR", "تطبيق EDR/XDR على جميع الأجهزة", "تأسيس فريق الاستجابة للحوادث"]},
            {"name": "أمن الهوية والوصول", "initiatives": ["تطبيق المصادقة متعددة العوامل", "نشر إدارة الوصول المتميز PAM", "أتمتة مراجعات الصلاحيات"]},
            {"name": "أمن الشبكات والبنية التحتية", "initiatives": ["تطبيق تجزئة الشبكة", "نشر جدار حماية الجيل التالي", "تأسيس الوصول الآمن عن بعد"]},
            {"name": "ثقافة الأمن والتوعية", "initiatives": ["إطلاق برنامج التوعية الأمنية", "إجراء محاكاة التصيد الشهرية", "تأسيس شبكة سفراء الأمن"]}
        ]
    },
    "Artificial Intelligence": {
        "vision": "تمكين المنظمة كرائد في تبني الذكاء الاصطناعي المسؤول، وضمان شفافية وعدالة وأمان جميع أنظمة الذكاء الاصطناعي مع الامتثال لمبادئ سدايا الأخلاقية.",
        "objectives": [
            "إنشاء لجنة أخلاقيات الذكاء الاصطناعي وإطار الحوكمة خلال ٦ أشهر",
            "تحقيق جرد كامل لنماذج الذكاء الاصطناعي وتصنيف المخاطر",
            "تطبيق كشف التحيز ومراقبة العدالة لجميع النماذج الإنتاجية",
            "ضمان الامتثال لمبادئ أخلاقيات سدايا",
            "تقليل حوادث الذكاء الاصطناعي بنسبة ٨٠٪"
        ],
        "pillars": [
            {"name": "إطار حوكمة الذكاء الاصطناعي", "initiatives": ["تأسيس لجنة أخلاقيات الذكاء الاصطناعي", "تطوير إطار سياسات الذكاء الاصطناعي", "تطبيق سجل النماذج"]},
            {"name": "الذكاء الاصطناعي المسؤول والأخلاقيات", "initiatives": ["نشر أدوات كشف التحيز", "تطبيق أطر قابلية التفسير", "تأسيس متطلبات الإشراف البشري"]},
            {"name": "أمن وخصوصية الذكاء الاصطناعي", "initiatives": ["تطبيق اختبار المتانة", "نشر ضوابط خصوصية البيانات", "تأسيس أمن النماذج"]},
            {"name": "أداء النماذج والمراقبة", "initiatives": ["نشر منصة مراقبة التعلم الآلي", "تطبيق خطوط إعادة التدريب الآلية", "تأسيس اتفاقيات مستوى الخدمة"]},
            {"name": "ثقافة ومحو أمية الذكاء الاصطناعي", "initiatives": ["إطلاق برنامج محو أمية الذكاء الاصطناعي", "تدريب علماء البيانات على الممارسات المسؤولة", "تأسيس مركز التميز"]}
        ]
    },
    "Data Management": {
        "vision": "تحويل المنظمة إلى منظمة تعتمد على البيانات مع حوكمة بيانات مؤسسية شاملة، وضمان جودة البيانات والامتثال لنظام حماية البيانات الشخصية.",
        "objectives": [
            "تحقيق الامتثال لنظام حماية البيانات الشخصية عبر جميع أنشطة المعالجة",
            "تطبيق كتالوج بيانات مؤسسي بتغطية ١٠٠٪ للأصول الحيوية",
            "تحسين درجة جودة البيانات إلى ٩٥٪+ للمجالات الحيوية",
            "تقليل الحوادث المتعلقة بالبيانات بنسبة ٧٠٪",
            "تمكين التحليلات الذاتية لـ ٨٠٪ من المستخدمين"
        ],
        "pillars": [
            {"name": "حوكمة البيانات والإشراف", "initiatives": ["تأسيس مجلس حوكمة البيانات", "تطبيق برنامج أمناء البيانات", "نشر كتالوج البيانات المؤسسي"]},
            {"name": "إدارة جودة البيانات", "initiatives": ["تطبيق أدوات مراقبة جودة البيانات", "تأسيس قواعد الجودة حسب المجال", "إنشاء لوحات جودة البيانات"]},
            {"name": "خصوصية البيانات وحمايتها", "initiatives": ["إجراء تقييم فجوات نظام حماية البيانات", "تطبيق منصة إدارة الموافقات", "نشر أدوات إخفاء البيانات"]},
            {"name": "هندسة البيانات والتكامل", "initiatives": ["تصميم بنية البيانات المستهدفة", "تطبيق إدارة البيانات الرئيسية", "نشر خطوط تكامل البيانات"]},
            {"name": "محو أمية البيانات والتمكين", "initiatives": ["إطلاق برنامج محو أمية البيانات", "نشر أدوات التحليلات الذاتية", "تأسيس مجتمع ممارسة البيانات"]}
        ]
    },
    "Digital Transformation": {
        "vision": "تسريع رحلة التحول الرقمي للمنظمة، وتقديم تجارب عملاء استثنائية والتميز التشغيلي ومصادر إيرادات رقمية جديدة بما يتوافق مع رؤية ٢٠٣٠.",
        "objectives": [
            "تحقيق ٨٠٪ تبني للقنوات الرقمية في معاملات العملاء",
            "تقليل التكاليف التشغيلية بنسبة ٣٠٪ من خلال الأتمتة",
            "إطلاق ٥ منتجات/خدمات رقمية جديدة خلال ٢٤ شهر",
            "تحسين إنتاجية الموظفين الرقمية بنسبة ٤٠٪",
            "تحقيق النضج الرقمي ضمن الربع الأعلى في القطاع"
        ],
        "pillars": [
            {"name": "تحويل تجربة العملاء", "initiatives": ["تطبيق منصة التفاعل متعددة القنوات", "نشر المساعد الافتراضي المدعوم بالذكاء الاصطناعي", "إنشاء رحلات عملاء رقمية مخصصة"]},
            {"name": "أتمتة العمليات والكفاءة", "initiatives": ["نشر RPA للعمليات عالية الحجم", "تطبيق منصة أتمتة سير العمل", "رقمنة العمليات الورقية"]},
            {"name": "المنتجات الرقمية والابتكار", "initiatives": ["تأسيس قدرة إدارة المنتجات الرقمية", "إنشاء مختبر الابتكار", "تطبيق منهجية التفكير التصميمي"]},
            {"name": "تحديث التقنية", "initiatives": ["تنفيذ استراتيجية الهجرة السحابية", "تطبيق بنية API أولاً", "تحديث الأنظمة القديمة"]},
            {"name": "الثقافة والقدرات الرقمية", "initiatives": ["إطلاق برنامج المهارات الرقمية", "تطبيق أساليب العمل الرشيقة", "تأسيس برنامج إدارة التغيير"]}
        ]
    },
    "Global Standards": {
        "vision": "ترسيخ المنظمة كمرجع للتميز في أنظمة الإدارة، وتحقيق والحفاظ على شهادات ISO 27001 و ISO 22301 و ISO 9001 مع تحقيق التحسين المستمر.",
        "objectives": [
            "الحصول على شهادة ISO 27001:2022 خلال ١٢ شهر",
            "تطبيق نظام إدارة استمرارية الأعمال ISO 22301",
            "الحصول على شهادة إدارة الجودة ISO 9001",
            "تحقيق نضج ITIL 4 لإدارة خدمات تقنية المعلومات",
            "إنشاء إطار نظام إدارة متكامل"
        ],
        "pillars": [
            {"name": "أمن المعلومات (ISO 27001)", "initiatives": ["إجراء تقييم فجوات ISO 27001", "تطبيق وثائق وضوابط ISMS", "تأسيس برنامج التدقيق الداخلي"]},
            {"name": "استمرارية الأعمال (ISO 22301)", "initiatives": ["إجراء تحليل تأثير الأعمال", "تطوير واختبار خطط استمرارية الأعمال", "تأسيس إدارة الأزمات"]},
            {"name": "إدارة الجودة (ISO 9001)", "initiatives": ["تحديد سياسة وأهداف الجودة", "تطبيق معايير توثيق العمليات", "تأسيس مقاييس ومراقبة الجودة"]},
            {"name": "إدارة خدمات تقنية المعلومات (ITIL)", "initiatives": ["تطبيق مكتب الخدمة وإدارة الحوادث", "نشر إدارة التغيير والإصدار", "تأسيس كتالوج الخدمات"]},
            {"name": "نظام الإدارة المتكامل", "initiatives": ["توحيد السياسات عبر أنظمة الإدارة", "تطبيق التحكم الموحد بالوثائق", "تأسيس برنامج تدقيق داخلي مشترك"]}
        ]
    }
}


# =============================================================================
# POLICY CONTENT
# =============================================================================

POLICY_CONTENT = {
    "Cyber Security": {
        "English": {
            "title": "Cybersecurity Policy",
            "purpose": "This policy establishes the cybersecurity requirements and controls to protect {org_name}'s information assets, systems, and networks from cyber threats in alignment with NCA Essential Cybersecurity Controls (ECC) and industry best practices.",
            "scope": "This policy applies to all information systems, networks, applications, data, and personnel including employees, contractors, and third parties who access {org_name}'s technology resources.",
            "key_requirements": [
                "All systems must be protected by approved endpoint detection and response (EDR) solutions",
                "Multi-factor authentication (MFA) is mandatory for all privileged access and remote connections",
                "Security events must be monitored 24/7 through the Security Operations Center (SOC)",
                "Vulnerability assessments must be conducted monthly; penetration testing annually",
                "All security incidents must be reported within 1 hour of detection",
                "Third-party access requires security assessment and contractual security requirements"
            ],
            "roles": [
                ("CISO", "Overall accountability for cybersecurity program"),
                ("Security Operations", "24/7 monitoring, incident detection and response"),
                ("IT Security", "Implementation and maintenance of security controls"),
                ("All Employees", "Compliance with security policies and reporting incidents")
            ]
        },
        "Arabic": {
            "title": "سياسة الأمن السيبراني",
            "purpose": "تحدد هذه السياسة متطلبات وضوابط الأمن السيبراني لحماية أصول المعلومات والأنظمة والشبكات من التهديدات السيبرانية بما يتوافق مع الضوابط الأساسية للأمن السيبراني للهيئة الوطنية للأمن السيبراني.",
            "scope": "تنطبق هذه السياسة على جميع أنظمة المعلومات والشبكات والتطبيقات والبيانات والموظفين بما في ذلك المتعاقدين والأطراف الثالثة.",
            "key_requirements": [
                "يجب حماية جميع الأنظمة بحلول كشف واستجابة نقاط النهاية المعتمدة",
                "المصادقة متعددة العوامل إلزامية لجميع الوصول المتميز والاتصالات عن بعد",
                "يجب مراقبة الأحداث الأمنية على مدار الساعة من خلال مركز العمليات الأمنية",
                "يجب إجراء تقييمات الثغرات شهرياً واختبارات الاختراق سنوياً",
                "يجب الإبلاغ عن جميع الحوادث الأمنية خلال ساعة واحدة من الاكتشاف",
                "يتطلب وصول الأطراف الثالثة تقييماً أمنياً ومتطلبات أمنية تعاقدية"
            ],
            "roles": [
                ("رئيس أمن المعلومات", "المسؤولية الشاملة عن برنامج الأمن السيبراني"),
                ("العمليات الأمنية", "المراقبة على مدار الساعة والكشف والاستجابة للحوادث"),
                ("أمن تقنية المعلومات", "تطبيق وصيانة الضوابط الأمنية"),
                ("جميع الموظفين", "الامتثال للسياسات الأمنية والإبلاغ عن الحوادث")
            ]
        }
    },
    "Artificial Intelligence": {
        "English": {
            "title": "AI Governance Policy",
            "purpose": "This policy establishes the governance framework for responsible development, deployment, and operation of Artificial Intelligence (AI) and Machine Learning (ML) systems in alignment with SDAIA AI Ethics Principles and NIST AI Risk Management Framework.",
            "scope": "This policy applies to all AI/ML systems developed, procured, or operated by {org_name}, including predictive models, generative AI, automated decision-making systems, and intelligent automation.",
            "key_requirements": [
                "All AI models must be registered in the central AI Model Registry before production deployment",
                "High-risk AI systems require Ethics Committee approval and human oversight mechanisms",
                "Bias and fairness testing is mandatory for all customer-facing AI applications",
                "Model explainability documentation is required for automated decisions affecting individuals",
                "AI systems must undergo security assessment including adversarial robustness testing",
                "Continuous monitoring for model drift, performance degradation, and bias emergence is required"
            ],
            "roles": [
                ("Chief Data Officer", "Overall accountability for AI governance"),
                ("AI Ethics Committee", "Review and approval of high-risk AI applications"),
                ("Data Science Lead", "Responsible AI development practices"),
                ("Model Risk Management", "AI model validation and monitoring")
            ]
        },
        "Arabic": {
            "title": "سياسة حوكمة الذكاء الاصطناعي",
            "purpose": "تحدد هذه السياسة إطار الحوكمة للتطوير والنشر والتشغيل المسؤول لأنظمة الذكاء الاصطناعي والتعلم الآلي بما يتوافق مع مبادئ أخلاقيات الذكاء الاصطناعي لسدايا وإطار إدارة مخاطر الذكاء الاصطناعي NIST.",
            "scope": "تنطبق هذه السياسة على جميع أنظمة الذكاء الاصطناعي المطورة أو المشتراة أو المشغلة بما في ذلك النماذج التنبؤية والذكاء الاصطناعي التوليدي وأنظمة اتخاذ القرار الآلي.",
            "key_requirements": [
                "يجب تسجيل جميع نماذج الذكاء الاصطناعي في السجل المركزي قبل النشر الإنتاجي",
                "تتطلب أنظمة الذكاء الاصطناعي عالية المخاطر موافقة لجنة الأخلاقيات وآليات إشراف بشري",
                "اختبار التحيز والعدالة إلزامي لجميع تطبيقات الذكاء الاصطناعي الموجهة للعملاء",
                "توثيق قابلية التفسير مطلوب للقرارات الآلية المؤثرة على الأفراد",
                "يجب أن تخضع أنظمة الذكاء الاصطناعي لتقييم أمني يشمل اختبار المتانة",
                "المراقبة المستمرة لانحراف النموذج وتدهور الأداء وظهور التحيز مطلوبة"
            ],
            "roles": [
                ("رئيس البيانات", "المسؤولية الشاملة عن حوكمة الذكاء الاصطناعي"),
                ("لجنة أخلاقيات الذكاء الاصطناعي", "مراجعة واعتماد تطبيقات الذكاء الاصطناعي عالية المخاطر"),
                ("قائد علوم البيانات", "ممارسات تطوير الذكاء الاصطناعي المسؤول"),
                ("إدارة مخاطر النماذج", "التحقق من نماذج الذكاء الاصطناعي ومراقبتها")
            ]
        }
    },
    "Data Management": {
        "English": {
            "title": "Data Governance Policy",
            "purpose": "This policy establishes the data governance framework to ensure data quality, privacy, security, and compliance with the Personal Data Protection Law (PDPL) and NDMO requirements across {org_name}.",
            "scope": "This policy applies to all data assets including personal data, business data, and metadata across all systems, applications, and data stores within {org_name}.",
            "key_requirements": [
                "All data must be classified according to the approved data classification scheme",
                "Personal data processing requires documented legal basis and data subject consent where applicable",
                "Data quality standards must be defined and monitored for all critical data domains",
                "Data retention periods must be defined and enforced; data must be securely disposed after retention",
                "Cross-border data transfers require PDPL compliance assessment and appropriate safeguards",
                "Data subject rights requests must be fulfilled within regulatory timeframes"
            ],
            "roles": [
                ("Chief Data Officer", "Overall accountability for data governance"),
                ("Data Protection Officer", "PDPL compliance and privacy oversight"),
                ("Data Stewards", "Domain-level data quality and governance"),
                ("Data Owners", "Accountability for specific data assets")
            ]
        },
        "Arabic": {
            "title": "سياسة حوكمة البيانات",
            "purpose": "تحدد هذه السياسة إطار حوكمة البيانات لضمان جودة البيانات والخصوصية والأمان والامتثال لنظام حماية البيانات الشخصية ومتطلبات المكتب الوطني لإدارة البيانات.",
            "scope": "تنطبق هذه السياسة على جميع أصول البيانات بما في ذلك البيانات الشخصية وبيانات الأعمال والبيانات الوصفية عبر جميع الأنظمة والتطبيقات ومخازن البيانات.",
            "key_requirements": [
                "يجب تصنيف جميع البيانات وفقاً لمخطط تصنيف البيانات المعتمد",
                "تتطلب معالجة البيانات الشخصية أساساً قانونياً موثقاً وموافقة صاحب البيانات حيثما ينطبق",
                "يجب تحديد ومراقبة معايير جودة البيانات لجميع مجالات البيانات الحيوية",
                "يجب تحديد فترات الاحتفاظ بالبيانات وإنفاذها مع التخلص الآمن بعد انتهاء الفترة",
                "تتطلب عمليات نقل البيانات عبر الحدود تقييم امتثال نظام حماية البيانات الشخصية",
                "يجب تلبية طلبات حقوق أصحاب البيانات ضمن الأطر الزمنية التنظيمية"
            ],
            "roles": [
                ("رئيس البيانات", "المسؤولية الشاملة عن حوكمة البيانات"),
                ("مسؤول حماية البيانات", "الامتثال لنظام حماية البيانات الشخصية والإشراف على الخصوصية"),
                ("أمناء البيانات", "جودة البيانات والحوكمة على مستوى المجال"),
                ("مالكو البيانات", "المسؤولية عن أصول بيانات محددة")
            ]
        }
    },
    "Digital Transformation": {
        "English": {
            "title": "Digital Transformation Policy",
            "purpose": "This policy establishes the governance framework for digital transformation initiatives to ensure alignment with business strategy, Vision 2030 objectives, and DGA Digital Government requirements while managing associated risks.",
            "scope": "This policy applies to all digital transformation programs, projects, and initiatives including digitization, automation, cloud adoption, and new digital product development.",
            "key_requirements": [
                "All digital initiatives must demonstrate alignment with strategic objectives and expected ROI",
                "Cloud adoption must follow the approved cloud strategy and security requirements",
                "Digital projects must follow agile methodology with defined governance checkpoints",
                "Customer-facing digital services must meet accessibility and user experience standards",
                "Legacy system modernization must include data migration and integration planning",
                "Change management and user adoption programs are mandatory for all major initiatives"
            ],
            "roles": [
                ("Chief Digital Officer", "Overall accountability for digital transformation"),
                ("Digital Program Office", "Portfolio management and governance"),
                ("Product Owners", "Digital product strategy and roadmap"),
                ("Change Management", "User adoption and organizational change")
            ]
        },
        "Arabic": {
            "title": "سياسة التحول الرقمي",
            "purpose": "تحدد هذه السياسة إطار حوكمة مبادرات التحول الرقمي لضمان التوافق مع استراتيجية الأعمال وأهداف رؤية ٢٠٣٠ ومتطلبات هيئة الحكومة الرقمية مع إدارة المخاطر المرتبطة.",
            "scope": "تنطبق هذه السياسة على جميع برامج ومشاريع ومبادرات التحول الرقمي بما في ذلك الرقمنة والأتمتة والتبني السحابي وتطوير المنتجات الرقمية الجديدة.",
            "key_requirements": [
                "يجب أن تثبت جميع المبادرات الرقمية التوافق مع الأهداف الاستراتيجية والعائد المتوقع",
                "يجب أن يتبع التبني السحابي الاستراتيجية السحابية المعتمدة والمتطلبات الأمنية",
                "يجب أن تتبع المشاريع الرقمية المنهجية الرشيقة مع نقاط حوكمة محددة",
                "يجب أن تستوفي الخدمات الرقمية الموجهة للعملاء معايير إمكانية الوصول وتجربة المستخدم",
                "يجب أن يشمل تحديث الأنظمة القديمة التخطيط لترحيل البيانات والتكامل",
                "برامج إدارة التغيير وتبني المستخدمين إلزامية لجميع المبادرات الكبرى"
            ],
            "roles": [
                ("رئيس التحول الرقمي", "المسؤولية الشاملة عن التحول الرقمي"),
                ("مكتب البرنامج الرقمي", "إدارة المحفظة والحوكمة"),
                ("مالكو المنتجات", "استراتيجية المنتجات الرقمية وخارطة الطريق"),
                ("إدارة التغيير", "تبني المستخدمين والتغيير المؤسسي")
            ]
        }
    },
    "Global Standards": {
        "English": {
            "title": "Integrated Management System Policy",
            "purpose": "This policy establishes the integrated management system (IMS) framework encompassing information security (ISO 27001), business continuity (ISO 22301), quality management (ISO 9001), and IT service management (ITIL) to ensure consistent governance and continual improvement.",
            "scope": "This policy applies to all management system processes, documentation, controls, and certification activities across {org_name}.",
            "key_requirements": [
                "All management systems must be documented, implemented, and maintained according to ISO requirements",
                "Internal audits must be conducted annually for all management systems",
                "Management reviews must be conducted quarterly with documented outcomes",
                "Non-conformities must be addressed through documented corrective action process",
                "Continual improvement opportunities must be identified and implemented",
                "Certification audits must be prepared for and successfully completed"
            ],
            "roles": [
                ("Management Representative", "Overall accountability for IMS"),
                ("Quality Manager", "ISO 9001 compliance and quality processes"),
                ("ISMS Manager", "ISO 27001 compliance and security controls"),
                ("BCM Manager", "ISO 22301 compliance and continuity planning")
            ]
        },
        "Arabic": {
            "title": "سياسة نظام الإدارة المتكامل",
            "purpose": "تحدد هذه السياسة إطار نظام الإدارة المتكامل الذي يشمل أمن المعلومات (ISO 27001) واستمرارية الأعمال (ISO 22301) وإدارة الجودة (ISO 9001) وإدارة خدمات تقنية المعلومات (ITIL) لضمان الحوكمة المتسقة والتحسين المستمر.",
            "scope": "تنطبق هذه السياسة على جميع عمليات نظام الإدارة والوثائق والضوابط وأنشطة الاعتماد.",
            "key_requirements": [
                "يجب توثيق وتطبيق وصيانة جميع أنظمة الإدارة وفقاً لمتطلبات ISO",
                "يجب إجراء التدقيق الداخلي سنوياً لجميع أنظمة الإدارة",
                "يجب إجراء مراجعات الإدارة ربع سنوياً مع نتائج موثقة",
                "يجب معالجة عدم المطابقات من خلال عملية إجراء تصحيحي موثقة",
                "يجب تحديد وتطبيق فرص التحسين المستمر",
                "يجب الاستعداد لتدقيقات الاعتماد وإتمامها بنجاح"
            ],
            "roles": [
                ("ممثل الإدارة", "المسؤولية الشاملة عن نظام الإدارة المتكامل"),
                ("مدير الجودة", "الامتثال لـ ISO 9001 وعمليات الجودة"),
                ("مدير ISMS", "الامتثال لـ ISO 27001 والضوابط الأمنية"),
                ("مدير BCM", "الامتثال لـ ISO 22301 وتخطيط الاستمرارية")
            ]
        }
    }
}


# =============================================================================
# AUDIT CONTENT
# =============================================================================

AUDIT_CONTENT = {
    "Cyber Security": {
        "English": {
            "title": "Cybersecurity Compliance Audit Report",
            "scope_template": "Assessment of cybersecurity controls against {framework} requirements covering governance, technical controls, operations, and third-party risk management.",
            "methodology": "The audit was conducted using a risk-based approach including documentation review, technical testing, interviews with key personnel, and evidence sampling in accordance with {framework} audit guidelines.",
            "typical_findings": [
                {"area": "Access Control", "finding": "Privileged accounts lack multi-factor authentication", "severity": "High", "recommendation": "Implement MFA for all privileged accounts within 30 days"},
                {"area": "Security Monitoring", "finding": "SIEM coverage incomplete for critical systems", "severity": "High", "recommendation": "Extend SIEM monitoring to all critical assets"},
                {"area": "Vulnerability Management", "finding": "Critical vulnerabilities exceed 30-day remediation window", "severity": "Medium", "recommendation": "Implement automated patching for critical systems"},
                {"area": "Incident Response", "finding": "IR procedures not tested in past 12 months", "severity": "Medium", "recommendation": "Conduct tabletop exercise quarterly"},
                {"area": "Third-Party Risk", "finding": "Vendor security assessments incomplete", "severity": "Medium", "recommendation": "Complete risk assessment for all critical vendors"}
            ]
        },
        "Arabic": {
            "title": "تقرير تدقيق الامتثال للأمن السيبراني",
            "scope_template": "تقييم ضوابط الأمن السيبراني مقابل متطلبات {framework} يشمل الحوكمة والضوابط التقنية والعمليات وإدارة مخاطر الأطراف الثالثة.",
            "methodology": "تم إجراء التدقيق باستخدام نهج قائم على المخاطر يشمل مراجعة الوثائق والاختبار التقني والمقابلات مع الموظفين الرئيسيين وأخذ عينات من الأدلة."
        }
    },
    "Artificial Intelligence": {
        "English": {
            "title": "AI Governance Compliance Audit Report",
            "scope_template": "Assessment of AI governance controls against {framework} requirements covering AI ethics, model risk management, transparency, and accountability.",
            "methodology": "The audit was conducted through review of AI model documentation, bias testing results, governance processes, and interviews with data science and ethics stakeholders.",
            "typical_findings": [
                {"area": "Model Registry", "finding": "AI model inventory incomplete - 40% of production models unregistered", "severity": "High", "recommendation": "Complete model inventory and registration within 60 days"},
                {"area": "Bias Testing", "finding": "Customer-facing models lack fairness testing documentation", "severity": "High", "recommendation": "Implement bias testing for all customer-impacting models"},
                {"area": "Explainability", "finding": "Automated decisions lack explanation mechanisms", "severity": "Medium", "recommendation": "Deploy explainability frameworks for high-risk decisions"},
                {"area": "Model Monitoring", "finding": "No drift detection for production models", "severity": "Medium", "recommendation": "Implement continuous model monitoring platform"},
                {"area": "Ethics Review", "finding": "High-risk AI deployments bypass ethics committee", "severity": "High", "recommendation": "Enforce mandatory ethics review for high-risk AI"}
            ]
        },
        "Arabic": {
            "title": "تقرير تدقيق امتثال حوكمة الذكاء الاصطناعي",
            "scope_template": "تقييم ضوابط حوكمة الذكاء الاصطناعي مقابل متطلبات {framework} يشمل أخلاقيات الذكاء الاصطناعي وإدارة مخاطر النماذج والشفافية والمساءلة.",
            "methodology": "تم إجراء التدقيق من خلال مراجعة وثائق نماذج الذكاء الاصطناعي ونتائج اختبار التحيز وعمليات الحوكمة والمقابلات مع أصحاب المصلحة."
        }
    },
    "Data Management": {
        "English": {
            "title": "Data Governance & PDPL Compliance Audit Report",
            "scope_template": "Assessment of data governance and privacy controls against {framework} and PDPL requirements covering data lifecycle, privacy rights, and data protection.",
            "methodology": "The audit was conducted through data mapping review, privacy impact assessments, consent mechanism testing, and data protection control validation.",
            "typical_findings": [
                {"area": "Data Classification", "finding": "60% of data assets lack classification labels", "severity": "High", "recommendation": "Complete data classification for all sensitive data"},
                {"area": "Consent Management", "finding": "Consent records incomplete for legacy data", "severity": "High", "recommendation": "Implement consent remediation program"},
                {"area": "Data Quality", "finding": "Critical data domains below 85% quality threshold", "severity": "Medium", "recommendation": "Implement data quality monitoring and remediation"},
                {"area": "Retention", "finding": "Data retention policies not enforced", "severity": "Medium", "recommendation": "Implement automated retention and disposal"},
                {"area": "Cross-Border Transfer", "finding": "International transfers lack PDPL assessment", "severity": "High", "recommendation": "Complete PDPL compliance for all cross-border flows"}
            ]
        },
        "Arabic": {
            "title": "تقرير تدقيق حوكمة البيانات والامتثال لنظام حماية البيانات الشخصية",
            "scope_template": "تقييم ضوابط حوكمة البيانات والخصوصية مقابل متطلبات {framework} ونظام حماية البيانات الشخصية يشمل دورة حياة البيانات وحقوق الخصوصية وحماية البيانات.",
            "methodology": "تم إجراء التدقيق من خلال مراجعة خرائط البيانات وتقييمات تأثير الخصوصية واختبار آليات الموافقة والتحقق من ضوابط حماية البيانات."
        }
    },
    "Digital Transformation": {
        "English": {
            "title": "Digital Transformation Governance Audit Report",
            "scope_template": "Assessment of digital transformation governance against {framework} requirements covering strategy alignment, project delivery, and technology management.",
            "methodology": "The audit was conducted through portfolio review, project documentation assessment, technology architecture evaluation, and stakeholder interviews.",
            "typical_findings": [
                {"area": "Strategy Alignment", "finding": "30% of digital projects lack clear business case", "severity": "High", "recommendation": "Implement mandatory business case approval"},
                {"area": "Project Delivery", "finding": "Digital projects averaging 40% budget overrun", "severity": "High", "recommendation": "Strengthen project governance and checkpoints"},
                {"area": "Cloud Governance", "finding": "Shadow IT identified in multiple departments", "severity": "Medium", "recommendation": "Implement cloud discovery and governance"},
                {"area": "Change Management", "finding": "User adoption rates below 50% for new systems", "severity": "Medium", "recommendation": "Mandatory change management for all projects"},
                {"area": "Technical Debt", "finding": "Legacy systems creating integration delays", "severity": "Medium", "recommendation": "Prioritize legacy modernization roadmap"}
            ]
        },
        "Arabic": {
            "title": "تقرير تدقيق حوكمة التحول الرقمي",
            "scope_template": "تقييم حوكمة التحول الرقمي مقابل متطلبات {framework} يشمل التوافق الاستراتيجي وتسليم المشاريع وإدارة التقنية.",
            "methodology": "تم إجراء التدقيق من خلال مراجعة المحفظة وتقييم وثائق المشاريع وتقييم البنية التقنية ومقابلات أصحاب المصلحة."
        }
    },
    "Global Standards": {
        "English": {
            "title": "Integrated Management System Audit Report",
            "scope_template": "Assessment of management system effectiveness against {framework} requirements covering process compliance, documentation control, and continual improvement.",
            "methodology": "The audit was conducted following ISO 19011 guidelines including process audits, documentation review, management interviews, and objective evidence sampling.",
            "typical_findings": [
                {"area": "Documentation Control", "finding": "Document version control inconsistent across departments", "severity": "Medium", "recommendation": "Implement centralized document management system"},
                {"area": "Internal Audit", "finding": "Internal audit program not covering all processes", "severity": "High", "recommendation": "Develop comprehensive audit schedule"},
                {"area": "Corrective Actions", "finding": "30% of CARs overdue beyond target closure", "severity": "Medium", "recommendation": "Implement CAR tracking and escalation"},
                {"area": "Management Review", "finding": "Management review outputs not fully actioned", "severity": "Medium", "recommendation": "Strengthen action tracking from reviews"},
                {"area": "Competency", "finding": "Training records incomplete for key roles", "severity": "Medium", "recommendation": "Complete competency assessment and training"}
            ]
        },
        "Arabic": {
            "title": "تقرير تدقيق نظام الإدارة المتكامل",
            "scope_template": "تقييم فعالية نظام الإدارة مقابل متطلبات {framework} يشمل امتثال العمليات والتحكم بالوثائق والتحسين المستمر.",
            "methodology": "تم إجراء التدقيق وفقاً لإرشادات ISO 19011 يشمل تدقيق العمليات ومراجعة الوثائق ومقابلات الإدارة وأخذ عينات من الأدلة الموضوعية."
        }
    }
}


# =============================================================================
# RISK ANALYSIS CONTENT
# =============================================================================

RISK_CONTENT = {
    "Cyber Security": {
        "categories": ["Ransomware Attack", "Data Breach", "Insider Threat", "Phishing Campaign", "DDoS Attack", "Supply Chain Compromise"],
        "impact_areas": ["Financial Loss", "Regulatory Penalties (NCA)", "Reputation Damage", "Operational Disruption", "Legal Liability"],
        "control_frameworks": ["NCA ECC", "SAMA CSF", "ISO 27001", "NIST CSF"]
    },
    "Artificial Intelligence": {
        "categories": ["Model Bias Incident", "AI Security Breach", "Privacy Violation", "Explainability Failure", "Model Performance Degradation", "Regulatory Non-Compliance"],
        "impact_areas": ["Discriminatory Outcomes", "Regulatory Penalties (SDAIA)", "Customer Trust Loss", "Legal Actions", "Operational Errors"],
        "control_frameworks": ["SDAIA AI Ethics", "NIST AI RMF", "EU AI Act", "ISO 42001"]
    },
    "Data Management": {
        "categories": ["PDPL Violation", "Data Quality Failure", "Unauthorized Access", "Data Loss", "Consent Management Breach", "Cross-Border Transfer Violation"],
        "impact_areas": ["PDPL Fines", "Reputation Damage", "Customer Churn", "Operational Impact", "Legal Actions"],
        "control_frameworks": ["PDPL", "NDMO Guidelines", "ISO 8000", "DAMA DMBOK"]
    },
    "Digital Transformation": {
        "categories": ["Project Failure", "Technology Obsolescence", "Integration Failure", "Change Resistance", "Vendor Lock-in", "Security Vulnerability"],
        "impact_areas": ["Financial Loss", "Competitive Disadvantage", "Customer Experience Degradation", "Operational Inefficiency", "Strategic Misalignment"],
        "control_frameworks": ["COBIT 2019", "TOGAF", "SAFe", "ITIL 4"]
    },
    "Global Standards": {
        "categories": ["Certification Loss", "Major Non-Conformity", "Audit Failure", "Process Deviation", "Competency Gap", "Documentation Failure"],
        "impact_areas": ["Certification Revocation", "Customer Contract Loss", "Reputation Damage", "Operational Issues", "Regulatory Impact"],
        "control_frameworks": ["ISO 27001", "ISO 22301", "ISO 9001", "ISO 31000"]
    }
}


def get_domain_config(domain: str) -> Dict:
    """Get configuration for a specific domain."""
    return DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG["Cyber Security"])


def get_strategy_arabic(domain: str) -> Dict:
    """Get Arabic strategy content for a domain."""
    return STRATEGY_ARABIC.get(domain, STRATEGY_ARABIC["Cyber Security"])


def get_policy_content(domain: str, language: str) -> Dict:
    """Get policy content for a domain and language."""
    domain_content = POLICY_CONTENT.get(domain, POLICY_CONTENT["Cyber Security"])
    return domain_content.get(language, domain_content["English"])


def get_audit_content(domain: str, language: str) -> Dict:
    """Get audit content for a domain and language."""
    domain_content = AUDIT_CONTENT.get(domain, AUDIT_CONTENT["Cyber Security"])
    return domain_content.get(language, domain_content["English"])


def get_risk_content(domain: str) -> Dict:
    """Get risk analysis content for a domain."""
    return RISK_CONTENT.get(domain, RISK_CONTENT["Cyber Security"])
