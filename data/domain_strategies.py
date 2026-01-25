"""
Mizan GRC - Domain-Specific Strategy Templates
Each domain has unique strategic pillars, initiatives, KPIs, and roadmaps.
"""

from typing import Dict, Any


def get_domain_strategy_content(domain: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get domain-specific strategy content.
    
    Returns dict with:
    - vision: Executive vision statement
    - objectives: List of strategic objectives
    - pillars: List of strategic pillars with initiatives
    - roadmap: Implementation roadmap items
    - kpis: Key Performance Indicators
    - kris: Key Risk Indicators
    """
    
    org_name = context.get('org_name', 'Organization')
    sector = context.get('sector', 'General')
    
    strategies = {
        "Cyber Security": _get_cyber_strategy(org_name, sector),
        "Artificial Intelligence": _get_ai_strategy(org_name, sector),
        "Data Management": _get_data_strategy(org_name, sector),
        "Digital Transformation": _get_dt_strategy(org_name, sector),
        "Global Standards": _get_global_strategy(org_name, sector),
    }
    
    return strategies.get(domain, strategies["Cyber Security"])


def _get_cyber_strategy(org_name: str, sector: str) -> Dict[str, Any]:
    """Cybersecurity-specific strategy content."""
    return {
        "vision": f"To establish {org_name} as a cyber-resilient organization with world-class security capabilities that protect critical assets, ensure regulatory compliance with NCA requirements, and enable secure digital innovation.",
        "vision_ar": f"تأسيس {org_name} كمنظمة مرنة سيبرانياً بقدرات أمنية عالمية المستوى تحمي الأصول الحيوية وتضمن الامتثال للمتطلبات التنظيمية وتمكّن الابتكار الرقمي الآمن.",
        
        "objectives": [
            "Achieve 95%+ compliance with NCA ECC/CCC frameworks within 18 months",
            "Reduce Mean Time to Detect (MTTD) threats to under 4 hours",
            "Implement Zero Trust architecture across critical systems",
            "Build 24/7 Security Operations Center (SOC) capability",
            "Achieve cyber insurance readiness with documented controls"
        ],
        "objectives_ar": [
            "تحقيق امتثال ٩٥٪+ لضوابط الهيئة الوطنية للأمن السيبراني خلال ١٨ شهر",
            "تقليل متوسط وقت اكتشاف التهديدات إلى أقل من ٤ ساعات",
            "تطبيق بنية انعدام الثقة عبر الأنظمة الحيوية",
            "بناء قدرات مركز عمليات أمنية يعمل على مدار الساعة",
            "تحقيق جاهزية التأمين السيبراني مع ضوابط موثقة"
        ],
        
        "pillars": [
            {
                "name": "Security Governance & Risk",
                "name_ar": "حوكمة الأمن والمخاطر",
                "initiatives": [
                    "Establish Cybersecurity Steering Committee with C-level sponsorship",
                    "Implement enterprise security policy framework (20+ policies)",
                    "Deploy GRC platform for continuous compliance monitoring",
                    "Conduct quarterly cyber risk assessments with board reporting"
                ]
            },
            {
                "name": "Threat Detection & Response",
                "name_ar": "كشف التهديدات والاستجابة",
                "initiatives": [
                    "Deploy SIEM/SOAR with 24/7 monitoring capability",
                    "Implement EDR/XDR across all endpoints",
                    "Establish Incident Response team with playbooks",
                    "Integrate threat intelligence feeds"
                ]
            },
            {
                "name": "Identity & Access Security",
                "name_ar": "أمن الهوية والوصول",
                "initiatives": [
                    "Deploy MFA for all users (phishing-resistant for privileged)",
                    "Implement Privileged Access Management (PAM)",
                    "Automate access certification and reviews",
                    "Establish Identity Governance program"
                ]
            },
            {
                "name": "Network & Infrastructure Security",
                "name_ar": "أمن الشبكات والبنية التحتية",
                "initiatives": [
                    "Implement network segmentation and micro-segmentation",
                    "Deploy Next-Gen Firewall with IPS/IDS",
                    "Establish secure remote access (ZTNA)",
                    "Implement DNS security and web filtering"
                ]
            },
            {
                "name": "Security Culture & Awareness",
                "name_ar": "ثقافة الأمن والتوعية",
                "initiatives": [
                    "Launch comprehensive security awareness program",
                    "Conduct monthly phishing simulations",
                    "Establish security champions network",
                    "Implement role-based security training"
                ]
            }
        ],
        
        "roadmap": [
            {"phase": "Foundation", "initiative": "Security Governance Framework", "duration": 3, "cost": 350000, "owner": "CISO", "kpi": "Policy coverage 100%"},
            {"phase": "Foundation", "initiative": "Risk Assessment & Gap Analysis", "duration": 2, "cost": 200000, "owner": "Risk Manager", "kpi": "Risks identified & prioritized"},
            {"phase": "Foundation", "initiative": "Quick Wins (MFA, Patching)", "duration": 3, "cost": 500000, "owner": "Security Lead", "kpi": "Critical vulnerabilities reduced 80%"},
            {"phase": "Build", "initiative": "SIEM/SOC Implementation", "duration": 6, "cost": 2500000, "owner": "SOC Manager", "kpi": "MTTD < 4 hours"},
            {"phase": "Build", "initiative": "IAM & PAM Deployment", "duration": 6, "cost": 1500000, "owner": "IAM Lead", "kpi": "MFA 100%, PAM for all privileged"},
            {"phase": "Build", "initiative": "EDR/XDR Rollout", "duration": 4, "cost": 800000, "owner": "Endpoint Security", "kpi": "100% endpoint coverage"},
            {"phase": "Build", "initiative": "Network Segmentation", "duration": 6, "cost": 1200000, "owner": "Network Security", "kpi": "Critical systems isolated"},
            {"phase": "Optimize", "initiative": "Security Automation (SOAR)", "duration": 6, "cost": 600000, "owner": "Security Arch", "kpi": "50% automation of L1 alerts"},
            {"phase": "Optimize", "initiative": "Threat Hunting Program", "duration": 4, "cost": 400000, "owner": "SOC Lead", "kpi": "Proactive threat detection"},
            {"phase": "Optimize", "initiative": "Red Team Assessment", "duration": 2, "cost": 300000, "owner": "External", "kpi": "Validate security posture"}
        ],
        
        "kpis": [
            ("NCA Compliance Score", "95%", "Current baseline"),
            ("Mean Time to Detect (MTTD)", "< 4 hours", "Industry: 24 hours"),
            ("Mean Time to Respond (MTTR)", "< 2 hours", "Industry: 8 hours"),
            ("Phishing Click Rate", "< 3%", "Current: ~15%"),
            ("Patch Compliance (Critical)", "100% in 72 hours", "Current: 14 days"),
            ("Security Training Completion", "95%", "Current: 60%")
        ],
        
        "kris": [
            ("Critical Vulnerabilities Unpatched > 30 days", "< 5", "Red > 20"),
            ("Security Incidents (Critical)", "< 2/quarter", "Red > 5"),
            ("Failed Phishing Simulations", "< 5%", "Red > 15%"),
            ("Privileged Account Violations", "0", "Red > 3"),
            ("Third-Party Security Findings", "< 10 high", "Red > 25")
        ]
    }


def _get_ai_strategy(org_name: str, sector: str) -> Dict[str, Any]:
    """AI Governance-specific strategy content."""
    return {
        "vision": f"To position {org_name} as a leader in responsible AI adoption, ensuring all AI/ML systems are transparent, fair, secure, and compliant with SDAIA guidelines while delivering measurable business value.",
        "vision_ar": f"تمكين {org_name} كرائد في تبني الذكاء الاصطناعي المسؤول، وضمان شفافية وعدالة وأمان جميع أنظمة الذكاء الاصطناعي والتعلم الآلي مع الامتثال لإرشادات سدايا وتحقيق قيمة أعمال قابلة للقياس.",
        
        "objectives": [
            "Establish AI Ethics Committee and governance framework within 6 months",
            "Achieve 100% AI model inventory and risk classification",
            "Implement bias detection and fairness monitoring for all production models",
            "Ensure SDAIA AI Ethics Principles compliance across all AI initiatives",
            "Reduce AI-related incidents by 80% through proactive governance"
        ],
        "objectives_ar": [
            "إنشاء لجنة أخلاقيات الذكاء الاصطناعي وإطار الحوكمة خلال ٦ أشهر",
            "تحقيق جرد كامل لنماذج الذكاء الاصطناعي وتصنيف المخاطر",
            "تطبيق كشف التحيز ومراقبة العدالة لجميع النماذج الإنتاجية",
            "ضمان الامتثال لمبادئ أخلاقيات سدايا عبر جميع مبادرات الذكاء الاصطناعي",
            "تقليل الحوادث المتعلقة بالذكاء الاصطناعي بنسبة ٨٠٪ من خلال الحوكمة الاستباقية"
        ],
        
        "pillars": [
            {
                "name": "AI Governance Framework",
                "name_ar": "إطار حوكمة الذكاء الاصطناعي",
                "initiatives": [
                    "Establish AI Ethics Committee with cross-functional representation",
                    "Develop AI policy framework (development, deployment, monitoring)",
                    "Implement AI model registry and lifecycle management",
                    "Create AI risk assessment methodology aligned with NIST AI RMF"
                ]
            },
            {
                "name": "Responsible AI & Ethics",
                "name_ar": "الذكاء الاصطناعي المسؤول والأخلاقيات",
                "initiatives": [
                    "Deploy bias detection and fairness testing tools",
                    "Implement explainability frameworks (SHAP, LIME)",
                    "Establish human oversight requirements for high-risk AI",
                    "Create AI incident response and escalation procedures"
                ]
            },
            {
                "name": "AI Security & Privacy",
                "name_ar": "أمن وخصوصية الذكاء الاصطناعي",
                "initiatives": [
                    "Implement adversarial robustness testing",
                    "Deploy data privacy controls for training data",
                    "Establish model security (tampering, extraction prevention)",
                    "Implement privacy-preserving ML techniques where required"
                ]
            },
            {
                "name": "Model Performance & Monitoring",
                "name_ar": "أداء النماذج والمراقبة",
                "initiatives": [
                    "Deploy ML monitoring platform (drift, performance)",
                    "Implement automated model retraining pipelines",
                    "Establish model performance SLAs and alerting",
                    "Create model validation and testing standards"
                ]
            },
            {
                "name": "AI Literacy & Culture",
                "name_ar": "ثقافة ومحو أمية الذكاء الاصطناعي",
                "initiatives": [
                    "Launch AI literacy program for business stakeholders",
                    "Train data scientists on responsible AI practices",
                    "Establish AI Center of Excellence",
                    "Create AI use case approval and prioritization process"
                ]
            }
        ],
        
        "roadmap": [
            {"phase": "Foundation", "initiative": "AI Governance Framework", "duration": 3, "cost": 250000, "owner": "Chief Data Officer", "kpi": "Framework approved"},
            {"phase": "Foundation", "initiative": "AI Model Inventory", "duration": 2, "cost": 150000, "owner": "AI Lead", "kpi": "100% models catalogued"},
            {"phase": "Foundation", "initiative": "Risk Classification", "duration": 2, "cost": 100000, "owner": "Risk Manager", "kpi": "All models risk-rated"},
            {"phase": "Build", "initiative": "Bias & Fairness Tools", "duration": 4, "cost": 400000, "owner": "MLOps Lead", "kpi": "Tools deployed for high-risk models"},
            {"phase": "Build", "initiative": "ML Monitoring Platform", "duration": 5, "cost": 600000, "owner": "Platform Team", "kpi": "Real-time monitoring active"},
            {"phase": "Build", "initiative": "Explainability Implementation", "duration": 4, "cost": 300000, "owner": "Data Science Lead", "kpi": "Explainability for customer-facing AI"},
            {"phase": "Build", "initiative": "AI Security Controls", "duration": 4, "cost": 350000, "owner": "Security Team", "kpi": "Security testing integrated"},
            {"phase": "Optimize", "initiative": "Automated Governance", "duration": 6, "cost": 500000, "owner": "Artificial Intelligence", "kpi": "80% automated checks"},
            {"phase": "Optimize", "initiative": "AI CoE Maturity", "duration": 6, "cost": 400000, "owner": "CDO", "kpi": "CoE fully operational"}
        ],
        
        "kpis": [
            ("AI Model Inventory Coverage", "100%", "Currently unknown"),
            ("High-Risk Models with Bias Testing", "100%", "Currently: 0%"),
            ("Model Documentation Compliance", "100%", "Currently: ~30%"),
            ("AI Incident Response Time", "< 4 hours", "Currently: ad-hoc"),
            ("Explainability Coverage (Customer AI)", "100%", "Currently: ~20%"),
            ("AI Training Completion (Data Scientists)", "100%", "Currently: 40%")
        ],
        
        "kris": [
            ("Unmonitored Production Models", "0", "Red > 5"),
            ("Models with Detected Bias", "0 unresolved", "Red > 2"),
            ("Model Drift Incidents", "< 3/quarter", "Red > 10"),
            ("AI Ethics Violations", "0", "Red > 1"),
            ("Unexplained Model Decisions (complaints)", "< 5/month", "Red > 20")
        ]
    }


def _get_data_strategy(org_name: str, sector: str) -> Dict[str, Any]:
    """Data Management-specific strategy content."""
    return {
        "vision": f"To transform {org_name} into a data-driven organization with enterprise-wide data governance, ensuring data quality, privacy compliance with PDPL/NDMO, and enabling data monetization opportunities.",
        "vision_ar": f"تحويل {org_name} إلى منظمة تعتمد على البيانات مع حوكمة بيانات مؤسسية شاملة، وضمان جودة البيانات والامتثال لنظام حماية البيانات الشخصية وتمكين فرص تحقيق الدخل من البيانات.",
        
        "objectives": [
            "Achieve PDPL compliance across all personal data processing activities",
            "Implement enterprise data catalog with 100% critical data asset coverage",
            "Improve data quality score to 95%+ for critical data domains",
            "Reduce data-related incidents by 70% through proactive governance",
            "Enable self-service analytics for 80% of business users"
        ],
        "objectives_ar": [
            "تحقيق الامتثال لنظام حماية البيانات الشخصية عبر جميع أنشطة معالجة البيانات",
            "تطبيق كتالوج بيانات مؤسسي بتغطية ١٠٠٪ لأصول البيانات الحيوية",
            "تحسين درجة جودة البيانات إلى ٩٥٪+ للمجالات الحيوية",
            "تقليل الحوادث المتعلقة بالبيانات بنسبة ٧٠٪ من خلال الحوكمة الاستباقية",
            "تمكين التحليلات الذاتية لـ ٨٠٪ من مستخدمي الأعمال"
        ],
        
        "pillars": [
            {
                "name": "Data Governance & Stewardship",
                "name_ar": "حوكمة البيانات والإشراف",
                "initiatives": [
                    "Establish Data Governance Council with executive sponsorship",
                    "Implement data stewardship program with domain stewards",
                    "Deploy enterprise data catalog and metadata management",
                    "Create data policies (classification, retention, sharing)"
                ]
            },
            {
                "name": "Data Quality Management",
                "name_ar": "إدارة جودة البيانات",
                "initiatives": [
                    "Implement data quality monitoring and profiling tools",
                    "Establish data quality rules and thresholds by domain",
                    "Create data quality dashboards and scorecards",
                    "Implement automated data cleansing and enrichment"
                ]
            },
            {
                "name": "Data Privacy & Protection",
                "name_ar": "خصوصية البيانات وحمايتها",
                "initiatives": [
                    "Conduct PDPL gap assessment and remediation",
                    "Implement consent management platform",
                    "Deploy data masking and anonymization tools",
                    "Establish data subject rights fulfillment process"
                ]
            },
            {
                "name": "Data Architecture & Integration",
                "name_ar": "هندسة البيانات والتكامل",
                "initiatives": [
                    "Design target data architecture (lake/warehouse/mesh)",
                    "Implement master data management for key domains",
                    "Deploy data integration and ETL/ELT pipelines",
                    "Establish API-based data sharing standards"
                ]
            },
            {
                "name": "Data Literacy & Enablement",
                "name_ar": "محو أمية البيانات والتمكين",
                "initiatives": [
                    "Launch data literacy training program",
                    "Deploy self-service BI and analytics tools",
                    "Establish data community of practice",
                    "Create data product management capability"
                ]
            }
        ],
        
        "roadmap": [
            {"phase": "Foundation", "initiative": "Data Governance Framework", "duration": 3, "cost": 300000, "owner": "CDO", "kpi": "Framework approved & council active"},
            {"phase": "Foundation", "initiative": "Data Catalog Implementation", "duration": 4, "cost": 500000, "owner": "Data Architect", "kpi": "Critical assets catalogued"},
            {"phase": "Foundation", "initiative": "PDPL Gap Assessment", "duration": 2, "cost": 200000, "owner": "DPO", "kpi": "Gaps identified & prioritized"},
            {"phase": "Build", "initiative": "Data Quality Platform", "duration": 5, "cost": 600000, "owner": "Data Quality Lead", "kpi": "DQ monitoring active"},
            {"phase": "Build", "initiative": "Privacy Controls (PDPL)", "duration": 6, "cost": 800000, "owner": "DPO", "kpi": "PDPL compliance achieved"},
            {"phase": "Build", "initiative": "MDM Implementation", "duration": 6, "cost": 900000, "owner": "Data Architect", "kpi": "Golden records for key entities"},
            {"phase": "Build", "initiative": "Data Stewardship Program", "duration": 4, "cost": 250000, "owner": "Data Governance", "kpi": "Stewards trained & active"},
            {"phase": "Optimize", "initiative": "Self-Service Analytics", "duration": 6, "cost": 700000, "owner": "BI Lead", "kpi": "80% user adoption"},
            {"phase": "Optimize", "initiative": "Data Monetization", "duration": 6, "cost": 400000, "owner": "CDO", "kpi": "Data products launched"}
        ],
        
        "kpis": [
            ("PDPL Compliance Score", "100%", "Currently: assessment needed"),
            ("Data Catalog Coverage (Critical)", "100%", "Currently: ~20%"),
            ("Data Quality Score (Critical Domains)", "95%+", "Currently: ~70%"),
            ("Data Steward Coverage", "100% domains", "Currently: 30%"),
            ("Self-Service Analytics Adoption", "80%", "Currently: 25%"),
            ("Data Incident Resolution Time", "< 24 hours", "Currently: 5 days")
        ],
        
        "kris": [
            ("PDPL Violations/Complaints", "0", "Red > 2"),
            ("Critical Data Quality Issues", "< 5", "Red > 20"),
            ("Unclassified Sensitive Data", "0", "Red > 10 datasets"),
            ("Data Breach Incidents", "0", "Red > 1"),
            ("Consent Management Failures", "0", "Red > 5")
        ]
    }


def _get_dt_strategy(org_name: str, sector: str) -> Dict[str, Any]:
    """Digital Transformation-specific strategy content."""
    return {
        "vision": f"To accelerate {org_name}'s digital transformation journey, delivering exceptional customer experiences, operational excellence, and new digital revenue streams aligned with Saudi Vision 2030.",
        "vision_ar": f"تسريع رحلة التحول الرقمي لـ {org_name}، وتقديم تجارب عملاء استثنائية والتميز التشغيلي ومصادر إيرادات رقمية جديدة بما يتوافق مع رؤية السعودية ٢٠٣٠.",
        
        "objectives": [
            "Achieve 80% digital channel adoption for customer transactions",
            "Reduce operational costs by 30% through process automation",
            "Launch 5 new digital products/services within 24 months",
            "Improve employee digital productivity by 40%",
            "Achieve top-quartile digital maturity in the sector"
        ],
        "objectives_ar": [
            "تحقيق ٨٠٪ تبني للقنوات الرقمية في معاملات العملاء",
            "تقليل التكاليف التشغيلية بنسبة ٣٠٪ من خلال أتمتة العمليات",
            "إطلاق ٥ منتجات/خدمات رقمية جديدة خلال ٢٤ شهر",
            "تحسين إنتاجية الموظفين الرقمية بنسبة ٤٠٪",
            "تحقيق النضج الرقمي ضمن الربع الأعلى في القطاع"
        ],
        
        "pillars": [
            {
                "name": "Customer Experience Transformation",
                "name_ar": "تحويل تجربة العملاء",
                "initiatives": [
                    "Implement omnichannel customer engagement platform",
                    "Deploy AI-powered chatbot and virtual assistant",
                    "Create personalized digital customer journeys",
                    "Implement real-time customer feedback and NPS tracking"
                ]
            },
            {
                "name": "Process Automation & Efficiency",
                "name_ar": "أتمتة العمليات والكفاءة",
                "initiatives": [
                    "Deploy RPA for high-volume manual processes",
                    "Implement workflow automation and BPM platform",
                    "Digitize paper-based processes end-to-end",
                    "Establish process mining and optimization capability"
                ]
            },
            {
                "name": "Digital Products & Innovation",
                "name_ar": "المنتجات الرقمية والابتكار",
                "initiatives": [
                    "Establish digital product management capability",
                    "Create innovation lab and rapid prototyping",
                    "Implement design thinking methodology",
                    "Launch digital marketplace/platform initiatives"
                ]
            },
            {
                "name": "Technology Modernization",
                "name_ar": "تحديث التقنية",
                "initiatives": [
                    "Execute cloud migration strategy",
                    "Implement API-first architecture",
                    "Modernize legacy core systems",
                    "Deploy low-code/no-code platforms for citizen developers"
                ]
            },
            {
                "name": "Digital Culture & Capability",
                "name_ar": "الثقافة والقدرات الرقمية",
                "initiatives": [
                    "Launch digital skills training program",
                    "Implement agile ways of working",
                    "Establish change management and adoption program",
                    "Create digital champions network"
                ]
            }
        ],
        
        "roadmap": [
            {"phase": "Foundation", "initiative": "Digital Strategy & Roadmap", "duration": 2, "cost": 300000, "owner": "CDO", "kpi": "Strategy approved"},
            {"phase": "Foundation", "initiative": "Digital Maturity Assessment", "duration": 1, "cost": 150000, "owner": "Transformation Lead", "kpi": "Baseline established"},
            {"phase": "Foundation", "initiative": "Quick Wins (Mobile App, Portal)", "duration": 4, "cost": 800000, "owner": "Digital Products", "kpi": "20% digital adoption"},
            {"phase": "Build", "initiative": "Customer Platform", "duration": 8, "cost": 2500000, "owner": "CX Lead", "kpi": "Omnichannel launched"},
            {"phase": "Build", "initiative": "RPA Program", "duration": 6, "cost": 1200000, "owner": "Automation Lead", "kpi": "20 processes automated"},
            {"phase": "Build", "initiative": "Cloud Migration", "duration": 12, "cost": 3000000, "owner": "Cloud Architect", "kpi": "60% workloads migrated"},
            {"phase": "Build", "initiative": "API Platform", "duration": 6, "cost": 800000, "owner": "Integration Lead", "kpi": "API gateway live"},
            {"phase": "Optimize", "initiative": "AI/ML Integration", "duration": 6, "cost": 1000000, "owner": "AI Lead", "kpi": "5 AI use cases deployed"},
            {"phase": "Optimize", "initiative": "Digital Products Launch", "duration": 8, "cost": 1500000, "owner": "Product Manager", "kpi": "3 new digital products"}
        ],
        
        "kpis": [
            ("Digital Channel Adoption", "80%", "Currently: 35%"),
            ("Customer Satisfaction (Digital)", "4.5/5", "Currently: 3.8/5"),
            ("Process Automation Rate", "60%", "Currently: 15%"),
            ("Time-to-Market (New Features)", "< 4 weeks", "Currently: 12 weeks"),
            ("Digital Revenue Contribution", "25%", "Currently: 10%"),
            ("Employee Digital Proficiency", "80%", "Currently: 45%")
        ],
        
        "kris": [
            ("Digital Service Downtime", "< 0.1%", "Red > 1%"),
            ("Digital Project Delays", "< 10%", "Red > 30%"),
            ("Customer Digital Complaints", "< 50/month", "Red > 200"),
            ("Legacy System Dependencies", "< 20%", "Red > 50%"),
            ("Digital Skills Gap", "< 20%", "Red > 40%")
        ]
    }


def _get_global_strategy(org_name: str, sector: str) -> Dict[str, Any]:
    """Global Standards & Compliance-specific strategy content."""
    return {
        "vision": f"To establish {org_name} as a benchmark organization for management system excellence, achieving and maintaining certifications in ISO 27001, ISO 22301, ISO 9001, and ITIL while driving continuous improvement.",
        "vision_ar": f"ترسيخ {org_name} كمنظمة مرجعية للتميز في أنظمة الإدارة، وتحقيق والحفاظ على شهادات ISO 27001 و ISO 22301 و ISO 9001 و ITIL مع تحقيق التحسين المستمر.",
        
        "objectives": [
            "Achieve ISO 27001:2022 certification within 12 months",
            "Implement ISO 22301 business continuity management system",
            "Attain ISO 9001 quality management certification",
            "Achieve ITIL 4 maturity for IT service management",
            "Establish integrated management system (IMS) framework"
        ],
        "objectives_ar": [
            "الحصول على شهادة ISO 27001:2022 خلال ١٢ شهر",
            "تطبيق نظام إدارة استمرارية الأعمال ISO 22301",
            "الحصول على شهادة إدارة الجودة ISO 9001",
            "تحقيق نضج ITIL 4 لإدارة خدمات تقنية المعلومات",
            "إنشاء إطار نظام إدارة متكامل (IMS)"
        ],
        
        "pillars": [
            {
                "name": "Information Security (ISO 27001)",
                "name_ar": "أمن المعلومات (ISO 27001)",
                "initiatives": [
                    "Conduct ISO 27001 gap assessment",
                    "Implement ISMS documentation and controls",
                    "Establish internal audit program",
                    "Prepare for Stage 1 and Stage 2 certification audits"
                ]
            },
            {
                "name": "Business Continuity (ISO 22301)",
                "name_ar": "استمرارية الأعمال (ISO 22301)",
                "initiatives": [
                    "Conduct Business Impact Analysis (BIA)",
                    "Develop and test Business Continuity Plans",
                    "Establish crisis management and communication",
                    "Implement DR capabilities and testing"
                ]
            },
            {
                "name": "Quality Management (ISO 9001)",
                "name_ar": "إدارة الجودة (ISO 9001)",
                "initiatives": [
                    "Define quality policy and objectives",
                    "Implement process documentation standards",
                    "Establish quality metrics and monitoring",
                    "Create customer feedback and improvement loop"
                ]
            },
            {
                "name": "IT Service Management (ITIL)",
                "name_ar": "إدارة خدمات تقنية المعلومات (ITIL)",
                "initiatives": [
                    "Implement ITIL service desk and incident management",
                    "Deploy change and release management processes",
                    "Establish service catalog and SLA management",
                    "Implement CMDB and configuration management"
                ]
            },
            {
                "name": "Integrated Management System",
                "name_ar": "نظام الإدارة المتكامل",
                "initiatives": [
                    "Harmonize policies across management systems",
                    "Implement unified document control",
                    "Establish combined internal audit program",
                    "Create integrated management review process"
                ]
            }
        ],
        
        "roadmap": [
            {"phase": "Foundation", "initiative": "Gap Assessment (All Standards)", "duration": 2, "cost": 250000, "owner": "Compliance Lead", "kpi": "Gaps identified"},
            {"phase": "Foundation", "initiative": "IMS Framework Design", "duration": 2, "cost": 150000, "owner": "Quality Manager", "kpi": "Framework approved"},
            {"phase": "Foundation", "initiative": "Documentation Development", "duration": 4, "cost": 300000, "owner": "Documentation Lead", "kpi": "Core docs complete"},
            {"phase": "Build", "initiative": "ISO 27001 Implementation", "duration": 8, "cost": 600000, "owner": "ISMS Manager", "kpi": "Stage 1 audit passed"},
            {"phase": "Build", "initiative": "ISO 22301 Implementation", "duration": 6, "cost": 400000, "owner": "BCM Manager", "kpi": "BCP tested"},
            {"phase": "Build", "initiative": "ITIL Process Implementation", "duration": 6, "cost": 500000, "owner": "Service Manager", "kpi": "ITSM processes live"},
            {"phase": "Build", "initiative": "Internal Audit Program", "duration": 3, "cost": 200000, "owner": "Internal Audit", "kpi": "Audit program active"},
            {"phase": "Optimize", "initiative": "Certification Audits", "duration": 4, "cost": 400000, "owner": "Compliance Lead", "kpi": "Certifications achieved"},
            {"phase": "Optimize", "initiative": "Continuous Improvement", "duration": 6, "cost": 250000, "owner": "Quality Manager", "kpi": "KPIs trending positive"}
        ],
        
        "kpis": [
            ("ISO 27001 Certification", "Achieved", "Currently: Not certified"),
            ("ISO 22301 Certification", "Achieved", "Currently: Not certified"),
            ("Internal Audit Findings Closure", "< 30 days", "Currently: 60 days"),
            ("Management Review Completion", "Quarterly", "Currently: Annual"),
            ("Process Documentation Coverage", "100%", "Currently: 60%"),
            ("Employee Training (Standards)", "100%", "Currently: 40%")
        ],
        
        "kris": [
            ("Major Non-Conformities", "0", "Red > 3"),
            ("Overdue Corrective Actions", "< 5", "Red > 15"),
            ("Failed Surveillance Audits", "0", "Red > 1"),
            ("BCP Test Failures", "0", "Red > 2"),
            ("SLA Breaches", "< 5%", "Red > 15%")
        ]
    }
