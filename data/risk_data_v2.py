"""
Sentinel GRC - Risk Knowledge Bases
Domain-specific risk data for Cyber, AI, Data Management, Digital Transformation, and Global Standards.
"""

from typing import Dict, List


# =============================================================================
# CYBER SECURITY RISK DATA
# =============================================================================

CYBER_RISK_DATA: Dict[str, Dict] = {
    "1. Threat Actor Risks": {
        "risks": [
            "Cybercrime groups (Ransomware)",
            "Nation-state/APT espionage",
            "Malicious Insiders",
            "Third-party vendor compromise"
        ],
        "mitigations": "Threat intel, access governance, background checks, TPRM."
    },
    "2. Identity & Access (IAM)": {
        "risks": [
            "Stolen credentials",
            "Weak MFA / MFA Fatigue",
            "Excessive privileges",
            "Orphan accounts",
            "Service account leakage"
        ],
        "mitigations": "Phishing-resistant MFA, Least Privilege, PAM, Secrets Management."
    },
    "3. Phishing & Social Engineering": {
        "risks": [
            "Email phishing / Spear phishing",
            "Business Email Compromise (BEC)",
            "Smishing/Vishing",
            "Deepfake impersonation"
        ],
        "mitigations": "User awareness, Email Security (DMARC), Anti-impersonation controls."
    },
    "4. Malware & Ransomware": {
        "risks": [
            "Endpoint compromise",
            "Data exfiltration + Encryption",
            "Lateral movement (Worms)",
            "Destructive wipers"
        ],
        "mitigations": "EDR/XDR, Patching, Network Segmentation, Immutable Backups."
    },
    "5. Vulnerability & Patching": {
        "risks": [
            "Unpatched systems",
            "End-of-life software",
            "Zero-day exploitation",
            "Weak prioritization"
        ],
        "mitigations": "Asset inventory, Vuln scanning, Risk-based patching, Virtual Patching (WAF)."
    },
    "6. Network & Perimeter": {
        "risks": [
            "Lateral movement (Flat network)",
            "Weak segmentation",
            "Unsecured DNS/HTTP",
            "Man-in-the-middle"
        ],
        "mitigations": "Zero Trust Network Access (ZTNA), Segmentation, TLS everywhere, NAC."
    },
    "7. Data Protection": {
        "risks": [
            "Data leakage (DLP failure)",
            "Poor encryption (Rest/Transit)",
            "Weak key management",
            "Unsafe sharing"
        ],
        "mitigations": "Data classification, Encryption, KMS/HSM, DLP, Access reviews."
    },
    "8. Third-Party & Supply Chain": {
        "risks": [
            "Vendor breach",
            "Compromised software updates",
            "Shared credentials",
            "Poor contracts"
        ],
        "mitigations": "Vendor due diligence, Security clauses, Continuous monitoring."
    },
}


# =============================================================================
# AI RISK DATA
# =============================================================================

AI_RISK_DATA: Dict[str, Dict] = {
    "1. Model Performance & Quality": {
        "risks": [
            "Model accuracy degradation over time",
            "Hallucinations and factual errors",
            "Context window limitations",
            "Non-deterministic outputs",
            "Domain mismatch / Out-of-distribution inputs"
        ],
        "mitigations": "Continuous evaluation, human-in-the-loop, grounded RAG, acceptance testing, drift monitoring."
    },
    "2. Bias & Fairness": {
        "risks": [
            "Algorithmic bias in decisions",
            "Discriminatory outcomes",
            "Underrepresentation in training data",
            "Reinforcing historical biases",
            "Disparate impact on protected groups"
        ],
        "mitigations": "Pre/post-deployment fairness testing, diverse training data, bias audits, restricted high-risk use cases."
    },
    "3. Privacy & Data Governance": {
        "risks": [
            "PII exposure in model outputs",
            "Training data privacy violations",
            "Unintentional data memorization",
            "Re-identification risks",
            "Cross-border data transfer issues"
        ],
        "mitigations": "Data classification, PII masking/tokenization, differential privacy, strict retention policies."
    },
    "4. Security & Adversarial": {
        "risks": [
            "Prompt injection attacks",
            "Jailbreak attempts",
            "Data exfiltration via RAG/plugins",
            "Model supply chain compromise",
            "Adversarial input manipulation"
        ],
        "mitigations": "Input/output guardrails, content filtering, red teaming, model provenance verification."
    },
    "5. Legal & Regulatory": {
        "risks": [
            "EU AI Act non-compliance",
            "IP/Copyright infringement",
            "Liability for AI decisions",
            "Lack of explainability (XAI)",
            "Consent and transparency gaps"
        ],
        "mitigations": "Legal review workflows, AI labeling, decision logging, impact assessments, SDAIA alignment."
    },
    "6. Ethical & Safety": {
        "risks": [
            "Harmful content generation",
            "Deepfake creation/misuse",
            "Social engineering automation",
            "Autonomous decision-making risks",
            "Unintended societal impacts"
        ],
        "mitigations": "Content policies, usage monitoring, rate limiting, watermarking, kill switches, ethics review."
    },
    "7. Operational & Business": {
        "risks": [
            "Vendor lock-in / API dependency",
            "Cost overruns (token usage)",
            "Latency and availability issues",
            "Skills gap in AI operations",
            "Shadow AI usage"
        ],
        "mitigations": "Multi-vendor strategy, cost monitoring, SLAs, MLOps training, AI governance policy."
    },
}


# =============================================================================
# DATA MANAGEMENT RISK DATA
# =============================================================================

DATA_RISK_DATA: Dict[str, Dict] = {
    "1. Data Governance & Ownership": {
        "risks": [
            "Unclear data ownership/accountability",
            "Policy gaps (retention/sharing)",
            "Weak data standards",
            "Inconsistent definitions across teams"
        ],
        "mitigations": "Governance model (RACI), data policies, enterprise standards, stewardship program."
    },
    "2. Data Quality & Integrity": {
        "risks": [
            "Inaccurate/incomplete data",
            "Data duplication / poor MDM",
            "ETL/Transformation errors",
            "Inconsistent formats"
        ],
        "mitigations": "Data quality rules, validation at entry, DQ monitoring, Master Data Management."
    },
    "3. Privacy & Confidentiality": {
        "risks": [
            "PII/PHI exposure",
            "Over-collection of sensitive data",
            "Re-identification of anonymized data",
            "Improper third-party sharing"
        ],
        "mitigations": "Data classification, minimization, masking/tokenization, DPIAs, audit logging."
    },
    "4. Compliance & Regulatory": {
        "risks": [
            "PDPL/GDPR violations",
            "Retention violations",
            "Cross-border transfer non-compliance",
            "Audit failures (lineage gaps)"
        ],
        "mitigations": "Retention schedules, legal holds, data residency controls, compliance mapping."
    },
    "5. Architecture & Integration": {
        "risks": [
            "Data silos",
            "Fragile ETL pipelines",
            "Schema versioning issues",
            "API integration failures"
        ],
        "mitigations": "Architecture standards, integration patterns, schema governance, automated testing."
    },
    "6. Metadata & Lineage": {
        "risks": [
            "No data catalog (low discoverability)",
            "Unknown lineage (trust issues)",
            "Poor documentation",
            "Key person dependency"
        ],
        "mitigations": "Data catalog implementation, automated lineage tools, documentation standards."
    },
}


# =============================================================================
# DIGITAL TRANSFORMATION RISK DATA
# =============================================================================

DT_RISK_DATA: Dict[str, Dict] = {
    "1. Strategy & Vision Risks": {
        "risks": [
            "Unclear digital vision / misalignment with business strategy",
            "Lack of executive sponsorship",
            "Conflicting priorities across departments",
            "No clear success metrics defined",
            "Digital strategy not communicated effectively"
        ],
        "mitigations": "Executive alignment workshops, digital strategy roadmap, OKR framework, communication plan."
    },
    "2. Program & Project Delivery": {
        "risks": [
            "Project delays and cost overruns",
            "Scope creep / requirements volatility",
            "Poor project governance",
            "Resource constraints / skill gaps",
            "Vendor delivery failures"
        ],
        "mitigations": "Agile delivery, PMO governance, change control process, capacity planning, vendor SLAs."
    },
    "3. Change Management & Adoption": {
        "risks": [
            "User resistance to new systems",
            "Inadequate training and support",
            "Cultural barriers to change",
            "Low adoption rates post-launch",
            "Middle management resistance"
        ],
        "mitigations": "Change impact assessment, stakeholder engagement, training programs, change champions network."
    },
    "4. Technology & Integration": {
        "risks": [
            "Legacy system integration challenges",
            "Technical debt accumulation",
            "Platform/vendor lock-in",
            "Interoperability issues",
            "Scalability limitations"
        ],
        "mitigations": "Architecture assessment, API-first approach, multi-cloud strategy, technical debt remediation."
    },
    "5. Data Migration & Quality": {
        "risks": [
            "Data loss during migration",
            "Data quality degradation",
            "Incomplete data mapping",
            "Extended cutover windows",
            "Historical data accessibility issues"
        ],
        "mitigations": "Migration strategy, data profiling, mock migrations, rollback plans, data validation."
    },
    "6. Business Continuity": {
        "risks": [
            "Service disruption during transformation",
            "Parallel running challenges",
            "Business process gaps",
            "Customer impact during transition",
            "Operational knowledge loss"
        ],
        "mitigations": "Continuity planning, phased rollouts, fallback procedures, customer communication."
    },
    "7. Value Realization": {
        "risks": [
            "Benefits not achieved as planned",
            "ROI not measurable",
            "Time-to-value exceeds expectations",
            "Opportunity cost of delayed delivery",
            "Benefits leakage post-implementation"
        ],
        "mitigations": "Benefits tracking framework, value dashboards, post-implementation reviews, continuous optimization."
    },
    "8. Governance & Operating Model": {
        "risks": [
            "Unclear accountability for digital assets",
            "Siloed digital initiatives",
            "No enterprise architecture governance",
            "Shadow IT proliferation",
            "Inconsistent standards across programs"
        ],
        "mitigations": "Digital governance framework, EA board, standards enforcement, portfolio management."
    },
}


# =============================================================================
# GLOBAL STANDARDS RISK DATA (ISO, ITIL, Quality Management)
# =============================================================================

GLOBAL_RISK_DATA: Dict[str, Dict] = {
    "1. Certification & Compliance": {
        "risks": [
            "Audit non-conformities (Major/Minor)",
            "Certification suspension or withdrawal",
            "Surveillance audit failures",
            "Gap between documented and actual practices",
            "Multi-standard integration conflicts"
        ],
        "mitigations": "Internal audit program, management reviews, gap assessments, pre-certification audits."
    },
    "2. Management System Effectiveness": {
        "risks": [
            "Management system not embedded in operations",
            "Policies not followed in practice",
            "Lack of continuous improvement culture",
            "Corrective actions not effective",
            "Management review not driving improvement"
        ],
        "mitigations": "Process ownership, KPI monitoring, PDCA cycle enforcement, leadership engagement."
    },
    "3. Documentation & Records": {
        "risks": [
            "Outdated or inaccurate documentation",
            "Missing mandatory records",
            "Poor document version control",
            "Inaccessible records during audits",
            "Non-standard document formats"
        ],
        "mitigations": "Document management system, retention schedules, version control, audit preparation."
    },
    "4. Resource & Competency": {
        "risks": [
            "Inadequate staff competency",
            "Training records gaps",
            "Key person dependency",
            "Insufficient resources for management system",
            "Awareness gaps across organization"
        ],
        "mitigations": "Competency framework, training needs analysis, succession planning, awareness programs."
    },
    "5. Business Continuity (ISO 22301)": {
        "risks": [
            "BIA not current or comprehensive",
            "Recovery strategies not tested",
            "RTO/RPO objectives not achievable",
            "Crisis communication gaps",
            "Supply chain continuity risks"
        ],
        "mitigations": "Annual BIA review, regular exercises, recovery capability testing, communication plans."
    },
    "6. Service Management (ITIL)": {
        "risks": [
            "SLA breaches",
            "Incident management failures",
            "Change-related outages",
            "Knowledge management gaps",
            "Service desk performance issues"
        ],
        "mitigations": "Service level monitoring, incident process improvement, CAB governance, knowledge base."
    },
    "7. Quality Management (ISO 9001)": {
        "risks": [
            "Customer complaints trending up",
            "Product/service non-conformities",
            "Supplier quality issues",
            "Process capability declining",
            "Customer satisfaction declining"
        ],
        "mitigations": "Customer feedback analysis, supplier audits, statistical process control, quality objectives."
    },
    "8. External & Regulatory": {
        "risks": [
            "New standard versions requiring transition",
            "Regulatory changes affecting compliance",
            "Industry-specific requirements gaps",
            "Customer/contractual requirements changes",
            "Accreditation body requirements"
        ],
        "mitigations": "Standards monitoring, regulatory tracking, customer requirements review, transition planning."
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_risk_data(domain_code: str) -> Dict[str, Dict]:
    """
    Get risk data for a specific domain.
    
    Args:
        domain_code: Domain code (cyber, ai, data, dt, global)
        
    Returns:
        Dict with risk categories and their risks/mitigations
    """
    mapping = {
        "cyber": CYBER_RISK_DATA,
        "ai": AI_RISK_DATA,
        "data": DATA_RISK_DATA,
        "dt": DT_RISK_DATA,
        "global": GLOBAL_RISK_DATA
    }
    return mapping.get(domain_code, CYBER_RISK_DATA)


def get_all_risk_categories(domain_code: str) -> List[str]:
    """Get list of risk categories for a domain."""
    risk_data = get_risk_data(domain_code)
    return list(risk_data.keys())


def get_risks_for_category(domain_code: str, category: str) -> List[str]:
    """Get specific risks for a category."""
    risk_data = get_risk_data(domain_code)
    if category in risk_data:
        return risk_data[category].get("risks", [])
    return []


def get_mitigations_for_category(domain_code: str, category: str) -> str:
    """Get mitigations for a category."""
    risk_data = get_risk_data(domain_code)
    if category in risk_data:
        return risk_data[category].get("mitigations", "Standard controls")
    return "Standard controls"
