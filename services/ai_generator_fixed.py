"""
Mizan GRC - Fixed AI Document Generator
Properly generates domain-specific content for all GRC documents.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class DocumentType(Enum):
    STRATEGY = "strategy"
    POLICY = "policy"
    AUDIT = "audit"
    RISK = "risk"

@dataclass
class AIResponse:
    content: str
    success: bool
    source: str = "ai"
    model: str = "simulation"


# Complete domain-specific content
DOMAIN_CONTENT = {
    "Cyber Security": {
        "ar_name": "الأمن السيبراني",
        "vision_ar": "تأسيس منظومة أمن سيبراني متكاملة ومرنة تحمي الأصول الحيوية وتضمن الامتثال للهيئة الوطنية للأمن السيبراني وتمكّن الابتكار الرقمي الآمن.",
        "vision_en": "Establish a comprehensive and resilient cybersecurity posture that protects critical assets, ensures NCA compliance, and enables secure digital innovation.",
        "objectives_ar": ["تحقيق امتثال ٩٥٪+ لضوابط NCA", "تقليل وقت اكتشاف التهديدات إلى أقل من ٤ ساعات", "تطبيق بنية انعدام الثقة", "بناء مركز عمليات أمنية ٢٤/٧", "تحقيق جاهزية التأمين السيبراني"],
        "objectives_en": ["Achieve 95%+ NCA compliance", "Reduce MTTD to < 4 hours", "Implement Zero Trust architecture", "Build 24/7 SOC capability", "Achieve cyber insurance readiness"],
        "pillars_ar": [
            ("حوكمة الأمن السيبراني", ["تأسيس لجنة الأمن السيبراني", "تطبيق إطار السياسات الأمنية", "نشر منصة GRC"]),
            ("كشف التهديدات والاستجابة", ["نشر نظام SIEM/SOAR", "تطبيق EDR/XDR", "تأسيس فريق الاستجابة للحوادث"]),
            ("أمن الهوية والوصول", ["تطبيق المصادقة متعددة العوامل MFA", "نشر إدارة الوصول المتميز PAM", "أتمتة مراجعات الصلاحيات"]),
            ("أمن البنية التحتية", ["تطبيق تجزئة الشبكة", "نشر جدار حماية الجيل التالي NGFW", "تأسيس الوصول الآمن عن بعد"])
        ],
        "pillars_en": [
            ("Cybersecurity Governance", ["Establish Cybersecurity Committee", "Implement Security Policy Framework", "Deploy GRC Platform"]),
            ("Threat Detection & Response", ["Deploy SIEM/SOAR", "Implement EDR/XDR", "Establish Incident Response Team"]),
            ("Identity & Access Management", ["Implement Multi-Factor Authentication", "Deploy Privileged Access Management", "Automate Access Reviews"]),
            ("Infrastructure Security", ["Implement Network Segmentation", "Deploy Next-Gen Firewall", "Establish Secure Remote Access"])
        ],
        "roadmap_ar": [
            ("التأسيس", "إطار حوكمة الأمن السيبراني", "٣", "٣٥٠,٠٠٠", "CISO", "اعتماد السياسات"),
            ("التأسيس", "تقييم المخاطر والفجوات", "٢", "٢٠٠,٠٠٠", "فريق الأمن", "تقرير الفجوات"),
            ("البناء", "نشر SIEM ومركز العمليات", "٦", "١,٨٠٠,٠٠٠", "SOC Manager", "تشغيل SOC ٢٤/٧"),
            ("البناء", "تعزيز IAM وPAM", "٦", "١,٢٠٠,٠٠٠", "IAM Team", "تغطية PAM ١٠٠٪"),
            ("التحسين", "بنية انعدام الثقة", "٨", "٢,٠٠٠,٠٠٠", "Enterprise Arch", "تطبيق Zero Trust")
        ],
        "roadmap_en": [
            ("Foundation", "Cybersecurity Governance Framework", "3", "350,000", "CISO", "Policy approval"),
            ("Foundation", "Risk & Gap Assessment", "2", "200,000", "Security Team", "Gap report"),
            ("Build", "SIEM & SOC Deployment", "6", "1,800,000", "SOC Manager", "24/7 SOC operational"),
            ("Build", "IAM & PAM Enhancement", "6", "1,200,000", "IAM Team", "100% PAM coverage"),
            ("Optimize", "Zero Trust Architecture", "8", "2,000,000", "Enterprise Arch", "Zero Trust implemented")
        ],
        "total_ar": "٥,٥٥٠,٠٠٠",
        "total_en": "5,550,000",
        "gaps_ar": "حوكمة الأمن السيبراني، إدارة الهوية والوصول، مراقبة التهديدات",
        "gaps_en": "Cybersecurity governance, Identity and access management, Threat monitoring",
        "kpis_ar": ["امتثال NCA: ٩٥٪", "وقت الاكتشاف MTTD: < ٤ ساعات", "تغطية MFA: ١٠٠٪", "الثغرات الحرجة: < ٥"],
        "kpis_en": ["NCA Compliance: 95%", "MTTD: < 4 hours", "MFA Coverage: 100%", "Critical Vulns: < 5"],
        "risks_ar": ["برامج الفدية", "اختراق البيانات", "التهديد الداخلي", "التصيد الاحتيالي"],
        "risks_en": ["Ransomware attack", "Data breach", "Insider threat", "Phishing attack"],
        "frameworks": "NCA ECC, SAMA CSF, ISO 27001",
        "frameworks_ar": "ضوابط NCA، إطار ساما، ISO 27001"
    },
    "Artificial Intelligence": {
        "ar_name": "الذكاء الاصطناعي",
        "vision_ar": "تمكين المنظمة كرائد في تبني الذكاء الاصطناعي المسؤول، وضمان شفافية وعدالة وأمان جميع أنظمة AI مع الامتثال لمبادئ سدايا الأخلاقية.",
        "vision_en": "Enable the organization as a leader in responsible AI adoption, ensuring transparency, fairness, and security of all AI systems while complying with SDAIA ethical principles.",
        "objectives_ar": ["إنشاء لجنة أخلاقيات AI خلال ٦ أشهر", "تحقيق جرد كامل لنماذج AI", "تطبيق اختبار التحيز لجميع النماذج", "ضمان الامتثال لمبادئ سدايا", "تقليل حوادث AI بنسبة ٨٠٪"],
        "objectives_en": ["Establish AI Ethics Committee within 6 months", "Achieve complete AI model inventory", "Implement bias testing for all models", "Ensure SDAIA compliance", "Reduce AI incidents by 80%"],
        "pillars_ar": [
            ("إطار حوكمة الذكاء الاصطناعي", ["تأسيس لجنة أخلاقيات AI", "تطوير سياسات حوكمة AI", "تطبيق سجل النماذج المركزي"]),
            ("الذكاء الاصطناعي المسؤول", ["نشر أدوات كشف التحيز", "تطبيق أطر قابلية التفسير XAI", "تأسيس متطلبات الإشراف البشري"]),
            ("أمن وخصوصية AI", ["تطبيق اختبار المتانة", "نشر ضوابط خصوصية بيانات التدريب", "تأسيس أمن النماذج"]),
            ("دورة حياة النماذج", ["تطبيق MLOps", "مراقبة انحراف النماذج", "إدارة إصدارات النماذج"])
        ],
        "pillars_en": [
            ("AI Governance Framework", ["Establish AI Ethics Committee", "Develop AI governance policies", "Implement central model registry"]),
            ("Responsible AI", ["Deploy bias detection tools", "Implement XAI frameworks", "Establish human oversight requirements"]),
            ("AI Security & Privacy", ["Implement robustness testing", "Deploy training data privacy controls", "Establish model security"]),
            ("Model Lifecycle", ["Implement MLOps", "Monitor model drift", "Manage model versions"])
        ],
        "roadmap_ar": [
            ("التأسيس", "لجنة أخلاقيات AI وإطار الحوكمة", "٣", "٢٥٠,٠٠٠", "AI Lead", "تشكيل اللجنة"),
            ("التأسيس", "جرد نماذج AI وتصنيف المخاطر", "٣", "٣٠٠,٠٠٠", "Data Science", "جرد ١٠٠٪"),
            ("البناء", "أدوات اختبار التحيز والعدالة", "٤", "٨٠٠,٠٠٠", "ML Team", "اختبار كل النماذج"),
            ("البناء", "منصة قابلية التفسير XAI", "٦", "١,٢٠٠,٠٠٠", "AI Team", "تغطية XAI ١٠٠٪"),
            ("التحسين", "أتمتة حوكمة AI", "٦", "٨٠٠,٠٠٠", "AI Governance", "أتمتة كاملة")
        ],
        "roadmap_en": [
            ("Foundation", "AI Ethics Committee & Governance", "3", "250,000", "AI Lead", "Committee formed"),
            ("Foundation", "AI Model Inventory & Risk Classification", "3", "300,000", "Data Science", "100% inventory"),
            ("Build", "Bias Testing & Fairness Tools", "4", "800,000", "ML Team", "All models tested"),
            ("Build", "XAI Explainability Platform", "6", "1,200,000", "AI Team", "100% XAI coverage"),
            ("Optimize", "AI Governance Automation", "6", "800,000", "AI Governance", "Full automation")
        ],
        "total_ar": "٣,٣٥٠,٠٠٠",
        "total_en": "3,350,000",
        "gaps_ar": "حوكمة الذكاء الاصطناعي، اختبار التحيز والعدالة، قابلية تفسير النماذج",
        "gaps_en": "AI governance, Bias testing and fairness, Model explainability",
        "kpis_ar": ["تحيز النماذج: صفر", "انتهاكات أخلاقيات AI: صفر", "تغطية XAI: ١٠٠٪", "حوادث انحراف النماذج: < ٣"],
        "kpis_en": ["Model bias detected: 0", "AI ethics violations: 0", "XAI coverage: 100%", "Model drift incidents: < 3"],
        "risks_ar": ["قرارات نماذج متحيزة", "انحراف النماذج", "الهجمات العدائية", "نقص قابلية التفسير"],
        "risks_en": ["Biased model decisions", "Model drift", "Adversarial attacks", "Lack of explainability"],
        "frameworks": "SDAIA AI Ethics, NIST AI RMF, ISO 42001",
        "frameworks_ar": "مبادئ أخلاقيات سدايا، NIST AI RMF، ISO 42001"
    },
    "Data Management": {
        "ar_name": "إدارة البيانات",
        "vision_ar": "تحويل المنظمة إلى منظمة تعتمد على البيانات مع حوكمة بيانات مؤسسية شاملة، وضمان جودة البيانات والامتثال لنظام حماية البيانات الشخصية PDPL.",
        "vision_en": "Transform the organization into a data-driven enterprise with comprehensive data governance, ensuring data quality and PDPL compliance.",
        "objectives_ar": ["تحقيق الامتثال الكامل لـ PDPL", "تطبيق كتالوج بيانات بتغطية ١٠٠٪", "تحسين جودة البيانات إلى ٩٥٪+", "تمكين التحليلات الذاتية", "تقليل حوادث البيانات بنسبة ٧٠٪"],
        "objectives_en": ["Achieve full PDPL compliance", "Implement data catalog with 100% coverage", "Improve data quality to 95%+", "Enable self-service analytics", "Reduce data incidents by 70%"],
        "pillars_ar": [
            ("حوكمة البيانات والإشراف", ["تأسيس مجلس حوكمة البيانات", "تطبيق برنامج أمناء البيانات", "نشر كتالوج البيانات المؤسسي"]),
            ("إدارة جودة البيانات", ["تطبيق أدوات مراقبة الجودة", "تأسيس قواعد الجودة حسب المجال", "إنشاء لوحات جودة البيانات"]),
            ("الامتثال لنظام PDPL", ["إجراء تقييم فجوات PDPL", "تطبيق منصة إدارة الموافقات", "نشر أدوات إخفاء البيانات"]),
            ("إدارة دورة حياة البيانات", ["تطبيق سياسات الاحتفاظ", "أتمتة حذف البيانات", "إدارة أرشفة البيانات"])
        ],
        "pillars_en": [
            ("Data Governance & Stewardship", ["Establish Data Governance Council", "Implement Data Stewardship Program", "Deploy Enterprise Data Catalog"]),
            ("Data Quality Management", ["Implement DQ monitoring tools", "Establish domain-specific quality rules", "Create DQ dashboards"]),
            ("PDPL Compliance", ["Conduct PDPL gap assessment", "Implement consent management platform", "Deploy data masking tools"]),
            ("Data Lifecycle Management", ["Implement retention policies", "Automate data deletion", "Manage data archival"])
        ],
        "roadmap_ar": [
            ("التأسيس", "مجلس حوكمة البيانات", "٢", "١٥٠,٠٠٠", "CDO", "تشكيل المجلس"),
            ("التأسيس", "تقييم فجوات PDPL", "٣", "٣٠٠,٠٠٠", "Privacy Officer", "تقرير الفجوات"),
            ("البناء", "كتالوج البيانات المؤسسي", "٦", "١,٥٠٠,٠٠٠", "Data Arch", "تغطية ١٠٠٪"),
            ("البناء", "منصة إدارة الموافقات", "٤", "٨٠٠,٠٠٠", "Privacy Team", "إدارة الموافقات"),
            ("التحسين", "أتمتة دورة حياة البيانات", "٦", "٧٠٠,٠٠٠", "Data Ops", "أتمتة كاملة")
        ],
        "roadmap_en": [
            ("Foundation", "Data Governance Council", "2", "150,000", "CDO", "Council formed"),
            ("Foundation", "PDPL Gap Assessment", "3", "300,000", "Privacy Officer", "Gap report"),
            ("Build", "Enterprise Data Catalog", "6", "1,500,000", "Data Arch", "100% coverage"),
            ("Build", "Consent Management Platform", "4", "800,000", "Privacy Team", "Consent managed"),
            ("Optimize", "Data Lifecycle Automation", "6", "700,000", "Data Ops", "Full automation")
        ],
        "total_ar": "٣,٤٥٠,٠٠٠",
        "total_en": "3,450,000",
        "gaps_ar": "حوكمة البيانات المؤسسية، الامتثال لـ PDPL، إدارة جودة البيانات",
        "gaps_en": "Enterprise data governance, PDPL compliance, Data quality management",
        "kpis_ar": ["امتثال PDPL: > ٩٥٪", "جودة البيانات: > ٩٥٪", "استجابة DSAR: < ٣٠ يوم", "تغطية الموافقات: ١٠٠٪"],
        "kpis_en": ["PDPL Compliance: > 95%", "Data Quality: > 95%", "DSAR Response: < 30 days", "Consent Coverage: 100%"],
        "risks_ar": ["عدم الامتثال لـ PDPL", "مشاكل جودة البيانات", "الوصول غير المصرح به", "انتهاكات الاحتفاظ"],
        "risks_en": ["PDPL non-compliance", "Data quality issues", "Unauthorized access", "Retention violations"],
        "frameworks": "PDPL, NDMO Guidelines, DAMA DMBOK",
        "frameworks_ar": "نظام حماية البيانات الشخصية PDPL، إرشادات NDMO"
    },
    "Digital Transformation": {
        "ar_name": "التحول الرقمي",
        "vision_ar": "تسريع رحلة التحول الرقمي للمنظمة، وتقديم تجارب عملاء استثنائية والتميز التشغيلي من خلال الابتكار التقني والقدرات الرقمية.",
        "vision_en": "Accelerate the organization's digital transformation journey, delivering exceptional customer experiences and operational excellence through technology innovation.",
        "objectives_ar": ["تحقيق معدل تبني رقمي ٨٠٪+", "أتمتة ٧٠٪ من العمليات اليدوية", "تحسين رضا العملاء إلى ٩٠٪", "ترحيل ٨٠٪ من الأنظمة للسحابة", "تقليل وقت إطلاق الخدمات بنسبة ٥٠٪"],
        "objectives_en": ["Achieve 80%+ digital adoption rate", "Automate 70% of manual processes", "Improve customer satisfaction to 90%", "Migrate 80% of systems to cloud", "Reduce time-to-market by 50%"],
        "pillars_ar": [
            ("تحويل تجربة العملاء", ["إطلاق منصة الخدمات الرقمية", "تطبيق القنوات الرقمية الموحدة", "نشر chatbot ذكي"]),
            ("أتمتة العمليات", ["تحديد فرص RPA", "تطبيق أتمتة العمليات الروبوتية", "رقمنة العمليات الورقية"]),
            ("البنية التحتية السحابية", ["تطوير استراتيجية السحابة", "ترحيل الأنظمة للسحابة", "تطبيق DevOps"]),
            ("إدارة التغيير والتبني", ["تطوير خطة إدارة التغيير", "برامج تدريب المستخدمين", "قياس التبني الرقمي"])
        ],
        "pillars_en": [
            ("Customer Experience Transformation", ["Launch digital services platform", "Implement omnichannel", "Deploy AI chatbot"]),
            ("Process Automation", ["Identify RPA opportunities", "Implement robotic process automation", "Digitize paper processes"]),
            ("Cloud Infrastructure", ["Develop cloud strategy", "Migrate systems to cloud", "Implement DevOps"]),
            ("Change Management & Adoption", ["Develop change management plan", "User training programs", "Measure digital adoption"])
        ],
        "roadmap_ar": [
            ("التأسيس", "استراتيجية التحول الرقمي", "٣", "٤٠٠,٠٠٠", "CDO", "اعتماد الاستراتيجية"),
            ("التأسيس", "تقييم الجاهزية الرقمية", "٢", "٢٠٠,٠٠٠", "DT Team", "تقرير الجاهزية"),
            ("البناء", "منصة الخدمات الرقمية", "٨", "٣,٠٠٠,٠٠٠", "Digital Team", "إطلاق المنصة"),
            ("البناء", "أتمتة العمليات RPA", "٦", "١,٢٠٠,٠٠٠", "Process Team", "أتمتة ٧٠٪"),
            ("التحسين", "برنامج إدارة التغيير", "٦", "٥٠٠,٠٠٠", "Change Mgmt", "تبني ٨٠٪")
        ],
        "roadmap_en": [
            ("Foundation", "Digital Transformation Strategy", "3", "400,000", "CDO", "Strategy approved"),
            ("Foundation", "Digital Readiness Assessment", "2", "200,000", "DT Team", "Readiness report"),
            ("Build", "Digital Services Platform", "8", "3,000,000", "Digital Team", "Platform launched"),
            ("Build", "RPA Process Automation", "6", "1,200,000", "Process Team", "70% automated"),
            ("Optimize", "Change Management Program", "6", "500,000", "Change Mgmt", "80% adoption")
        ],
        "total_ar": "٥,٣٠٠,٠٠٠",
        "total_en": "5,300,000",
        "gaps_ar": "استراتيجية التحول الرقمي، تجربة العملاء الرقمية، أتمتة العمليات",
        "gaps_en": "Digital transformation strategy, Digital customer experience, Process automation",
        "kpis_ar": ["التبني الرقمي: > ٨٠٪", "أتمتة العمليات: > ٧٠٪", "رضا العملاء: > ٩٠٪", "الترحيل السحابي: > ٨٠٪"],
        "kpis_en": ["Digital Adoption: > 80%", "Process Automation: > 70%", "Customer Satisfaction: > 90%", "Cloud Migration: > 80%"],
        "risks_ar": ["فشل المشروع", "مقاومة التغيير", "فشل التكامل", "تجاوز الميزانية"],
        "risks_en": ["Project failure", "Change resistance", "Integration failure", "Budget overrun"],
        "frameworks": "DGA Standards, Vision 2030, TOGAF",
        "frameworks_ar": "معايير هيئة الحكومة الرقمية، رؤية ٢٠٣٠، TOGAF"
    },
    "Global Standards": {
        "ar_name": "المعايير العالمية",
        "vision_ar": "ترسيخ المنظمة كمرجع للتميز في أنظمة الإدارة، وتحقيق والحفاظ على شهادات ISO 27001 و ISO 22301 و ISO 9001.",
        "vision_en": "Establish the organization as a benchmark for management system excellence, achieving and maintaining ISO 27001, ISO 22301, and ISO 9001 certifications.",
        "objectives_ar": ["الحصول على شهادة ISO 27001", "تحقيق شهادة ISO 22301", "الحفاظ على شهادة ISO 9001", "تحقيق صفر عدم مطابقات جوهرية", "تطبيق ثقافة التحسين المستمر"],
        "objectives_en": ["Achieve ISO 27001 certification", "Achieve ISO 22301 certification", "Maintain ISO 9001 certification", "Zero major non-conformities", "Implement continual improvement culture"],
        "pillars_ar": [
            ("أمن المعلومات ISO 27001", ["تطبيق نظام ISMS", "تحديد نطاق الشهادة", "تنفيذ ضوابط Annex A"]),
            ("استمرارية الأعمال ISO 22301", ["إجراء تحليل أثر الأعمال BIA", "تطوير خطط الاستمرارية", "اختبار خطط BCM"]),
            ("إدارة الجودة ISO 9001", ["توثيق العمليات", "تطبيق مؤشرات الجودة", "إدارة رضا العملاء"]),
            ("التدقيق والتحسين المستمر", ["برنامج التدقيق الداخلي", "عملية الإجراءات التصحيحية CAPA", "مراجعات الإدارة الدورية"])
        ],
        "pillars_en": [
            ("Information Security ISO 27001", ["Implement ISMS", "Define certification scope", "Implement Annex A controls"]),
            ("Business Continuity ISO 22301", ["Conduct BIA", "Develop continuity plans", "Test BCM plans"]),
            ("Quality Management ISO 9001", ["Document processes", "Implement quality KPIs", "Manage customer satisfaction"]),
            ("Audit & Continual Improvement", ["Internal audit program", "CAPA process", "Management reviews"])
        ],
        "roadmap_ar": [
            ("التأسيس", "تحليل الفجوات ISO", "٢", "٢٠٠,٠٠٠", "ISMS Manager", "تقرير الفجوات"),
            ("التأسيس", "توثيق نظام ISMS", "٤", "٣٥٠,٠٠٠", "QMS Team", "وثائق ISMS"),
            ("البناء", "تطبيق ضوابط ISO 27001", "٨", "١,٥٠٠,٠٠٠", "Security Team", "تطبيق الضوابط"),
            ("البناء", "برنامج BCM وISO 22301", "٦", "٨٠٠,٠٠٠", "BCM Manager", "خطط الاستمرارية"),
            ("التحسين", "التدقيق الخارجي والشهادة", "٣", "٣٠٠,٠٠٠", "QMS Manager", "الحصول على الشهادة")
        ],
        "roadmap_en": [
            ("Foundation", "ISO Gap Analysis", "2", "200,000", "ISMS Manager", "Gap report"),
            ("Foundation", "ISMS Documentation", "4", "350,000", "QMS Team", "ISMS documented"),
            ("Build", "ISO 27001 Controls Implementation", "8", "1,500,000", "Security Team", "Controls implemented"),
            ("Build", "BCM & ISO 22301 Program", "6", "800,000", "BCM Manager", "Continuity plans"),
            ("Optimize", "External Audit & Certification", "3", "300,000", "QMS Manager", "Certification achieved")
        ],
        "total_ar": "٣,١٥٠,٠٠٠",
        "total_en": "3,150,000",
        "gaps_ar": "نظام إدارة أمن المعلومات ISMS، إدارة استمرارية الأعمال BCM، نضج عمليات التدقيق",
        "gaps_en": "ISMS implementation, BCM management, Audit process maturity",
        "kpis_ar": ["اكتمال التدقيق: ١٠٠٪", "عدم المطابقات المفتوحة: < ٥", "اختبار BCM: ١٠٠٪", "مراجعات الإدارة: ١٠٠٪"],
        "kpis_en": ["Audit Completion: 100%", "Open NCs: < 5", "BCM Tests: 100%", "Management Reviews: 100%"],
        "risks_ar": ["فشل الاعتماد", "عدم مطابقة جوهرية", "فجوات التوثيق", "فشل اختبار BCM"],
        "risks_en": ["Certification failure", "Major non-conformity", "Documentation gaps", "BCM test failure"],
        "frameworks": "ISO 27001, ISO 22301, ISO 9001",
        "frameworks_ar": "ISO 27001، ISO 22301، ISO 9001"
    }
}


def get_domain_content(domain: str) -> Dict:
    """Get complete domain content."""
    # Try exact match first
    if domain in DOMAIN_CONTENT:
        return DOMAIN_CONTENT[domain]
    
    # Try partial match
    domain_lower = domain.lower()
    if "ai" in domain_lower or "artificial" in domain_lower or "ذكاء" in domain:
        return DOMAIN_CONTENT["Artificial Intelligence"]
    elif "data" in domain_lower or "بيانات" in domain:
        return DOMAIN_CONTENT["Data Management"]
    elif "digital" in domain_lower or "transform" in domain_lower or "تحول" in domain or "رقمي" in domain:
        return DOMAIN_CONTENT["Digital Transformation"]
    elif "global" in domain_lower or "standard" in domain_lower or "iso" in domain_lower or "معايير" in domain:
        return DOMAIN_CONTENT["Global Standards"]
    else:
        return DOMAIN_CONTENT["Cyber Security"]


def generate_strategy(domain: str, org_name: str, sector: str, language: str) -> str:
    """Generate complete strategy document."""
    ctx = get_domain_content(domain)
    
    if language in ["Arabic", "العربية"]:
        # Build pillars
        pillars_text = ""
        for i, (name, inits) in enumerate(ctx['pillars_ar'], 1):
            pillars_text += f"\n**الركيزة {i}: {name}**\n"
            for init in inits:
                pillars_text += f"- {init}\n"
        
        # Build objectives
        objectives_text = "\n".join([f"{i}. {obj}" for i, obj in enumerate(ctx['objectives_ar'], 1)])
        
        # Build roadmap table
        roadmap_text = "| المرحلة | المبادرة | المدة (شهر) | الاستثمار (ريال) | المسؤول | مؤشر النجاح |\n"
        roadmap_text += "|---------|----------|-------------|------------------|---------|-------------|\n"
        for phase, init, dur, cost, owner, kpi in ctx['roadmap_ar']:
            roadmap_text += f"| {phase} | {init} | {dur} | {cost} | {owner} | {kpi} |\n"
        
        # Build KPIs
        kpis_text = "\n".join([f"- {kpi}" for kpi in ctx['kpis_ar']])
        
        # Build KRIs
        kris_text = "\n".join([f"- {risk}" for risk in ctx['risks_ar']])
        
        return f"""**الرؤية التنفيذية**

{ctx['vision_ar']}

**الأهداف الاستراتيجية:**
{objectives_text}

---

**الركائز الاستراتيجية والمبادرات**
{pillars_text}

---

**خطة التنفيذ التفصيلية**

{roadmap_text}

**إجمالي الاستثمار المقدر: {ctx['total_ar']} ريال**
**مدة التنفيذ: ٢٤ شهر**

---

**مؤشرات الأداء الرئيسية:**
{kpis_text}

**مؤشرات المخاطر الرئيسية:**
{kris_text}

---

**الفجوات الحرجة المحددة:** {ctx['gaps_ar']}

**الأطر المرجعية:** {ctx['frameworks_ar']}

**درجة الثقة: 85/100**
"""
    
    else:  # English
        # Build pillars
        pillars_text = ""
        for i, (name, inits) in enumerate(ctx['pillars_en'], 1):
            pillars_text += f"\n**Pillar {i}: {name}**\n"
            for init in inits:
                pillars_text += f"- {init}\n"
        
        # Build objectives
        objectives_text = "\n".join([f"{i}. {obj}" for i, obj in enumerate(ctx['objectives_en'], 1)])
        
        # Build roadmap table
        roadmap_text = "| Phase | Initiative | Duration (Months) | Investment (SAR) | Owner | Success KPI |\n"
        roadmap_text += "|-------|------------|-------------------|------------------|-------|-------------|\n"
        for phase, init, dur, cost, owner, kpi in ctx['roadmap_en']:
            roadmap_text += f"| {phase} | {init} | {dur} | {cost} | {owner} | {kpi} |\n"
        
        # Build KPIs
        kpis_text = "\n".join([f"- {kpi}" for kpi in ctx['kpis_en']])
        
        # Build KRIs
        kris_text = "\n".join([f"- {risk}" for risk in ctx['risks_en']])
        
        return f"""**Executive Vision**

{ctx['vision_en']}

**Strategic Objectives:**
{objectives_text}

---

**Strategic Pillars & Initiatives**
{pillars_text}

---

**Detailed Implementation Plan**

{roadmap_text}

**Total Estimated Investment: SAR {ctx['total_en']}**
**Implementation Timeline: 24 months**

---

**Key Performance Indicators:**
{kpis_text}

**Key Risk Indicators:**
{kris_text}

---

**Critical Gaps Identified:** {ctx['gaps_en']}

**Reference Frameworks:** {ctx['frameworks']}

**Confidence Score: 85/100**
"""


def generate_policy(domain: str, policy_name: str, language: str) -> str:
    """Generate policy document."""
    ctx = get_domain_content(domain)
    
    if language in ["Arabic", "العربية"]:
        return f"""**سياسة {ctx['ar_name']}**

**١. الغرض**
تحدد هذه السياسة الإطار والمتطلبات لـ {ctx['ar_name']} في المنظمة، وتضمن الامتثال لـ {ctx['frameworks_ar']}.

**٢. النطاق**
تنطبق على جميع الموظفين والمتعاقدين والأطراف الثالثة التي تتعامل مع أنظمة وبيانات المنظمة.

**٣. المتطلبات الرئيسية**

{chr(10).join([f'- {obj}' for obj in ctx['objectives_ar']])}

**٤. الأدوار والمسؤوليات**

| الدور | المسؤولية |
|-------|----------|
| الإدارة العليا | الرعاية والدعم التنفيذي |
| مدير البرنامج | الإشراف على التنفيذ والامتثال |
| الفريق التقني | تطبيق الضوابط والإجراءات |
| جميع الموظفين | الالتزام بمتطلبات السياسة |

**٥. الضوابط والإجراءات**

الضوابط المطبقة وفقاً لـ {ctx['frameworks_ar']}:
{chr(10).join([f'- {p[0]}' for p in ctx['pillars_ar']])}

**٦. الامتثال والتنفيذ**
- مراجعة دورية للامتثال
- التدقيق الداخلي والخارجي
- العقوبات في حالة المخالفة
- آلية طلب الاستثناءات

**٧. المراجعة والتحديث**
- دورة المراجعة: سنوياً أو عند وجود تغييرات جوهرية
- مالك السياسة: مدير البرنامج
- تاريخ المراجعة القادمة: [+١ سنة]

---
*اعتمد من: [اسم المعتمد] | التاريخ: [تاريخ الاعتماد]*
"""
    else:
        return f"""**{domain} Policy**

**1. Purpose**
This policy establishes the framework and requirements for {domain} within the organization, ensuring compliance with {ctx['frameworks']}.

**2. Scope**
Applies to all employees, contractors, and third parties handling organizational systems and data.

**3. Key Requirements**

{chr(10).join([f'- {obj}' for obj in ctx['objectives_en']])}

**4. Roles and Responsibilities**

| Role | Responsibility |
|------|----------------|
| Executive Management | Sponsorship and support |
| Program Manager | Implementation oversight and compliance |
| Technical Team | Control and procedure implementation |
| All Employees | Compliance with policy requirements |

**5. Controls and Procedures**

Controls implemented per {ctx['frameworks']}:
{chr(10).join([f'- {p[0]}' for p in ctx['pillars_en']])}

**6. Compliance and Enforcement**
- Regular compliance reviews
- Internal and external audits
- Penalties for violations
- Exception request process

**7. Review and Update**
- Review Cycle: Annually or upon significant changes
- Policy Owner: Program Manager
- Next Review Date: [+1 year]

---
*Approved by: [Approver Name] | Date: [Approval Date]*
"""


def generate_audit(domain: str, language: str) -> str:
    """Generate audit report."""
    ctx = get_domain_content(domain)
    
    if language in ["Arabic", "العربية"]:
        return f"""**تقرير تدقيق الامتثال - {ctx['ar_name']}**

**١. الملخص التنفيذي**

تم تقييم بيئة الضوابط مقابل متطلبات {ctx['frameworks_ar']}. 

**التقييم العام: امتثال جزئي (65%)**

| التصنيف | العدد |
|---------|-------|
| مطابق | 8 |
| مطابق جزئياً | 5 |
| غير مطابق | 3 |

**٢. نطاق التدقيق والمنهجية**
- مراجعة وثائقية شاملة
- اختبار الضوابط
- مقابلات أصحاب المصلحة
- حجم العينة: 50 ضابط

**٣. النتائج الرئيسية**

**النتيجة ١: {ctx['risks_ar'][0]} (عالي)**
| البند | التفاصيل |
|-------|----------|
| المرجع | {ctx['frameworks_ar']} |
| الملاحظة | تم تحديد فجوات في تطبيق الضوابط المطلوبة |
| الأدلة | مراجعة الوثائق، اختبار النظام |
| السبب الجذري | العملية: إجراءات غير موثقة؛ التقنية: أدوات غير مطبقة |
| الأثر | عدم الامتثال التنظيمي المحتمل |
| التوصية | تطوير وتطبيق الإجراءات المطلوبة |
| الموعد | الربع القادم |

**النتيجة ٢: {ctx['risks_ar'][1] if len(ctx['risks_ar']) > 1 else 'نقص في التوثيق'} (متوسط)**
| البند | التفاصيل |
|-------|----------|
| المرجع | {ctx['frameworks_ar']} |
| الملاحظة | التوثيق غير مكتمل أو قديم |
| التوصية | تحديث التوثيق |
| الموعد | ٣٠ يوم |

**النتيجة ٣: {ctx['risks_ar'][2] if len(ctx['risks_ar']) > 2 else 'فجوة في التدريب'} (متوسط)**
| البند | التفاصيل |
|-------|----------|
| المرجع | متطلبات التوعية |
| الملاحظة | برنامج التدريب يحتاج تحسين |
| التوصية | تعزيز برنامج التوعية |
| الموعد | الربع القادم |

**٤. الملاحظات الإيجابية**
✓ دعم تنفيذي قوي
✓ فريق ملتزم
✓ إطار سياسات موثق

**٥. ملخص التوصيات**

| الأولوية | النتيجة | المسؤول | الموعد |
|----------|---------|---------|--------|
| عالي | تطبيق الضوابط | الفريق التقني | الربع القادم |
| متوسط | تحديث التوثيق | مدير البرنامج | ٣٠ يوم |

**٦. الخلاصة**
المنظمة أسست ضوابط أساسية ولكن تتطلب معالجة الفجوات المحددة لتحقيق الامتثال الكامل.

**درجة الثقة: 78/100**
"""
    else:
        return f"""**Compliance Audit Report - {domain}**

**1. Executive Summary**

Control environment assessed against {ctx['frameworks']} requirements.

**Overall Assessment: Partial Compliance (65%)**

| Rating | Count |
|--------|-------|
| Conforming | 8 |
| Partially Conforming | 5 |
| Non-Conforming | 3 |

**2. Scope and Methodology**
- Comprehensive document review
- Control testing
- Stakeholder interviews
- Sample size: 50 controls

**3. Key Findings**

**Finding 1: {ctx['risks_en'][0]} (HIGH)**
| Item | Details |
|------|---------|
| Reference | {ctx['frameworks']} |
| Observation | Gaps identified in required control implementation |
| Evidence | Document review, system testing |
| Root Cause | Process: Undocumented procedures; Technology: Tools not implemented |
| Impact | Potential regulatory non-compliance |
| Recommendation | Develop and implement required procedures |
| Target | Next quarter |

**Finding 2: {ctx['risks_en'][1] if len(ctx['risks_en']) > 1 else 'Documentation Gap'} (MEDIUM)**
| Item | Details |
|------|---------|
| Reference | {ctx['frameworks']} |
| Observation | Documentation incomplete or outdated |
| Recommendation | Update documentation |
| Target | 30 days |

**Finding 3: {ctx['risks_en'][2] if len(ctx['risks_en']) > 2 else 'Training Gap'} (MEDIUM)**
| Item | Details |
|------|---------|
| Reference | Awareness requirements |
| Observation | Training program needs improvement |
| Recommendation | Enhance awareness program |
| Target | Next quarter |

**4. Positive Observations**
✓ Strong executive support
✓ Committed team
✓ Documented policy framework

**5. Recommendations Summary**

| Priority | Finding | Owner | Target |
|----------|---------|-------|--------|
| High | Control implementation | Technical Team | Next quarter |
| Medium | Documentation update | Program Manager | 30 days |

**6. Conclusion**
Organization has established foundational controls but requires remediation of identified gaps.

**Confidence Score: 78/100**
"""


def generate_risk(domain: str, threat: str, asset: str, language: str) -> str:
    """Generate risk assessment."""
    ctx = get_domain_content(domain)
    
    if language in ["Arabic", "العربية"]:
        return f"""**تقييم المخاطر - {ctx['ar_name']}**

**١. تحديد المخاطر**
- **سيناريو التهديد:** {threat}
- **الأصل المتأثر:** {asset}
- **الأطر المرجعية:** {ctx['frameworks_ar']}

**٢. سجل المخاطر**

| المعرف | الخطر | الاحتمال | الأثر | الدرجة | الفئة |
|--------|-------|---------|-------|--------|-------|
| R-01 | {ctx['risks_ar'][0]} | 4 | 5 | 20 | حرج |
| R-02 | {ctx['risks_ar'][1] if len(ctx['risks_ar']) > 1 else 'خطر ثانوي'} | 3 | 4 | 12 | عالي |
| R-03 | {ctx['risks_ar'][2] if len(ctx['risks_ar']) > 2 else 'خطر تشغيلي'} | 4 | 3 | 12 | عالي |
| R-04 | {ctx['risks_ar'][3] if len(ctx['risks_ar']) > 3 else 'خطر امتثال'} | 3 | 4 | 12 | عالي |

**٣. تقييم الأثر**

| البعد | التقييم | الوصف |
|-------|---------|-------|
| المالي | عالي | خسائر محتملة كبيرة |
| التشغيلي | عالي | تعطل العمليات |
| السمعة | متوسط | تأثير على الثقة |
| التنظيمي | عالي | غرامات محتملة |

**٤. مصفوفة المخاطر**

| القياس | القيمة |
|--------|--------|
| الخطر الكامن | عالي (18) |
| فعالية الضوابط | 50% |
| الخطر المتبقي | متوسط-عالي (9) |

**٥. الضوابط الموصى بها**

{chr(10).join([f'- {p[0]}' for p in ctx['pillars_ar']])}

**٦. استراتيجية التخفيف**

**إجراءات فورية (٠-٣٠ يوم):**
- مراجعة الضوابط الحالية
- تفعيل المراقبة المكثفة

**قصيرة المدى (١-٣ أشهر):**
- تطبيق ضوابط إضافية
- تحديث الإجراءات

**طويلة المدى (٣-١٢ شهر):**
- تعزيز البنية
- أتمتة الضوابط

**٧. مؤشرات المخاطر الرئيسية**

| المؤشر | الحد المقبول | العلامة الحمراء |
|--------|-------------|----------------|
{chr(10).join([f'| {kpi} | تحقيق الهدف | تجاوز الحد |' for kpi in ctx['kpis_ar'][:4]])}

**درجة الثقة: 80/100**
"""
    else:
        return f"""**Risk Assessment - {domain}**

**1. Risk Identification**
- **Threat Scenario:** {threat}
- **Affected Asset:** {asset}
- **Reference Frameworks:** {ctx['frameworks']}

**2. Risk Register**

| ID | Risk | Likelihood | Impact | Score | Category |
|----|------|------------|--------|-------|----------|
| R-01 | {ctx['risks_en'][0]} | 4 | 5 | 20 | Critical |
| R-02 | {ctx['risks_en'][1] if len(ctx['risks_en']) > 1 else 'Secondary Risk'} | 3 | 4 | 12 | High |
| R-03 | {ctx['risks_en'][2] if len(ctx['risks_en']) > 2 else 'Operational Risk'} | 4 | 3 | 12 | High |
| R-04 | {ctx['risks_en'][3] if len(ctx['risks_en']) > 3 else 'Compliance Risk'} | 3 | 4 | 12 | High |

**3. Impact Assessment**

| Dimension | Rating | Description |
|-----------|--------|-------------|
| Financial | High | Significant potential losses |
| Operational | High | Service disruption |
| Reputational | Medium | Trust impact |
| Regulatory | High | Potential fines |

**4. Risk Matrix**

| Measure | Value |
|---------|-------|
| Inherent Risk | High (18) |
| Control Effectiveness | 50% |
| Residual Risk | Medium-High (9) |

**5. Recommended Controls**

{chr(10).join([f'- {p[0]}' for p in ctx['pillars_en']])}

**6. Mitigation Strategy**

**Immediate (0-30 days):**
- Review current controls
- Activate enhanced monitoring

**Short-term (1-3 months):**
- Implement additional controls
- Update procedures

**Long-term (3-12 months):**
- Architecture enhancement
- Control automation

**7. Key Risk Indicators**

| KRI | Threshold | Red Flag |
|-----|-----------|----------|
{chr(10).join([f'| {kpi} | Achieve target | Exceeded |' for kpi in ctx['kpis_en'][:4]])}

**Confidence Score: 80/100**
"""


# Test the generator
if __name__ == "__main__":
    print("Testing Fixed AI Generator...")
    
    domains = ["Cyber Security", "Artificial Intelligence", "Data Management", "Digital Transformation", "Global Standards"]
    
    for domain in domains:
        strategy = generate_strategy(domain, "Test Org", "Banking", "Arabic")
        # Get first line of vision
        lines = strategy.split('\n')
        for i, line in enumerate(lines):
            if "الرؤية" in line and i+2 < len(lines):
                vision = lines[i+2][:60] if lines[i+2].strip() else lines[i+3][:60]
                print(f"{domain}: {vision}...")
                break
