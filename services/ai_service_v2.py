"""
Sentinel GRC - AI Service
Unified AI service with Big4-level strategy generation and domain-specific analysis.
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

# =============================================================================
# BENCHMARK DATA IMPORT
# =============================================================================
try:
    from data.benchmarks import get_benchmark_comparison, get_sector_benchmark, get_all_sources
    HAS_BENCHMARKS = True
    logger.info("Benchmark data module loaded successfully")
except ImportError:
    HAS_BENCHMARKS = False
    logger.warning("Benchmark data module not available, using estimates")
    
    def get_benchmark_comparison(domain, sector, score):
        return {"industry_average": 55, "top_quartile": 75, "gap_to_average": 55 - score}
    
    def get_sector_benchmark(domain, sector):
        return {"average": 55, "top_quartile": 75, "source": "Industry estimates"}

# =============================================================================
# ENSURE .env IS LOADED
# =============================================================================
try:
    from dotenv import load_dotenv
    
    _possible_paths = [
        Path(__file__).parent.parent / ".env",
        Path.cwd() / ".env",
        Path(__file__).parent / ".env",
    ]
    
    for _env_path in _possible_paths:
        if _env_path.exists():
            load_dotenv(_env_path)
            logger.info(f"AI Service: Loaded .env from {_env_path}")
            break
except ImportError:
    logger.warning("python-dotenv not installed")


class ResponseType(Enum):
    """Types of AI responses for mock fallback."""
    STRATEGY = "strategy"
    POLICY = "policy"
    AUDIT = "audit"
    RISK = "risk"
    GENERAL = "general"


@dataclass
class AIResponse:
    """Structured AI response."""
    content: str
    success: bool
    source: str
    model: str
    error: Optional[str] = None


class AIService:
    """
    Unified AI service with OpenAI integration and Big4-level output quality.
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4-turbo"
        self.fallback_delay = 1.5
        self._client = None
        self._initialized = False
        
        if self.api_key:
            masked_key = self.api_key[:8] + "..." + self.api_key[-4:] if len(self.api_key) > 12 else "***"
            logger.info(f"AI Service: API key found ({masked_key})")
        else:
            logger.warning("AI Service: No OPENAI_API_KEY found")
    
    def reload_api_key(self):
        """Reload API key from environment."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._client = None
        self._initialized = False
        return self.api_key is not None
    
    @property
    def client(self):
        """Lazy initialization of OpenAI client."""
        if not self._initialized:
            self._initialized = True
            if not self.api_key:
                self.api_key = os.getenv("OPENAI_API_KEY")
            
            if self.api_key:
                try:
                    import openai
                    self._client = openai.OpenAI(api_key=self.api_key)
                    logger.info("OpenAI client initialized successfully")
                except ImportError:
                    logger.warning("openai package not installed")
                    self._client = None
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI client: {e}")
                    self._client = None
        return self._client
    
    @property
    def is_available(self) -> bool:
        """Check if AI service is available."""
        return self.client is not None
    
    def generate(
        self,
        prompt: str,
        response_type: ResponseType = ResponseType.GENERAL,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        language: str = "English"
    ) -> AIResponse:
        """Generate AI response with fallback support and language-specific system message."""
        
        # Language-specific system messages
        if language in ["Arabic", "العربية"]:
            system_message = """أنت مستشار إداري أول من إحدى شركات الاستشارات الأربعة الكبرى (ديلويت، برايس ووترهاوس كوبرز، إرنست آند يونغ، كي بي إم جي) متخصص في الحوكمة والمخاطر والامتثال والأمن السيبراني والتحول الرقمي.

تعليمات صارمة وملزمة:
- اكتب جميع المخرجات باللغة العربية الفصحى فقط
- ممنوع منعاً باتاً استخدام أي كلمة أو مصطلح أو اختصار باللغة الإنجليزية
- استخدم المصطلحات العربية الرسمية المعتمدة في المملكة العربية السعودية
- استخدم الأرقام العربية (١، ٢، ٣) بدلاً من (1, 2, 3)
- جميع العناوين والجداول والمحتوى يجب أن تكون بالعربية فقط"""
        elif language in ["Bilingual", "ثنائي اللغة"]:
            system_message = """You are a senior management consultant from a Big 4 firm specializing in GRC, cybersecurity, and digital transformation.

CRITICAL BILINGUAL INSTRUCTION:
- For EVERY paragraph, sentence, and bullet point: write English FIRST, then Arabic translation IMMEDIATELY after
- Format: **English:** [content] followed by **العربية:** [Arabic translation]
- Both languages must have EQUAL content - no skipping translations
- Tables must have bilingual headers"""
        else:
            system_message = "You are an elite management consultant from a Big 4 firm (Deloitte/PwC/EY/KPMG) specializing in GRC, cybersecurity, and digital transformation strategy."
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                content = response.choices[0].message.content
                
                return AIResponse(
                    content=content,
                    success=True,
                    source="api",
                    model=self.model
                )
                
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"AI API error: {error_msg}")
                return self._get_fallback_response(response_type, error_msg, language)
        
        logger.info("No API key available, using fallback response")
        return self._get_fallback_response(response_type, language=language)
    
    def _get_fallback_response(
        self,
        response_type: ResponseType,
        error: str = None,
        language: str = "English",
        context: Dict[str, Any] = None
    ) -> AIResponse:
        """Get a mock fallback response based on language with dynamic benchmarks."""
        time.sleep(self.fallback_delay)
        
        # Use dynamic generator if context available, otherwise use static
        if context and response_type == ResponseType.STRATEGY:
            content = self._generate_dynamic_strategy_fallback(context, language)
        elif language in ["Arabic", "العربية"]:
            content = MOCK_RESPONSES_ARABIC.get(response_type, MOCK_RESPONSES_ARABIC[ResponseType.GENERAL])
        else:
            content = MOCK_RESPONSES.get(response_type, MOCK_RESPONSES[ResponseType.GENERAL])
        
        return AIResponse(
            content=content,
            success=True,
            source="fallback",
            model="simulation",
            error=error
        )
    
    def _generate_dynamic_strategy_fallback(self, context: Dict[str, Any], language: str) -> str:
        """Generate dynamic strategy fallback with real benchmark data."""
        domain = context.get('domain', 'Cyber Security')
        sector = context.get('sector', 'General')
        org_name = context.get('org_name', 'Organization')
        current_score = context.get('gap_data', {}).get('compliance_score', 45)
        
        # Get real benchmark data
        benchmark = get_sector_benchmark(domain, sector)
        industry_avg = benchmark.get('average', 55)
        top_quartile = benchmark.get('top_quartile', 75)
        saudi_avg = benchmark.get('saudi_average', industry_avg)
        source = benchmark.get('source', 'Industry reports')
        
        # Calculate gaps
        gap_to_avg = industry_avg - current_score
        gap_to_top = top_quartile - current_score
        
        # Confidence score based on data completeness
        confidence = 78 if context.get('tech') and context.get('challenges') else 72
        
        if language in ["Arabic", "العربية"]:
            return f"""نسعى لبناء منظومة متكاملة تحقق التميز المؤسسي وتضمن الامتثال الكامل للمتطلبات التنظيمية وتدعم النمو المستدام للأعمال.

الأهداف الاستراتيجية:
١. تحقيق نسبة امتثال ٩٥٪ للأطر التنظيمية المستهدفة خلال ١٨ شهر
٢. بناء إطار حوكمة مؤسسي متكامل مع مساءلة واضحة
٣. تقليل التعرض للمخاطر بنسبة ٤٠٪ من خلال تطبيق الضوابط الاستباقية
٤. بناء القدرات الداخلية لضمان التميز المستدام
٥. تمكين مبادرات التحول الرقمي الآمنة
|||
مستوى النضج الحالي: المرحلة الثانية (التطوير) - المستوى ٢ من ٥

**المقارنة المرجعية (المصدر: {source}):**
- النسبة الحالية للمنظمة: {current_score}٪
- متوسط قطاع {sector}: {industry_avg}٪
- الربع الأعلى أداءً: {top_quartile}٪
- متوسط المملكة العربية السعودية: {saudi_avg}٪
- الفجوة عن المتوسط: {gap_to_avg}٪

الفجوات الحرجة المكتشفة:
- الحوكمة: إطار السياسات موجود لكن آليات التطبيق والقياس غير ناضجة
- إدارة المخاطر: نهج تفاعلي بدون منهجية تقييم مخاطر منظمة
- الضوابط التقنية: حلول منفصلة منشورة بدون بنية متكاملة
- المراقبة: رؤية محدودة للأحداث الأمنية وحالة الامتثال
- مخاطر الأطراف الثالثة: تقييمات موردين عشوائية بدون برنامج موحد
|||
الركيزة الأولى: التميز في الحوكمة
- تأسيس لجنة الحوكمة والمخاطر والامتثال برعاية تنفيذية
- تطبيق نظام إدارة دورة حياة السياسات
- نشر لوحة مراقبة الامتثال

الركيزة الثانية: الأمن المبني على المخاطر
- تطبيق إطار إدارة المخاطر المؤسسية
- نشر نظام المراقبة المستمرة للضوابط
- تحديد مستويات تقبل وتحمل المخاطر

الركيزة الثالثة: المرونة التشغيلية
- تعزيز قدرات الاستجابة للحوادث
- تطبيق برنامج استمرارية الأعمال
- تأسيس إطار إدارة الأزمات

الركيزة الرابعة: التمكين التقني
- نشر منصة حوكمة ومخاطر وامتثال متكاملة
- تطبيق الأتمتة الأمنية
- تأسيس معايير البنية الآمنة

الركيزة الخامسة: الكفاءات والثقافة
- إطلاق برنامج التوعية الأمنية
- بناء الخبرات الداخلية من خلال التدريب
- تأسيس شبكة سفراء الأمن
|||
| المرحلة | المبادرة | المدة (شهر) | الاستثمار (ريال) | المسؤول | مؤشر النجاح |
|---------|----------|-------------|------------------|---------|-------------|
| التأسيس | إطار الحوكمة | ٣ | ٣٥٠,٠٠٠ | مدير الحوكمة | تغطية السياسات ١٠٠٪ |
| التأسيس | تقييم المخاطر | ٢ | ٢٠٠,٠٠٠ | مدير المخاطر | تحديد المخاطر الحرجة |
| التأسيس | المكاسب السريعة | ٣ | ٥٠٠,٠٠٠ | مدير الأمن | إغلاق الفجوات الحرجة |
| البناء | تعزيز الهوية والوصول | ٦ | ١,٢٠٠,٠٠٠ | مدير الهوية | تغطية التحقق الثنائي ١٠٠٪ |
| البناء | نشر نظام المراقبة الأمنية | ٦ | ١,٨٠٠,٠٠٠ | مدير مركز العمليات | وقت الاكتشاف أقل من ٢٤ ساعة |
| البناء | برنامج مخاطر الأطراف الثالثة | ٤ | ٤٠٠,٠٠٠ | مدير مخاطر الموردين | تقييم الموردين الحرجين |
| البناء | برنامج التوعية | ٤ | ٣٠٠,٠٠٠ | الموارد البشرية والأمن | إكمال التدريب ٩٥٪ |
| التحسين | الأتمتة | ٦ | ٨٠٠,٠٠٠ | مهندس الأمن | تقليل الجهد اليدوي ٥٠٪ |
| التحسين | المراقبة المستمرة | ٦ | ٦٠٠,٠٠٠ | مدير الحوكمة | امتثال فوري |

إجمالي الاستثمار: ٦,٣٥٠,٠٠٠ ريال | المدة: ٢٤ شهر
|||
مؤشرات الأداء الرئيسية:
١. نسبة الامتثال: الهدف ٩٥٪ (الحالي: {current_score}٪)
٢. تغطية السياسات: الهدف ١٠٠٪ (الحالي: ٦٠٪)
٣. معالجة المخاطر: الهدف ٩٠٪ من المخاطر الحرجة
٤. الاستجابة للحوادث: أقل من ٤ ساعات
٥. إكمال التدريب: ٩٥٪ من الموظفين
٦. تقييم الموردين: ١٠٠٪ من الموردين الحرجين

مؤشرات المخاطر الرئيسية:
١. ملاحظات التدقيق المفتوحة: أقل من ٥ عالية الخطورة
٢. معالجات المخاطر المتأخرة: أقل من ١٠٪
٣. الحوادث الأمنية: أقل من ٢ حرجة/ربع سنوي
٤. استثناءات الامتثال: أقل من ٣٪

دورية الحوكمة:
- أسبوعياً: مراجعة المقاييس التشغيلية
- شهرياً: مراجعة لوحة الإدارة
- ربع سنوياً: تقارير اللجنة التنفيذية
- سنوياً: عرض مجلس الإدارة وتحديث الاستراتيجية
|||
**درجة الثقة: {confidence} من ١٠٠**

مصادر البيانات المرجعية: {source}

الافتراضات:
- توفر الرعاية التنفيذية واستمرارها
- اعتماد الميزانية كما هو مقدر
- توفر الموارد الرئيسية للتنفيذ
- عدم حدوث تغييرات تنظيمية كبيرة

المخاطر الرئيسية:
- قيود الموارد قد تؤثر على الجدول الزمني
- مقاومة التغيير في الفرق التشغيلية
- تعقيد تكامل التقنيات

الخطوات التالية الموصى بها:
١. الحصول على الرعاية التنفيذية واعتماد الميزانية
٢. تأسيس مكتب إدارة البرنامج
٣. إجراء تقييم تفصيلي للوضع الحالي
٤. تطوير خطط تنفيذ المرحلة الأولى
٥. بدء المكاسب السريعة لبناء الزخم"""
        
        else:  # English
            return f"""**Executive Vision**

To establish a world-class, resilient {domain} posture that enables digital trust, regulatory compliance, and sustainable business growth while positioning {org_name} as an industry leader in governance excellence.

**Strategic Objectives:**
1. Achieve 95%+ compliance with target frameworks within 18 months
2. Establish enterprise-wide governance operating model with clear accountability
3. Reduce risk exposure by 40% through proactive controls implementation
4. Build internal capabilities to sustain long-term excellence
5. Enable secure digital transformation initiatives
|||
**Current State Assessment**

**Maturity Level:** Developing (Level 2 of 5)

Based on our assessment, the organization demonstrates foundational capabilities but lacks the process maturity and control effectiveness required for target state compliance.

**Benchmark Comparison (Source: {source}):**
- **Current Organization Score:** {current_score}%
- **{sector} Industry Average:** {industry_avg}%
- **Top Quartile Performance:** {top_quartile}%
- **Saudi Arabia Average:** {saudi_avg}%
- **Gap to Industry Average:** {gap_to_avg}%
- **Gap to Top Quartile:** {gap_to_top}%

**Critical Gaps Identified:**
- Governance: Policy framework exists but enforcement and measurement mechanisms are immature
- Risk Management: Reactive approach without systematic risk assessment methodology
- Technical Controls: Point solutions deployed without integrated architecture
- Monitoring: Limited visibility into security events and compliance status
- Third-Party Risk: Ad-hoc vendor assessments without standardized program
|||
**Strategic Pillars & Initiatives**

**Pillar 1: Governance Excellence**
- Establish GRC Committee with executive sponsorship
- Implement policy lifecycle management
- Deploy compliance monitoring dashboard

**Pillar 2: Risk-Based Security**
- Implement enterprise risk management framework
- Deploy continuous control monitoring
- Establish risk appetite and tolerance thresholds

**Pillar 3: Operational Resilience**
- Enhance incident response capabilities
- Implement business continuity program
- Establish crisis management framework

**Pillar 4: Technology Enablement**
- Deploy integrated GRC platform
- Implement security automation
- Establish secure architecture standards

**Pillar 5: People & Culture**
- Launch security awareness program
- Build internal expertise through training
- Establish security champions network
|||
| Phase | Initiative | Duration (Months) | Investment (SAR) | Owner | Success KPI |
|-------|------------|-------------------|------------------|-------|-------------|
| Foundation | Governance Framework | 3 | 350,000 | GRC Lead | Policy coverage 100% |
| Foundation | Risk Assessment | 2 | 200,000 | Risk Manager | Critical risks identified |
| Foundation | Quick Wins Implementation | 3 | 500,000 | Security Lead | Critical gaps closed |
| Build | IAM Enhancement | 6 | 1,200,000 | IAM Lead | MFA coverage 100% |
| Build | SIEM Deployment | 6 | 1,800,000 | SOC Manager | MTTD < 24hrs |
| Build | TPRM Program | 4 | 400,000 | Vendor Risk | Critical vendors assessed |
| Build | Awareness Program | 4 | 300,000 | HR/Security | Training completion 95% |
| Optimize | Automation | 6 | 800,000 | Security Arch | Manual effort -50% |
| Optimize | Continuous Monitoring | 6 | 600,000 | GRC Lead | Real-time compliance |

**Total Investment: SAR 6,150,000 | Timeline: 24 months**
|||
**Key Performance Indicators (KPIs):**
1. Compliance Score: Target 95% (Current: {current_score}%)
2. Policy Coverage: Target 100% (Current: 60%)
3. Risk Treatment: Target 90% of critical risks mitigated
4. Incident Response: MTTR < 4 hours
5. Training Completion: 95% of employees
6. Vendor Assessment: 100% of critical vendors

**Key Risk Indicators (KRIs):**
1. Open Audit Findings: Threshold < 5 high-severity
2. Overdue Risk Treatments: Threshold < 10%
3. Security Incidents: Threshold < 2 critical/quarter
4. Compliance Exceptions: Threshold < 3%

**Governance Cadence:**
- Weekly: Operational metrics review
- Monthly: Management dashboard review
- Quarterly: Executive Committee reporting
- Annual: Board presentation and strategy refresh
|||
**Confidence Score: {confidence}/100**

**Benchmark Data Sources:** {source}

**Assumptions:**
- Executive sponsorship secured and sustained
- Budget approved as estimated
- Key resources available for implementation
- No major regulatory changes during implementation

**Key Risks:**
- Resource constraints may impact timeline
- Change resistance in operational teams
- Technology integration complexity

**Recommended Next Steps:**
1. Secure executive sponsorship and budget approval
2. Establish Program Management Office (PMO)
3. Conduct detailed current state assessment
4. Develop detailed implementation plans for Phase 1
5. Initiate quick wins to build momentum"""
    
    def generate_strategy(self, context: Dict[str, Any]) -> AIResponse:
        """Generate a Big4-level strategic roadmap."""
        prompt = self._build_strategy_prompt(context)
        language = context.get('language', 'English')
        response = self.generate(prompt, ResponseType.STRATEGY, max_tokens=4500, temperature=0.6, language=language)
        
        # Post-processing: If Arabic was requested but output contains significant English, use Arabic fallback
        if language in ["Arabic", "العربية"] and response.source == "api":
            english_indicators = ["Vision", "Strategy", "Objectives", "Executive", "Assessment", "Pillar", 
                                  "Initiative", "Roadmap", "Implementation", "KPI", "Confidence", "Score",
                                  "Phase", "Duration", "Cost", "Owner", "Current", "Target", "The ", " the ",
                                  "To ", " to ", "and ", " and", "with ", " with"]
            english_count = sum(1 for indicator in english_indicators if indicator in response.content)
            
            # If more than 5 English indicators found, the AI didn't follow Arabic instructions
            if english_count > 5:
                logger.warning(f"Arabic output contains {english_count} English indicators, using Arabic fallback")
                return self._get_fallback_response(ResponseType.STRATEGY, language=language, context=context)
        
        # If fallback was used without context, regenerate with context for dynamic benchmarks
        if response.source == "fallback":
            return self._get_fallback_response(ResponseType.STRATEGY, language=language, context=context)
        
        return response
    
    def generate_policy(
        self,
        policy_name: str,
        domain: str,
        framework: str,
        language: str = "English"
    ) -> AIResponse:
        """Generate a comprehensive policy document."""
        prompt = self._build_policy_prompt(policy_name, domain, framework, language)
        response = self.generate(prompt, ResponseType.POLICY, max_tokens=3500, temperature=0.5, language=language)
        
        # Post-processing: If Arabic was requested but output contains significant English, use Arabic fallback
        if language in ["Arabic", "العربية"] and response.source == "api":
            english_indicators = ["Policy", "Statement", "Scope", "Purpose", "Roles", "Responsibilities",
                                  "Compliance", "Requirements", "Review", "The ", " the ", "This ", " this ",
                                  "shall ", "must ", "will ", "should "]
            english_count = sum(1 for indicator in english_indicators if indicator in response.content)
            
            if english_count > 5:
                logger.warning(f"Arabic policy contains {english_count} English indicators, using Arabic fallback")
                return self._get_fallback_response(ResponseType.POLICY, language=language)
        
        return response
    
    def generate_audit_report(
        self,
        standard: str,
        evidence_text: str,
        language: str = "English"
    ) -> AIResponse:
        """Generate an audit report based on evidence with full language support."""
        max_evidence = 10000
        if len(evidence_text) > max_evidence:
            evidence_text = evidence_text[:max_evidence] + "\n[...truncated...]"
        
        if language in ["Arabic", "العربية"]:
            prompt = f"""
أنت مدقق رئيسي أول في إحدى شركات الأربعة الكبار (ديلويت/برايس ووترهاوس/إرنست آند يونغ/كي بي إم جي).

المعيار المرجعي: {standard}

راجع الأدلة التالية:
{evidence_text}

المطلوب: إعداد تقرير تدقيق احترافي شامل باللغة العربية.

هيكل التقرير المطلوب:

**1. الملخص التنفيذي**
- نظرة عامة على نطاق التدقيق
- أهم النتائج والاستنتاجات
- التقييم العام للامتثال
- التوصيات الرئيسية

**2. نطاق التدقيق والمنهجية**
- حدود التدقيق
- المعايير المستخدمة
- منهجية التقييم
- مصادر الأدلة

**3. النتائج الرئيسية**

**3.1 حالات عدم المطابقة الجوهرية (Major Non-Conformities)**
- الوصف التفصيلي
- الأثر المحتمل
- البند المرجعي من المعيار

**3.2 حالات عدم المطابقة البسيطة (Minor Non-Conformities)**
- الوصف
- التوصية

**3.3 الملاحظات وفرص التحسين**
- نقاط القوة
- مجالات التحسين

**4. مصفوفة تحليل الفجوات**
| البند | المتطلب | الوضع الحالي | الفجوة | الأولوية | التوصية |
|-------|---------|--------------|--------|----------|---------|

**5. التوصيات حسب الأولوية**
- توصيات عاجلة (خلال 30 يوم)
- توصيات قصيرة المدى (1-3 أشهر)
- توصيات متوسطة المدى (3-6 أشهر)

**6. خطة العمل الإدارية المقترحة**
| الإجراء | المسؤول | الموعد المستهدف | الموارد المطلوبة |
|---------|---------|-----------------|-----------------|

**7. الخلاصة والرأي**
- الرأي العام للمدقق
- مستوى الثقة
- الخطوات التالية

استخدم لغة رسمية ومهنية. كن موضوعياً ودقيقاً. اكتب التقرير كاملاً باللغة العربية.
"""
        elif language in ["Bilingual", "ثنائي اللغة"]:
            prompt = f"""
You are a Senior Lead Auditor from a Big 4 firm. | أنت مدقق رئيسي أول في إحدى شركات الأربعة الكبار.

STANDARD: {standard}
EVIDENCE REVIEW:
{evidence_text}

Generate a BILINGUAL audit report. For each section, write in English first, then Arabic translation.

**1. Executive Summary | الملخص التنفيذي**
[English content]
[Arabic translation]

**2. Scope & Methodology | نطاق التدقيق والمنهجية**
[Bilingual content]

**3. Key Findings | النتائج الرئيسية**
**3.1 Major Non-Conformities | حالات عدم المطابقة الجوهرية**
**3.2 Minor Non-Conformities | حالات عدم المطابقة البسيطة**
**3.3 Observations | الملاحظات**

**4. Gap Analysis Matrix | مصفوفة تحليل الفجوات**
[Bilingual table]

**5. Risk-Prioritized Recommendations | التوصيات حسب الأولوية**
[Bilingual content]

**6. Management Action Plan | خطة العمل الإدارية**
[Bilingual table]

**7. Conclusion & Opinion | الخلاصة والرأي**
[Bilingual conclusion]

Each section MUST have both English and Arabic content.
"""
        else:  # English
            prompt = f"""
You are a Senior Lead Auditor from a Big 4 firm (Deloitte/PwC/EY/KPMG).

STANDARD: {standard}

REVIEW THE FOLLOWING EVIDENCE:
{evidence_text}

Generate a comprehensive, professional audit report.

REQUIRED STRUCTURE:

**1. Executive Summary**
- Audit scope overview
- Key findings summary
- Overall compliance assessment
- Critical recommendations

**2. Scope & Methodology**
- Audit boundaries and limitations
- Standards and criteria used
- Assessment methodology
- Evidence sources reviewed

**3. Key Findings**

**3.1 Major Non-Conformities**
- Detailed description
- Potential impact
- Reference to standard clause
- Required corrective action

**3.2 Minor Non-Conformities**
- Description
- Recommendation

**3.3 Observations & Opportunities for Improvement**
- Strengths identified
- Areas for enhancement

**4. Gap Analysis Matrix**
| Clause | Requirement | Current State | Gap | Priority | Recommendation |
|--------|-------------|---------------|-----|----------|----------------|

**5. Risk-Prioritized Recommendations**
- Immediate actions (within 30 days)
- Short-term (1-3 months)
- Medium-term (3-6 months)

**6. Management Action Plan**
| Action | Owner | Target Date | Resources Required | Status |
|--------|-------|-------------|-------------------|--------|

**7. Conclusion & Opinion**
- Auditor's overall opinion
- Confidence level
- Next steps

TONE: Formal, authoritative, objective, professional.
"""
        response = self.generate(prompt, ResponseType.AUDIT, max_tokens=4000, language=language)
        
        # Post-processing: If Arabic was requested but output contains significant English, use Arabic fallback
        if language in ["Arabic", "العربية"] and response.source == "api":
            english_indicators = ["Executive", "Summary", "Scope", "Methodology", "Findings", "Analysis",
                                  "Recommendation", "Conclusion", "Opinion", "The ", " the ", "This ", " this "]
            english_count = sum(1 for indicator in english_indicators if indicator in response.content)
            
            if english_count > 5:
                logger.warning(f"Arabic audit contains {english_count} English indicators, using Arabic fallback")
                return self._get_fallback_response(ResponseType.AUDIT, language=language)
        
        return response
    
    def generate_risk_analysis(
        self,
        domain: str,
        threat: str,
        asset: str,
        context: Dict[str, Any] = None
    ) -> AIResponse:
        """Generate domain-specific risk analysis."""
        context = context or {}
        
        # Get domain-specific context
        domain_context = self._get_domain_risk_context(domain)
        
        prompt = f"""
أنت مستشار أول في إدارة المخاطر من إحدى شركات الأربعة الكبار. قدم تحليل مخاطر شامل.

ACT AS: Senior Risk Management Consultant from a Big 4 firm.
DOMAIN: {domain}
DOMAIN CONTEXT: {domain_context}
THREAT/RISK SCENARIO: {threat}
ASSET/SUBJECT: {asset}
ADDITIONAL CONTEXT: {context.get('notes', 'N/A')}
DEPLOYMENT/ENVIRONMENT: {context.get('deployment', 'N/A')}
EXISTING CONTROLS: {context.get('controls', 'N/A')}

PROVIDE ANALYSIS IN THIS FORMAT:

**1. Risk Identification (تحديد المخاطر)**
- Detailed description of the risk scenario
- Attack vectors / failure modes specific to {domain}
- Affected stakeholders and assets

**2. Impact Assessment (تقييم الأثر)**
- Business Impact (Financial, Operational, Reputational, Legal)
- Severity Rating: [Critical/High/Medium/Low]
- Potential loss scenarios with estimates

**3. Likelihood Assessment (تقييم الاحتمالية)**
- Threat actor motivation and capability (if applicable)
- Vulnerability exposure
- Historical incident data
- Probability Rating: [Very High/High/Medium/Low/Very Low]

**4. Risk Rating Matrix (مصفوفة تصنيف المخاطر)**
- Inherent Risk Score
- Current Control Effectiveness
- Residual Risk Score

**5. Mitigation Strategy (استراتيجية التخفيف)**
**Immediate Actions (0-30 days):**
- Quick wins and urgent controls

**Short-Term (1-3 months):**
- Process improvements
- Technical controls

**Long-Term (3-12 months):**
- Strategic initiatives
- Architecture changes

**6. Key Risk Indicators (KRIs) (مؤشرات المخاطر الرئيسية)**
- Specific metrics to monitor
- Thresholds and alerting criteria

**7. Control Recommendations (توصيات الضوابط)**
- Preventive controls
- Detective controls
- Corrective controls

IMPORTANT: Ensure all analysis is specific to the {domain} domain, not generic cybersecurity.
"""
        return self.generate(prompt, ResponseType.RISK)
    
    def _get_domain_risk_context(self, domain: str) -> str:
        """Get domain-specific risk context."""
        domain_lower = domain.lower()
        
        if "digital" in domain_lower or "transformation" in domain_lower:
            return """
            DOMAIN: Digital Transformation
            RISK CATEGORIES:
            - Program/Project Delivery Risk: Delays, cost overruns, scope creep
            - Technology Adoption Risk: Integration failures, legacy system compatibility
            - Change Management Risk: User resistance, skills gap, cultural barriers
            - Vendor/Partner Risk: Dependency, lock-in, service continuity
            - Business Model Disruption: Market changes, competitive pressure
            - Data Migration Risk: Loss, corruption, integrity issues
            - Regulatory Compliance Risk: New requirements from digital services
            - ROI/Value Realization Risk: Benefits not achieved
            
            FOCUS ON: Business outcomes, stakeholder adoption, technology integration, change management.
            DO NOT focus on cybersecurity threats - focus on transformation execution risks.
            """
        
        elif "global" in domain_lower or "standard" in domain_lower:
            return """
            DOMAIN: Global Standards & Quality Management
            RISK CATEGORIES:
            - Certification Risk: Audit failures, non-conformities, suspension
            - Process Compliance Risk: Procedure gaps, documentation issues
            - Continuous Improvement Risk: Stagnation, failure to address NCRs
            - Resource Competency Risk: Training gaps, qualification issues
            - Supplier/External Provider Risk: Non-conforming inputs
            - Customer Satisfaction Risk: Complaints, SLA breaches
            - Management System Integration Risk: Conflicting requirements
            - Regulatory Change Risk: New standards, updated requirements
            
            FOCUS ON: Management systems (ISO 9001, ISO 22301, ITIL), process maturity, audit readiness.
            DO NOT focus on cybersecurity threats - focus on quality and business continuity risks.
            """
        
        elif "ai" in domain_lower or "artificial" in domain_lower:
            return """
            DOMAIN: Artificial Intelligence Governance
            RISK CATEGORIES:
            - Model Performance Risk: Accuracy degradation, drift, hallucinations
            - Bias & Fairness Risk: Discriminatory outcomes, unfair treatment
            - Explainability Risk: Black-box decisions, regulatory non-compliance
            - Data Quality Risk: Training data issues, poisoning, privacy
            - Security Risk: Adversarial attacks, prompt injection, data leakage
            - Ethical Risk: Misuse, harmful outputs, societal impact
            - Regulatory Risk: AI Act compliance, liability, accountability
            - Operational Risk: Availability, latency, cost overruns
            
            FOCUS ON: Responsible AI, model governance, ethical considerations, AI-specific regulations.
            """
        
        elif "data" in domain_lower:
            return """
            DOMAIN: Data Management & Governance
            RISK CATEGORIES:
            - Data Quality Risk: Inaccuracy, incompleteness, inconsistency
            - Data Privacy Risk: PII exposure, consent violations, PDPL/GDPR
            - Data Governance Risk: Unclear ownership, poor stewardship
            - Data Architecture Risk: Silos, integration issues, technical debt
            - Master Data Risk: Duplicates, golden record issues
            - Metadata Risk: Poor documentation, lineage gaps
            - Data Retention Risk: Over-retention, premature deletion
            - Analytics/BI Risk: Misleading insights, decision errors
            
            FOCUS ON: Data quality, privacy compliance, governance frameworks, data lifecycle.
            """
        
        else:  # Cyber Security
            return """
            DOMAIN: Cybersecurity
            RISK CATEGORIES:
            - Threat Actor Risk: APT, ransomware, insider threats
            - Vulnerability Risk: Unpatched systems, misconfigurations
            - Identity & Access Risk: Credential theft, privilege abuse
            - Data Protection Risk: Breach, leakage, encryption failures
            - Network Security Risk: Lateral movement, perimeter breach
            - Application Security Risk: OWASP vulnerabilities, API abuse
            - Third-Party Risk: Supply chain, vendor compromise
            - Incident Response Risk: Detection gaps, slow response
            
            FOCUS ON: Technical threats, security controls, detection and response capabilities.
            """
    
    def _build_strategy_prompt(self, context: Dict[str, Any]) -> str:
        """Build a Big4-level strategy prompt with full language support."""
        org_name = context.get('org_name', 'Organization')
        sector = context.get('sector', 'Unknown')
        size = context.get('size', 'Medium')
        domain = context.get('domain', 'Cyber Security')
        frameworks = context.get('frameworks', [])
        tech = context.get('tech', '')
        challenges = context.get('challenges', '')
        budget = context.get('budget', 'Unknown')
        horizon = context.get('horizon', 36)
        language = context.get('language', 'English')
        gap_data = context.get('gap_data', {})
        
        # Get benchmark data for this domain and sector
        current_score = gap_data.get('compliance_score', 45)
        benchmark = get_sector_benchmark(domain, sector)
        industry_avg = benchmark.get('average', 55)
        top_quartile = benchmark.get('top_quartile', 75)
        saudi_avg = benchmark.get('saudi_average', industry_avg)
        benchmark_source = benchmark.get('source', 'Industry reports')
        
        # Domain translation for Arabic
        domain_ar = {
            "Cyber Security": "الأمن السيبراني",
            "AI Governance": "حوكمة الذكاء الاصطناعي", 
            "Data Management": "إدارة البيانات",
            "Digital Transformation": "التحول الرقمي",
            "Global Standards": "المعايير العالمية"
        }.get(domain, domain)
        
        # For Arabic - completely Arabic prompt with NO English whatsoever
        if language == "Arabic":
            return f"""أنت مستشار استراتيجي من شركة ماكنزي متخصص في {domain_ar}.

العميل: {org_name}
القطاع: {sector}
الحجم: {size}
الأطر التنظيمية: {', '.join(frameworks) if frameworks else 'أفضل الممارسات'}
التقنيات: {tech if tech else 'غير محدد'}
التحديات: {challenges if challenges else 'غير محدد'}
الميزانية: {budget}
المدة: {horizon} شهر

بيانات المقارنة المرجعية:
- النسبة الحالية المقدرة: {current_score}٪
- متوسط القطاع: {industry_avg}٪
- الربع الأعلى: {top_quartile}٪
- متوسط المملكة: {saudi_avg}٪

اكتب خارطة طريق استراتيجية كاملة باللغة العربية فقط.

القسم الأول ||| الرؤية والأهداف

اكتب رؤية استراتيجية ملهمة (جملتان أو ثلاث) ثم خمسة أهداف استراتيجية مرقمة بالأرقام العربية.

القسم الثاني ||| تقييم الوضع الحالي

اكتب تقييم لمستوى النضج الحالي والفجوات الرئيسية. قارن مع متوسط القطاع ({industry_avg}٪) والربع الأعلى ({top_quartile}٪).

القسم الثالث ||| الركائز والمبادرات

اكتب خمس ركائز استراتيجية مع مبادرتين أو ثلاث لكل ركيزة.

القسم الرابع ||| خارطة التنفيذ

اكتب جدول بهذا التنسيق:
| المرحلة | المبادرة | المدة | التكلفة | المسؤول | المؤشر |

القسم الخامس ||| المؤشرات

اكتب ستة مؤشرات أداء وأربعة مؤشرات مخاطر.

القسم السادس ||| الثقة

اكتب درجة الثقة والافتراضات والمخاطر والخطوات التالية.

مهم جداً:
- افصل بين الأقسام بـ |||
- اكتب بالعربية فقط
- لا تستخدم أي كلمة إنجليزية
- استخدم أرقام عربية مثل ١ ٢ ٣
- اكتب محتوى تفصيلي وليس عناوين فقط"""

        elif language == "Bilingual":
            return f"""You are a strategy consultant from McKinsey specializing in {domain}.

Client: {org_name} | Sector: {sector} | Size: {size}
Frameworks: {', '.join(frameworks) if frameworks else 'Best Practices'}
Technology: {tech if tech else 'Not specified'}
Challenges: {challenges if challenges else 'Not specified'}
Budget: {budget} | Timeline: {horizon} months

Generate a strategic roadmap in BILINGUAL format (English then Arabic for each paragraph).

SECTION 1 ||| Vision & Objectives

Write a vision statement and 5 objectives.
First in English, then translate to Arabic.

SECTION 2 ||| Current State Assessment

Write maturity assessment and gaps.
English first, then Arabic translation.

SECTION 3 ||| Strategic Pillars

Write 5 pillars with 2-3 initiatives each.
English first, then Arabic translation.

SECTION 4 ||| Implementation Roadmap

Create a table:
| Phase | Initiative | Duration | Cost (SAR) | Owner | KPI |

SECTION 5 ||| KPIs & KRIs

Write 6 KPIs and 4 KRIs.
English first, then Arabic translation.

SECTION 6 ||| Confidence Score

Write confidence score, assumptions, risks, next steps.
English first, then Arabic translation.

CRITICAL: 
- Separate sections with |||
- Every paragraph must have English THEN Arabic
- Format: [English text] then [Arabic translation]"""

        else:  # English
            return f"""You are a strategy consultant from McKinsey specializing in {domain}.

Client: {org_name}
Sector: {sector}
Size: {size}
Frameworks: {', '.join(frameworks) if frameworks else 'Best Practices'}
Technology: {tech if tech else 'Not specified'}
Challenges: {challenges if challenges else 'Not specified'}
Budget: {budget}
Timeline: {horizon} months

BENCHMARK DATA (Source: {benchmark_source}):
- Current Estimated Score: {current_score}%
- Industry Average ({sector}): {industry_avg}%
- Top Quartile: {top_quartile}%
- Saudi Market Average: {saudi_avg}%
- Gap to Average: {industry_avg - current_score}%

Generate a comprehensive strategic roadmap.

SECTION 1 ||| Executive Vision & Strategic Objectives

Write a compelling 2-3 sentence vision statement.
List 5 SMART strategic objectives with success criteria.

SECTION 2 ||| Current State Assessment

Assess current maturity level (1-5 scale).
Identify critical gaps prioritized by risk.
Compare against industry benchmarks:
- Current: {current_score}% vs Industry Average: {industry_avg}%
- Gap to top quartile: {top_quartile - current_score}%

SECTION 3 ||| Strategic Pillars & Initiatives

Define 5 strategic pillars.
For each pillar, list 2-3 specific initiatives with expected outcomes.

SECTION 4 ||| Implementation Roadmap

Create a markdown table:
| Phase | Initiative | Duration (Months) | Investment (SAR) | Owner | Success KPI |

Include 10-12 initiatives across Foundation/Build/Optimize phases.
Use realistic cost estimates for {size} organization.

SECTION 5 ||| Measuring Success (KPIs & KRIs)

List 6-8 Key Performance Indicators with targets.
List 4-6 Key Risk Indicators with thresholds.
Define governance and reporting cadence.

SECTION 6 ||| Confidence Score

Provide confidence score (0-100).
List key assumptions.
Identify risk factors.
Recommend next steps.

IMPORTANT:
- Separate sections with |||
- Be specific to {domain}, not generic
- Reference the benchmark data provided
- Each section should be 150-250 words
- Use professional consulting language"""
    
    def _build_policy_prompt(self, policy_name: str, domain: str, framework: str, language: str) -> str:
        """Build a comprehensive policy prompt with Arabic support."""
        
        if language in ["Arabic", "العربية"]:
            return f"""
أنت مستشار سياسات أول من إحدى شركات الأربعة الكبار. قم بصياغة سياسة احترافية شاملة.

المطلوب: صياغة سياسة "{policy_name}"
المجال: {domain}
الإطار المرجعي: {framework}

اكتب السياسة كاملة باللغة العربية الفصحى الرسمية المستخدمة في الوثائق الحكومية والمؤسسية في المملكة العربية السعودية.

هيكل السياسة المطلوب:

**1. بيان السياسة (Policy Statement)**
- الغرض والهدف من السياسة
- التزام الإدارة العليا

**2. النطاق والتطبيق (Scope & Applicability)**
- الأشخاص والأنظمة والعمليات المشمولة
- الاستثناءات إن وجدت

**3. التعريفات والمصطلحات (Definitions)**
- تعريف المصطلحات الفنية المستخدمة
- الاختصارات

**4. الأدوار والمسؤوليات (Roles & Responsibilities)**
- مسؤوليات الإدارة التنفيذية
- مسؤوليات مديري الإدارات
- مسؤوليات الموظفين
- مسؤوليات إدارة {domain}

**5. متطلبات السياسة (Policy Requirements)**
- المتطلبات التفصيلية مرقمة
- الضوابط والإجراءات
- معايير الامتثال

**6. الامتثال والإنفاذ (Compliance & Enforcement)**
- آلية مراقبة الامتثال
- العقوبات والإجراءات التأديبية
- إجراءات الإبلاغ عن المخالفات

**7. المراجعة والتحديث (Review & Updates)**
- دورة المراجعة
- مسؤولية التحديث
- إدارة التغيير

**8. الوثائق ذات العلاقة (Related Documents)**
- السياسات المرتبطة
- الإجراءات التفصيلية
- المعايير والأدلة

**9. سجل الإصدارات (Version History)**

استخدم لغة رسمية واضحة ومحددة. تجنب الغموض. اجعل المتطلبات قابلة للقياس والتدقيق.
"""
        else:
            lang_instruction = self._get_language_instruction(language)
            
            return f"""
ACT AS: Senior Policy Consultant from a Big 4 firm (Deloitte/PwC/EY/KPMG).

DELIVERABLE: Draft a comprehensive, board-ready policy document.

POLICY: {policy_name}
DOMAIN: {domain}
REFERENCE FRAMEWORK: {framework}
{lang_instruction}

POLICY STRUCTURE:

**1. Policy Statement**
- Purpose and objectives
- Management commitment
- Policy principles

**2. Scope & Applicability**
- In-scope personnel, systems, processes
- Exclusions with justification
- Geographic and organizational coverage

**3. Definitions & Terminology**
- Technical terms used in this policy
- Acronyms and abbreviations

**4. Roles & Responsibilities**
- Executive Management
- Department Heads
- {domain} Team
- All Employees
- Third Parties (if applicable)

**5. Policy Requirements**
- Numbered, specific requirements
- Controls and procedures
- Compliance criteria
- Technical standards

**6. Compliance & Enforcement**
- Monitoring mechanisms
- Non-compliance consequences
- Escalation procedures
- Exception handling process

**7. Review & Maintenance**
- Review frequency
- Change management
- Approval workflow

**8. Related Documents**
- Associated policies
- Procedures and guidelines
- Standards and frameworks

**9. Document Control**
- Version history table
- Approval signatures

QUALITY: Write in formal, precise language suitable for regulatory review. Make requirements measurable and auditable.
"""
    
    def _get_language_instruction(self, language: str) -> str:
        """Get language instruction for prompts."""
        if language in ["Bilingual", "ثنائي اللغة"]:
            return """
LANGUAGE: Bilingual (English & Arabic)
MANDATORY FORMAT: For EVERY paragraph and section:
1. Write the content in English first
2. Immediately follow with the Arabic translation

Example:
"This policy establishes the framework for..."
"تحدد هذه السياسة الإطار العام لـ..."

Ensure Arabic text is formal (فصحى) and uses standard Saudi government terminology.
"""
        elif language in ["Arabic", "العربية"]:
            return """
LANGUAGE: Arabic (اللغة العربية)
اكتب جميع المحتوى باللغة العربية الفصحى الرسمية.
استخدم المصطلحات المعتمدة في الجهات الحكومية السعودية.
تجنب الترجمة الحرفية - اكتب بأسلوب عربي أصيل.
"""
        return f"LANGUAGE: {language}. Write all content in {language}."
    
    def _get_section_titles(self, language: str) -> Dict[str, str]:
        """Get section titles based on language."""
        if language in ["Arabic", "العربية"]:
            return {
                "vision": "الرؤية التنفيذية والأهداف الاستراتيجية",
                "gaps": "تقييم الوضع الراهن (تحليل الفجوات)",
                "pillars": "الركائز الاستراتيجية والمبادرات",
                "roadmap": "خارطة طريق التنفيذ",
                "kpis": "قياس النجاح (مؤشرات الأداء والمخاطر)",
                "confidence": "درجة الثقة والتحقق"
            }
        elif language in ["Bilingual", "ثنائي اللغة"]:
            return {
                "vision": "Executive Vision & Strategic Objectives | الرؤية التنفيذية والأهداف الاستراتيجية",
                "gaps": "Current State Assessment | تقييم الوضع الراهن",
                "pillars": "Strategic Pillars & Initiatives | الركائز الاستراتيجية والمبادرات",
                "roadmap": "Implementation Roadmap | خارطة طريق التنفيذ",
                "kpis": "Measuring Success (KPIs & KRIs) | قياس النجاح",
                "confidence": "Confidence Score | درجة الثقة"
            }
        else:
            return {
                "vision": "Executive Vision & Strategic Objectives",
                "gaps": "Current State Assessment (Gap Analysis)",
                "pillars": "Strategic Pillars & Initiatives",
                "roadmap": "Implementation Roadmap",
                "kpis": "Measuring Success (KPIs & KRIs)",
                "confidence": "Confidence Score & Validation"
            }


# =============================================================================
# MOCK RESPONSES FOR FALLBACK - Language Specific
# =============================================================================

MOCK_RESPONSES_ARABIC = {
    ResponseType.STRATEGY: """
نسعى لبناء منظومة أمن سيبراني متكاملة تحقق التميز المؤسسي وتضمن الامتثال الكامل للمتطلبات التنظيمية وتدعم النمو المستدام للأعمال وتمكّن التحول الرقمي الآمن.

الأهداف الاستراتيجية:
١. تحقيق نسبة امتثال ٩٥٪ للأطر التنظيمية المستهدفة خلال ١٨ شهر
٢. بناء إطار حوكمة مؤسسي متكامل مع مساءلة واضحة
٣. تقليل التعرض للمخاطر بنسبة ٤٠٪ من خلال تطبيق الضوابط الاستباقية
٤. بناء القدرات الداخلية لضمان التميز المستدام
٥. تمكين مبادرات التحول الرقمي الآمنة
|||
مستوى النضج الحالي: المرحلة الثانية (التطوير) - المستوى ٢ من ٥

بناءً على تقييمنا، تُظهر المنظمة قدرات تأسيسية لكنها تفتقر إلى نضج العمليات وفعالية الضوابط المطلوبة للامتثال للحالة المستهدفة.

الفجوات الحرجة المكتشفة:
- الحوكمة: إطار السياسات موجود لكن آليات التطبيق والقياس غير ناضجة
- إدارة المخاطر: نهج تفاعلي بدون منهجية تقييم مخاطر منظمة
- الضوابط التقنية: حلول منفصلة منشورة بدون بنية متكاملة
- المراقبة: رؤية محدودة للأحداث الأمنية وحالة الامتثال
- مخاطر الأطراف الثالثة: تقييمات موردين عشوائية بدون برنامج موحد

المقارنة المرجعية: المنظمة تحقق ٤٥٪ مقارنة بمتوسط نظراء الصناعة البالغ ٦٨٪
|||
الركيزة الأولى: التميز في الحوكمة
- تأسيس لجنة الحوكمة والمخاطر والامتثال برعاية تنفيذية
- تطبيق نظام إدارة دورة حياة السياسات
- نشر لوحة مراقبة الامتثال

الركيزة الثانية: الأمن المبني على المخاطر
- تطبيق إطار إدارة المخاطر المؤسسية
- نشر نظام المراقبة المستمرة للضوابط
- تحديد مستويات تقبل وتحمل المخاطر

الركيزة الثالثة: المرونة التشغيلية
- تعزيز قدرات الاستجابة للحوادث
- تطبيق برنامج استمرارية الأعمال
- تأسيس إطار إدارة الأزمات

الركيزة الرابعة: التمكين التقني
- نشر منصة حوكمة ومخاطر وامتثال متكاملة
- تطبيق الأتمتة الأمنية
- تأسيس معايير البنية الآمنة

الركيزة الخامسة: الكفاءات والثقافة
- إطلاق برنامج التوعية الأمنية
- بناء الخبرات الداخلية من خلال التدريب
- تأسيس شبكة سفراء الأمن
|||
| المرحلة | المبادرة | المدة (شهر) | الاستثمار (ريال) | المسؤول | مؤشر النجاح |
|---------|----------|-------------|------------------|---------|-------------|
| التأسيس | إطار الحوكمة | ٣ | ٣٥٠,٠٠٠ | مدير الحوكمة | تغطية السياسات ١٠٠٪ |
| التأسيس | تقييم المخاطر | ٢ | ٢٠٠,٠٠٠ | مدير المخاطر | تحديد المخاطر الحرجة |
| التأسيس | المكاسب السريعة | ٣ | ٥٠٠,٠٠٠ | مدير الأمن | إغلاق الفجوات الحرجة |
| البناء | تعزيز الهوية والوصول | ٦ | ١,٢٠٠,٠٠٠ | مدير الهوية | تغطية التحقق الثنائي ١٠٠٪ |
| البناء | نشر نظام المراقبة الأمنية | ٦ | ١,٨٠٠,٠٠٠ | مدير مركز العمليات | وقت الاكتشاف أقل من ٢٤ ساعة |
| البناء | برنامج مخاطر الأطراف الثالثة | ٤ | ٤٠٠,٠٠٠ | مدير مخاطر الموردين | تقييم الموردين الحرجين |
| البناء | برنامج التوعية | ٤ | ٣٠٠,٠٠٠ | الموارد البشرية والأمن | إكمال التدريب ٩٥٪ |
| التحسين | الأتمتة | ٦ | ٨٠٠,٠٠٠ | مهندس الأمن | تقليل الجهد اليدوي ٥٠٪ |
| التحسين | المراقبة المستمرة | ٦ | ٦٠٠,٠٠٠ | مدير الحوكمة | امتثال فوري |
| التحسين | تقييم النضج | ٢ | ١٥٠,٠٠٠ | جهة خارجية | تحقيق النضج المستهدف |

إجمالي الاستثمار: ٦,٣٠٠,٠٠٠ ريال | المدة: ٢٤ شهر
|||
مؤشرات الأداء الرئيسية:
١. نسبة الامتثال: الهدف ٩٥٪ (الحالي: ٤٥٪)
٢. تغطية السياسات: الهدف ١٠٠٪ (الحالي: ٦٠٪)
٣. معالجة المخاطر: الهدف ٩٠٪ من المخاطر الحرجة
٤. الاستجابة للحوادث: متوسط وقت الحل أقل من ٤ ساعات
٥. إكمال التدريب: ٩٥٪ من الموظفين
٦. تقييم الموردين: ١٠٠٪ من الموردين الحرجين

مؤشرات المخاطر الرئيسية:
١. ملاحظات التدقيق المفتوحة: الحد الأقصى ٥ عالية الخطورة
٢. معالجات المخاطر المتأخرة: الحد الأقصى ١٠٪
٣. الحوادث الأمنية: الحد الأقصى ٢ حرجة لكل ربع سنة
٤. استثناءات الامتثال: الحد الأقصى ٣٪

دورية الحوكمة:
- أسبوعياً: مراجعة المقاييس التشغيلية
- شهرياً: مراجعة لوحة الإدارة
- ربع سنوياً: تقارير اللجنة التنفيذية
- سنوياً: عرض مجلس الإدارة وتحديث الاستراتيجية
|||
درجة الثقة الإجمالية: ٨٢ من ١٠٠

الافتراضات الرئيسية:
- توفر الرعاية التنفيذية واستمرارها طوال فترة التنفيذ
- اعتماد الميزانية كما هو مقدر
- توفر الموارد البشرية الرئيسية للتنفيذ
- عدم حدوث تغييرات تنظيمية كبيرة خلال فترة التنفيذ

المخاطر الرئيسية:
- قيود الموارد قد تؤثر على الجدول الزمني
- مقاومة التغيير في الفرق التشغيلية
- تعقيد تكامل التقنيات القائمة

الخطوات التالية الموصى بها:
١. الحصول على الرعاية التنفيذية واعتماد الميزانية
٢. تأسيس مكتب إدارة البرنامج
٣. إجراء تقييم تفصيلي للوضع الحالي
٤. تطوير خطط تنفيذ تفصيلية للمرحلة الأولى
٥. بدء المكاسب السريعة لبناء الزخم
""",

    ResponseType.POLICY: """
**١. بيان السياسة**

تلتزم المنظمة بحماية أصول المعلومات من جميع التهديدات الداخلية والخارجية، المتعمدة أو العرضية، لضمان استمرارية الأعمال وتقليل الأضرار والمخاطر.

**٢. النطاق والتطبيق**

تنطبق هذه السياسة على:
- جميع الموظفين بما في ذلك العاملين بدوام كامل وجزئي
- المقاولين والاستشاريين
- الأطراف الثالثة الذين يصلون إلى أنظمة ومعلومات المنظمة
- جميع الأنظمة والشبكات والبيانات المملوكة أو المدارة من قبل المنظمة

**٣. التعريفات والمصطلحات**

- **التحكم في الوصول:** التدابير الأمنية التي تنظم من يمكنه عرض أو استخدام الموارد
- **الوصول المتميز:** حقوق الوصول الإدارية أو المرتفعة
- **المصادقة متعددة العوامل:** المصادقة التي تتطلب طريقتين أو أكثر للتحقق

**٤. الأدوار والمسؤوليات**

- **أمن تقنية المعلومات:** تطبيق وصيانة أنظمة التحكم في الوصول
- **مالكو الأنظمة:** الموافقة على ومراجعة الوصول إلى أنظمتهم
- **المستخدمون:** حماية بيانات الاعتماد والإبلاغ عن الأنشطة المشبوهة
- **الموارد البشرية:** إخطار تقنية المعلومات بتغييرات حالة الموظفين

**٥. متطلبات السياسة**

٥.١ يجب منح الوصول على أساس "الحاجة للمعرفة" و"أقل الصلاحيات"
٥.٢ المصادقة متعددة العوامل إلزامية لجميع الوصول عن بعد والحسابات المتميزة
٥.٣ يجب مراجعة حقوق وصول المستخدمين ربع سنوياً من قبل مالكي البيانات/الأنظمة
٥.٤ يجب تسجيل ومراقبة جميع عمليات الوصول للأحداث الأمنية

**٦. الامتثال والإنفاذ**

- قد تؤدي المخالفات إلى إجراءات تأديبية تصل إلى إنهاء الخدمة
- سيتم إجراء عمليات تدقيق منتظمة لضمان الامتثال
- يجب الإبلاغ عن جميع الحوادث الأمنية خلال ٢٤ ساعة

**٧. المراجعة والتحديث**

تتم مراجعة هذه السياسة سنوياً أو عند حدوث تغييرات جوهرية في المنظمة أو مشهد التهديدات.

---
**درجة الثقة: ٨٥ من ١٠٠**

هذه السياسة مبنية على أفضل الممارسات الدولية والمتطلبات التنظيمية المحلية. يُنصح بمراجعة السياسة مع الإدارة القانونية والتنظيمية قبل الاعتماد النهائي.
""",

    ResponseType.AUDIT: """
**تقرير التدقيق: تقييم الامتثال**

**١. الملخص التنفيذي**

تشير مراجعة الأدلة المقدمة إلى حالة امتثال جزئية مع الإطار المستهدف. تم تحديد عدة فجوات حرجة في وثائق الحوكمة وأدلة التحكم في الوصول وقدرات المراقبة.

**٢. نطاق التدقيق والمنهجية**

- مراجعة وثائقية للأدلة المقدمة
- مطابقة الضوابط مع متطلبات الإطار
- تحديد الفجوات وتصنيف المخاطر

**٣. النتائج الرئيسية**

**النتيجة ١: أدلة مراجعة الوصول غير مكتملة**
- **الخطورة:** عالية
- **الملاحظة:** لم يتم العثور على دليل لمراجعات الوصول الربع سنوية (الضابط: إدارة الهوية-٠٤)
- **المخاطر:** قد تتراكم الصلاحيات المفرطة مما يزيد من مخاطر التهديد الداخلي
- **التوصية:** تطبيق عملية شهادة وصول ربع سنوية آلية

**النتيجة ٢: فجوة في سياسة كلمات المرور**
- **الخطورة:** متوسطة
- **الملاحظة:** متطلبات تعقيد كلمة المرور لا تستوفي الحد الأدنى البالغ ١٢ حرفاً
- **المخاطر:** زيادة التعرض لهجمات القوة الغاشمة
- **التوصية:** تحديث سياسة كلمات المرور وإنفاذها عبر الضوابط التقنية

**النتيجة ٣: قصور في التسجيل**
- **الخطورة:** عالية
- **الملاحظة:** يتم الاحتفاظ بسجلات الأمان لمدة ٣٠ يوماً فقط مقابل ١٢ شهراً المطلوبة
- **المخاطر:** عدم القدرة على التحقيق في الحوادث التي تتجاوز ٣٠ يوماً
- **التوصية:** تمديد فترة الاحتفاظ بالسجلات إلى ١٢ شهراً أو أكثر مع تكامل نظام إدارة المعلومات الأمنية

**٤. ملخص تحليل الفجوات**

- الضوابط الممتثلة: ٦٥٪
- الامتثال الجزئي: ٢٠٪
- عدم الامتثال: ١٥٪

**٥. أولوية التوصيات**

١. فورية (٠-٣٠ يوم): معالجة فجوات مراجعة الوصول والتسجيل
٢. قصيرة المدى (٣٠-٩٠ يوم): تحديث سياسات كلمات المرور
٣. متوسطة المدى (٩٠-١٨٠ يوم): تطبيق مراقبة شاملة

**٦. الخلاصة**

تُظهر المنظمة ممارسات أمنية تأسيسية لكنها تتطلب تحسيناً كبيراً في جمع الأدلة والتحقق من الضوابط لتحقيق الامتثال الكامل.

---
**درجة الثقة: ٧٨ من ١٠٠**

ملاحظة: يعتمد هذا التقرير على الأدلة المقدمة. قد تتغير النتائج عند توفر معلومات إضافية. يُنصح بإجراء تدقيق ميداني شامل للتحقق النهائي.
""",

    ResponseType.RISK: """
**تقرير تحليل المخاطر**

**١. ملخص المخاطر**

يشكل التهديد المحدد خطراً كبيراً على الأصل المستهدف. بناءً على سياق النشر والضوابط الحالية، يُقيّم مستوى المخاطر الحالي بأنه **عالٍ**.

**٢. تقييم الأثر**

- **السرية:** احتمال كشف البيانات مما يؤثر على المعلومات الحساسة
- **السلامة:** خطر التعديلات غير المصرح بها
- **التوفر:** احتمال انقطاع الخدمة
- **المالي:** نطاق الأثر المقدر: ٥٠٠ ألف - ٢ مليون ريال
- **السمعة:** ضرر كبير بالعلامة التجارية في حال الاستغلال

**٣. خطة التخفيف الاستراتيجية**

**الإجراءات الفورية (٠-٣ أشهر):**
١. عزل الأصل المتأثر عن قطاع الشبكة الرئيسي
٢. تطبيق التصحيحات الحرجة فوراً أو تمكين التصحيح الافتراضي عبر جدار حماية التطبيقات
٣. تطبيق مراقبة وتنبيه معززين
٤. إجراء مراجعة طارئة للوصول للأنظمة المتأثرة

**الإجراءات متوسطة المدى (٣-٦ أشهر):**
١. نشر ضوابط أمنية إضافية (كشف واستجابة نقاط النهاية، منع فقدان البيانات)
٢. تطبيق تحسينات تجزئة الشبكة
٣. إجراء تدريب توعية أمنية للفرق المعنية
٤. إنشاء إجراءات استجابة للحوادث خاصة بهذا الخطر

**الإجراءات طويلة المدى (٦+ أشهر):**
١. تطبيق إصلاح معماري دائم (مثل استبدال الأنظمة القديمة)
٢. نشر مبادئ بنية الثقة الصفرية
٣. إجراء اختبار اختراق كامل للتحقق من المعالجة
٤. الدمج في برنامج مراقبة المخاطر المستمرة

**٤. مؤشرات المخاطر الرئيسية**

- عدد الثغرات الحرجة غير المصححة
- متوسط وقت تصحيح الأنظمة الحرجة
- عدد محاولات الوصول غير المصرح بها
- عدد الحوادث الأمنية المتعلقة بمتجه التهديد هذا

**٥. المخاطر المتبقية**

بعد تطبيق الضوابط الموصى بها، من المتوقع أن تكون المخاطر المتبقية **منخفضة-متوسطة**.

---
**درجة الثقة: ٧٥ من ١٠٠**

يعتمد هذا التحليل على المعلومات المقدمة حول الأصل والتهديد والضوابط الحالية. لتقييم أكثر دقة، يُنصح بإجراء تقييم مخاطر ميداني شامل.
""",

    ResponseType.GENERAL: """
شكراً لاستفسارك. أنا أعمل في وضع المحاكاة حيث أن واجهة برمجة التطبيقات للذكاء الاصطناعي غير متوفرة حالياً.

للاستخدام الإنتاجي، يرجى التأكد من:
١. تعيين مفتاح واجهة برمجة التطبيقات صالح في البيئة
٢. عدم تجاوز حصة الاستخدام
٣. توفر الاتصال بخدمات الذكاء الاصطناعي

في هذه الأثناء، يمكنني تقديم إرشادات بناءً على أفضل الممارسات والأطر المعتمدة.
"""
}

MOCK_RESPONSES = {
    ResponseType.STRATEGY: """
**الرؤية التنفيذية | Executive Vision**

To establish a world-class, resilient security posture that enables digital trust, regulatory compliance, and sustainable business growth while positioning the organization as an industry leader in governance excellence.

لتأسيس موقف أمني عالمي المستوى ومرن يمكّن الثقة الرقمية والامتثال التنظيمي والنمو المستدام للأعمال مع وضع المنظمة كرائدة في التميز في الحوكمة.

**Strategic Objectives | الأهداف الاستراتيجية:**
1. Achieve 95%+ compliance with target frameworks within 18 months
2. Establish enterprise-wide governance operating model with clear accountability
3. Reduce risk exposure by 40% through proactive controls implementation
4. Build internal capabilities to sustain long-term excellence
5. Enable secure digital transformation initiatives
|||
**Current State Assessment | تقييم الوضع الراهن**

**Maturity Level:** Developing (Level 2 of 5)

Based on our assessment, the organization demonstrates foundational capabilities but lacks the process maturity and control effectiveness required for target state compliance.

**Critical Gaps Identified:**
- Governance: Policy framework exists but enforcement and measurement mechanisms are immature
- Risk Management: Reactive approach without systematic risk assessment methodology
- Technical Controls: Point solutions deployed without integrated architecture
- Monitoring: Limited visibility into security events and compliance status
- Third-Party Risk: Ad-hoc vendor assessments without standardized program

**Industry Benchmark:** Organization scores 45% against industry peers averaging 68%
|||
**Strategic Pillars | الركائز الاستراتيجية**

**Pillar 1: Governance Excellence**
- Establish GRC Committee with executive sponsorship
- Implement policy lifecycle management
- Deploy compliance monitoring dashboard

**Pillar 2: Risk-Based Security**
- Implement enterprise risk management framework
- Deploy continuous control monitoring
- Establish risk appetite and tolerance thresholds

**Pillar 3: Operational Resilience**
- Enhance incident response capabilities
- Implement business continuity program
- Establish crisis management framework

**Pillar 4: Technology Enablement**
- Deploy integrated GRC platform
- Implement security automation
- Establish secure architecture standards

**Pillar 5: People & Culture**
- Launch security awareness program
- Build internal expertise through training
- Establish security champions network
|||
**Implementation Roadmap | خارطة طريق التنفيذ**

| Phase | Initiative | Duration | Investment (SAR) | Owner | KPI |
|-------|------------|----------|------------------|-------|-----|
| Foundation | Governance Framework | 3 | 350,000 | GRC Lead | Policy coverage 100% |
| Foundation | Risk Assessment | 2 | 200,000 | Risk Manager | Risks identified |
| Foundation | Quick Wins Implementation | 3 | 500,000 | Security Lead | Critical gaps closed |
| Build | IAM Enhancement | 6 | 1,200,000 | IAM Lead | MFA coverage 100% |
| Build | SIEM Deployment | 6 | 1,800,000 | SOC Manager | MTTD < 24hrs |
| Build | TPRM Program | 4 | 400,000 | Vendor Risk | Critical vendors assessed |
| Build | Awareness Program | 4 | 300,000 | HR/Security | Training completion 95% |
| Optimize | Automation | 6 | 800,000 | Security Arch | Manual effort -50% |
| Optimize | Continuous Monitoring | 6 | 600,000 | GRC Lead | Real-time compliance |
| Optimize | Maturity Assessment | 2 | 150,000 | External | Target maturity achieved |

**Total Investment: SAR 6,300,000 | Timeline: 24 months**
|||
**Measuring Success | قياس النجاح**

**Key Performance Indicators (KPIs):**
1. Compliance Score: Target 95% (Current: 45%)
2. Policy Coverage: Target 100% (Current: 60%)
3. Risk Treatment: Target 90% of critical risks mitigated
4. Incident Response: MTTR < 4 hours
5. Training Completion: 95% of employees
6. Vendor Assessment: 100% of critical vendors

**Key Risk Indicators (KRIs):**
1. Open Audit Findings: Threshold < 5 high-severity
2. Overdue Risk Treatments: Threshold < 10%
3. Security Incidents: Threshold < 2 critical/quarter
4. Compliance Exceptions: Threshold < 3%

**Governance Cadence:**
- Weekly: Operational metrics review
- Monthly: Management dashboard review
- Quarterly: Executive Committee reporting
- Annual: Board presentation and strategy refresh
|||
**Confidence Score | درجة الثقة**

**Overall Confidence: 82/100**

**Assumptions:**
- Executive sponsorship secured and sustained
- Budget approved as estimated
- Key resources available for implementation
- No major regulatory changes during implementation

**Key Risks:**
- Resource constraints may impact timeline
- Change resistance in operational teams
- Technology integration complexity

**Recommended Next Steps:**
1. Secure executive sponsorship and budget approval
2. Establish Program Management Office (PMO)
3. Conduct detailed current state assessment
4. Develop detailed implementation plans for Phase 1
5. Initiate quick wins to build momentum
""",
    
    ResponseType.POLICY: """
**سياسة أمن المعلومات | Information Security Policy**

**1. بيان السياسة | Policy Statement**

تلتزم المنظمة بحماية أصول المعلومات من جميع التهديدات الداخلية والخارجية، المتعمدة أو العرضية، لضمان استمرارية الأعمال وتقليل الأضرار والمخاطر.

The organization is committed to protecting information assets from all threats, internal or external, deliberate or accidental, to ensure business continuity and minimize damage and risk.

**2. النطاق | Scope**

تنطبق هذه السياسة على جميع الموظفين والمقاولين والأطراف الثالثة الذين يصلون إلى أنظمة ومعلومات المنظمة.

**3. المتطلبات | Requirements**

3.1 يجب تصنيف جميع المعلومات وفقاً لمستوى حساسيتها
3.2 يجب تطبيق ضوابط الوصول بناءً على مبدأ الحاجة للمعرفة
3.3 يجب الإبلاغ عن جميع الحوادث الأمنية خلال 24 ساعة
3.4 يجب مراجعة صلاحيات الوصول بشكل ربع سنوي

**4. الامتثال | Compliance**

عدم الامتثال لهذه السياسة قد يؤدي إلى إجراءات تأديبية تصل إلى إنهاء الخدمة.

---
**Confidence Score: 85/100**

This policy is based on international best practices and local regulatory requirements. It is recommended to review with legal and compliance teams before final approval.
""",
    
    ResponseType.AUDIT: """
**تقرير التدقيق | Audit Report**

**الملخص التنفيذي | Executive Summary**

Based on our review of the provided evidence, we have identified several areas requiring management attention. The overall control environment demonstrates foundational capabilities but requires enhancement to meet target framework requirements.

**النتائج الرئيسية | Key Findings**

1. **Non-Conformity (Major):** Access control procedures not consistently followed
2. **Non-Conformity (Minor):** Documentation gaps in change management records
3. **Observation:** Opportunity to enhance monitoring capabilities
4. **Good Practice:** Strong executive commitment to compliance

**التوصيات | Recommendations**

1. Implement automated access review process
2. Enhance documentation standards and training
3. Deploy continuous monitoring solution
4. Continue executive engagement program

**الخلاصة | Conclusion**

The organization demonstrates commitment to compliance but requires focused effort on identified gaps to achieve certification readiness.

---
**Confidence Score: 78/100**

Note: This report is based on submitted evidence. Findings may change with additional information. A comprehensive on-site audit is recommended for final verification.
""",
    
    ResponseType.RISK: """
**تحليل المخاطر | Risk Analysis**

**1. تحديد المخاطر | Risk Identification**

The identified risk scenario presents a significant threat to organizational operations with potential for material business impact.

**2. تقييم الأثر | Impact Assessment**

- **Financial Impact:** Potential losses of SAR 500,000 - 2,000,000
- **Operational Impact:** Service disruption of 24-72 hours
- **Reputational Impact:** Moderate stakeholder concern
- **Severity Rating:** HIGH

**3. تقييم الاحتمالية | Likelihood Assessment**

- **Threat Capability:** Moderate to High
- **Vulnerability Exposure:** Medium
- **Probability Rating:** MEDIUM-HIGH

**4. استراتيجية التخفيف | Mitigation Strategy**

**Immediate (0-30 days):**
- Implement compensating controls
- Enhance monitoring for early detection
- Update incident response procedures

**Short-Term (1-3 months):**
- Deploy technical controls
- Conduct staff awareness training
- Establish vendor requirements

**Long-Term (3-12 months):**
- Architecture improvements
- Process automation
- Continuous improvement program

**5. مؤشرات المخاطر | Key Risk Indicators**

- Monitor for anomalous activity
- Track control effectiveness metrics
- Regular vulnerability assessments

---
**Confidence Score: 75/100**

This analysis is based on provided information about the asset, threat, and existing controls. For a more precise assessment, a comprehensive field-based risk assessment is recommended.
""",
    
    ResponseType.GENERAL: """
Thank you for your query. As your AI advisor, I'm here to help with governance, risk, and compliance matters.

شكراً لاستفسارك. بصفتي مستشارك الذكي، أنا هنا للمساعدة في شؤون الحوكمة والمخاطر والامتثال.

Please provide more specific details about your requirements, and I'll provide tailored guidance based on industry best practices and relevant frameworks.
"""
}


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

ai_service = AIService()
