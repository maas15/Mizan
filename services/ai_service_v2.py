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
    from data.benchmarks import get_benchmark_comparison, get_sector_benchmark, get_all_sources, calculate_maturity_level
    from data.maturity_assessment import assess_maturity_from_controls, get_maturity_assessment_summary
    from data.domain_strategies import get_domain_strategy_content
    from data.domain_content import get_strategy_arabic, get_policy_content, get_audit_content, get_risk_content, get_domain_config
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
        """Generate dynamic strategy fallback with real benchmark data and control-based maturity."""
        domain = context.get('domain', 'Cyber Security')
        sector = context.get('sector', 'General')
        org_name = context.get('org_name', 'Organization')
        tech_stack = context.get('tech', '')
        challenges = context.get('challenges', '')
        self_reported_score = context.get('gap_data', {}).get('compliance_score')
        
        # Get real benchmark data
        benchmark = get_sector_benchmark(domain, sector)
        industry_avg = benchmark.get('average', 55)
        top_quartile = benchmark.get('top_quartile', 75)
        saudi_avg = benchmark.get('saudi_average', industry_avg)
        source = benchmark.get('source', 'Industry reports')
        
        # Use CONTROL-BASED maturity assessment for realistic scoring
        maturity_assessment = assess_maturity_from_controls(
            tech_stack=tech_stack,
            challenges=challenges,
            domain=domain,
            self_reported_score=self_reported_score
        )
        
        # Use calculated score from controls (more realistic than self-reported)
        current_score = maturity_assessment['calculated_score']
        maturity_level = maturity_assessment['maturity_level']
        maturity_name_en = maturity_assessment['maturity_name_en']
        maturity_name_ar = maturity_assessment['maturity_name_ar']
        confidence = maturity_assessment['confidence']
        
        # Calculate gaps (positive = above benchmark, negative = below)
        gap_to_avg = current_score - industry_avg  # Positive means above average
        gap_to_top = current_score - top_quartile   # Negative means below top quartile
        
        # Format gap strings with proper signs
        gap_avg_str = f"+{gap_to_avg:.0f}" if gap_to_avg > 0 else f"{gap_to_avg:.0f}"
        gap_top_str = f"+{gap_to_top:.0f}" if gap_to_top > 0 else f"{gap_to_top:.0f}"
        
        # Position assessment
        if gap_to_avg >= 0:
            position_en = "above industry average"
            position_ar = "أعلى من متوسط الصناعة"
        else:
            position_en = "below industry average"
            position_ar = "أقل من متوسط الصناعة"
        
        # Build critical gaps string
        critical_gaps = maturity_assessment.get('critical_gaps', [])
        gaps_en = ', '.join(critical_gaps[:3]) if critical_gaps else "Focus on operational maturity"
        gaps_ar = "الحوكمة، إدارة الهوية والوصول، العمليات الأمنية" if critical_gaps else "التركيز على النضج التشغيلي"
        
        # Add note if self-reported differs from calculated
        score_note_en = ""
        score_note_ar = ""
        if self_reported_score and abs(self_reported_score - current_score) > 15:
            score_note_en = f"\n\n**Note:** Self-reported score ({self_reported_score}%) differs from control-based assessment ({current_score:.0f}%). Detailed gap analysis recommended."
            score_note_ar = f"\n\n**ملاحظة:** النسبة المقررة ذاتياً ({self_reported_score}٪) تختلف عن التقييم المبني على الضوابط ({current_score:.0f}٪). يوصى بتحليل فجوات تفصيلي."
        
        if language in ["Arabic", "العربية"]:
            # Get domain-specific Arabic content
            ar_content = get_strategy_arabic(domain)
            
            # Build Arabic pillars
            pillars_ar = ""
            for i, pillar in enumerate(ar_content["pillars"], 1):
                pillars_ar += f"\n**الركيزة {i}: {pillar['name']}**\n"
                for initiative in pillar["initiatives"]:
                    pillars_ar += f"- {initiative}\n"
            
            # Build Arabic objectives
            objectives_ar = ""
            for i, obj in enumerate(ar_content["objectives"], 1):
                objectives_ar += f"{i}. {obj}\n"
            
            return f"""**الرؤية التنفيذية**

{ar_content["vision"]}

**الأهداف الاستراتيجية:**
{objectives_ar}|||
**تقييم الوضع الراهن**

**مستوى النضج:** {maturity_name_ar} (المستوى {maturity_level} من ٥)

الموقع الحالي: {position_ar}{score_note_ar}

**المقارنة المرجعية (المصدر: {source}):**
- النسبة الحالية للمنظمة: {current_score:.0f}٪
- متوسط قطاع {sector}: {industry_avg}٪
- الربع الأعلى أداءً: {top_quartile}٪
- متوسط المملكة العربية السعودية: {saudi_avg}٪
- الفرق عن المتوسط: {gap_avg_str}٪
- الفرق عن الربع الأعلى: {gap_top_str}٪

**الفجوات الحرجة:** {gaps_ar}
|||
**الركائز الاستراتيجية والمبادرات**
{pillars_ar}|||
**خارطة طريق التنفيذ**

| المرحلة | المبادرة | المدة (شهر) | الاستثمار (ريال) |
|---------|----------|-------------|------------------|
| التأسيس | إطار الحوكمة | ٣ | ٣٥٠,٠٠٠ |
| التأسيس | تقييم المخاطر | ٢ | ٢٠٠,٠٠٠ |
| البناء | تطبيق الضوابط | ٦ | ١,٥٠٠,٠٠٠ |
| البناء | التدريب والتوعية | ٤ | ٣٠٠,٠٠٠ |
| التحسين | الأتمتة والتحسين | ٦ | ٦٠٠,٠٠٠ |

**الإجمالي: ٢,٩٥٠,٠٠٠ ريال | المدة: ٢٤ شهر**
|||
**مؤشرات الأداء الرئيسية:**
١. نسبة الامتثال: الهدف ٩٥٪ (الحالي: {current_score:.0f}٪)
٢. تغطية السياسات: الهدف ١٠٠٪
٣. معالجة المخاطر: الهدف ٩٠٪ من المخاطر الحرجة
٤. إكمال التدريب: ٩٥٪ من الموظفين

**مؤشرات المخاطر الرئيسية:**
١. الملاحظات عالية الخطورة: أقل من ٥
٢. المعالجات المتأخرة: أقل من ١٠٪
٣. الحوادث الحرجة: أقل من ٢/ربع سنوي
|||
**درجة الثقة: {confidence}/١٠٠**

**مصادر البيانات:** {source}

**الافتراضات:**
- توفر الرعاية التنفيذية واستمرارها
- اعتماد الميزانية كما هو مقدر
- توفر الموارد الرئيسية للتنفيذ

**المخاطر الرئيسية:**
- قيود الموارد قد تؤثر على الجدول الزمني
- مقاومة التغيير في الفرق التشغيلية
- تعقيد تكامل التقنيات

**الخطوات التالية:**
١. الحصول على الرعاية التنفيذية واعتماد الميزانية
٢. تأسيس مكتب إدارة البرنامج
٣. إجراء تقييم تفصيلي للوضع الحالي
٤. تطوير خطط التنفيذ التفصيلية
٥. بدء المكاسب السريعة"""
        
        else:  # English only
            # Get domain-specific strategy content
            strategy_content = get_domain_strategy_content(domain, context)
            
            # Build domain-specific pillars section
            pillars_text = ""
            for i, pillar in enumerate(strategy_content["pillars"], 1):
                pillars_text += f"\n**Pillar {i}: {pillar['name']}**\n"
                for initiative in pillar["initiatives"]:
                    pillars_text += f"- {initiative}\n"
            
            # Build domain-specific roadmap
            roadmap_rows = []
            total_cost = 0
            for item in strategy_content["roadmap"]:
                roadmap_rows.append(f"| {item['phase']} | {item['initiative']} | {item['duration']} | {item['cost']:,} | {item['owner']} | {item['kpi']} |")
                total_cost += item['cost']
            roadmap_text = "\n".join(roadmap_rows)
            
            # Build domain-specific KPIs
            kpis_text = ""
            for i, (kpi, target, current) in enumerate(strategy_content["kpis"], 1):
                kpis_text += f"{i}. {kpi}: Target {target} (Current: {current})\n"
            
            # Build domain-specific KRIs
            kris_text = ""
            for i, (kri, threshold, red) in enumerate(strategy_content["kris"], 1):
                kris_text += f"{i}. {kri}: Threshold {threshold} ({red})\n"
            
            # Build objectives
            objectives_text = ""
            for i, obj in enumerate(strategy_content["objectives"], 1):
                objectives_text += f"{i}. {obj}\n"
            
            return f"""**Executive Vision**

{strategy_content["vision"]}

**Strategic Objectives:**
{objectives_text}|||
**Current State Assessment**

**Maturity Level:** {maturity_name_en} (Level {maturity_level} of 5)

Based on our control-based assessment, the organization is currently {position_en}, demonstrating {'solid capabilities with room for optimization' if gap_to_avg >= 0 else 'foundational capabilities requiring focused improvement'}.{score_note_en}

**Benchmark Comparison (Source: {source}):**
- **Current Organization Score:** {current_score:.0f}%
- **{sector} Industry Average:** {industry_avg}%
- **Top Quartile Performance:** {top_quartile}%
- **Saudi Arabia Average:** {saudi_avg}%
- **Gap to Industry Average:** {gap_avg_str}% {'(above average ✓)' if gap_to_avg >= 0 else '(below average)'}
- **Gap to Top Quartile:** {gap_top_str}%

**Critical Gaps Identified:** {gaps_en}
|||
**Strategic Pillars & Initiatives**
{pillars_text}|||
**Implementation Roadmap**

| Phase | Initiative | Duration (Months) | Investment (SAR) | Owner | Success KPI |
|-------|------------|-------------------|------------------|-------|-------------|
{roadmap_text}

**Total Investment: SAR {total_cost:,} | Timeline: 24 months**
|||
**Key Performance Indicators (KPIs):**
{kpis_text}
**Key Risk Indicators (KRIs):**
{kris_text}
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
    
    def _generate_bilingual_strategy(self, context, maturity_level, maturity_name_en, maturity_name_ar,
                                      current_score, industry_avg, top_quartile, saudi_avg,
                                      gap_avg_str, gap_top_str, position_en, position_ar,
                                      source, confidence, domain, org_name, sector):
        """Generate bilingual (English + Arabic side-by-side) strategy output with domain-specific content."""
        gap_to_avg = current_score - industry_avg
        
        # Get domain-specific strategy content
        strategy_content = get_domain_strategy_content(domain, context)
        
        # Build bilingual pillars section
        pillars_text = ""
        for i, pillar in enumerate(strategy_content["pillars"], 1):
            pillars_text += f"\n**Pillar {i}: {pillar['name']} | {pillar['name_ar']}**\n"
            for j, initiative in enumerate(pillar["initiatives"][:3]):  # Limit to 3 for bilingual
                pillars_text += f"- {initiative}\n"
        
        # Build bilingual objectives
        objectives_text = ""
        for i, (obj_en, obj_ar) in enumerate(zip(strategy_content["objectives"][:5], strategy_content["objectives_ar"][:5]), 1):
            objectives_text += f"{i}. {obj_en[:60]}... | {obj_ar[:60]}...\n"
        
        # Build bilingual roadmap (simplified)
        roadmap_rows = []
        total_cost = 0
        for item in strategy_content["roadmap"][:5]:  # Top 5 for bilingual
            roadmap_rows.append(f"| {item['phase']} | {item['initiative'][:20]} | {item['duration']} mo | {item['cost']:,} |")
            total_cost += item['cost']
        roadmap_text = "\n".join(roadmap_rows)
        
        # Build bilingual KPIs
        kpis_text = ""
        for i, (kpi, target, current) in enumerate(strategy_content["kpis"][:4], 1):
            kpis_text += f"| {kpi[:25]} | {target} | {current[:15]} |\n"
        
        return f"""**Executive Vision | الرؤية التنفيذية**

{strategy_content["vision"][:200]}...

{strategy_content["vision_ar"][:200]}...

**Strategic Objectives | الأهداف الاستراتيجية:**
{objectives_text}|||
**Current State Assessment | تقييم الوضع الراهن**

**Maturity Level | مستوى النضج:** {maturity_name_en} / {maturity_name_ar} (Level {maturity_level} of 5 | المستوى {maturity_level} من ٥)

Current Position | الموقع الحالي: {position_en} | {position_ar}

**Benchmark Comparison | المقارنة المرجعية (Source | المصدر: {source}):**

| Metric | القياس | Value | القيمة |
|--------|--------|-------|--------|
| Current Score | النسبة الحالية | {current_score:.0f}% | {current_score:.0f}٪ |
| Industry Average | متوسط الصناعة | {industry_avg}% | {industry_avg}٪ |
| Top Quartile | الربع الأعلى | {top_quartile}% | {top_quartile}٪ |
| Saudi Average | متوسط السعودية | {saudi_avg}% | {saudi_avg}٪ |
| Gap to Average | الفرق عن المتوسط | {gap_avg_str}% | {gap_avg_str}٪ |
| Gap to Top Quartile | الفرق عن الربع الأعلى | {gap_top_str}% | {gap_top_str}٪ |

**Status | الحالة:** {'Above Average ✓ | أعلى من المتوسط ✓' if gap_to_avg >= 0 else 'Below Average | أقل من المتوسط'}
|||
**Strategic Pillars | الركائز الاستراتيجية**
{pillars_text}|||
**Implementation Roadmap | خارطة طريق التنفيذ**

| Phase | Initiative | Duration | Investment (SAR) |
|-------|------------|----------|------------------|
{roadmap_text}

**Total | الإجمالي: SAR {total_cost:,} | Timeline | المدة: 24 months | ٢٤ شهر**
|||
**KPIs | مؤشرات الأداء الرئيسية:**

| KPI | Target | Current |
|-----|--------|---------|
{kpis_text}

**KRIs | مؤشرات المخاطر الرئيسية:**
1. {strategy_content["kris"][0][0]}: {strategy_content["kris"][0][1]}
2. {strategy_content["kris"][1][0]}: {strategy_content["kris"][1][1]}
3. {strategy_content["kris"][2][0]}: {strategy_content["kris"][2][1]}
|||
**Confidence Score | درجة الثقة: {confidence}/100**

**Data Sources | مصادر البيانات:** {source}

**Assumptions | الافتراضات:**
- Executive sponsorship secured | توفر الرعاية التنفيذية
- Budget approved as estimated | اعتماد الميزانية
- Key resources available | توفر الموارد الرئيسية

**Key Risks | المخاطر الرئيسية:**
- Resource constraints | قيود الموارد
- Change resistance | مقاومة التغيير
- Integration complexity | تعقيد التكامل

**Next Steps | الخطوات التالية:**
1. Secure executive sponsorship | الحصول على الرعاية التنفيذية
2. Establish PMO | تأسيس مكتب إدارة البرنامج
3. Detailed assessment | تقييم تفصيلي
4. Phase 1 planning | تخطيط المرحلة الأولى
5. Quick wins | المكاسب السريعة"""
    
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
        """Generate a comprehensive domain-specific policy document."""
        prompt = self._build_policy_prompt(policy_name, domain, framework, language)
        response = self.generate(prompt, ResponseType.POLICY, max_tokens=3500, temperature=0.5, language=language)
        
        # If using fallback, generate domain-specific policy
        if response.source == "fallback":
            content = self._build_domain_policy(domain, framework, language)
            return AIResponse(content=content, success=True, source="fallback", model="simulation")
        
        # Post-processing: If Arabic was requested but output contains significant English, use domain fallback
        if language in ["Arabic", "العربية"] and response.source == "api":
            english_indicators = ["Policy", "Statement", "Scope", "Purpose", "Roles", "Responsibilities",
                                  "Compliance", "Requirements", "Review", "The ", " the ", "This ", " this ",
                                  "shall ", "must ", "will ", "should "]
            english_count = sum(1 for indicator in english_indicators if indicator in response.content)
            
            if english_count > 5:
                logger.warning(f"Arabic policy contains {english_count} English indicators, using domain fallback")
                content = self._build_domain_policy(domain, framework, language)
                return AIResponse(content=content, success=True, source="fallback", model="simulation")
        
        return response
    
    def _build_domain_policy(self, domain: str, framework: str, language: str) -> str:
        """Build domain-specific policy content."""
        policy_data = get_policy_content(domain, language)
        
        if language in ["Arabic", "العربية"]:
            # Build Arabic requirements list
            requirements_ar = "\n".join([f"- {req}" for req in policy_data["key_requirements"]])
            roles_ar = "\n".join([f"| {role} | {resp} |" for role, resp in policy_data["roles"]])
            
            return f"""**{policy_data["title"]}**
**رقم الوثيقة:** POL-{domain[:3].upper()}-001 | **الإصدار:** 1.0 | **التصنيف:** داخلي

---

**١. الغرض وبيان السياسة**

{policy_data["purpose"]}

**٢. النطاق**

{policy_data["scope"]}

**٣. المتطلبات الرئيسية**

{requirements_ar}

**٤. الأدوار والمسؤوليات**

| الدور | المسؤولية |
|-------|-----------|
{roles_ar}

**٥. الامتثال والإنفاذ**

- عدم الامتثال لهذه السياسة قد يؤدي إلى إجراءات تأديبية
- يجب الإبلاغ عن الاستثناءات واعتمادها من الإدارة المعنية
- سيتم إجراء مراجعات دورية لضمان الامتثال

**٦. المراجعة والتحديث**

- **دورة المراجعة:** سنوياً أو عند حدوث تغييرات جوهرية
- **المالك:** {policy_data["roles"][0][0]}
- **آخر مراجعة:** [التاريخ]
- **المراجعة القادمة:** [التاريخ + سنة]

**٧. الوثائق ذات الصلة**

- إطار {framework}
- معايير وإجراءات {domain}
- سياسات الحوكمة المؤسسية

---
*تمت الموافقة من قبل: [اسم المعتمد] | التاريخ: [تاريخ الاعتماد]*
"""
        else:
            # Build English requirements list  
            requirements_en = "\n".join([f"- {req}" for req in policy_data["key_requirements"]])
            roles_en = "\n".join([f"| {role} | {resp} |" for role, resp in policy_data["roles"]])
            
            return f"""**{policy_data["title"]}**
**Document ID:** POL-{domain[:3].upper()}-001 | **Version:** 1.0 | **Classification:** Internal

---

**1. Purpose and Policy Statement**

{policy_data["purpose"]}

**2. Scope**

{policy_data["scope"]}

**3. Key Requirements**

{requirements_en}

**4. Roles and Responsibilities**

| Role | Responsibility |
|------|----------------|
{roles_en}

**5. Compliance and Enforcement**

- Non-compliance with this policy may result in disciplinary action
- Exceptions must be documented and approved by relevant management
- Periodic reviews will be conducted to ensure compliance

**6. Review and Update**

- **Review Cycle:** Annually or upon significant changes
- **Policy Owner:** {policy_data["roles"][0][0]}
- **Last Review:** [Date]
- **Next Review:** [Date + 1 year]

**7. Related Documents**

- {framework} Framework
- {domain} Standards and Procedures
- Corporate Governance Policies

---
*Approved by: [Approver Name] | Date: [Approval Date]*
"""
    
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
        context: Dict[str, Any] = None,
        language: str = "English"
    ) -> AIResponse:
        """Generate domain-specific risk analysis with full language support."""
        context = context or {}
        
        # Get domain-specific context
        domain_context = self._get_domain_risk_context(domain)
        risk_content = get_risk_content(domain)
        
        if language in ["Arabic", "العربية"]:
            prompt = f"""
أنت مستشار أول في إدارة المخاطر من إحدى شركات الأربعة الكبار (ديلويت/برايس ووترهاوس/إرنست آند يونغ/كي بي إم جي).

المجال: {domain}
سيناريو التهديد/الخطر: {threat}
الأصل/الموضوع: {asset}
ملاحظات إضافية: {context.get('notes', 'لا يوجد')}
الضوابط الحالية: {context.get('controls', 'لا يوجد')}

قدم تحليل مخاطر شامل باللغة العربية بالتنسيق التالي:

**١. تحديد المخاطر**
- وصف تفصيلي لسيناريو الخطر
- نواقل الهجوم / أنماط الفشل الخاصة بمجال {domain}
- الأصول وأصحاب المصلحة المتأثرون

**٢. تقييم الأثر**
- الأثر على الأعمال (مالي، تشغيلي، سمعة، قانوني)
- تصنيف الخطورة: [حرج/عالي/متوسط/منخفض]
- سيناريوهات الخسارة المحتملة مع التقديرات

**٣. تقييم الاحتمالية**
- دوافع وقدرات الجهات المهددة
- مستوى التعرض للثغرات
- تصنيف الاحتمالية: [عالي جداً/عالي/متوسط/منخفض/منخفض جداً]

**٤. مصفوفة تصنيف المخاطر**
- درجة الخطر الكامن
- فعالية الضوابط الحالية
- درجة الخطر المتبقي

**٥. استراتيجية التخفيف**
**إجراءات فورية (٠-٣٠ يوم):**
- المكاسب السريعة والضوابط العاجلة

**قصيرة المدى (١-٣ أشهر):**
- تحسينات العمليات
- الضوابط التقنية

**طويلة المدى (٣-١٢ شهر):**
- المبادرات الاستراتيجية
- تغييرات البنية

**٦. مؤشرات المخاطر الرئيسية (KRIs)**
- مقاييس محددة للمراقبة
- العتبات ومعايير التنبيه

**٧. توصيات الضوابط**
- ضوابط وقائية
- ضوابط كشفية
- ضوابط تصحيحية

مهم: تأكد من أن التحليل خاص بمجال {domain} وليس عام.
اكتب الرد بالكامل باللغة العربية.
"""
        else:
            prompt = f"""
ACT AS: Senior Risk Management Consultant from a Big 4 firm.
DOMAIN: {domain}
DOMAIN CONTEXT: {domain_context}
THREAT/RISK SCENARIO: {threat}
ASSET/SUBJECT: {asset}
ADDITIONAL CONTEXT: {context.get('notes', 'N/A')}
EXISTING CONTROLS: {context.get('controls', 'N/A')}

RELEVANT RISK CATEGORIES FOR THIS DOMAIN:
{', '.join(risk_content.get('categories', []))}

IMPACT AREAS TO CONSIDER:
{', '.join(risk_content.get('impact_areas', []))}

APPLICABLE FRAMEWORKS:
{', '.join(risk_content.get('control_frameworks', []))}

PROVIDE ANALYSIS IN THIS FORMAT:

**1. Risk Identification**
- Detailed description of the risk scenario
- Attack vectors / failure modes specific to {domain}
- Affected stakeholders and assets

**2. Impact Assessment**
- Business Impact (Financial, Operational, Reputational, Legal)
- Severity Rating: [Critical/High/Medium/Low]
- Potential loss scenarios with estimates

**3. Likelihood Assessment**
- Threat actor motivation and capability (if applicable)
- Vulnerability exposure
- Probability Rating: [Very High/High/Medium/Low/Very Low]

**4. Risk Rating Matrix**
- Inherent Risk Score
- Current Control Effectiveness
- Residual Risk Score

**5. Mitigation Strategy**
**Immediate Actions (0-30 days):**
- Quick wins and urgent controls

**Short-Term (1-3 months):**
- Process improvements
- Technical controls

**Long-Term (3-12 months):**
- Strategic initiatives
- Architecture changes

**6. Key Risk Indicators (KRIs)**
- Specific metrics to monitor
- Thresholds and alerting criteria

**7. Control Recommendations**
- Preventive controls
- Detective controls
- Corrective controls

IMPORTANT: Ensure all analysis is specific to the {domain} domain, not generic.
"""
        
        response = self.generate(prompt, ResponseType.RISK, language=language)
        
        # If fallback and Arabic requested, generate Arabic fallback
        if response.source == "fallback" and language in ["Arabic", "العربية"]:
            content = self._build_arabic_risk_fallback(domain, threat, asset, risk_content)
            return AIResponse(content=content, success=True, source="fallback", model="simulation")
        
        return response
    
    def _build_arabic_risk_fallback(self, domain: str, threat: str, asset: str, risk_content: Dict) -> str:
        """Build Arabic risk analysis fallback."""
        domain_ar = {
            "Cyber Security": "الأمن السيبراني",
            "AI Governance": "حوكمة الذكاء الاصطناعي",
            "Data Management": "إدارة البيانات",
            "Digital Transformation": "التحول الرقمي",
            "Global Standards": "المعايير العالمية"
        }.get(domain, domain)
        
        return f"""**تحليل المخاطر - {domain_ar}**

**١. تحديد المخاطر**
- **سيناريو الخطر:** {threat}
- **الأصل المتأثر:** {asset}
- **نواقل الهجوم المحتملة:** بناءً على طبيعة {domain_ar}، قد تشمل نواقل الهجوم الرئيسية الهندسة الاجتماعية، استغلال الثغرات التقنية، والتهديدات الداخلية.

**٢. تقييم الأثر**
- **الأثر المالي:** خسائر مباشرة محتملة + تكاليف الاستجابة والتعافي
- **الأثر التشغيلي:** تعطل العمليات وانخفاض الإنتاجية
- **الأثر على السمعة:** فقدان ثقة العملاء وأصحاب المصلحة
- **الأثر القانوني:** عقوبات تنظيمية محتملة ومسؤولية قانونية
- **تصنيف الخطورة:** عالي

**٣. تقييم الاحتمالية**
- **مستوى التهديد:** متوسط إلى عالي بناءً على بيئة التهديدات الحالية
- **التعرض للثغرات:** يتطلب تقييم تفصيلي للضوابط الحالية
- **تصنيف الاحتمالية:** متوسط

**٤. مصفوفة تصنيف المخاطر**

| المقياس | القيمة |
|---------|--------|
| الخطر الكامن | عالي |
| فعالية الضوابط | متوسطة |
| الخطر المتبقي | متوسط-عالي |

**٥. استراتيجية التخفيف**

**إجراءات فورية (٠-٣٠ يوم):**
- مراجعة وتعزيز الضوابط الحالية
- تفعيل المراقبة المكثفة
- إبلاغ أصحاب المصلحة المعنيين

**قصيرة المدى (١-٣ أشهر):**
- تطبيق ضوابط إضافية
- تحديث السياسات والإجراءات
- تدريب الموظفين المعنيين

**طويلة المدى (٣-١٢ شهر):**
- تعزيز البنية الأمنية
- تطبيق أتمتة الضوابط
- مراجعة شاملة للبرنامج

**٦. مؤشرات المخاطر الرئيسية (KRIs)**
- عدد الحوادث المكتشفة: العتبة < ٥ شهرياً
- وقت الاكتشاف: العتبة < ٤ ساعات
- معدل إغلاق الثغرات: العتبة > ٩٠٪

**٧. توصيات الضوابط**
- **ضوابط وقائية:** تعزيز التحكم في الوصول، التشفير، التوعية
- **ضوابط كشفية:** المراقبة المستمرة، التنبيهات، التدقيق
- **ضوابط تصحيحية:** خطط الاستجابة، النسخ الاحتياطي، التعافي

---
*تم إنشاء هذا التحليل بواسطة نظام ميزان للحوكمة والمخاطر والامتثال*
"""
    
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
**Information Security Policy**
**Document Control: Version 1.0 | Classification: Internal**

---

**1. Purpose and Policy Statement**

This policy establishes the organization's commitment to protecting information assets from all threats—internal, external, deliberate, or accidental—to ensure business continuity, regulatory compliance, and stakeholder trust. This policy aligns with NCA Essential Cybersecurity Controls, ISO 27001:2022, and industry best practices.

**2. Scope and Applicability**

This policy applies to:
- All employees (full-time, part-time, temporary)
- Contractors, consultants, and third-party service providers
- All information systems, networks, applications, and data owned or managed by the organization
- All locations including head office, branches, and remote work environments

**3. Definitions and Key Terms**

- **Information Asset:** Any data, system, or resource that has value to the organization
- **Access Control:** Security measures regulating who may view or use organizational resources
- **Privileged Access:** Administrative or elevated access rights beyond standard user permissions
- **Multi-Factor Authentication (MFA):** Authentication requiring two or more verification methods

**4. Roles and Responsibilities**

| Role | Responsibilities |
|------|------------------|
| Executive Management | Policy sponsorship, resource allocation, risk acceptance |
| Information Security | Policy development, control implementation, monitoring |
| System Owners | Access approval, quarterly access reviews, risk assessment |
| IT Operations | Technical implementation, incident response, patching |
| Human Resources | Onboarding/offboarding notifications, awareness training |
| All Users | Policy compliance, credential protection, incident reporting |

**5. Policy Requirements**

5.1 **Access Control Principles**
- Access shall be granted based on "need-to-know" and "least privilege" principles
- All access requests require documented approval from data/system owners
- Generic, shared, or anonymous accounts are prohibited except where explicitly approved

5.2 **Authentication Requirements**
- Multi-factor authentication is mandatory for: remote access, privileged accounts, sensitive systems
- Password minimum: 12 characters, complexity requirements per security standards
- Account lockout after 5 failed attempts; automatic unlock after 30 minutes

5.3 **Access Review and Certification**
- Quarterly access reviews required for all critical systems
- Annual recertification of all user access rights
- Immediate revocation upon employment termination or role change

5.4 **Monitoring and Logging**
- All access events shall be logged and retained for minimum 12 months
- Security monitoring for anomalous access patterns
- Regular review of privileged account activities

**6. Compliance and Enforcement**

- Violations may result in disciplinary action up to and including termination
- Security exceptions require documented risk acceptance by executive management
- Regular audits will be conducted to verify compliance
- All security incidents must be reported within 24 hours

**7. Related Documents**

- Access Control Standard | Password Management Standard
- Acceptable Use Policy | Incident Response Procedure
- Third-Party Risk Management Policy

**8. Review and Maintenance**

This policy shall be reviewed annually or upon significant organizational, technological, or regulatory changes. Policy owner: Chief Information Security Officer (CISO).

---
**Confidence Score: 85/100**

This policy template is based on international best practices (ISO 27001, NIST CSF) and Saudi regulatory requirements (NCA ECC). Customize organizational details, approval workflows, and specific technical requirements before final adoption. Legal and compliance review recommended.
""",
    
    ResponseType.AUDIT: """
**Compliance Audit Report**
**Assessment Period: Q4 2024 | Classification: Confidential**

---

**1. Executive Summary**

This audit assessed the organization's control environment against target framework requirements. Based on evidence review and control testing, the organization demonstrates foundational capabilities but requires enhancement in specific areas to achieve full compliance.

**Overall Assessment: Partial Compliance (65%)**

| Rating | Description | Count |
|--------|-------------|-------|
| Conforming | Control fully meets requirements | 8 |
| Partially Conforming | Control needs enhancement | 5 |
| Non-Conforming | Significant gap identified | 3 |
| Not Assessed | Insufficient evidence | 2 |

**2. Scope and Methodology**

**Audit Scope:**
- Documentary review of policies, procedures, and evidence
- Control mapping against framework requirements
- Gap identification and risk prioritization
- Recommendation development

**Methodology:** Risk-based audit approach following ISO 19011 guidelines

**Limitations:** Assessment based on provided documentation; on-site verification recommended for certification readiness.

**3. Key Findings**

**Finding 1: Access Control Review Gaps (HIGH PRIORITY)**
- **Control Reference:** IAM-04 (Access Review)
- **Observation:** No evidence of quarterly access reviews for critical systems
- **Risk Impact:** Privilege accumulation increasing insider threat exposure
- **Recommendation:** Implement automated access certification with quarterly cadence
- **Target Date:** Q1 2025

**Finding 2: Password Policy Non-Compliance (MEDIUM PRIORITY)**
- **Control Reference:** IAM-02 (Authentication)
- **Observation:** Password complexity below 12-character minimum requirement
- **Risk Impact:** Increased susceptibility to brute force attacks
- **Recommendation:** Update password policy and enforce via technical controls
- **Target Date:** Immediate

**Finding 3: Incident Response Documentation (MEDIUM PRIORITY)**
- **Control Reference:** IR-01 (Incident Management)
- **Observation:** Incident response plan not tested in past 12 months
- **Risk Impact:** Potential delays in incident containment and recovery
- **Recommendation:** Schedule tabletop exercise and update procedures
- **Target Date:** Q1 2025

**Finding 4: Third-Party Risk Assessment (LOW PRIORITY)**
- **Control Reference:** TPM-03 (Vendor Assessment)
- **Observation:** Security assessments completed for 70% of critical vendors
- **Risk Impact:** Unknown risk exposure from unassessed vendors
- **Recommendation:** Complete critical vendor assessments by Q2 2025
- **Target Date:** Q2 2025

**4. Positive Observations**

✓ Strong executive sponsorship for security initiatives
✓ Well-documented information security policy framework
✓ Active security awareness training program (78% completion)
✓ Established vulnerability management process

**5. Recommendations Summary**

| Priority | Finding | Owner | Target |
|----------|---------|-------|--------|
| High | Access Review Implementation | IT Security | Q1 2025 |
| Medium | Password Policy Update | IT Operations | Immediate |
| Medium | IR Plan Testing | Security Lead | Q1 2025 |
| Low | Vendor Assessment Completion | Procurement | Q2 2025 |

**6. Conclusion**

The organization has established foundational security controls but requires focused remediation on identified gaps to achieve compliance certification. We recommend prioritizing high-risk findings and establishing a remediation tracking process.

**Next Steps:**
1. Management response to findings within 30 days
2. Remediation plan development with assigned owners
3. Follow-up assessment scheduled for Q2 2025

---
**Confidence Score: 78/100**

**Basis:** Assessment confidence reflects evidence quality and scope. Higher confidence requires on-site verification, interviews, and technical testing. Findings may be updated with additional evidence submission.

**Assumptions:** Current threat landscape, stable regulatory requirements, management commitment to remediation.
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
