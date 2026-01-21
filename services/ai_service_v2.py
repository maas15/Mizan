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
        temperature: float = 0.7
    ) -> AIResponse:
        """Generate AI response with fallback support."""
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an elite management consultant from a Big 4 firm (Deloitte/PwC/EY/KPMG) specializing in GRC, cybersecurity, and digital transformation strategy."},
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
                return self._get_fallback_response(response_type, error_msg)
        
        logger.info("No API key available, using fallback response")
        return self._get_fallback_response(response_type)
    
    def _get_fallback_response(
        self,
        response_type: ResponseType,
        error: str = None
    ) -> AIResponse:
        """Get a mock fallback response."""
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
        """Generate a Big4-level strategic roadmap."""
        prompt = self._build_strategy_prompt(context)
        return self.generate(prompt, ResponseType.STRATEGY, max_tokens=4500, temperature=0.6)
    
    def generate_policy(
        self,
        policy_name: str,
        domain: str,
        framework: str,
        language: str = "English"
    ) -> AIResponse:
        """Generate a comprehensive policy document."""
        prompt = self._build_policy_prompt(policy_name, domain, framework, language)
        return self.generate(prompt, ResponseType.POLICY, max_tokens=3500, temperature=0.5)
    
    def generate_audit_report(
        self,
        standard: str,
        evidence_text: str,
        language: str = "English"
    ) -> AIResponse:
        """Generate an audit report based on evidence."""
        max_evidence = 10000
        if len(evidence_text) > max_evidence:
            evidence_text = evidence_text[:max_evidence] + "\n[...truncated...]"
        
        prompt = f"""
أنت مدقق رئيسي أول في إحدى شركات الأربعة الكبار (Big 4). راجع الأدلة التالية وقدم تقرير تدقيق احترافي.

ACT AS: Senior Lead Auditor from a Big 4 firm (Deloitte/PwC/EY/KPMG).
STANDARD: {standard}.
REVIEW THE FOLLOWING EVIDENCE:
{evidence_text}

OUTPUT FORMAT:
1. Executive Summary (الملخص التنفيذي)
2. Scope & Methodology (النطاق والمنهجية)
3. Key Findings - Observations & Non-Conformities (النتائج الرئيسية)
4. Gap Analysis Matrix (مصفوفة تحليل الفجوات)
5. Risk-Prioritized Recommendations (التوصيات حسب الأولوية)
6. Management Action Plan (خطة العمل الإدارية)
7. Conclusion & Opinion (الخلاصة والرأي)

TONE: Formal, authoritative, objective, professional.
{"LANGUAGE: Arabic (اللغة العربية). اكتب التقرير كاملاً باللغة العربية مع مصطلحات تقنية دقيقة." if language in ["Arabic", "العربية"] else f"LANGUAGE: {language}"}
"""
        return self.generate(prompt, ResponseType.AUDIT)
    
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
        """Build a Big4-level strategy prompt."""
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
        
        lang_instruction = self._get_language_instruction(language)
        section_titles = self._get_section_titles(language)
        
        return f"""
أنت شريك استراتيجي أول من إحدى شركات الأربعة الكبار (McKinsey/Deloitte/PwC/BCG) متخصص في {domain}.

ACT AS: Senior Strategy Partner from a top-tier consulting firm (McKinsey, Deloitte, PwC, BCG) specializing in {domain}.

CLIENT PROFILE:
- Organization: {org_name}
- Sector: {sector}
- Size: {size}
- Target Frameworks: {', '.join(frameworks) if frameworks else 'Best Practices'}

CURRENT STATE:
- Technology Stack: {tech if tech else 'Not specified'}
- Key Challenges: {challenges if challenges else 'Not specified'}
- Budget Range: {budget}
- Strategic Horizon: {horizon} months

GAP ANALYSIS DATA:
- Compliance Score: {gap_data.get('compliance_score', 'N/A')}%
- Gap Count: {gap_data.get('gap_count', 'N/A')}
- Top Gap Areas: {gap_data.get('top_gap_controls', {})}

{lang_instruction}

DELIVERABLE: Executive-grade strategic roadmap that would be presented to a Board of Directors.

QUALITY STANDARDS:
- Write in the authoritative, insight-driven style of Big 4 strategy documents
- Include specific, measurable recommendations (not generic advice)
- Provide realistic cost estimates in SAR based on organization size
- Include industry benchmarks and best practices
- Balance ambition with pragmatic execution

REQUIRED OUTPUT FORMAT (6 sections separated by '|||'):

**{section_titles['vision']}** |||
- Compelling 2-3 sentence vision statement that inspires action
- 4-5 SMART strategic objectives with clear success criteria
- Strategic themes aligned with {domain} best practices
- Link to business value and competitive advantage

**{section_titles['gaps']}** |||
- Current maturity level assessment (using recognized maturity models)
- Critical gaps prioritized by risk and impact
- Benchmark comparison against industry peers
- Root cause analysis of key gaps
- Quick wins vs. strategic investments

**{section_titles['pillars']}** |||
- 4-5 Strategic Pillars with clear rationale
- For each pillar: 2-3 specific initiatives with outcomes
- Dependencies and sequencing considerations
- Resource requirements (people, technology, budget)
- Expected benefits and value drivers

**{section_titles['roadmap']}** |||
Provide a detailed implementation roadmap as a Markdown table:

| Phase | Initiative | Duration (Months) | Investment (SAR) | Owner/Role | Success KPI |
|-------|------------|-------------------|------------------|------------|-------------|
| Phase 1: Foundation (0-6 months) | ... | ... | ... | ... | ... |
| Phase 2: Build (6-18 months) | ... | ... | ... | ... | ... |
| Phase 3: Optimize (18-36 months) | ... | ... | ... | ... | ... |

Include 8-12 initiatives with realistic estimates based on {size} organization.

**{section_titles['kpis']}** |||
- 6-8 Key Performance Indicators (KPIs) with targets
- 4-6 Key Risk Indicators (KRIs) with thresholds
- Governance and reporting cadence
- Balanced scorecard approach (Financial, Customer, Process, Learning)

**{section_titles['confidence']}** |||
- Confidence Score: X/100
- Key assumptions and dependencies
- Risk factors that could impact success
- Recommended next steps

CRITICAL INSTRUCTIONS:
- DO NOT include section headers in the output text (they are for structure only)
- Each section must be substantial (150-300 words minimum)
- Be specific to {domain} domain, not generic business advice
- Use professional consulting language
"""
    
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
# MOCK RESPONSES FOR FALLBACK
# =============================================================================

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
