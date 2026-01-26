"""
Mizan GRC - Domain-Specific Audit and Risk Content
Comprehensive audit findings and risk scenarios for each domain.
"""

from typing import Dict, List, Any

# =============================================================================
# DOMAIN-SPECIFIC AUDIT FINDINGS
# =============================================================================

DOMAIN_AUDIT_FINDINGS = {
    "Cyber Security": {
        "findings_en": [
            {
                "id": "CS-F01",
                "title": "Privileged Access Management Gaps",
                "control_ref": "NCA ECC 2-3-1, ISO 27001 A.9.2.3",
                "priority": "HIGH",
                "observation": "Privileged accounts lack adequate controls. 23% of admin accounts have no MFA, PAM solution covers only 45% of privileged access, and quarterly access reviews are not performed consistently.",
                "evidence": ["AD privileged group listing", "PAM coverage report", "Access review records"],
                "root_cause": "Process: Undocumented PAM onboarding; Technology: Legacy systems not integrated",
                "risk_impact": "Unauthorized privileged access could lead to data breach or system compromise",
                "recommendation": "Implement MFA for all privileged accounts; Expand PAM coverage to 100%",
                "target_date": "Q1 2025"
            },
            {
                "id": "CS-F02",
                "title": "Security Monitoring Coverage Gaps",
                "control_ref": "NCA ECC 2-7-1, ISO 27001 A.12.4.1",
                "priority": "HIGH",
                "observation": "SIEM coverage is incomplete with only 67% of critical systems sending logs. Alert rules not updated in 8 months.",
                "evidence": ["SIEM data source inventory", "Alert rule configuration", "SOC shift schedule"],
                "root_cause": "Technology: Integration challenges; People: SOC understaffing",
                "risk_impact": "Delayed threat detection increasing MTTD",
                "recommendation": "Complete SIEM integration; Update alert rules quarterly",
                "target_date": "Q1-Q2 2025"
            },
            {
                "id": "CS-F03",
                "title": "Vulnerability Management Delays",
                "control_ref": "NCA ECC 2-6-2, ISO 27001 A.12.6.1",
                "priority": "MEDIUM",
                "observation": "Critical vulnerabilities not patched within SLA. Average remediation time is 45 days vs 14-day target.",
                "evidence": ["Vulnerability scan reports", "Patch deployment logs", "Exception records"],
                "root_cause": "Process: No automated patching; Governance: Unclear ownership",
                "risk_impact": "Extended exposure to known vulnerabilities",
                "recommendation": "Implement automated patch management; Define clear ownership",
                "target_date": "Q1 2025"
            },
            {
                "id": "CS-F04",
                "title": "Incident Response Plan Not Tested",
                "control_ref": "NCA ECC 2-9-1, ISO 27001 A.16.1.1",
                "priority": "MEDIUM",
                "observation": "Incident response plan not tested in past 12 months. No tabletop exercises conducted.",
                "evidence": ["IR plan document", "Test records", "Incident logs"],
                "root_cause": "People: Resource constraints; Process: No scheduled testing",
                "risk_impact": "Potential delays in incident containment",
                "recommendation": "Schedule quarterly tabletop exercises",
                "target_date": "Q1 2025"
            }
        ],
        "findings_ar": [
            {
                "id": "CS-F01",
                "title": "فجوات في إدارة الوصول المتميز",
                "control_ref": "NCA ECC 2-3-1، ISO 27001 A.9.2.3",
                "priority": "عالي",
                "observation": "الحسابات المتميزة تفتقر إلى ضوابط كافية. ٢٣٪ من حسابات المسؤولين بدون MFA، وتغطية PAM ٤٥٪ فقط",
                "evidence": ["قائمة مجموعات الصلاحيات", "تقرير تغطية PAM", "سجلات مراجعة الوصول"],
                "root_cause": "العملية: عدم توثيق إجراءات PAM؛ التقنية: عدم تكامل الأنظمة القديمة",
                "risk_impact": "الوصول غير المصرح به قد يؤدي إلى اختراق البيانات",
                "recommendation": "تطبيق MFA لجميع الحسابات المتميزة؛ توسيع تغطية PAM إلى ١٠٠٪",
                "target_date": "الربع الأول ٢٠٢٥"
            },
            {
                "id": "CS-F02",
                "title": "فجوات في تغطية المراقبة الأمنية",
                "control_ref": "NCA ECC 2-7-1، ISO 27001 A.12.4.1",
                "priority": "عالي",
                "observation": "تغطية SIEM غير مكتملة مع ٦٧٪ فقط من الأنظمة الحيوية. قواعد التنبيه لم تُحدّث منذ ٨ أشهر",
                "evidence": ["جرد مصادر بيانات SIEM", "تكوين قواعد التنبيه", "جدول نوبات SOC"],
                "root_cause": "التقنية: تحديات التكامل؛ الأفراد: نقص موظفي SOC",
                "risk_impact": "تأخر اكتشاف التهديدات",
                "recommendation": "استكمال تكامل SIEM؛ تحديث قواعد التنبيه ربع سنوياً",
                "target_date": "الربع الأول-الثاني ٢٠٢٥"
            },
            {
                "id": "CS-F03",
                "title": "تأخر إدارة الثغرات",
                "control_ref": "NCA ECC 2-6-2، ISO 27001 A.12.6.1",
                "priority": "متوسط",
                "observation": "الثغرات الحرجة لم تُعالج ضمن الإطار الزمني المحدد. متوسط وقت المعالجة ٤٥ يوماً مقابل ١٤ يوماً كهدف",
                "evidence": ["تقارير فحص الثغرات", "سجلات نشر التصحيحات", "سجلات الاستثناءات"],
                "root_cause": "العملية: عدم وجود تصحيح آلي؛ الحوكمة: عدم وضوح الملكية",
                "risk_impact": "التعرض المطول للثغرات المعروفة",
                "recommendation": "تطبيق إدارة التصحيحات الآلية؛ تحديد ملكية واضحة",
                "target_date": "الربع الأول ٢٠٢٥"
            }
        ],
        "positive_observations_en": [
            "Strong executive sponsorship for security initiatives",
            "Well-documented information security policy framework",
            "Active security awareness training program (78% completion)",
            "Established vulnerability management process",
            "24/7 SOC operational capability"
        ],
        "positive_observations_ar": [
            "دعم تنفيذي قوي لمبادرات الأمن",
            "إطار سياسات أمن المعلومات موثق جيداً",
            "برنامج توعية أمنية نشط (٧٨٪ إتمام)",
            "عملية إدارة ثغرات مؤسسة",
            "قدرة مركز العمليات الأمنية تعمل على مدار الساعة"
        ]
    },
    
    "Artificial Intelligence": {
        "findings_en": [
            {
                "id": "AI-F01",
                "title": "AI Model Inventory Incomplete",
                "control_ref": "SDAIA AI Ethics Principle 3, NIST AI RMF MAP",
                "priority": "HIGH",
                "observation": "No centralized AI model registry exists. Organization identified 12 production ML models but cannot provide complete inventory. Model documentation is inconsistent.",
                "evidence": ["Stakeholder interviews", "Discovered model list", "Sample model documentation"],
                "root_cause": "Governance: No AI governance policy; Process: No model registration requirement",
                "risk_impact": "Unknown AI risk exposure, inability to demonstrate SDAIA compliance",
                "recommendation": "Establish AI model registry; Conduct organization-wide model discovery",
                "target_date": "Q1 2025"
            },
            {
                "id": "AI-F02",
                "title": "Bias Testing Not Performed",
                "control_ref": "SDAIA AI Ethics Principle 2 (Fairness), NIST AI RMF MEASURE",
                "priority": "HIGH",
                "observation": "None of the 3 customer-facing AI models sampled have documented bias testing. Credit scoring model shows potential demographic disparities.",
                "evidence": ["Model documentation review", "Bias testing records (none)", "Model output analysis"],
                "root_cause": "People: Lack of bias testing expertise; Governance: No fairness requirements",
                "risk_impact": "Discriminatory outcomes, regulatory violations, reputational damage",
                "recommendation": "Assess credit scoring model for bias; Implement bias testing tools",
                "target_date": "Immediate / Q1 2025"
            },
            {
                "id": "AI-F03",
                "title": "Model Explainability Gaps",
                "control_ref": "SDAIA AI Ethics Principle 4 (Transparency)",
                "priority": "MEDIUM",
                "observation": "Customer-facing AI decisions lack explainability. No documentation on how model decisions are made or communicated to affected individuals.",
                "evidence": ["Model documentation", "Customer communication samples", "Explainability reports (none)"],
                "root_cause": "Technology: No XAI tools deployed; Process: No explainability requirements",
                "risk_impact": "Non-compliance with transparency requirements, customer complaints",
                "recommendation": "Implement SHAP/LIME for model explanations; Document decision logic",
                "target_date": "Q2 2025"
            },
            {
                "id": "AI-F04",
                "title": "AI Ethics Committee Not Established",
                "control_ref": "SDAIA AI Ethics Principles, ISO 42001",
                "priority": "MEDIUM",
                "observation": "No AI Ethics Committee or review process for high-risk AI applications. AI deployment decisions made without ethical review.",
                "evidence": ["Governance documentation", "AI project approvals", "Stakeholder interviews"],
                "root_cause": "Governance: AI governance framework not developed",
                "risk_impact": "Ethical issues undetected, SDAIA non-compliance",
                "recommendation": "Establish AI Ethics Committee with cross-functional membership",
                "target_date": "Q1 2025"
            }
        ],
        "findings_ar": [
            {
                "id": "AI-F01",
                "title": "جرد نماذج الذكاء الاصطناعي غير مكتمل",
                "control_ref": "مبدأ أخلاقيات سدايا ٣، NIST AI RMF MAP",
                "priority": "عالي",
                "observation": "لا يوجد سجل مركزي لنماذج الذكاء الاصطناعي. تم تحديد ١٢ نموذج ML في الإنتاج لكن لا يمكن توفير جرد كامل",
                "evidence": ["مقابلات أصحاب المصلحة", "قائمة النماذج المكتشفة", "عينات توثيق النماذج"],
                "root_cause": "الحوكمة: عدم وجود سياسة حوكمة AI؛ العملية: عدم وجود متطلب تسجيل النماذج",
                "risk_impact": "تعرض غير معروف لمخاطر AI، عدم القدرة على إثبات الامتثال لسدايا",
                "recommendation": "إنشاء سجل نماذج AI؛ إجراء اكتشاف شامل للنماذج",
                "target_date": "الربع الأول ٢٠٢٥"
            },
            {
                "id": "AI-F02",
                "title": "عدم إجراء اختبار التحيز",
                "control_ref": "مبدأ أخلاقيات سدايا ٢ (العدالة)، NIST AI RMF MEASURE",
                "priority": "عالي",
                "observation": "لا توجد اختبارات تحيز موثقة لأي من نماذج AI الثلاثة التي تواجه العملاء. نموذج تسجيل الائتمان يظهر تفاوتات ديموغرافية محتملة",
                "evidence": ["مراجعة توثيق النماذج", "سجلات اختبار التحيز (لا يوجد)", "تحليل مخرجات النموذج"],
                "root_cause": "الأفراد: نقص خبرة اختبار التحيز؛ الحوكمة: عدم وجود متطلبات عدالة",
                "risk_impact": "نتائج تمييزية، انتهاكات تنظيمية، ضرر بالسمعة",
                "recommendation": "تقييم نموذج تسجيل الائتمان للتحيز؛ تطبيق أدوات اختبار التحيز",
                "target_date": "فوري / الربع الأول ٢٠٢٥"
            },
            {
                "id": "AI-F03",
                "title": "فجوات قابلية تفسير النماذج",
                "control_ref": "مبدأ أخلاقيات سدايا ٤ (الشفافية)",
                "priority": "متوسط",
                "observation": "قرارات AI التي تواجه العملاء تفتقر إلى قابلية التفسير. لا توجد وثائق حول كيفية اتخاذ قرارات النموذج",
                "evidence": ["توثيق النموذج", "عينات تواصل العملاء", "تقارير قابلية التفسير (لا يوجد)"],
                "root_cause": "التقنية: عدم نشر أدوات XAI؛ العملية: عدم وجود متطلبات التفسير",
                "risk_impact": "عدم الامتثال لمتطلبات الشفافية، شكاوى العملاء",
                "recommendation": "تطبيق SHAP/LIME لتفسيرات النموذج؛ توثيق منطق القرار",
                "target_date": "الربع الثاني ٢٠٢٥"
            }
        ],
        "positive_observations_en": [
            "Strong data science team with ML expertise",
            "Active use of version control for model code",
            "Regular model performance monitoring in place",
            "Executive interest in responsible AI adoption"
        ],
        "positive_observations_ar": [
            "فريق علوم بيانات قوي مع خبرة في التعلم الآلي",
            "استخدام نشط للتحكم في الإصدارات لكود النماذج",
            "مراقبة أداء النماذج بشكل منتظم",
            "اهتمام تنفيذي بتبني الذكاء الاصطناعي المسؤول"
        ]
    },
    
    "Data Management": {
        "findings_en": [
            {
                "id": "DM-F01",
                "title": "PDPL Consent Management Gaps",
                "control_ref": "PDPL Article 6, 10",
                "priority": "HIGH",
                "observation": "Consent collection mechanisms do not meet PDPL requirements. 40% of sampled consent forms lack required disclosures. Consent withdrawal takes 15+ days.",
                "evidence": ["Consent form samples", "Consent database records", "Withdrawal request log"],
                "root_cause": "Process: Legacy consent forms not updated; Technology: Manual withdrawal process",
                "risk_impact": "PDPL non-compliance, regulatory fines up to SAR 5M",
                "recommendation": "Update consent forms; Implement consent management platform",
                "target_date": "Q1 2025"
            },
            {
                "id": "DM-F02",
                "title": "Data Classification Not Implemented",
                "control_ref": "PDPL Article 4, NDMO Guidelines",
                "priority": "HIGH",
                "observation": "No enterprise data classification scheme applied. Personal data mixed with non-sensitive data without proper labeling or protection.",
                "evidence": ["Data classification policy (draft)", "Sample data repositories", "Access control configs"],
                "root_cause": "Governance: Classification scheme not approved; Technology: No DLP tools",
                "risk_impact": "Unauthorized access to personal data, compliance violations",
                "recommendation": "Finalize and implement data classification; Deploy DLP solution",
                "target_date": "Q1-Q2 2025"
            },
            {
                "id": "DM-F03",
                "title": "Data Retention Violations",
                "control_ref": "PDPL Article 18, Records Management",
                "priority": "MEDIUM",
                "observation": "Data retained beyond legal requirements. 35% of sampled personal data exceeded retention periods with no documented justification.",
                "evidence": ["Data inventory", "Retention schedule", "Sample data age analysis"],
                "root_cause": "Process: No automated retention enforcement; Technology: Manual deletion",
                "risk_impact": "PDPL violation, increased breach exposure",
                "recommendation": "Implement automated data lifecycle management",
                "target_date": "Q2 2025"
            },
            {
                "id": "DM-F04",
                "title": "Data Quality Issues",
                "control_ref": "NDMO Data Quality Framework",
                "priority": "MEDIUM",
                "observation": "Critical data domains show quality issues. Customer master data has 12% duplicate rate, 8% incomplete records.",
                "evidence": ["Data quality reports", "Profiling results", "Business impact analysis"],
                "root_cause": "Process: No data stewardship program; Technology: No DQ monitoring",
                "risk_impact": "Incorrect business decisions, regulatory reporting issues",
                "recommendation": "Implement data stewardship; Deploy DQ monitoring tools",
                "target_date": "Q2 2025"
            }
        ],
        "findings_ar": [
            {
                "id": "DM-F01",
                "title": "فجوات إدارة الموافقات وفق PDPL",
                "control_ref": "نظام حماية البيانات الشخصية المادة ٦، ١٠",
                "priority": "عالي",
                "observation": "آليات جمع الموافقات لا تلبي متطلبات PDPL. ٤٠٪ من نماذج الموافقات تفتقر إلى الإفصاحات المطلوبة. سحب الموافقة يستغرق ١٥+ يوم",
                "evidence": ["عينات نماذج الموافقة", "سجلات قاعدة بيانات الموافقات", "سجل طلبات السحب"],
                "root_cause": "العملية: نماذج الموافقة القديمة لم تُحدّث؛ التقنية: عملية سحب يدوية",
                "risk_impact": "عدم الامتثال لـ PDPL، غرامات تصل إلى ٥ مليون ريال",
                "recommendation": "تحديث نماذج الموافقة؛ تطبيق منصة إدارة الموافقات",
                "target_date": "الربع الأول ٢٠٢٥"
            },
            {
                "id": "DM-F02",
                "title": "تصنيف البيانات غير مطبق",
                "control_ref": "نظام حماية البيانات الشخصية المادة ٤، إرشادات NDMO",
                "priority": "عالي",
                "observation": "لا يوجد مخطط تصنيف بيانات مؤسسي مطبق. البيانات الشخصية مختلطة مع بيانات غير حساسة بدون تصنيف أو حماية مناسبة",
                "evidence": ["سياسة تصنيف البيانات (مسودة)", "عينات مستودعات البيانات", "تكوينات التحكم في الوصول"],
                "root_cause": "الحوكمة: مخطط التصنيف غير معتمد؛ التقنية: عدم وجود أدوات DLP",
                "risk_impact": "وصول غير مصرح به للبيانات الشخصية، انتهاكات الامتثال",
                "recommendation": "اعتماد وتطبيق تصنيف البيانات؛ نشر حل DLP",
                "target_date": "الربع الأول-الثاني ٢٠٢٥"
            },
            {
                "id": "DM-F03",
                "title": "انتهاكات الاحتفاظ بالبيانات",
                "control_ref": "نظام حماية البيانات الشخصية المادة ١٨",
                "priority": "متوسط",
                "observation": "البيانات محتفظ بها بعد المتطلبات القانونية. ٣٥٪ من البيانات الشخصية تجاوزت فترات الاحتفاظ بدون مبرر موثق",
                "evidence": ["جرد البيانات", "جدول الاحتفاظ", "تحليل عمر البيانات"],
                "root_cause": "العملية: عدم وجود إنفاذ احتفاظ آلي؛ التقنية: حذف يدوي",
                "risk_impact": "انتهاك PDPL، زيادة التعرض للاختراق",
                "recommendation": "تطبيق إدارة دورة حياة البيانات الآلية",
                "target_date": "الربع الثاني ٢٠٢٥"
            }
        ],
        "positive_observations_en": [
            "Data Protection Officer appointed",
            "PDPL awareness program initiated",
            "Data catalog project underway",
            "Strong management commitment to compliance"
        ],
        "positive_observations_ar": [
            "تعيين مسؤول حماية البيانات",
            "إطلاق برنامج توعية PDPL",
            "مشروع كتالوج البيانات قيد التنفيذ",
            "التزام إداري قوي بالامتثال"
        ]
    },
    
    "Digital Transformation": {
        "findings_en": [
            {
                "id": "DT-F01",
                "title": "Change Management Process Gaps",
                "control_ref": "DGA Digital Standards, PROSCI Best Practices",
                "priority": "HIGH",
                "observation": "Digital transformation initiatives lack formal change management. User adoption rates for recent tools average 45% vs 80% target. No change impact assessment.",
                "evidence": ["Adoption metrics", "Change management documentation (none)", "User feedback surveys"],
                "root_cause": "Process: No change management framework; People: CM skills gap",
                "risk_impact": "Failed digital adoption reducing ROI, employee frustration",
                "recommendation": "Establish change management framework; Hire CM resources",
                "target_date": "Q1 2025"
            },
            {
                "id": "DT-F02",
                "title": "Legacy System Integration Failures",
                "control_ref": "Enterprise Architecture Standards",
                "priority": "HIGH",
                "observation": "45% of digital initiatives experienced integration delays. API strategy not defined. Point-to-point integrations creating technical debt.",
                "evidence": ["Project status reports", "Integration architecture", "Issue logs"],
                "root_cause": "Technology: No integration platform; Governance: No API standards",
                "risk_impact": "Project delays, increased costs, data inconsistencies",
                "recommendation": "Implement integration platform; Define API governance",
                "target_date": "Q2 2025"
            },
            {
                "id": "DT-F03",
                "title": "Digital Project Governance Weak",
                "control_ref": "DGA Project Governance, PMBOK",
                "priority": "MEDIUM",
                "observation": "No consistent project governance for digital initiatives. 30% of projects lack clear success metrics. Benefits tracking not performed.",
                "evidence": ["Project charters", "Governance meeting minutes", "Benefits realization reports (none)"],
                "root_cause": "Governance: No digital PMO; Process: No standard methodology",
                "risk_impact": "Scope creep, budget overruns, benefits not realized",
                "recommendation": "Establish Digital PMO; Define project governance standards",
                "target_date": "Q1 2025"
            },
            {
                "id": "DT-F04",
                "title": "Cloud Security Gaps",
                "control_ref": "NCA Cloud Computing Controls, CSA CCM",
                "priority": "MEDIUM",
                "observation": "Cloud security posture inconsistent. 25% of cloud resources not compliant with security baseline. No CSPM solution deployed.",
                "evidence": ["Cloud configuration review", "Security baseline", "Compliance reports"],
                "root_cause": "Technology: No CSPM; Process: No cloud security reviews",
                "risk_impact": "Data exposure, compliance violations",
                "recommendation": "Deploy CSPM solution; Enforce security baseline",
                "target_date": "Q2 2025"
            }
        ],
        "findings_ar": [
            {
                "id": "DT-F01",
                "title": "فجوات عملية إدارة التغيير",
                "control_ref": "معايير هيئة الحكومة الرقمية، أفضل ممارسات PROSCI",
                "priority": "عالي",
                "observation": "مبادرات التحول الرقمي تفتقر إلى إدارة تغيير رسمية. معدلات تبني المستخدمين ٤٥٪ مقابل ٨٠٪ كهدف. لا يوجد تقييم أثر التغيير",
                "evidence": ["مقاييس التبني", "وثائق إدارة التغيير (لا يوجد)", "استطلاعات ملاحظات المستخدمين"],
                "root_cause": "العملية: عدم وجود إطار إدارة التغيير؛ الأفراد: فجوة مهارات إدارة التغيير",
                "risk_impact": "فشل التبني الرقمي مما يقلل العائد على الاستثمار، إحباط الموظفين",
                "recommendation": "تأسيس إطار إدارة التغيير؛ توظيف موارد إدارة التغيير",
                "target_date": "الربع الأول ٢٠٢٥"
            },
            {
                "id": "DT-F02",
                "title": "فشل تكامل الأنظمة القديمة",
                "control_ref": "معايير البنية المؤسسية",
                "priority": "عالي",
                "observation": "٤٥٪ من المبادرات الرقمية واجهت تأخيرات تكامل. استراتيجية API غير محددة. التكاملات نقطة لنقطة تخلق ديوناً تقنية",
                "evidence": ["تقارير حالة المشاريع", "بنية التكامل", "سجلات المشاكل"],
                "root_cause": "التقنية: عدم وجود منصة تكامل؛ الحوكمة: عدم وجود معايير API",
                "risk_impact": "تأخيرات المشاريع، زيادة التكاليف، عدم اتساق البيانات",
                "recommendation": "تطبيق منصة تكامل؛ تحديد حوكمة API",
                "target_date": "الربع الثاني ٢٠٢٥"
            },
            {
                "id": "DT-F03",
                "title": "ضعف حوكمة المشاريع الرقمية",
                "control_ref": "حوكمة مشاريع هيئة الحكومة الرقمية، PMBOK",
                "priority": "متوسط",
                "observation": "لا توجد حوكمة مشاريع متسقة للمبادرات الرقمية. ٣٠٪ من المشاريع تفتقر إلى مقاييس نجاح واضحة. لا يتم تتبع الفوائد",
                "evidence": ["ميثاق المشاريع", "محاضر اجتماعات الحوكمة", "تقارير تحقيق الفوائد (لا يوجد)"],
                "root_cause": "الحوكمة: عدم وجود مكتب إدارة مشاريع رقمي؛ العملية: عدم وجود منهجية قياسية",
                "risk_impact": "زحف النطاق، تجاوز الميزانية، عدم تحقيق الفوائد",
                "recommendation": "تأسيس مكتب إدارة المشاريع الرقمي؛ تحديد معايير حوكمة المشاريع",
                "target_date": "الربع الأول ٢٠٢٥"
            }
        ],
        "positive_observations_en": [
            "Strong executive commitment to digital transformation",
            "Digital strategy aligned with Vision 2030",
            "Agile practices adopted by some teams",
            "Cloud-first policy established"
        ],
        "positive_observations_ar": [
            "التزام تنفيذي قوي بالتحول الرقمي",
            "استراتيجية رقمية متوافقة مع رؤية ٢٠٣٠",
            "ممارسات أجايل مُتبناة من بعض الفرق",
            "سياسة السحابة أولاً مؤسسة"
        ]
    },
    
    "Global Standards": {
        "findings_en": [
            {
                "id": "GS-F01",
                "title": "Internal Audit Program Deficiencies",
                "control_ref": "ISO 19011, ISO 27001 9.2, ISO 22301 9.2",
                "priority": "HIGH",
                "observation": "Internal audit program covers only 60% of ISO requirements. Auditor competency records incomplete. Audit evidence not consistently retained.",
                "evidence": ["Audit plan and status", "Auditor training records", "Sample audit reports"],
                "root_cause": "People: Insufficient auditor capacity; Process: No audit management tool",
                "risk_impact": "Certification risk, missed improvement opportunities",
                "recommendation": "Complete audit coverage; Establish auditor competency matrix",
                "target_date": "Q1 2025"
            },
            {
                "id": "GS-F02",
                "title": "Management Review Not Effective",
                "control_ref": "ISO 27001 9.3, ISO 22301 9.3, ISO 9001 9.3",
                "priority": "HIGH",
                "observation": "Management reviews lack required inputs. No trend analysis of KPIs. Action items not tracked to completion.",
                "evidence": ["Management review minutes", "KPI dashboards", "Action tracking records"],
                "root_cause": "Process: No standard agenda; Governance: Unclear accountability",
                "risk_impact": "Certification major NC, ineffective continual improvement",
                "recommendation": "Standardize management review process; Implement action tracking",
                "target_date": "Q1 2025"
            },
            {
                "id": "GS-F03",
                "title": "Document Control Gaps",
                "control_ref": "ISO 27001 7.5, ISO 22301 7.5",
                "priority": "MEDIUM",
                "observation": "Documented information not consistently controlled. 20% of sampled documents are outdated versions. No master document register.",
                "evidence": ["Document samples", "Version history", "Distribution records"],
                "root_cause": "Technology: No document management system; Process: Manual control",
                "risk_impact": "Staff using outdated procedures, compliance gaps",
                "recommendation": "Implement document management system; Establish master register",
                "target_date": "Q2 2025"
            },
            {
                "id": "GS-F04",
                "title": "BCM Testing Insufficient",
                "control_ref": "ISO 22301 8.5, 8.6",
                "priority": "MEDIUM",
                "observation": "Business continuity plans not fully tested. Only 2 of 8 critical processes tested in past 12 months. No lessons learned documented.",
                "evidence": ["BC test schedule", "Test reports", "Lessons learned log (empty)"],
                "root_cause": "Process: No testing schedule; People: Resource constraints",
                "risk_impact": "BCPs may not work in actual incident, certification NC",
                "recommendation": "Establish annual testing schedule; Document lessons learned",
                "target_date": "Q1 2025"
            }
        ],
        "findings_ar": [
            {
                "id": "GS-F01",
                "title": "قصور برنامج التدقيق الداخلي",
                "control_ref": "ISO 19011، ISO 27001 9.2، ISO 22301 9.2",
                "priority": "عالي",
                "observation": "برنامج التدقيق الداخلي يغطي ٦٠٪ فقط من متطلبات ISO. سجلات كفاءة المدققين غير مكتملة. أدلة التدقيق غير محتفظ بها باستمرار",
                "evidence": ["خطة التدقيق وحالتها", "سجلات تدريب المدققين", "عينات تقارير التدقيق"],
                "root_cause": "الأفراد: قدرة المدققين غير كافية؛ العملية: عدم وجود أداة إدارة التدقيق",
                "risk_impact": "خطر الشهادة، فرص تحسين مفقودة",
                "recommendation": "استكمال تغطية التدقيق؛ إنشاء مصفوفة كفاءة المدققين",
                "target_date": "الربع الأول ٢٠٢٥"
            },
            {
                "id": "GS-F02",
                "title": "مراجعة الإدارة غير فعالة",
                "control_ref": "ISO 27001 9.3، ISO 22301 9.3، ISO 9001 9.3",
                "priority": "عالي",
                "observation": "مراجعات الإدارة تفتقر إلى المدخلات المطلوبة. لا يوجد تحليل اتجاهات للـ KPIs. بنود العمل لا تُتبع حتى الاكتمال",
                "evidence": ["محاضر مراجعة الإدارة", "لوحات KPI", "سجلات تتبع الإجراءات"],
                "root_cause": "العملية: عدم وجود جدول أعمال قياسي؛ الحوكمة: المساءلة غير واضحة",
                "risk_impact": "عدم مطابقة جوهرية للشهادة، تحسين مستمر غير فعال",
                "recommendation": "توحيد عملية مراجعة الإدارة؛ تطبيق تتبع الإجراءات",
                "target_date": "الربع الأول ٢٠٢٥"
            },
            {
                "id": "GS-F03",
                "title": "فجوات ضبط الوثائق",
                "control_ref": "ISO 27001 7.5، ISO 22301 7.5",
                "priority": "متوسط",
                "observation": "المعلومات الموثقة لا تُضبط باستمرار. ٢٠٪ من الوثائق المعاينة إصدارات قديمة. لا يوجد سجل رئيسي للوثائق",
                "evidence": ["عينات الوثائق", "سجل الإصدارات", "سجلات التوزيع"],
                "root_cause": "التقنية: عدم وجود نظام إدارة وثائق؛ العملية: ضبط يدوي",
                "risk_impact": "الموظفون يستخدمون إجراءات قديمة، فجوات امتثال",
                "recommendation": "تطبيق نظام إدارة الوثائق؛ إنشاء سجل رئيسي",
                "target_date": "الربع الثاني ٢٠٢٥"
            }
        ],
        "positive_observations_en": [
            "ISO 27001 certification maintained",
            "Management commitment to integrated management system",
            "Corrective action process established",
            "Regular external audits conducted"
        ],
        "positive_observations_ar": [
            "شهادة ISO 27001 محافظ عليها",
            "التزام الإدارة بنظام الإدارة المتكامل",
            "عملية الإجراءات التصحيحية مؤسسة",
            "تدقيقات خارجية منتظمة"
        ]
    }
}

# =============================================================================
# DOMAIN-SPECIFIC RISK SCENARIOS
# =============================================================================

DOMAIN_RISK_SCENARIOS = {
    "Cyber Security": {
        "risks_en": [
            {"id": "CS-R01", "name": "Ransomware Attack", "description": "Ransomware encrypting critical systems and demanding payment", "likelihood": 4, "impact": 5, "category": "Malware"},
            {"id": "CS-R02", "name": "Data Breach", "description": "Unauthorized access exposing sensitive customer data", "likelihood": 3, "impact": 5, "category": "Data Security"},
            {"id": "CS-R03", "name": "Insider Threat", "description": "Malicious or negligent insider causing data loss", "likelihood": 3, "impact": 4, "category": "People"},
            {"id": "CS-R04", "name": "Phishing Attack", "description": "Social engineering attack compromising credentials", "likelihood": 5, "impact": 3, "category": "Social Engineering"},
            {"id": "CS-R05", "name": "Third-Party Breach", "description": "Vendor compromise affecting organization", "likelihood": 3, "impact": 4, "category": "Supply Chain"}
        ],
        "controls_en": ["Endpoint Detection & Response (EDR)", "Security Information & Event Management (SIEM)", "Multi-Factor Authentication (MFA)", "Security Operations Center (SOC)", "Vulnerability Management", "Security Awareness Training"],
        "kris_en": [
            {"name": "Security Incidents (Critical)", "threshold": "< 2/quarter", "red": "> 5"},
            {"name": "Mean Time to Detect (MTTD)", "threshold": "< 4 hours", "red": "> 24 hours"},
            {"name": "Phishing Click Rate", "threshold": "< 5%", "red": "> 15%"},
            {"name": "Critical Vulnerabilities Unpatched > 30 days", "threshold": "< 5", "red": "> 20"}
        ]
    },
    "Artificial Intelligence": {
        "risks_en": [
            {"id": "AI-R01", "name": "Biased Model Decisions", "description": "AI model producing unfair or discriminatory outcomes", "likelihood": 4, "impact": 5, "category": "Fairness"},
            {"id": "AI-R02", "name": "Model Drift", "description": "Model performance degrading over time without detection", "likelihood": 4, "impact": 3, "category": "Performance"},
            {"id": "AI-R03", "name": "Adversarial Attack", "description": "Malicious inputs causing model misclassification", "likelihood": 3, "impact": 4, "category": "Security"},
            {"id": "AI-R04", "name": "Training Data Poisoning", "description": "Compromised training data affecting model behavior", "likelihood": 2, "impact": 5, "category": "Data"},
            {"id": "AI-R05", "name": "Unexplainable Decisions", "description": "Inability to explain AI decisions to regulators/customers", "likelihood": 4, "impact": 4, "category": "Transparency"}
        ],
        "controls_en": ["Bias Testing Framework", "Model Monitoring Platform", "Explainability Tools (SHAP/LIME)", "AI Ethics Committee", "Model Registry", "Adversarial Robustness Testing"],
        "kris_en": [
            {"name": "Models with Detected Bias", "threshold": "0 unresolved", "red": "> 2"},
            {"name": "Model Drift Incidents", "threshold": "< 3/quarter", "red": "> 10"},
            {"name": "Unregistered Production Models", "threshold": "0", "red": "> 5"},
            {"name": "AI Ethics Violations", "threshold": "0", "red": "> 1"}
        ]
    },
    "Data Management": {
        "risks_en": [
            {"id": "DM-R01", "name": "PDPL Non-Compliance", "description": "Failure to meet Personal Data Protection Law requirements", "likelihood": 4, "impact": 5, "category": "Regulatory"},
            {"id": "DM-R02", "name": "Data Quality Issues", "description": "Inaccurate or incomplete data affecting decisions", "likelihood": 5, "impact": 3, "category": "Quality"},
            {"id": "DM-R03", "name": "Unauthorized Data Access", "description": "Access to personal data without proper authorization", "likelihood": 3, "impact": 4, "category": "Access"},
            {"id": "DM-R04", "name": "Data Retention Violation", "description": "Keeping data beyond legal retention periods", "likelihood": 4, "impact": 4, "category": "Lifecycle"},
            {"id": "DM-R05", "name": "Cross-Border Transfer Violation", "description": "Illegal transfer of personal data outside Saudi Arabia", "likelihood": 3, "impact": 5, "category": "Transfer"}
        ],
        "controls_en": ["Data Classification Scheme", "Consent Management Platform", "Data Quality Monitoring", "Data Loss Prevention (DLP)", "Privacy Impact Assessments", "Data Retention Automation"],
        "kris_en": [
            {"name": "PDPL Compliance Score", "threshold": "> 95%", "red": "< 80%"},
            {"name": "Data Quality Score (Critical Domains)", "threshold": "> 95%", "red": "< 85%"},
            {"name": "DSAR Response Time", "threshold": "< 30 days", "red": "> 45 days"},
            {"name": "Data Retention Violations", "threshold": "0", "red": "> 5"}
        ]
    },
    "Digital Transformation": {
        "risks_en": [
            {"id": "DT-R01", "name": "Project Failure", "description": "Digital initiative failing to deliver expected outcomes", "likelihood": 4, "impact": 4, "category": "Delivery"},
            {"id": "DT-R02", "name": "Change Resistance", "description": "Employees resisting adoption of digital tools", "likelihood": 5, "impact": 3, "category": "People"},
            {"id": "DT-R03", "name": "Integration Failure", "description": "Systems failing to integrate properly", "likelihood": 4, "impact": 4, "category": "Technology"},
            {"id": "DT-R04", "name": "Vendor Lock-in", "description": "Over-dependence on single technology vendor", "likelihood": 3, "impact": 3, "category": "Strategy"},
            {"id": "DT-R05", "name": "Budget Overrun", "description": "Digital projects exceeding allocated budget", "likelihood": 4, "impact": 3, "category": "Financial"}
        ],
        "controls_en": ["Change Management Framework", "Digital PMO", "Integration Platform", "Multi-Cloud Strategy", "Benefits Tracking", "Agile Project Methodology"],
        "kris_en": [
            {"name": "Digital Adoption Rate", "threshold": "> 80%", "red": "< 50%"},
            {"name": "Project On-Time Delivery", "threshold": "> 85%", "red": "< 60%"},
            {"name": "Budget Variance", "threshold": "< 10%", "red": "> 25%"},
            {"name": "Integration Success Rate", "threshold": "> 90%", "red": "< 70%"}
        ]
    },
    "Global Standards": {
        "risks_en": [
            {"id": "GS-R01", "name": "Certification Failure", "description": "Failing ISO certification or surveillance audit", "likelihood": 2, "impact": 5, "category": "Compliance"},
            {"id": "GS-R02", "name": "Major Non-Conformity", "description": "Critical audit finding threatening certification", "likelihood": 3, "impact": 4, "category": "Audit"},
            {"id": "GS-R03", "name": "Documentation Gaps", "description": "Policies and procedures not properly documented", "likelihood": 4, "impact": 3, "category": "Documentation"},
            {"id": "GS-R04", "name": "BCP Test Failure", "description": "Business continuity plans failing during test", "likelihood": 3, "impact": 4, "category": "BCM"},
            {"id": "GS-R05", "name": "Management System Fatigue", "description": "Staff disengaged from management system requirements", "likelihood": 4, "impact": 3, "category": "Culture"}
        ],
        "controls_en": ["Internal Audit Program", "Management Review Process", "Document Control System", "CAPA Process", "BCM Testing Schedule", "Continual Improvement Program"],
        "kris_en": [
            {"name": "Internal Audit Completion", "threshold": "100%", "red": "< 80%"},
            {"name": "Open Non-Conformities", "threshold": "< 5", "red": "> 15"},
            {"name": "Management Review Actions Overdue", "threshold": "0", "red": "> 5"},
            {"name": "BCM Test Coverage", "threshold": "100%", "red": "< 50%"}
        ]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_domain_audit_findings(domain: str, language: str = "English") -> Dict:
    """Get domain-specific audit findings."""
    findings = DOMAIN_AUDIT_FINDINGS.get(domain, DOMAIN_AUDIT_FINDINGS["Cyber Security"])
    
    if language in ["Arabic", "العربية"]:
        return {
            "findings": findings.get("findings_ar", findings["findings_en"]),
            "positive_observations": findings.get("positive_observations_ar", findings["positive_observations_en"])
        }
    return {
        "findings": findings["findings_en"],
        "positive_observations": findings["positive_observations_en"]
    }


def get_domain_risk_scenarios(domain: str, language: str = "English") -> Dict:
    """Get domain-specific risk scenarios."""
    scenarios = DOMAIN_RISK_SCENARIOS.get(domain, DOMAIN_RISK_SCENARIOS["Cyber Security"])
    return scenarios


def format_audit_findings(domain: str, language: str = "English") -> str:
    """Format audit findings as text."""
    data = get_domain_audit_findings(domain, language)
    findings = data["findings"]
    positive = data["positive_observations"]
    
    if language in ["Arabic", "العربية"]:
        output = "**النتائج الرئيسية:**\n\n"
        for f in findings:
            output += f"**النتيجة: {f['title']} ({f['priority']})**\n"
            output += f"- **المرجع:** {f['control_ref']}\n"
            output += f"- **الملاحظة:** {f['observation']}\n"
            output += f"- **السبب الجذري:** {f['root_cause']}\n"
            output += f"- **الأثر:** {f['risk_impact']}\n"
            output += f"- **التوصية:** {f['recommendation']}\n"
            output += f"- **الموعد المستهدف:** {f['target_date']}\n\n"
        
        output += "\n**الملاحظات الإيجابية:**\n"
        for p in positive:
            output += f"✓ {p}\n"
    else:
        output = "**Key Findings:**\n\n"
        for f in findings:
            output += f"**Finding: {f['title']} ({f['priority']})**\n"
            output += f"- **Control Reference:** {f['control_ref']}\n"
            output += f"- **Observation:** {f['observation']}\n"
            output += f"- **Root Cause:** {f['root_cause']}\n"
            output += f"- **Risk Impact:** {f['risk_impact']}\n"
            output += f"- **Recommendation:** {f['recommendation']}\n"
            output += f"- **Target Date:** {f['target_date']}\n\n"
        
        output += "\n**Positive Observations:**\n"
        for p in positive:
            output += f"✓ {p}\n"
    
    return output


def format_risk_analysis(domain: str, language: str = "English") -> str:
    """Format risk analysis as text."""
    data = get_domain_risk_scenarios(domain, language)
    risks = data["risks_en"]
    controls = data["controls_en"]
    kris = data["kris_en"]
    
    output = "**Risk Register:**\n\n"
    output += "| ID | Risk | Likelihood | Impact | Score | Category |\n"
    output += "|----|------|------------|--------|-------|----------|\n"
    for r in risks:
        score = r["likelihood"] * r["impact"]
        output += f"| {r['id']} | {r['name']} | {r['likelihood']} | {r['impact']} | {score} | {r['category']} |\n"
    
    output += "\n**Recommended Controls:**\n"
    for c in controls:
        output += f"- {c}\n"
    
    output += "\n**Key Risk Indicators (KRIs):**\n"
    output += "| KRI | Threshold | Red Flag |\n"
    output += "|-----|-----------|----------|\n"
    for k in kris:
        output += f"| {k['name']} | {k['threshold']} | {k['red']} |\n"
    
    return output
