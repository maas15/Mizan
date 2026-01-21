"""
Sentinel GRC - AI Service
Unified AI service with fallback support and proper error handling.
"""

import os
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

# =============================================================================
# ENSURE .env IS LOADED
# =============================================================================
try:
    from dotenv import load_dotenv
    
    # Try multiple locations for .env file
    _possible_paths = [
        Path(__file__).parent.parent / ".env",  # Project root
        Path.cwd() / ".env",                     # Current working directory
        Path(__file__).parent / ".env",          # Services directory
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
    source: str  # 'api' or 'fallback'
    model: str
    error: Optional[str] = None


class AIService:
    """
    Unified AI service with OpenAI integration and fallback support.
    
    Features:
    - Automatic fallback to mock responses if API unavailable
    - Rate limiting protection
    - Structured error handling
    - Response caching (optional)
    """
    
    def __init__(self):
        # Re-read API key fresh (in case .env was loaded after initial import)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4-turbo"
        self.fallback_delay = 1.5
        self._client = None
        self._initialized = False
        
        # Debug logging
        if self.api_key:
            masked_key = self.api_key[:8] + "..." + self.api_key[-4:] if len(self.api_key) > 12 else "***"
            logger.info(f"AI Service: API key found ({masked_key})")
        else:
            logger.warning("AI Service: No OPENAI_API_KEY found in environment")
    
    def reload_api_key(self):
        """Reload API key from environment (useful after .env changes)."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self._client = None
        self._initialized = False
        return self.api_key is not None
    
    @property
    def client(self):
        """Lazy initialization of OpenAI client."""
        if not self._initialized:
            self._initialized = True
            # Re-check API key in case it was set after __init__
            if not self.api_key:
                self.api_key = os.getenv("OPENAI_API_KEY")
            
            if self.api_key:
                try:
                    import openai
                    self._client = openai.OpenAI(api_key=self.api_key)
                    logger.info("OpenAI client initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize OpenAI client: {e}")
                    self._client = None
        return self._client
    
    @property
    def is_available(self) -> bool:
        """Check if AI API is available."""
        return self.client is not None
    
    def generate(
        self,
        prompt: str,
        response_type: ResponseType = ResponseType.GENERAL,
        max_tokens: int = 4000,
        temperature: float = 0.7
    ) -> AIResponse:
        """
        Generate AI response with automatic fallback.
        
        Args:
            prompt: The prompt to send to the AI
            response_type: Type of response for fallback
            max_tokens: Maximum tokens in response
            temperature: Creativity parameter (0-1)
            
        Returns:
            AIResponse with content and metadata
        """
        # Try API first
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                content = response.choices[0].message.content
                logger.info(f"AI response generated successfully ({len(content)} chars)")
                return AIResponse(
                    content=content,
                    success=True,
                    source="api",
                    model=self.model
                )
            except Exception as e:
                error_msg = str(e)
                logger.warning(f"AI API error: {error_msg}")
                
                # Check for specific error types
                if "rate_limit" in error_msg.lower() or "429" in error_msg:
                    logger.warning("Rate limit hit, using fallback")
                elif "insufficient_quota" in error_msg.lower():
                    logger.warning("API quota exceeded, using fallback")
                
                return self._get_fallback_response(response_type, error_msg)
        
        # No API available, use fallback
        logger.info("No API key available, using fallback response")
        return self._get_fallback_response(response_type)
    
    def _get_fallback_response(
        self,
        response_type: ResponseType,
        error: str = None
    ) -> AIResponse:
        """Get a mock fallback response."""
        # Simulate processing time
        time.sleep(self.fallback_delay)
        
        content = MOCK_RESPONSES.get(response_type, MOCK_RESPONSES[ResponseType.GENERAL])
        
        return AIResponse(
            content=content,
            success=True,
            source="fallback",
            model="simulation",
            error=error
        )
    
    def generate_strategy(self, context: Dict[str, Any]) -> AIResponse:
        """
        Generate a strategic roadmap.
        
        Args:
            context: Dictionary with org details, domain, frameworks, etc.
            
        Returns:
            AIResponse with strategy content
        """
        prompt = self._build_strategy_prompt(context)
        return self.generate(prompt, ResponseType.STRATEGY)
    
    def generate_policy(
        self,
        policy_name: str,
        domain: str,
        framework: str,
        language: str = "English"
    ) -> AIResponse:
        """
        Generate a policy document.
        
        Args:
            policy_name: Name of the policy
            domain: Domain (cyber, data, ai, etc.)
            framework: Reference framework
            language: Output language
            
        Returns:
            AIResponse with policy content
        """
        lang_instruction = self._get_language_instruction(language)
        
        prompt = f"""
ACT AS: Lead Policy Consultant acting as Your AI Advisor.
DRAFT: {policy_name}.
DOMAIN: {domain}.
REF: {framework}.
{lang_instruction}

STRUCTURE:
1. Policy Statement
2. Scope & Applicability
3. Definitions
4. Roles & Responsibilities
5. Compliance Requirements
6. Enforcement
7. Review & Updates
"""
        return self.generate(prompt, ResponseType.POLICY)
    
    def generate_audit_report(
        self,
        standard: str,
        evidence_text: str,
        language: str = "English"
    ) -> AIResponse:
        """
        Generate an audit report based on evidence.
        
        Args:
            standard: Audit standard/framework
            evidence_text: Extracted text from evidence documents
            language: Output language
            
        Returns:
            AIResponse with audit findings
        """
        # Truncate evidence to prevent token overflow
        max_evidence = 10000
        if len(evidence_text) > max_evidence:
            evidence_text = evidence_text[:max_evidence] + "\n[...truncated...]"
        
        prompt = f"""
ACT AS: Senior Lead Auditor (Your AI Advisor).
STANDARD: {standard}.
REVIEW THE FOLLOWING EVIDENCE:
{evidence_text}

OUTPUT FORMAT:
1. Executive Summary
2. Scope & Methodology
3. Key Findings (Observations, Non-Conformities)
4. Gap Analysis
5. Recommendations
6. Conclusion

TONE: Formal, authoritative, objective.
"""
        return self.generate(prompt, ResponseType.AUDIT)
    
    def generate_risk_analysis(
        self,
        domain: str,
        threat: str,
        asset: str,
        context: Dict[str, Any]
    ) -> AIResponse:
        """
        Generate risk analysis and mitigation recommendations.
        
        Args:
            domain: Risk domain
            threat: Threat/risk scenario
            asset: Affected asset
            context: Additional context (controls, deployment, etc.)
            
        Returns:
            AIResponse with risk analysis
        """
        prompt = f"""
ACT AS: Chief Risk Officer / Security Advisor.
DOMAIN: {domain}.
RISK SCENARIO: {threat} targeting {asset}.
DEPLOYMENT CONTEXT: {context.get('deployment', 'Unknown')}.
CURRENT CONTROLS: {context.get('controls', 'None specified')}.
ADDITIONAL CONTEXT: {context.get('notes', 'None')}.

OUTPUT:
1. **Risk Analysis**: Severity assessment and specific attack vectors/failure modes.
2. **Impact Assessment**: Business impact if risk materializes.
3. **Strategic Mitigation Plan**:
    - Immediate Actions (0-3 Months): Specific technical configurations.
    - Medium-Term (3-6 Months): Process improvements.
    - Long-Term Resilience (6+ Months): Architecture changes.
4. **Key Risk Indicators (KRIs)**: Metrics to monitor.
"""
        return self.generate(prompt, ResponseType.RISK)
    
    def _build_strategy_prompt(self, context: Dict[str, Any]) -> str:
        """Build a comprehensive strategy prompt."""
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
        roadmap_data = context.get('roadmap_data', [])
        
        lang_instruction = self._get_language_instruction(language)
        
        return f"""
ACT AS: Lead Strategy Partner acting as Your AI Advisor.
CLIENT: {org_name} ({sector}, {size}).
DOMAIN: {domain}.
FRAMEWORKS: {frameworks}.
INPUTS:
- Technology: {tech}
- Challenges: {challenges}
- Budget: {budget}
- Horizon: {horizon} months.

OBJECTIVE: Develop a world-class, executive-level strategic roadmap.
TONE: Authoritative, sophisticated, actionable. No fluff.

{lang_instruction}

STRUCTURED DATA (Use to inform strategy, do not output raw):
- Gaps: {str(gap_data)[:2000]}
- Roadmap Draft: {str(roadmap_data)[:2000]}

REQUIRED OUTPUT FORMAT (Strictly 6 sections separated by '|||'):

1. Executive Vision & Strategic Objectives |||
    - Compelling vision statement.
    - 3-5 strategic objectives (e.g., "Achieve Cyber Resilience").
    - Content ONLY. No header.

2. Current State Assessment (Gap Analysis) |||
    - Maturity posture summary based on gaps.
    - Critical risks.
    - Content ONLY. No header.

3. Strategic Pillars & Initiatives |||
    - 3-5 Strategic Pillars (e.g., "Zero Trust Architecture").
    - Specific high-impact initiatives.
    - Content ONLY. No header.

4. Implementation Roadmap |||
    - Markdown Table columns: | Phase | Initiative | Duration (Months) | Cost (SAR) | Owner | KPI |.
    - Specific values based on client size/budget.

5. Measuring Success (KPIs & KRIs) |||
    - Key metrics (e.g., "Compliance %", "MTTR").
    - Content ONLY.

6. Confidence Score & Fact Check
    - Score (0-100%) and validation.

IMPORTANT:
- DO NOT repeat section titles in the output body.
- If Bilingual, every paragraph must be English then Arabic.
"""
    
    def _get_language_instruction(self, language: str) -> str:
        """Get language instruction for prompts."""
        if language in ["Bilingual", "ثنائي اللغة"]:
            return (
                "Language: Bilingual (Side-by-Side). MANDATORY: "
                "Provide English text followed immediately by Arabic translation for every section."
            )
        elif language in ["Arabic", "العربية"]:
            return "Language: Arabic. Output all content in Arabic."
        return f"Language: {language}."


# =============================================================================
# MOCK RESPONSES FOR FALLBACK
# =============================================================================

MOCK_RESPONSES = {
    ResponseType.STRATEGY: """
**Executive Vision & Strategic Objectives** |||
**Vision:** To build a resilient, data-driven cybersecurity posture that enables digital trust and business agility.
**Strategic Objectives:**
1. Achieve 100% compliance with NCA/SAMA mandates within 18 months.
2. Establish a 24/7 proactive SOC monitoring capability.
3. Embed security-by-design into all digital transformation initiatives.

**الرؤية التنفيذية:**
بناء موقف أمن سيبراني مرن ومعتمد على البيانات يمكّن الثقة الرقمية ومرونة الأعمال.
**الأهداف الاستراتيجية:**
1. تحقيق الامتثال بنسبة 100% لمتطلبات الهيئة الوطنية للأمن السيبراني/ساما خلال 18 شهرًا.
2. إنشاء قدرة مراقبة استباقية لمركز العمليات الأمنية (SOC) على مدار الساعة طوال أيام الأسبوع.
3. دمج "الأمن حسب التصميم" في جميع مبادرات التحول الرقمي.
|||
**Current State Assessment (Gap Analysis)** |||
**Maturity Level:** Initial (Tier 1).
**Key Findings:**
- Governance: Policies exist but are not enforced or measured.
- Technical: Lack of MFA on critical systems and no centralized logging.
- Risk: Third-party risk is currently unmanaged.

**تقييم الوضع الحالي (تحليل الفجوات):**
**مستوى النضج:** أولي (المستوى 1).
**النتائج الرئيسية:**
- الحوكمة: السياسات موجودة ولكنها غير مطبقة أو مقاسة.
- التقنية: نقص المصادقة متعددة العوامل (MFA) على الأنظمة الحساسة وعدم وجود تسجيل مركزي.
- المخاطر: مخاطر الأطراف الثالثة غير مُدارة حاليًا.
|||
**Strategic Pillars & Initiatives** |||
1. **Governance & Compliance:** Formalize the GRC framework and policy lifecycle.
2. **Identity First:** Implement Zero Trust principles starting with IAM/MFA.
3. **Cyber Defense:** Build a hybrid SOC for real-time threat detection.
4. **Data Privacy:** Classify all data assets and implement DLP controls.

1. **الحوكمة والامتثال:** مأسسة إطار الحوكمة والمخاطر والامتثال ودورة حياة السياسات.
2. **الهوية أولاً:** تطبيق مبادئ الثقة الصفرية بدءًا من إدارة الهوية والوصول (IAM) والمصادقة متعددة العوامل (MFA).
3. **الدفاع السيبراني:** بناء مركز عمليات أمنية (SOC) هجين للكشف عن التهديدات في الوقت الفعلي.
4. **خصوصية البيانات:** تصنيف جميع أصول البيانات وتطبيق ضوابط منع فقدان البيانات (DLP).
|||
Phase | Initiative | Duration | Cost | Role | KPI
0–3 months | Establish Governance Framework | 3 | 400000 | GRC Lead | Policy Approval %
0–3 months | Implement MFA & IAM Baseline | 4 | 850000 | IAM Lead | Identity Coverage %
3–12 months | Deploy SIEM & SOC Level 1 | 9 | 1500000 | SOC Mgr | MTTD / MTTR
12–36 months | Zero Trust Network Architecture | 18 | 2500000 | Chief Arch | Segmentation %
|||
**Measuring Success (KPIs & KRIs)** |||
- **Compliance Score:** Target 95% by Q4.
- **Mean Time to Detect (MTTD):** < 1 hour.
- **Critical Risk Remediation:** < 48 hours.

**قياس النجاح (مؤشرات الأداء الرئيسية):**
- **درجة الامتثال:** استهداف 95% بحلول الربع الرابع.
- **متوسط وقت الكشف (MTTD):** أقل من ساعة واحدة.
- **معالجة المخاطر الحرجة:** أقل من 48 ساعة.
|||
**Confidence Score & Fact Check**
Confidence: 90% (Simulated Mode).
This output is generated from selected framework packs and rule-based mappings.
""",

    ResponseType.POLICY: """
**1. Purpose**
The purpose of this Policy is to establish the rules for granting, reviewing, and revoking access to organizational information systems and data assets.

**2. Scope**
This policy applies to all employees, contractors, consultants, and third-party users who access organizational systems, networks, or data.

**3. Definitions**
- **Access Control:** Security measures that regulate who can view or use resources.
- **Privileged Access:** Administrative or elevated access rights.
- **MFA:** Multi-Factor Authentication requiring two or more verification methods.

**4. Policy Statement**
- Access shall be granted on a "Need-to-Know" and "Least Privilege" basis.
- Multi-Factor Authentication (MFA) is mandatory for all remote access and privileged accounts.
- User access rights must be reviewed quarterly by data/system owners.
- All access must be logged and monitored for security events.

**5. Roles & Responsibilities**
- **IT Security:** Implement and maintain access control systems.
- **System Owners:** Approve and review access to their systems.
- **Users:** Protect credentials and report suspicious activity.
- **HR:** Notify IT of employee status changes.

**6. Compliance Requirements**
- Violations may result in disciplinary action up to termination.
- Regular audits will be conducted to ensure compliance.

**7. Review & Updates**
This policy shall be reviewed annually or upon significant changes to the organization or threat landscape.
""",

    ResponseType.AUDIT: """
**Audit Report: Compliance Assessment**

**1. Executive Summary**
The review of the provided evidence indicates a partial compliance status with the target framework. Several critical gaps were identified in governance documentation, access control evidence, and monitoring capabilities.

**2. Scope & Methodology**
- Document review of submitted evidence
- Control mapping against framework requirements
- Gap identification and risk rating

**3. Key Findings**

**Finding 1: Incomplete Access Review Evidence**
- **Severity:** High
- **Observation:** No evidence of quarterly access reviews was found (Control: IAM-04).
- **Risk:** Excessive privileges may accumulate, increasing insider threat risk.
- **Recommendation:** Implement automated quarterly access certification process.

**Finding 2: Password Policy Gap**
- **Severity:** Medium
- **Observation:** Password complexity requirements do not meet the 12-character minimum standard.
- **Risk:** Increased vulnerability to brute force attacks.
- **Recommendation:** Update password policy and enforce via technical controls.

**Finding 3: Logging Deficiency**
- **Severity:** High
- **Observation:** Security logs are retained for only 30 days vs. required 12 months.
- **Risk:** Unable to investigate incidents beyond 30 days.
- **Recommendation:** Extend log retention to 12+ months with SIEM integration.

**4. Gap Analysis Summary**
- Compliant Controls: 65%
- Partial Compliance: 20%
- Non-Compliant: 15%

**5. Recommendations Priority**
1. Immediate (0-30 days): Address access review and logging gaps
2. Short-term (30-90 days): Update password policies
3. Medium-term (90-180 days): Implement comprehensive monitoring

**6. Conclusion**
The organization demonstrates foundational security practices but requires significant improvement in evidence collection and control validation to achieve full compliance.
""",

    ResponseType.RISK: """
**Risk Analysis Report**

**1. Risk Summary**
The identified threat poses a significant risk to the target asset. Based on the deployment context and existing controls, the current risk level is assessed as **HIGH**.

**2. Impact Assessment**
- **Confidentiality:** Potential data exposure affecting sensitive information
- **Integrity:** Risk of unauthorized modifications
- **Availability:** Service disruption possible
- **Financial:** Estimated impact range: SAR 500K - 2M
- **Reputational:** Significant brand damage if exploited

**3. Strategic Mitigation Plan**

**Immediate Actions (0-3 Months):**
1. Isolate the affected asset from the main network segment
2. Apply critical patches immediately or enable virtual patching via WAF
3. Implement enhanced monitoring and alerting
4. Conduct emergency access review for affected systems

**Medium-Term Actions (3-6 Months):**
1. Deploy additional security controls (EDR, DLP as applicable)
2. Implement network segmentation improvements
3. Conduct security awareness training for relevant teams
4. Establish incident response procedures specific to this risk

**Long-Term Actions (6+ Months):**
1. Implement permanent architectural fix (e.g., replace legacy systems)
2. Deploy Zero Trust architecture principles
3. Conduct full penetration test to verify remediation
4. Integrate into continuous risk monitoring program

**4. Key Risk Indicators (KRIs)**
- Number of unpatched critical vulnerabilities
- Mean time to patch critical systems
- Number of unauthorized access attempts
- Security incident count related to this threat vector

**5. Residual Risk**
After implementing recommended controls, residual risk is expected to be **LOW-MEDIUM**.
""",

    ResponseType.GENERAL: """
Thank you for your query. I'm operating in simulation mode as the AI API is currently unavailable.

For production use, please ensure:
1. A valid OPENAI_API_KEY is set in the environment
2. The API quota has not been exceeded
3. Network connectivity to OpenAI services is available

In the meantime, I can provide guidance based on established best practices and frameworks.
"""
}


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

ai_service = AIService()
