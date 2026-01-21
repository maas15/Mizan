"""
Sentinel GRC - Risk Knowledge Bases
Domain-specific risk data for Cyber, AI, and Data Management.
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
    "6. Misconfiguration & Hardening": {
        "risks": [
            "Open cloud buckets",
            "Exposed admin panels",
            "Over-permissive firewalls",
            "Insecure RDP/VPN"
        ],
        "mitigations": "CIS Benchmarks, CSPM, IaC scanning, Change Control."
    },
    "7. Application & API Security": {
        "risks": [
            "OWASP Top 10 (Injection, etc.)",
            "API abuse / Broken Auth",
            "Insecure dependencies",
            "CI/CD compromise"
        ],
        "mitigations": "Secure SDLC, SAST/DAST, WAF/API Gateway, SBOM, Secret Scanning."
    },
    "8. Network & Perimeter": {
        "risks": [
            "Lateral movement (Flat network)",
            "Weak segmentation",
            "Unsecured DNS/HTTP",
            "Man-in-the-middle"
        ],
        "mitigations": "Zero Trust Network Access (ZTNA), Segmentation, TLS everywhere, NAC."
    },
    "9. Data Protection": {
        "risks": [
            "Data leakage (DLP failure)",
            "Poor encryption (Rest/Transit)",
            "Weak key management",
            "Unsafe sharing"
        ],
        "mitigations": "Data classification, Encryption, KMS/HSM, DLP, Access reviews."
    },
    "10. Monitoring & Detection": {
        "risks": [
            "Lack of visibility (No logs)",
            "Alert fatigue",
            "Slow incident response",
            "No playbooks"
        ],
        "mitigations": "SIEM, SOAR, 24/7 SOC, Tabletop exercises."
    },
    "11. Business Continuity": {
        "risks": [
            "DDoS attacks",
            "Single points of failure",
            "Weak DR plans",
            "Backup failure"
        ],
        "mitigations": "DDoS protection, Redundancy, RTO/RPO testing, Resilience engineering."
    },
    "12. Third-Party & Supply Chain": {
        "risks": [
            "Vendor breach",
            "Compromised software updates",
            "Shared credentials",
            "Poor contracts"
        ],
        "mitigations": "Vendor due diligence, Security clauses, Continuous monitoring."
    },
    "13. Physical & Endpoint": {
        "risks": [
            "Lost/Stolen devices",
            "Unmanaged BYOD",
            "USB malware",
            "Weak disk encryption"
        ],
        "mitigations": "MDM, Full-disk encryption, Remote wipe, Endpoint hardening."
    },
    "14. Governance & Human": {
        "risks": [
            "Weak policies",
            "Poor segregation of duties",
            "Inadequate training",
            "Shadow IT"
        ],
        "mitigations": "Governance framework, Policy lifecycle, Audit monitoring."
    }
}


# =============================================================================
# AI RISK DATA
# =============================================================================

AI_RISK_DATA: Dict[str, Dict] = {
    "1. Cybersecurity risks": {
        "risks": [
            "Prompt injection / jailbreaks",
            "Data exfiltration (via RAG/Plugins)",
            "Model supply chain risk",
            "Adversarial inputs",
            "Credential leakage"
        ],
        "mitigations": "Content policies, execution guardrails, secret isolation, least privilege for tools, red-teaming."
    },
    "2. Privacy & Data Governance": {
        "risks": [
            "PII exposure in outputs",
            "Unintentional data retention",
            "Re-identification",
            "Data poisoning"
        ],
        "mitigations": "Data classification rules, PII masking/tokenization, strict retention/deletion policies, access audits."
    },
    "3. Accuracy & Quality": {
        "risks": [
            "Hallucinations",
            "Over-reliance",
            "Domain mismatch",
            "Non-determinism"
        ],
        "mitigations": "Human-in-the-loop, Grounded RAG, acceptance testing, refusal correctness metrics."
    },
    "4. Bias & Fairness": {
        "risks": [
            "Algorithmic bias",
            "Unfair outcomes",
            "Reinforcing stereotypes"
        ],
        "mitigations": "Pre/Post-deployment fairness testing, training data review, restricted use cases."
    },
    "5. Legal & Regulatory": {
        "risks": [
            "IP/Copyright infringement",
            "Non-compliance (GDPR/AI Act)",
            "Lack of Explainability"
        ],
        "mitigations": "License review, legal approval workflows, AI labeling/disclaimers, decision logs."
    },
    "6. Operational & Continuity": {
        "risks": [
            "Model drift",
            "Latency/Cost spikes",
            "Vendor lock-in",
            "Dependency outages"
        ],
        "mitigations": "Continuous monitoring (MLOps), caching/batching, model abstraction layers, SLAs."
    },
    "7. Safety & Misuse": {
        "risks": [
            "Harmful content generation",
            "Social engineering scaling",
            "Deepfakes"
        ],
        "mitigations": "Misuse policies, detection rate limiting, watermarking/provenance, kill switches."
    }
}


# =============================================================================
# DATA MANAGEMENT RISK DATA
# =============================================================================

DATA_RISK_DATA: Dict[str, Dict] = {
    "1. Data Governance & Ownership": {
        "risks": [
            "Unclear ownership/accountability",
            "Policy gaps (retention/sharing)",
            "Weak data standards (inconsistent definitions)"
        ],
        "mitigations": "Governance model (RACI), data policies, enterprise data standards, stewardship program."
    },
    "2. Data Quality & Integrity": {
        "risks": [
            "Inaccurate/incomplete data",
            "Inconsistent definitions across teams",
            "Duplication / poor master data",
            "Data corruption (ETL/Transformation errors)"
        ],
        "mitigations": "Data quality rules, validation at entry, DQ monitoring, Master Data Management (MDM), automated reconciliations."
    },
    "3. Privacy & Confidentiality": {
        "risks": [
            "PII/PHI exposure",
            "Over-collection of sensitive data",
            "Re-identification of anonymized data",
            "Improper sharing with third parties"
        ],
        "mitigations": "Data classification, minimization, masking/tokenization, DPIAs, third-party risk controls, audit logging."
    },
    "4. Security & Access Control": {
        "risks": [
            "Excessive privileges (Insider risk)",
            "Weak authentication / key management",
            "Insecure storage or transport (No encryption)",
            "Ransomware/data theft"
        ],
        "mitigations": "IAM least privilege, MFA, encryption (rest/transit), DLP, key management, network segmentation."
    },
    "5. Compliance & Regulatory": {
        "risks": [
            "Retention violations (keeping too long/short)",
            "Cross-border transfer violations",
            "Audit failure (cannot prove lineage)"
        ],
        "mitigations": "Retention schedules, legal holds, data residency controls, robust audit trails, compliance mapping."
    },
    "6. Lifecycle & Records Mgmt": {
        "risks": [
            "No end-to-end lifecycle (hoarding)",
            "Orphaned datasets (unknown owner)",
            "Backup/restore gaps"
        ],
        "mitigations": "Lifecycle management policies, archiving strategy, backup/restore testing, records management."
    },
    "7. Architecture & Integration": {
        "risks": [
            "Data silos & inconsistent integration",
            "Fragile pipelines (ETL/ELT breaks)",
            "Schema versioning issues"
        ],
        "mitigations": "Architecture standards, integration patterns, schema governance, automated pipeline testing."
    },
    "8. Metadata & Lineage": {
        "risks": [
            "No data catalog (low discoverability)",
            "Unknown lineage (trust issues)",
            "Poor documentation (Key person risk)"
        ],
        "mitigations": "Data catalog implementation, automated lineage tools, documentation standards."
    },
    "9. Availability & Performance": {
        "risks": [
            "Latency / System downtime",
            "Capacity/Cost blowouts (Cloud bills)"
        ],
        "mitigations": "SLOs/SLAs definitions, capacity planning, FinOps, performance monitoring."
    },
    "10. Usage & Decision Risks": {
        "risks": [
            "Misinterpretation of data (Context gap)",
            "Shadow analytics (Excel chaos)",
            "Model risk (Biased AI training data)"
        ],
        "mitigations": "Metric governance, certified datasets, BI governance, model risk management review."
    }
}


# =============================================================================
# CONTROL EXPLANATIONS
# =============================================================================

CONTROL_EXPLANATIONS: Dict[str, Dict[str, str]] = {
    "Unified.GOV": {
        "en": "**Unified.GOV (Governance):** Missing formal policies, risk methodology, or steering committees.",
        "ar": "**Unified.GOV (الحوكمة):** نقص في السياسات المعتمدة، منهجية المخاطر، أو اللجان التوجيهية."
    },
    "Unified.IAM": {
        "en": "**Unified.IAM (Identity):** Weak password policies, lack of MFA, or unmanaged privileged access.",
        "ar": "**Unified.IAM (الهوية):** سياسات كلمات مرور ضعيفة، عدم تفعيل MFA، أو وصول امتيازي غير مدار."
    },
    "Unified.LOG": {
        "en": "**Unified.LOG (Monitoring):** No centralized logging (SIEM) or 24/7 security monitoring (SOC).",
        "ar": "**Unified.LOG (المراقبة):** غياب التسجيل المركزي (SIEM) أو فريق مراقبة أمنية على مدار الساعة (SOC)."
    },
    "Unified.CTRL": {
        "en": "**Unified.CTRL (Controls):** Missing technical evidence, asset inventory, or endpoint protection.",
        "ar": "**Unified.CTRL (الضوابط):** نقص في الأدلة التقنية، حصر الأصول، أو حماية الأجهزة الطرفية."
    },
    "Unified.IR": {
        "en": "**Unified.IR (Response):** Lack of documented incident response plan or regular drills.",
        "ar": "**Unified.IR (الاستجابة):** عدم وجود خطة استجابة للحوادث موثقة أو تمارين دورية."
    },
    "Unified.ASSET": {
        "en": "**Unified.ASSET (Assets):** Incomplete asset inventory or classification of critical systems.",
        "ar": "**Unified.ASSET (الأصول):** سجل أصول غير مكتمل أو غياب تصنيف الأنظمة الحرجة."
    },
    "Unified.TPRM": {
        "en": "**Unified.TPRM (Third-Party):** No vendor risk assessments or supplier security requirements.",
        "ar": "**Unified.TPRM (الأطراف الثالثة):** غياب تقييمات مخاطر الموردين أو متطلبات الأمان."
    },
    "Unified.BCDR": {
        "en": "**Unified.BCDR (Continuity):** Missing BIA, DR plans, or recovery testing.",
        "ar": "**Unified.BCDR (الاستمرارية):** غياب تحليل الأثر، خطط التعافي، أو اختبارات الاسترداد."
    }
}


def get_risk_data(domain_code: str) -> Dict[str, Dict]:
    """
    Get risk data for a specific domain.
    
    Args:
        domain_code: Domain code (cyber, ai, data)
        
    Returns:
        Dict with risk categories and their risks/mitigations
    """
    mapping = {
        "cyber": CYBER_RISK_DATA,
        "ai": AI_RISK_DATA,
        "data": DATA_RISK_DATA
    }
    return mapping.get(domain_code, CYBER_RISK_DATA)


def get_control_explanation(control_id: str, language: str = "en") -> str:
    """
    Get explanation for a control ID.
    
    Args:
        control_id: Control identifier (e.g., "Unified.GOV")
        language: Language code ("en" or "ar")
        
    Returns:
        Explanation string
    """
    if control_id in CONTROL_EXPLANATIONS:
        return CONTROL_EXPLANATIONS[control_id].get(language, CONTROL_EXPLANATIONS[control_id]["en"])
    return f"**{control_id}**: Control gap identified."
