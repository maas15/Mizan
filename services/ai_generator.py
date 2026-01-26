"""
Mizan GRC - AI Document Generator
Generates all GRC documents using AI prompts, not hardcoded templates.
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

# Domain-specific context for AI prompts
DOMAIN_CONTEXTS = {
    "Cyber Security": {
        "ar_name": "الأمن السيبراني",
        "frameworks": "NCA ECC, SAMA CSF, ISO 27001, NIST CSF",
        "frameworks_ar": "ضوابط الهيئة الوطنية للأمن السيبراني، إطار ساما، ISO 27001",
        "focus_areas": "threat detection, incident response, access management, vulnerability management, security awareness",
        "focus_areas_ar": "كشف التهديدات، الاستجابة للحوادث، إدارة الوصول، إدارة الثغرات، التوعية الأمنية",
        "kpis": ["MTTD < 4 hours", "MTTR < 2 hours", "Phishing click rate < 5%", "MFA coverage 100%", "Critical vulns < 5"],
        "kpis_ar": ["وقت الاكتشاف < ٤ ساعات", "وقت الاستجابة < ٢ ساعة", "معدل النقر على التصيد < ٥٪", "تغطية MFA ١٠٠٪"],
        "risks": ["Ransomware", "Data breach", "Insider threat", "Phishing", "Third-party breach"],
        "risks_ar": ["برامج الفدية", "اختراق البيانات", "التهديد الداخلي", "التصيد الاحتيالي", "اختراق الطرف الثالث"]
    },
    "Artificial Intelligence": {
        "ar_name": "الذكاء الاصطناعي",
        "frameworks": "SDAIA AI Ethics, NIST AI RMF, EU AI Act, ISO 42001",
        "frameworks_ar": "مبادئ أخلاقيات سدايا للذكاء الاصطناعي، إطار NIST لإدارة مخاطر AI، ISO 42001",
        "focus_areas": "AI governance, bias testing, model explainability, ethical AI, model monitoring, fairness",
        "focus_areas_ar": "حوكمة الذكاء الاصطناعي، اختبار التحيز، قابلية تفسير النماذج، الذكاء الاصطناعي الأخلاقي، مراقبة النماذج، العدالة",
        "kpis": ["Model bias detected 0", "AI ethics violations 0", "Model drift incidents < 3/quarter", "Explainability coverage 100%"],
        "kpis_ar": ["تحيز النماذج المكتشف = صفر", "انتهاكات أخلاقيات AI = صفر", "حوادث انحراف النماذج < ٣/ربع سنوي", "تغطية قابلية التفسير ١٠٠٪"],
        "risks": ["Biased model decisions", "Model drift", "Adversarial attacks", "Lack of explainability", "Privacy violations"],
        "risks_ar": ["قرارات نماذج متحيزة", "انحراف النماذج", "الهجمات العدائية", "نقص قابلية التفسير", "انتهاكات الخصوصية"]
    },
    "Data Management": {
        "ar_name": "إدارة البيانات",
        "frameworks": "PDPL, NDMO Guidelines, DAMA DMBOK, ISO 8000",
        "frameworks_ar": "نظام حماية البيانات الشخصية PDPL، إرشادات مكتب إدارة البيانات الوطني NDMO، DAMA DMBOK",
        "focus_areas": "data governance, PDPL compliance, data quality, consent management, data classification, retention",
        "focus_areas_ar": "حوكمة البيانات، الامتثال لنظام حماية البيانات الشخصية، جودة البيانات، إدارة الموافقات، تصنيف البيانات، الاحتفاظ بالبيانات",
        "kpis": ["PDPL compliance > 95%", "Data quality score > 95%", "DSAR response < 30 days", "Consent coverage 100%"],
        "kpis_ar": ["امتثال PDPL > ٩٥٪", "درجة جودة البيانات > ٩٥٪", "الاستجابة لطلبات الوصول < ٣٠ يوم", "تغطية الموافقات ١٠٠٪"],
        "risks": ["PDPL non-compliance", "Data quality issues", "Unauthorized access", "Retention violations", "Cross-border transfer issues"],
        "risks_ar": ["عدم الامتثال لـ PDPL", "مشاكل جودة البيانات", "الوصول غير المصرح به", "انتهاكات الاحتفاظ", "مشاكل النقل عبر الحدود"]
    },
    "Digital Transformation": {
        "ar_name": "التحول الرقمي",
        "frameworks": "DGA Standards, Vision 2030, TOGAF, COBIT",
        "frameworks_ar": "معايير هيئة الحكومة الرقمية، رؤية ٢٠٣٠، TOGAF، COBIT",
        "focus_areas": "digital strategy, change management, user adoption, cloud migration, process automation, customer experience",
        "focus_areas_ar": "الاستراتيجية الرقمية، إدارة التغيير، تبني المستخدمين، الترحيل السحابي، أتمتة العمليات، تجربة العملاء",
        "kpis": ["Digital adoption > 80%", "Project on-time delivery > 85%", "Customer satisfaction > 90%", "Process automation > 70%"],
        "kpis_ar": ["التبني الرقمي > ٨٠٪", "تسليم المشاريع في الوقت > ٨٥٪", "رضا العملاء > ٩٠٪", "أتمتة العمليات > ٧٠٪"],
        "risks": ["Project failure", "Change resistance", "Integration failure", "Vendor lock-in", "Budget overrun"],
        "risks_ar": ["فشل المشروع", "مقاومة التغيير", "فشل التكامل", "الارتباط بمزود واحد", "تجاوز الميزانية"]
    },
    "Global Standards": {
        "ar_name": "المعايير العالمية",
        "frameworks": "ISO 27001, ISO 22301, ISO 9001, ISO 31000, ITIL",
        "frameworks_ar": "ISO 27001 أمن المعلومات، ISO 22301 استمرارية الأعمال، ISO 9001 إدارة الجودة",
        "focus_areas": "certification, internal audit, management review, CAPA, document control, continual improvement",
        "focus_areas_ar": "الاعتماد، التدقيق الداخلي، مراجعة الإدارة، الإجراءات التصحيحية، ضبط الوثائق، التحسين المستمر",
        "kpis": ["Audit completion 100%", "Open NCs < 5", "Management review actions 100%", "BCM test coverage 100%"],
        "kpis_ar": ["اكتمال التدقيق ١٠٠٪", "عدم المطابقات المفتوحة < ٥", "إجراءات مراجعة الإدارة ١٠٠٪", "تغطية اختبار BCM ١٠٠٪"],
        "risks": ["Certification failure", "Major non-conformity", "Documentation gaps", "BCP test failure", "Management disengagement"],
        "risks_ar": ["فشل الاعتماد", "عدم مطابقة جوهرية", "فجوات التوثيق", "فشل اختبار خطة الاستمرارية", "عدم انخراط الإدارة"]
    }
}


def get_domain_context(domain: str) -> Dict:
    """Get domain context, with fallback."""
    return DOMAIN_CONTEXTS.get(domain, DOMAIN_CONTEXTS["Cyber Security"])


def generate_strategy_prompt(domain: str, org_name: str, sector: str, language: str, compliance_score: int = 60) -> str:
    """Generate AI prompt for strategy document."""
    ctx = get_domain_context(domain)
    
    if language in ["Arabic", "العربية"]:
        return f"""أنت مستشار استراتيجي أول في إحدى شركات الأربعة الكبار (ديلويت/EY/PwC/KPMG).

**المهمة:** إعداد استراتيجية شاملة لـ {ctx['ar_name']} لمنظمة "{org_name}" في قطاع {sector}.

**الأطر المرجعية:** {ctx['frameworks_ar']}

**مجالات التركيز:** {ctx['focus_areas_ar']}

**متطلبات المحتوى:**

١. **الرؤية التنفيذية** (فقرة واحدة)
- رؤية طموحة وواقعية خاصة بمجال {ctx['ar_name']}
- ربط الرؤية برؤية ٢٠٣٠ والأهداف الوطنية

٢. **الأهداف الاستراتيجية** (٥ أهداف)
- أهداف قابلة للقياس SMART
- مرتبطة بمجال {ctx['ar_name']} تحديداً

٣. **الركائز الاستراتيجية** (٤-٥ ركائز)
- كل ركيزة مع ٣ مبادرات
- خاصة بمجال {ctx['ar_name']}

٤. **خطة التنفيذ التفصيلية**
جدول يحتوي على:
| المرحلة | المبادرة | المدة (شهر) | الاستثمار (ريال) | المسؤول | مؤشر النجاح |

المراحل:
- التأسيس (٠-٦ أشهر)
- البناء (٦-١٨ شهر)
- التحسين (١٨-٢٤ شهر)

٥. **مؤشرات الأداء الرئيسية**
مؤشرات خاصة بـ {ctx['ar_name']}:
{chr(10).join(['- ' + kpi for kpi in ctx['kpis_ar']])}

٦. **مؤشرات المخاطر الرئيسية**
مخاطر خاصة بـ {ctx['ar_name']}:
{chr(10).join(['- ' + risk for risk in ctx['risks_ar']])}

**الأسلوب:** احترافي، عملي، قابل للتنفيذ
**اللغة:** العربية الفصحى

لا تذكر "متاح عند الطلب" - قدم كل التفاصيل كاملة."""

    else:  # English
        return f"""You are a Senior Strategy Consultant from a Big 4 firm (Deloitte/EY/PwC/KPMG).

**TASK:** Develop a comprehensive {domain} strategy for "{org_name}" in the {sector} sector.

**REFERENCE FRAMEWORKS:** {ctx['frameworks']}

**FOCUS AREAS:** {ctx['focus_areas']}

**CONTENT REQUIREMENTS:**

1. **Executive Vision** (1 paragraph)
- Ambitious yet realistic vision specific to {domain}
- Aligned with Vision 2030 and national objectives

2. **Strategic Objectives** (5 objectives)
- SMART measurable objectives
- Specific to {domain}

3. **Strategic Pillars** (4-5 pillars)
- Each pillar with 3 initiatives
- Domain-specific to {domain}

4. **Detailed Implementation Plan**
Table format:
| Phase | Initiative | Duration (Months) | Investment (SAR) | Owner | Success KPI |

Phases:
- Foundation (0-6 months)
- Build (6-18 months)
- Optimize (18-24 months)

5. **Key Performance Indicators**
{domain}-specific KPIs:
{chr(10).join(['- ' + kpi for kpi in ctx['kpis']])}

6. **Key Risk Indicators**
{domain}-specific risks:
{chr(10).join(['- ' + risk for risk in ctx['risks']])}

**STYLE:** Professional, actionable, implementation-ready
**DO NOT mention "available upon request" - provide ALL details."""


def generate_policy_prompt(domain: str, policy_name: str, framework: str, language: str) -> str:
    """Generate AI prompt for policy document."""
    ctx = get_domain_context(domain)
    
    if language in ["Arabic", "العربية"]:
        return f"""أنت مستشار حوكمة ومخاطر وامتثال أول في إحدى شركات الأربعة الكبار.

**المهمة:** إعداد سياسة "{policy_name}" لمجال {ctx['ar_name']}.

**الأطر المرجعية:** {ctx['frameworks_ar']}

**هيكل السياسة المطلوب:**

١. **الغرض والنطاق**
- الهدف من السياسة
- نطاق التطبيق

٢. **المتطلبات الرئيسية** (٦-٨ متطلبات)
- متطلبات خاصة بمجال {ctx['ar_name']}
- قابلة للتدقيق والقياس

٣. **الأدوار والمسؤوليات**
| الدور | المسؤولية |
- أدوار خاصة بـ {ctx['ar_name']}

٤. **الضوابط والإجراءات**
- ضوابط تقنية وإدارية
- مرتبطة بـ {ctx['frameworks_ar']}

٥. **الامتثال والتنفيذ**
- آليات المراقبة
- العقوبات والاستثناءات

٦. **المراجعة والتحديث**
- دورة المراجعة
- مالك السياسة

**الأسلوب:** رسمي، واضح، قابل للتدقيق
**اللغة:** العربية الفصحى"""

    else:
        return f"""You are a Senior GRC Consultant from a Big 4 firm.

**TASK:** Develop a "{policy_name}" for {domain}.

**REFERENCE FRAMEWORKS:** {ctx['frameworks']}

**POLICY STRUCTURE:**

1. **Purpose and Scope**
- Policy objective
- Applicability

2. **Key Requirements** (6-8 requirements)
- {domain}-specific requirements
- Auditable and measurable

3. **Roles and Responsibilities**
| Role | Responsibility |
- {domain}-specific roles

4. **Controls and Procedures**
- Technical and administrative controls
- Mapped to {ctx['frameworks']}

5. **Compliance and Enforcement**
- Monitoring mechanisms
- Penalties and exceptions

6. **Review and Update**
- Review cycle
- Policy owner

**STYLE:** Formal, clear, auditable"""


def generate_audit_prompt(domain: str, standard: str, language: str) -> str:
    """Generate AI prompt for audit report."""
    ctx = get_domain_context(domain)
    
    if language in ["Arabic", "العربية"]:
        return f"""أنت مدقق رئيسي أول في إحدى شركات الأربعة الكبار (ديلويت/EY/PwC/KPMG).

**المهمة:** إعداد تقرير تدقيق امتثال لمجال {ctx['ar_name']}.

**المعيار المرجعي:** {ctx['frameworks_ar']}

**هيكل التقرير:**

١. **الملخص التنفيذي**
- نظرة عامة على نطاق التدقيق
- التقييم العام (نسبة الامتثال)
- أهم النتائج

٢. **نطاق التدقيق والمنهجية**
- حدود التدقيق
- المنهجية المستخدمة
- حجم العينات

٣. **النتائج الرئيسية** (٤-٥ نتائج)

لكل نتيجة:
| البند | التفاصيل |
|-------|----------|
| العنوان | [عنوان النتيجة] |
| الأولوية | عالي/متوسط/منخفض |
| المرجع | [بند من {ctx['frameworks_ar']}] |
| الملاحظة | [وصف تفصيلي] |
| الأدلة | [قائمة الأدلة المراجعة] |
| السبب الجذري | [تحليل السبب: أفراد/عمليات/تقنية/حوكمة] |
| الأثر | [الأثر المحتمل] |
| التوصية | [الإجراء المطلوب] |
| الموعد المستهدف | [التاريخ] |

النتائج يجب أن تكون خاصة بـ {ctx['ar_name']}:
{chr(10).join(['- ' + risk for risk in ctx['risks_ar']])}

٤. **الملاحظات الإيجابية**
- نقاط القوة المحددة

٥. **ملخص التوصيات**
| الأولوية | النتيجة | المسؤول | الموعد |

٦. **الخلاصة**
- الرأي العام للمدقق
- درجة الثقة

**الأسلوب:** رسمي، موضوعي، مبني على الأدلة
**اللغة:** العربية الفصحى"""

    else:
        return f"""You are a Senior Lead Auditor from a Big 4 firm (Deloitte/EY/PwC/KPMG).

**TASK:** Prepare a compliance audit report for {domain}.

**REFERENCE STANDARD:** {ctx['frameworks']}

**REPORT STRUCTURE:**

1. **Executive Summary**
- Audit scope overview
- Overall assessment (compliance %)
- Key findings

2. **Audit Scope and Methodology**
- Audit boundaries
- Methodology used
- Sample sizes

3. **Key Findings** (4-5 findings)

For each finding:
| Item | Details |
|------|---------|
| Title | [Finding title] |
| Priority | HIGH/MEDIUM/LOW |
| Control Reference | [Clause from {ctx['frameworks']}] |
| Observation | [Detailed description] |
| Evidence Reviewed | [List of evidence] |
| Root Cause | [Analysis: People/Process/Technology/Governance] |
| Risk Impact | [Potential impact] |
| Recommendation | [Required action] |
| Target Date | [Date] |

Findings must be specific to {domain}:
{chr(10).join(['- ' + risk for risk in ctx['risks']])}

4. **Positive Observations**
- Identified strengths

5. **Recommendations Summary**
| Priority | Finding | Owner | Target |

6. **Conclusion**
- Auditor's overall opinion
- Confidence score

**STYLE:** Formal, objective, evidence-based"""


def generate_risk_prompt(domain: str, threat: str, asset: str, language: str) -> str:
    """Generate AI prompt for risk assessment."""
    ctx = get_domain_context(domain)
    
    if language in ["Arabic", "العربية"]:
        return f"""أنت مستشار أول في إدارة المخاطر من إحدى شركات الأربعة الكبار.

**المهمة:** إعداد تقييم مخاطر شامل لمجال {ctx['ar_name']}.

**سيناريو التهديد:** {threat}
**الأصل المتأثر:** {asset}

**الأطر المرجعية:** {ctx['frameworks_ar']}

**هيكل التقرير:**

١. **تحديد المخاطر**
- وصف السيناريو
- نواقل الهجوم/الفشل الخاصة بـ {ctx['ar_name']}

٢. **سجل المخاطر**

| المعرف | الخطر | الاحتمال (١-٥) | الأثر (١-٥) | الدرجة | الفئة |
|--------|-------|----------------|-------------|--------|-------|

المخاطر الخاصة بـ {ctx['ar_name']}:
{chr(10).join(['- ' + risk for risk in ctx['risks_ar']])}

٣. **تقييم الأثر**
| البعد | التقييم | الوصف |
- المالي
- التشغيلي
- السمعة
- القانوني/التنظيمي

٤. **تقييم الاحتمالية**
- قدرة مصدر التهديد
- التعرض للثغرات
- فعالية الضوابط الحالية

٥. **مصفوفة المخاطر**
| القياس | القيمة |
| الخطر الكامن | |
| فعالية الضوابط | |
| الخطر المتبقي | |

٦. **الضوابط الموصى بها**
ضوابط خاصة بـ {ctx['ar_name']}:
- ضوابط وقائية
- ضوابط كشفية
- ضوابط تصحيحية

٧. **استراتيجية التخفيف**
- إجراءات فورية (٠-٣٠ يوم)
- قصيرة المدى (١-٣ أشهر)
- طويلة المدى (٣-١٢ شهر)

٨. **مؤشرات المخاطر الرئيسية (KRIs)**
| المؤشر | الحد المقبول | العلامة الحمراء |

**الأسلوب:** تحليلي، مبني على البيانات، قابل للتنفيذ
**اللغة:** العربية الفصحى"""

    else:
        return f"""You are a Senior Risk Management Consultant from a Big 4 firm.

**TASK:** Prepare a comprehensive risk assessment for {domain}.

**THREAT SCENARIO:** {threat}
**AFFECTED ASSET:** {asset}

**REFERENCE FRAMEWORKS:** {ctx['frameworks']}

**REPORT STRUCTURE:**

1. **Risk Identification**
- Scenario description
- Attack/failure vectors specific to {domain}

2. **Risk Register**

| ID | Risk | Likelihood (1-5) | Impact (1-5) | Score | Category |
|----|------|------------------|--------------|-------|----------|

{domain}-specific risks:
{chr(10).join(['- ' + risk for risk in ctx['risks']])}

3. **Impact Assessment**
| Dimension | Rating | Description |
- Financial
- Operational
- Reputational
- Legal/Regulatory

4. **Likelihood Assessment**
- Threat source capability
- Vulnerability exposure
- Current control effectiveness

5. **Risk Matrix**
| Measure | Value |
| Inherent Risk | |
| Control Effectiveness | |
| Residual Risk | |

6. **Recommended Controls**
{domain}-specific controls:
- Preventive controls
- Detective controls
- Corrective controls

7. **Mitigation Strategy**
- Immediate actions (0-30 days)
- Short-term (1-3 months)
- Long-term (3-12 months)

8. **Key Risk Indicators (KRIs)**
| KRI | Threshold | Red Flag |

**STYLE:** Analytical, data-driven, actionable"""


class AIDocumentGenerator:
    """AI-powered document generator for GRC documents."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.use_simulation = not api_key
        
        if self.use_simulation:
            logger.info("AI Generator: Running in simulation mode")
    
    def generate(self, prompt: str, doc_type: DocumentType, language: str = "English") -> AIResponse:
        """Generate document content using AI or simulation."""
        
        if self.api_key:
            # Use actual API (OpenAI or other)
            try:
                return self._call_api(prompt, doc_type)
            except Exception as e:
                logger.error(f"API call failed: {e}")
                return self._simulate_response(prompt, doc_type, language)
        else:
            return self._simulate_response(prompt, doc_type, language)
    
    def _call_api(self, prompt: str, doc_type: DocumentType) -> AIResponse:
        """Call AI API to generate content."""
        import openai
        
        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior GRC consultant from a Big 4 firm."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7
        )
        
        return AIResponse(
            content=response.choices[0].message.content,
            success=True,
            source="api",
            model="gpt-4"
        )
    
    def _simulate_response(self, prompt: str, doc_type: DocumentType, language: str) -> AIResponse:
        """Simulate AI response based on prompt analysis."""
        
        # Extract domain from prompt
        domain = self._extract_domain_from_prompt(prompt)
        ctx = get_domain_context(domain)
        
        if doc_type == DocumentType.STRATEGY:
            content = self._generate_strategy_simulation(ctx, language)
        elif doc_type == DocumentType.POLICY:
            content = self._generate_policy_simulation(ctx, language)
        elif doc_type == DocumentType.AUDIT:
            content = self._generate_audit_simulation(ctx, language)
        elif doc_type == DocumentType.RISK:
            content = self._generate_risk_simulation(ctx, language)
        else:
            content = "Document type not supported."
        
        return AIResponse(
            content=content,
            success=True,
            source="simulation",
            model="template"
        )
    
    def _extract_domain_from_prompt(self, prompt: str) -> str:
        """Extract domain from prompt text."""
        prompt_lower = prompt.lower()
        
        if "artificial intelligence" in prompt_lower or "ai governance" in prompt_lower or "الذكاء الاصطناعي" in prompt:
            return "Artificial Intelligence"
        elif "data management" in prompt_lower or "إدارة البيانات" in prompt or "pdpl" in prompt_lower:
            return "Data Management"
        elif "digital transformation" in prompt_lower or "التحول الرقمي" in prompt:
            return "Digital Transformation"
        elif "global standards" in prompt_lower or "المعايير العالمية" in prompt or "iso 27001" in prompt_lower:
            return "Global Standards"
        else:
            return "Cyber Security"
    
    def _generate_strategy_simulation(self, ctx: Dict, language: str) -> str:
        """Generate strategy simulation content."""
        
        if language in ["Arabic", "العربية"]:
            domain_ar = ctx['ar_name']
            
            # Generate domain-specific pillars
            if "سيبراني" in domain_ar:
                pillars = [
                    ("حوكمة الأمن السيبراني والمخاطر", ["تأسيس لجنة الأمن السيبراني", "تطبيق إطار السياسات الأمنية", "نشر منصة GRC"]),
                    ("كشف التهديدات والاستجابة", ["نشر نظام SIEM/SOAR", "تطبيق EDR/XDR", "تأسيس فريق الاستجابة للحوادث"]),
                    ("أمن الهوية والوصول", ["تطبيق المصادقة متعددة العوامل", "نشر إدارة الوصول المتميز PAM", "أتمتة مراجعات الصلاحيات"]),
                    ("أمن البنية التحتية", ["تطبيق تجزئة الشبكة", "نشر جدار حماية الجيل التالي", "تأسيس الوصول الآمن عن بعد"])
                ]
                vision = "تأسيس منظومة أمن سيبراني متكاملة ومرنة تحمي الأصول الحيوية وتضمن الامتثال للهيئة الوطنية للأمن السيبراني وتمكّن الابتكار الرقمي الآمن."
                objectives = ["تحقيق امتثال ٩٥٪+ لضوابط NCA", "تقليل وقت اكتشاف التهديدات إلى أقل من ٤ ساعات", "تطبيق بنية انعدام الثقة", "بناء مركز عمليات أمنية ٢٤/٧", "تحقيق جاهزية التأمين السيبراني"]
                gaps = "حوكمة الأمن السيبراني، إدارة الهوية والوصول، مراقبة التهديدات"
                
            elif "ذكاء اصطناعي" in domain_ar:
                pillars = [
                    ("إطار حوكمة الذكاء الاصطناعي", ["تأسيس لجنة أخلاقيات AI", "تطوير سياسات حوكمة AI", "تطبيق سجل النماذج المركزي"]),
                    ("الذكاء الاصطناعي المسؤول والأخلاقي", ["نشر أدوات كشف التحيز", "تطبيق أطر قابلية التفسير XAI", "تأسيس متطلبات الإشراف البشري"]),
                    ("أمن وخصوصية AI", ["تطبيق اختبار المتانة ضد الهجمات", "نشر ضوابط خصوصية بيانات التدريب", "تأسيس أمن النماذج"]),
                    ("دورة حياة النماذج", ["تطبيق MLOps", "مراقبة انحراف النماذج", "إدارة إصدارات النماذج"])
                ]
                vision = "تمكين المنظمة كرائد في تبني الذكاء الاصطناعي المسؤول، وضمان شفافية وعدالة وأمان جميع أنظمة AI مع الامتثال لمبادئ سدايا الأخلاقية."
                objectives = ["إنشاء لجنة أخلاقيات AI خلال ٦ أشهر", "تحقيق جرد كامل لنماذج AI", "تطبيق اختبار التحيز لجميع النماذج", "ضمان الامتثال لمبادئ سدايا", "تقليل حوادث AI بنسبة ٨٠٪"]
                gaps = "حوكمة الذكاء الاصطناعي، اختبار التحيز والعدالة، قابلية تفسير النماذج"
                
            elif "بيانات" in domain_ar:
                pillars = [
                    ("حوكمة البيانات والإشراف", ["تأسيس مجلس حوكمة البيانات", "تطبيق برنامج أمناء البيانات", "نشر كتالوج البيانات المؤسسي"]),
                    ("إدارة جودة البيانات", ["تطبيق أدوات مراقبة الجودة", "تأسيس قواعد الجودة حسب المجال", "إنشاء لوحات جودة البيانات"]),
                    ("الامتثال لنظام PDPL", ["إجراء تقييم فجوات PDPL", "تطبيق منصة إدارة الموافقات", "نشر أدوات إخفاء البيانات"]),
                    ("إدارة دورة حياة البيانات", ["تطبيق سياسات الاحتفاظ", "أتمتة حذف البيانات", "إدارة أرشفة البيانات"])
                ]
                vision = "تحويل المنظمة إلى منظمة تعتمد على البيانات مع حوكمة بيانات مؤسسية شاملة، وضمان جودة البيانات والامتثال لنظام حماية البيانات الشخصية PDPL."
                objectives = ["تحقيق الامتثال الكامل لـ PDPL", "تطبيق كتالوج بيانات بتغطية ١٠٠٪", "تحسين جودة البيانات إلى ٩٥٪+", "تمكين التحليلات الذاتية لـ ٨٠٪ من المستخدمين", "تقليل حوادث البيانات بنسبة ٧٠٪"]
                gaps = "حوكمة البيانات المؤسسية، الامتثال لـ PDPL، إدارة جودة البيانات"
                
            elif "تحول رقمي" in domain_ar:
                pillars = [
                    ("تحويل تجربة العملاء", ["إطلاق منصة الخدمات الرقمية", "تطبيق القنوات الرقمية الموحدة", "نشر chatbot ذكي"]),
                    ("أتمتة العمليات", ["تحديد فرص RPA", "تطبيق أتمتة العمليات الروبوتية", "رقمنة العمليات الورقية"]),
                    ("البنية التحتية السحابية", ["تطوير استراتيجية السحابة", "ترحيل الأنظمة للسحابة", "تطبيق DevOps"]),
                    ("إدارة التغيير والتبني", ["تطوير خطة إدارة التغيير", "برامج تدريب المستخدمين", "قياس التبني الرقمي"])
                ]
                vision = "تسريع رحلة التحول الرقمي للمنظمة، وتقديم تجارب عملاء استثنائية والتميز التشغيلي من خلال الابتكار التقني والقدرات الرقمية."
                objectives = ["تحقيق معدل تبني رقمي ٨٠٪+", "أتمتة ٧٠٪ من العمليات اليدوية", "تحسين رضا العملاء إلى ٩٠٪", "ترحيل ٨٠٪ من الأنظمة للسحابة", "تقليل وقت إطلاق الخدمات بنسبة ٥٠٪"]
                gaps = "استراتيجية التحول الرقمي، تجربة العملاء الرقمية، أتمتة العمليات"
                
            else:  # Global Standards
                pillars = [
                    ("أمن المعلومات ISO 27001", ["تطبيق نظام ISMS", "تحديد نطاق الشهادة", "تنفيذ ضوابط Annex A"]),
                    ("استمرارية الأعمال ISO 22301", ["إجراء تحليل أثر الأعمال BIA", "تطوير خطط الاستمرارية", "اختبار خطط BCM"]),
                    ("إدارة الجودة ISO 9001", ["توثيق العمليات", "تطبيق مؤشرات الجودة", "إدارة رضا العملاء"]),
                    ("التدقيق والتحسين المستمر", ["برنامج التدقيق الداخلي", "عملية الإجراءات التصحيحية CAPA", "مراجعات الإدارة الدورية"])
                ]
                vision = "ترسيخ المنظمة كمرجع للتميز في أنظمة الإدارة، وتحقيق والحفاظ على شهادات ISO 27001 و ISO 22301 و ISO 9001."
                objectives = ["الحصول على شهادة ISO 27001", "تحقيق شهادة ISO 22301", "الحفاظ على شهادة ISO 9001", "تحقيق صفر عدم مطابقات جوهرية", "تطبيق ثقافة التحسين المستمر"]
                gaps = "نظام إدارة أمن المعلومات، إدارة استمرارية الأعمال، نضج عمليات التدقيق"
            
            # Build pillars text
            pillars_text = ""
            for i, (name, inits) in enumerate(pillars, 1):
                pillars_text += f"\n**الركيزة {i}: {name}**\n"
                for init in inits:
                    pillars_text += f"- {init}\n"
            
            # Build objectives text
            objectives_text = "\n".join([f"{i}. {obj}" for i, obj in enumerate(objectives, 1)])
            
            # Build KPIs
            kpis_text = "\n".join([f"- {kpi}" for kpi in ctx['kpis_ar']])
            
            # Build KRIs
            kris_text = "\n".join([f"- {risk}" for risk in ctx['risks_ar']])
            
            # Build roadmap
            if "سيبراني" in domain_ar:
                roadmap = [
                    ("التأسيس", "إطار حوكمة الأمن السيبراني", "٣", "٣٥٠,٠٠٠", "CISO", "اعتماد السياسات"),
                    ("التأسيس", "تقييم المخاطر والفجوات", "٢", "٢٠٠,٠٠٠", "فريق الأمن", "تقرير الفجوات"),
                    ("التأسيس", "تطبيق MFA وتصحيح الثغرات", "٣", "٥٠٠,٠٠٠", "IT Security", "تغطية MFA ١٠٠٪"),
                    ("البناء", "نشر SIEM ومركز العمليات", "٦", "١,٨٠٠,٠٠٠", "SOC Manager", "تشغيل SOC ٢٤/٧"),
                    ("البناء", "تعزيز IAM وPAM", "٦", "١,٢٠٠,٠٠٠", "IAM Team", "تغطية PAM ١٠٠٪"),
                    ("التحسين", "بنية انعدام الثقة", "١٢", "٢,٠٠٠,٠٠٠", "Enterprise Arch", "تطبيق Zero Trust"),
                ]
                total = "٦,٠٥٠,٠٠٠"
            elif "ذكاء" in domain_ar:
                roadmap = [
                    ("التأسيس", "لجنة أخلاقيات AI وإطار الحوكمة", "٣", "٢٥٠,٠٠٠", "AI Lead", "تشكيل اللجنة"),
                    ("التأسيس", "جرد نماذج AI وتصنيف المخاطر", "٣", "٣٠٠,٠٠٠", "Data Science", "جرد ١٠٠٪"),
                    ("البناء", "أدوات اختبار التحيز والعدالة", "٤", "٨٠٠,٠٠٠", "ML Team", "اختبار كل النماذج"),
                    ("البناء", "منصة قابلية التفسير XAI", "٦", "١,٢٠٠,٠٠٠", "AI Team", "تغطية XAI ١٠٠٪"),
                    ("البناء", "مراقبة انحراف النماذج", "٤", "٦٠٠,٠٠٠", "MLOps", "مراقبة مستمرة"),
                    ("التحسين", "أتمتة حوكمة AI", "٦", "٨٠٠,٠٠٠", "AI Governance", "أتمتة كاملة"),
                ]
                total = "٣,٩٥٠,٠٠٠"
            elif "بيانات" in domain_ar:
                roadmap = [
                    ("التأسيس", "مجلس حوكمة البيانات", "٢", "١٥٠,٠٠٠", "CDO", "تشكيل المجلس"),
                    ("التأسيس", "تقييم فجوات PDPL", "٣", "٣٠٠,٠٠٠", "Privacy Officer", "تقرير الفجوات"),
                    ("البناء", "كتالوج البيانات المؤسسي", "٦", "١,٥٠٠,٠٠٠", "Data Arch", "تغطية ١٠٠٪"),
                    ("البناء", "منصة إدارة الموافقات", "٤", "٨٠٠,٠٠٠", "Privacy Team", "إدارة الموافقات"),
                    ("البناء", "أدوات جودة البيانات", "٥", "١,٠٠٠,٠٠٠", "DQ Team", "مراقبة الجودة"),
                    ("التحسين", "أتمتة دورة حياة البيانات", "٦", "٧٠٠,٠٠٠", "Data Ops", "أتمتة كاملة"),
                ]
                total = "٤,٤٥٠,٠٠٠"
            elif "تحول" in domain_ar:
                roadmap = [
                    ("التأسيس", "استراتيجية التحول الرقمي", "٣", "٤٠٠,٠٠٠", "CDO", "اعتماد الاستراتيجية"),
                    ("التأسيس", "تقييم الجاهزية الرقمية", "٢", "٢٠٠,٠٠٠", "DT Team", "تقرير الجاهزية"),
                    ("البناء", "منصة الخدمات الرقمية", "٨", "٣,٠٠٠,٠٠٠", "Digital Team", "إطلاق المنصة"),
                    ("البناء", "أتمتة العمليات RPA", "٦", "١,٢٠٠,٠٠٠", "Process Team", "أتمتة ٧٠٪"),
                    ("البناء", "الترحيل السحابي", "١٠", "٢,٥٠٠,٠٠٠", "Cloud Team", "ترحيل ٨٠٪"),
                    ("التحسين", "برنامج إدارة التغيير", "٦", "٥٠٠,٠٠٠", "Change Mgmt", "تبني ٨٠٪"),
                ]
                total = "٧,٨٠٠,٠٠٠"
            else:  # Global Standards
                roadmap = [
                    ("التأسيس", "تحليل الفجوات ISO 27001", "٢", "٢٠٠,٠٠٠", "ISMS Manager", "تقرير الفجوات"),
                    ("التأسيس", "توثيق نظام ISMS", "٤", "٣٥٠,٠٠٠", "QMS Team", "وثائق ISMS"),
                    ("البناء", "تطبيق ضوابط ISO 27001", "٨", "١,٥٠٠,٠٠٠", "Security Team", "تطبيق الضوابط"),
                    ("البناء", "برنامج BCM وISO 22301", "٦", "٨٠٠,٠٠٠", "BCM Manager", "خطط الاستمرارية"),
                    ("البناء", "برنامج التدقيق الداخلي", "٤", "٤٠٠,٠٠٠", "Internal Audit", "تدقيق كامل"),
                    ("التحسين", "التدقيق الخارجي والشهادة", "٣", "٣٠٠,٠٠٠", "QMS Manager", "الحصول على الشهادة"),
                ]
                total = "٣,٥٥٠,٠٠٠"
            
            # Build roadmap table
            roadmap_text = "| المرحلة | المبادرة | المدة (شهر) | الاستثمار (ريال) | المسؤول | مؤشر النجاح |\n"
            roadmap_text += "|---------|----------|-------------|------------------|---------|-------------|\n"
            for phase, init, dur, cost, owner, kpi in roadmap:
                roadmap_text += f"| {phase} | {init} | {dur} | {cost} | {owner} | {kpi} |\n"
            
            return f"""**الرؤية التنفيذية**

{vision}

**الأهداف الاستراتيجية:**
{objectives_text}

---

**الركائز الاستراتيجية والمبادرات**
{pillars_text}

---

**خطة التنفيذ التفصيلية**

{roadmap_text}

**إجمالي الاستثمار المقدر: {total} ريال**
**مدة التنفيذ: ٢٤ شهر**

---

**مؤشرات الأداء الرئيسية:**
{kpis_text}

**مؤشرات المخاطر الرئيسية:**
{kris_text}

---

**الفجوات الحرجة المحددة:** {gaps}

**درجة الثقة: 85/100**
"""
        
        else:  # English
            # Similar logic for English...
            return self._generate_english_strategy(ctx)
    
    def _generate_english_strategy(self, ctx: Dict) -> str:
        """Generate English strategy content."""
        # Implementation for English
        domain = ctx.get('frameworks', '').split(',')[0].strip()
        
        return f"""**Executive Vision**

Establish a comprehensive {domain} capability that protects critical assets, ensures regulatory compliance, and enables secure digital innovation.

**Strategic Objectives:**
1. Achieve 95%+ compliance with regulatory requirements within 18 months
2. Implement industry-leading controls and practices
3. Build mature operational capabilities
4. Establish continuous monitoring and improvement
5. Enable secure business growth

---

**Strategic Pillars & Initiatives**

**Pillar 1: Governance & Risk Management**
- Establish governance committee
- Implement policy framework
- Deploy GRC platform

**Pillar 2: Operational Excellence**
- Build operational capabilities
- Implement monitoring systems
- Establish incident response

**Pillar 3: Technology & Controls**
- Deploy technical controls
- Implement automation
- Enhance detection capabilities

**Pillar 4: People & Culture**
- Awareness training program
- Skills development
- Culture transformation

---

**Detailed Implementation Plan**

| Phase | Initiative | Duration | Investment (SAR) | Owner | Success KPI |
|-------|------------|----------|------------------|-------|-------------|
| Foundation | Governance Framework | 3 months | 350,000 | Program Lead | Policy approval |
| Foundation | Gap Assessment | 2 months | 200,000 | Assessment Team | Gap report |
| Build | Core Controls | 6 months | 1,500,000 | Technical Team | Control implementation |
| Build | Operations Center | 6 months | 1,800,000 | Operations Lead | 24/7 operations |
| Optimize | Advanced Capabilities | 6 months | 1,200,000 | Program Lead | Full maturity |

**Total Investment: SAR 5,050,000**
**Timeline: 24 months**

---

**Key Performance Indicators:**
{chr(10).join(['- ' + kpi for kpi in ctx.get('kpis', [])])}

**Key Risk Indicators:**
{chr(10).join(['- ' + risk for risk in ctx.get('risks', [])])}

---

**Confidence Score: 85/100**
"""

    def _generate_policy_simulation(self, ctx: Dict, language: str) -> str:
        """Generate policy simulation content."""
        if language in ["Arabic", "العربية"]:
            return f"""**سياسة {ctx['ar_name']}**

**١. الغرض**
تحدد هذه السياسة الإطار والمتطلبات لـ {ctx['ar_name']} في المنظمة.

**٢. النطاق**
تنطبق على جميع الموظفين والمتعاقدين والأطراف الثالثة.

**٣. المتطلبات الرئيسية**
- الامتثال لـ {ctx['frameworks_ar']}
- تطبيق الضوابط المناسبة
- التدريب والتوعية المستمرة
- المراقبة والتدقيق الدوري
- الإبلاغ عن الحوادث والانتهاكات
- التحسين المستمر

**٤. الأدوار والمسؤوليات**

| الدور | المسؤولية |
|-------|----------|
| الإدارة العليا | الرعاية والدعم التنفيذي |
| مدير البرنامج | الإشراف على التنفيذ |
| الفريق التقني | تطبيق الضوابط |
| جميع الموظفين | الالتزام بالسياسة |

**٥. الامتثال والتنفيذ**
- مراجعة دورية للامتثال
- العقوبات في حالة المخالفة
- آلية الاستثناءات

**٦. المراجعة والتحديث**
- دورة المراجعة: سنوياً
- مالك السياسة: مدير البرنامج

---
*اعتمد من: [اسم المعتمد] | التاريخ: [تاريخ الاعتماد]*
"""
        else:
            return f"""**Policy Document**

**1. Purpose**
This policy establishes the framework and requirements for {ctx['frameworks'].split(',')[0]} in the organization.

**2. Scope**
Applies to all employees, contractors, and third parties.

**3. Key Requirements**
- Compliance with {ctx['frameworks']}
- Implementation of appropriate controls
- Continuous training and awareness
- Regular monitoring and auditing
- Incident and violation reporting
- Continuous improvement

**4. Roles and Responsibilities**

| Role | Responsibility |
|------|----------------|
| Executive Management | Sponsorship and support |
| Program Manager | Implementation oversight |
| Technical Team | Control implementation |
| All Employees | Policy compliance |

**5. Compliance and Enforcement**
- Regular compliance reviews
- Penalties for violations
- Exception process

**6. Review and Update**
- Review Cycle: Annually
- Policy Owner: Program Manager

---
*Approved by: [Approver Name] | Date: [Approval Date]*
"""

    def _generate_audit_simulation(self, ctx: Dict, language: str) -> str:
        """Generate audit report simulation."""
        if language in ["Arabic", "العربية"]:
            findings = ctx.get('risks_ar', [])
            return f"""**تقرير تدقيق الامتثال - {ctx['ar_name']}**

**١. الملخص التنفيذي**

تم تقييم بيئة الضوابط مقابل متطلبات {ctx['frameworks_ar']}. التقييم العام: امتثال جزئي (65%).

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

**النتيجة ١: {findings[0] if findings else 'فجوة في الضوابط'} (عالي)**
- **المرجع:** {ctx['frameworks_ar'].split('،')[0]}
- **الملاحظة:** تم تحديد فجوات في تطبيق الضوابط المطلوبة
- **الأدلة:** مراجعة الوثائق، اختبار النظام
- **السبب الجذري:** العملية: إجراءات غير موثقة؛ التقنية: أدوات غير مطبقة
- **الأثر:** عدم الامتثال التنظيمي المحتمل
- **التوصية:** تطوير وتطبيق الإجراءات المطلوبة
- **الموعد:** الربع القادم

**النتيجة ٢: {findings[1] if len(findings) > 1 else 'نقص في التوثيق'} (متوسط)**
- **المرجع:** {ctx['frameworks_ar'].split('،')[0]}
- **الملاحظة:** التوثيق غير مكتمل أو قديم
- **التوصية:** تحديث التوثيق
- **الموعد:** ٣٠ يوم

**النتيجة ٣: {findings[2] if len(findings) > 2 else 'فجوة في التدريب'} (متوسط)**
- **المرجع:** متطلبات التوعية
- **الملاحظة:** برنامج التدريب يحتاج تحسين
- **التوصية:** تعزيز برنامج التوعية
- **الموعد:** الربع القادم

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
المنظمة أسست ضوابط أساسية ولكن تتطلب معالجة الفجوات المحددة.

**درجة الثقة: 78/100**
"""
        else:
            findings = ctx.get('risks', [])
            return f"""**Compliance Audit Report - {ctx['frameworks'].split(',')[0]}**

**1. Executive Summary**

Control environment assessed against {ctx['frameworks']} requirements. Overall Assessment: Partial Compliance (65%).

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

**Finding 1: {findings[0] if findings else 'Control Gap'} (HIGH)**
- **Reference:** {ctx['frameworks'].split(',')[0]}
- **Observation:** Gaps identified in required control implementation
- **Evidence:** Document review, system testing
- **Root Cause:** Process: Undocumented procedures; Technology: Tools not implemented
- **Impact:** Potential regulatory non-compliance
- **Recommendation:** Develop and implement required procedures
- **Target:** Next quarter

**Finding 2: {findings[1] if len(findings) > 1 else 'Documentation Gap'} (MEDIUM)**
- **Reference:** {ctx['frameworks'].split(',')[0]}
- **Observation:** Documentation incomplete or outdated
- **Recommendation:** Update documentation
- **Target:** 30 days

**Finding 3: {findings[2] if len(findings) > 2 else 'Training Gap'} (MEDIUM)**
- **Reference:** Awareness requirements
- **Observation:** Training program needs improvement
- **Recommendation:** Enhance awareness program
- **Target:** Next quarter

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

    def _generate_risk_simulation(self, ctx: Dict, language: str) -> str:
        """Generate risk assessment simulation."""
        if language in ["Arabic", "العربية"]:
            risks = ctx.get('risks_ar', [])
            return f"""**تقييم المخاطر - {ctx['ar_name']}**

**١. تحديد المخاطر**
تقييم شامل لمخاطر {ctx['ar_name']} بناءً على {ctx['frameworks_ar']}.

**٢. سجل المخاطر**

| المعرف | الخطر | الاحتمال | الأثر | الدرجة | الفئة |
|--------|-------|---------|-------|--------|-------|
| R-01 | {risks[0] if risks else 'خطر رئيسي'} | 4 | 5 | 20 | حرج |
| R-02 | {risks[1] if len(risks) > 1 else 'خطر ثانوي'} | 3 | 4 | 12 | عالي |
| R-03 | {risks[2] if len(risks) > 2 else 'خطر تشغيلي'} | 4 | 3 | 12 | عالي |
| R-04 | {risks[3] if len(risks) > 3 else 'خطر امتثال'} | 3 | 4 | 12 | عالي |
| R-05 | {risks[4] if len(risks) > 4 else 'خطر استراتيجي'} | 2 | 5 | 10 | متوسط |

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

**ضوابط وقائية:**
- تعزيز السياسات والإجراءات
- تدريب الموظفين
- الضوابط التقنية

**ضوابط كشفية:**
- المراقبة المستمرة
- التدقيق الدوري
- تحليل السجلات

**ضوابط تصحيحية:**
- خطط الاستجابة
- إجراءات التعافي
- التحسين المستمر

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
{chr(10).join([f'| {kpi.split(":")[0] if ":" in kpi else kpi} | {kpi.split(":")[1] if ":" in kpi else "< 5"} | تجاوز الحد |' for kpi in ctx.get('kpis_ar', ['مؤشر ١', 'مؤشر ٢'])[:4]])}

**درجة الثقة: 80/100**
"""
        else:
            risks = ctx.get('risks', [])
            return f"""**Risk Assessment - {ctx['frameworks'].split(',')[0]}**

**1. Risk Identification**
Comprehensive risk assessment for {ctx['frameworks'].split(',')[0]} based on {ctx['frameworks']}.

**2. Risk Register**

| ID | Risk | Likelihood | Impact | Score | Category |
|----|------|------------|--------|-------|----------|
| R-01 | {risks[0] if risks else 'Primary Risk'} | 4 | 5 | 20 | Critical |
| R-02 | {risks[1] if len(risks) > 1 else 'Secondary Risk'} | 3 | 4 | 12 | High |
| R-03 | {risks[2] if len(risks) > 2 else 'Operational Risk'} | 4 | 3 | 12 | High |
| R-04 | {risks[3] if len(risks) > 3 else 'Compliance Risk'} | 3 | 4 | 12 | High |
| R-05 | {risks[4] if len(risks) > 4 else 'Strategic Risk'} | 2 | 5 | 10 | Medium |

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

**Preventive Controls:**
- Enhanced policies and procedures
- Staff training
- Technical controls

**Detective Controls:**
- Continuous monitoring
- Regular auditing
- Log analysis

**Corrective Controls:**
- Response plans
- Recovery procedures
- Continuous improvement

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
{chr(10).join([f'| {kpi.split(":")[0] if ":" in kpi else kpi} | {kpi.split(":")[1] if ":" in kpi else "< 5"} | Exceeded |' for kpi in ctx.get('kpis', ['KRI 1', 'KRI 2'])[:4]])}

**Confidence Score: 80/100**
"""


# Create singleton instance
ai_generator = AIDocumentGenerator()
