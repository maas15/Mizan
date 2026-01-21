"""
Sentinel GRC - Framework Packs
Comprehensive framework obligations and control mappings.
"""

from typing import Dict, List, Any


# =============================================================================
# LOCAL FRAMEWORK PACKS
# =============================================================================

LOCAL_FRAMEWORK_PACKS: Dict[str, Dict[str, Any]] = {
    # ---------- NCA FRAMEWORKS ----------
    "NCA ECC (Essential Cybersecurity Controls)": {
        "framework_id": "KSA_NCA_ECC",
        "version": "ECC-2-2024",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "ECC-GOV-01", "text": "Establish cybersecurity governance roles, responsibilities, and oversight.", "tags": ["governance", "policy"], "evidence": ["Governance charter", "Cybersecurity policy"]},
            {"id": "ECC-IAM-01", "text": "Implement access control, privileged access management, and authentication controls.", "tags": ["iam", "pam"], "evidence": ["IAM configs", "PAM reports", "Access reviews"]},
            {"id": "ECC-LOG-01", "text": "Centralize security logging and monitoring for detection.", "tags": ["logging", "monitoring"], "evidence": ["SIEM dashboards", "Log retention config"]},
            {"id": "ECC-IR-01", "text": "Maintain incident response plans, playbooks, and exercises.", "tags": ["ir", "exercise"], "evidence": ["IR plan", "Exercise reports"]},
        ],
        "mapping_hints": {
            "Unified.GOV": ["governance", "policy"],
            "Unified.IAM": ["iam", "pam"],
            "Unified.LOG": ["logging", "monitoring"],
            "Unified.IR": ["ir", "exercise"],
        },
    },
    "NCA CCC (Cloud Cybersecurity Controls)": {
        "framework_id": "KSA_NCA_CCC",
        "version": "CCC-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "CCC-GOV-01", "text": "Define cloud security governance, shared responsibility, and cloud risk management.", "tags": ["cloud", "governance", "risk"], "evidence": ["Cloud governance model", "Cloud risk register"]},
            {"id": "CCC-IAM-01", "text": "Enforce strong IAM for cloud consoles, APIs, and privileged identities.", "tags": ["cloud", "iam", "pam"], "evidence": ["Cloud IAM policies", "MFA enforcement", "PAM integration"]},
            {"id": "CCC-LOG-01", "text": "Enable cloud-native logging and centralized monitoring for cloud workloads.", "tags": ["cloud", "logging", "monitoring"], "evidence": ["Cloud audit logs", "SIEM integration"]},
        ],
        "mapping_hints": {
            "Unified.GOV": ["cloud", "governance", "risk"],
            "Unified.IAM": ["cloud", "iam", "pam"],
            "Unified.LOG": ["cloud", "logging", "monitoring"],
        },
    },
    "NCA DCC (Data Cybersecurity Controls)": {
        "framework_id": "KSA_NCA_DCC",
        "version": "DCC-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "DCC-CLASS-01", "text": "Classify data and apply protection controls based on sensitivity.", "tags": ["data", "classification"], "evidence": ["Data classification policy", "Labeling records"]},
            {"id": "DCC-ENC-01", "text": "Encrypt sensitive data at rest and in transit with managed keys.", "tags": ["data", "encryption", "crypto"], "evidence": ["Encryption configs", "KMS settings"]},
            {"id": "DCC-DLP-01", "text": "Implement DLP and data leakage monitoring for sensitive information.", "tags": ["data", "dlp", "monitoring"], "evidence": ["DLP policies", "Alerts"]},
        ],
        "mapping_hints": {
            "Unified.DATA.PRIV": ["data", "classification"],
            "Unified.CTRL": ["data", "dlp", "monitoring"],
            "Unified.GOV": ["data", "classification"],
        },
    },
    "NCA OTCC (Operational Technology Cybersecurity Controls)": {
        "framework_id": "KSA_NCA_OTCC",
        "version": "OTCC-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "OTCC-ZONE-01", "text": "Segment OT networks and enforce zones/conduits with strict access control.", "tags": ["ot", "segmentation", "iam"], "evidence": ["Network diagrams", "Firewall rules"]},
            {"id": "OTCC-MON-01", "text": "Monitor OT environments for anomalies and security events.", "tags": ["ot", "monitoring", "logging"], "evidence": ["OT monitoring dashboards", "Log exports"]},
        ],
        "mapping_hints": {
            "Unified.IAM": ["ot", "segmentation", "iam"],
            "Unified.LOG": ["ot", "monitoring", "logging"],
        },
    },
    "NCA TCC (Telework Cybersecurity Controls)": {
        "framework_id": "KSA_NCA_TCC",
        "version": "TCC-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "TCC-ENDPOINT-01", "text": "Secure telework endpoints with EDR, hardening, and patching.", "tags": ["telework", "endpoint"], "evidence": ["EDR coverage", "Patch reports"]},
            {"id": "TCC-ACCESS-01", "text": "Enforce secure remote access (VPN/ZTNA) with MFA.", "tags": ["telework", "iam", "mfa"], "evidence": ["VPN/ZTNA configs", "MFA reports"]},
        ],
        "mapping_hints": {
            "Unified.IAM": ["telework", "iam", "mfa"],
            "Unified.CTRL": ["telework", "endpoint"],
        },
    },
    "NCA OSMACC (Social Media Accounts Cybersecurity Controls)": {
        "framework_id": "KSA_NCA_OSMACC",
        "version": "OSMACC-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "OSMACC-ACC-01", "text": "Secure official social media accounts with MFA and privileged access governance.", "tags": ["social", "iam", "mfa", "governance"], "evidence": ["Account inventory", "MFA enabled proof"]},
            {"id": "OSMACC-IR-01", "text": "Maintain incident procedures for account takeover and defacement.", "tags": ["social", "ir"], "evidence": ["Playbooks", "Incident logs"]},
        ],
        "mapping_hints": {
            "Unified.IAM": ["social", "iam", "mfa"],
            "Unified.IR": ["social", "ir"],
            "Unified.GOV": ["governance"],
        },
    },
    "NCA CSCC (Critical Systems Cybersecurity Controls)": {
        "framework_id": "KSA_NCA_CSCC",
        "version": "CSCC-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "CSCC-RES-01", "text": "Define resilience requirements for critical systems, including redundancy and recovery objectives.", "tags": ["critical", "bcdr", "resilience"], "evidence": ["RTO/RPO", "DR tests"]},
            {"id": "CSCC-SEC-01", "text": "Harden critical systems and enforce strict change control.", "tags": ["critical", "hardening", "change"], "evidence": ["Baselines", "Change tickets"]},
        ],
        "mapping_hints": {
            "Unified.BCDR": ["bcdr", "resilience"],
            "Unified.CTRL": ["hardening", "change", "critical"],
        },
    },
    "NCA NCS (National Cryptographic Standards)": {
        "framework_id": "KSA_NCA_NCS",
        "version": "NCS-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "NCS-CRYPTO-01", "text": "Use approved cryptographic algorithms and key management practices.", "tags": ["crypto", "encryption", "keys"], "evidence": ["Crypto standards mapping", "KMS configs"]},
            {"id": "NCS-KEYS-01", "text": "Manage cryptographic keys securely across lifecycle (generation, storage, rotation, revocation).", "tags": ["crypto", "keys", "governance"], "evidence": ["Key rotation logs", "HSM/KMS policies"]},
        ],
        "mapping_hints": {
            "Unified.CTRL": ["crypto", "encryption", "keys"],
            "Unified.GOV": ["governance", "keys"]
        },
    },
    "NCA CGIoT (Cybersecurity Guidelines for IoT)": {
        "framework_id": "KSA_NCA_CGIOT",
        "version": "CGIoT-latest",
        "authority": "NCA",
        "domain": "cyber",
        "obligations": [
            {"id": "CGIOT-INV-01", "text": "Maintain inventory of IoT devices and associated risks.", "tags": ["iot", "asset", "inventory"], "evidence": ["IoT inventory", "Network scans"]},
            {"id": "CGIOT-SEC-01", "text": "Secure IoT devices (default credentials, patching, segmentation).", "tags": ["iot", "hardening", "segmentation"], "evidence": ["Hardening checklist", "Segmentation rules"]},
        ],
        "mapping_hints": {
            "Unified.ASSET": ["iot", "asset", "inventory"],
            "Unified.CTRL": ["iot", "hardening", "segmentation"]
        },
    },

    # ---------- SAMA ----------
    "SAMA CSF": {
        "framework_id": "KSA_SAMA_CSF",
        "version": "latest",
        "authority": "SAMA",
        "domain": "cyber",
        "obligations": [
            {"id": "SAMA-GOV-01", "text": "Maintain cybersecurity governance aligned to SAMA CSF.", "tags": ["governance", "risk"], "evidence": ["Charter", "Risk reports"]},
            {"id": "SAMA-TPRM-01", "text": "Manage third-party risks for critical suppliers per SAMA CSF.", "tags": ["third_party", "risk"], "evidence": ["TPRM assessments", "Contracts"]},
        ],
        "mapping_hints": {
            "Unified.GOV": ["governance", "risk"],
            "Unified.TPRM": ["third_party", "risk"]
        },
    },

    # ---------- DATA FRAMEWORKS ----------
    "NDMO/SDAIA": {
        "framework_id": "KSA_NDMO",
        "version": "latest",
        "authority": "SDAIA/NDMO",
        "domain": "data",
        "obligations": [
            {"id": "NDMO-GOV-01", "text": "Establish data governance roles and stewardship model.", "tags": ["data_governance", "roles"], "evidence": ["DG charter", "Data RACI"]},
            {"id": "NDMO-DQ-01", "text": "Define and monitor data quality dimensions and metrics.", "tags": ["data_quality"], "evidence": ["DQ KPIs", "DQ reports"]},
        ],
        "mapping_hints": {
            "Unified.DATA.GOV": ["data_governance", "roles"],
            "Unified.DATA.DQ": ["data_quality"]
        },
    },
    "GDPR": {
        "framework_id": "GDPR_2016_679",
        "version": "2016",
        "authority": "EU",
        "domain": "data",
        "obligations": [
            {"id": "GDPR-PRIN-01", "text": "Ensure processing adheres to privacy principles and lawful basis.", "tags": ["privacy", "lawful_basis"], "evidence": ["Privacy notices", "Lawful basis register"]},
            {"id": "GDPR-ROPA-01", "text": "Maintain Records of Processing Activities (RoPA).", "tags": ["ropa"], "evidence": ["RoPA"]},
            {"id": "GDPR-DPIA-01", "text": "Conduct DPIAs where required and maintain outcomes.", "tags": ["dpia", "risk"], "evidence": ["DPIA reports"]},
            {"id": "GDPR-BREACH-01", "text": "Maintain breach response procedures and notification process.", "tags": ["breach", "ir"], "evidence": ["Breach procedure", "Incident log"]},
        ],
        "mapping_hints": {
            "Unified.DATA.PRIV": ["privacy", "lawful_basis"],
            "Unified.DATA.ROPA": ["ropa"],
            "Unified.DATA.DPIA": ["dpia", "risk"],
            "Unified.IR": ["breach", "ir"]
        },
    },
    "DGA Data Standards": {
        "framework_id": "KSA_DGA_DATA",
        "version": "latest",
        "authority": "DGA",
        "domain": "data",
        "obligations": [
            {"id": "DGA-DATA-01", "text": "Define enterprise data standards and interoperability requirements.", "tags": ["standards", "interoperability"], "evidence": ["Data standards", "APIs specs"]},
        ],
        "mapping_hints": {
            "Unified.DATA.GOV": ["standards"],
            "Unified.CTRL": ["interoperability"]
        },
    },

    # ---------- AI FRAMEWORKS ----------
    "NIST AI RMF": {
        "framework_id": "NIST_AI_RMF_1_0",
        "version": "1.0",
        "authority": "NIST",
        "domain": "ai",
        "obligations": [
            {"id": "AIRMF-GOV-01", "text": "Establish AI governance, accountability, and oversight for AI systems.", "tags": ["ai_governance", "accountability"], "evidence": ["AI policy", "Model approval minutes"]},
            {"id": "AIRMF-MAP-01", "text": "Map AI use-cases, contexts, stakeholders, and potential impacts.", "tags": ["usecase", "impact"], "evidence": ["Use-case register", "Impact assessment"]},
            {"id": "AIRMF-MEAS-01", "text": "Define and execute evaluation, testing, and validation for AI models.", "tags": ["tevv", "testing"], "evidence": ["Test reports", "Metrics"]},
            {"id": "AIRMF-MGMT-01", "text": "Monitor AI performance and manage drift, incidents, and changes.", "tags": ["monitoring", "drift", "incident"], "evidence": ["Monitoring dashboards", "Incident log"]},
        ],
        "mapping_hints": {
            "Unified.AI.GOV": ["ai_governance", "accountability"],
            "Unified.AI.MAP": ["usecase", "impact"],
            "Unified.AI.TEVV": ["tevv", "testing"],
            "Unified.AI.MON": ["monitoring", "drift", "incident"]
        },
    },
    "EU AI Act": {
        "framework_id": "EU_AI_ACT_2024",
        "version": "2024",
        "authority": "EU",
        "domain": "ai",
        "obligations": [
            {"id": "EUAIA-CLASS-01", "text": "Classify AI systems by risk category and document classification rationale.", "tags": ["classification", "risk"], "evidence": ["AI classification register"]},
            {"id": "EUAIA-HR-01", "text": "For high-risk systems, implement risk management, documentation, and human oversight.", "tags": ["high_risk", "oversight", "documentation"], "evidence": ["Tech file", "Risk plan", "Oversight procedure"]},
        ],
        "mapping_hints": {
            "Unified.AI.CLASS": ["classification", "risk"],
            "Unified.AI.HR": ["high_risk", "oversight", "documentation"]
        },
    },
    "SDAIA AI Ethics": {
        "framework_id": "KSA_SDAIA_AI_ETHICS",
        "version": "latest",
        "authority": "SDAIA",
        "domain": "ai",
        "obligations": [
            {"id": "SDAIA-AI-ETH-01", "text": "Define AI ethical principles and ensure governance and compliance.", "tags": ["ai_ethics", "governance"], "evidence": ["AI ethics policy", "Review records"]},
        ],
        "mapping_hints": {
            "Unified.AI.GOV": ["ai_ethics", "governance"]
        },
    },

    # ---------- DT FRAMEWORKS ----------
    "DGA Digital Gov Policy": {
        "framework_id": "KSA_DGA_DG",
        "version": "latest",
        "authority": "DGA",
        "domain": "dt",
        "obligations": [
            {"id": "DGA-GOV-01", "text": "Establish digital governance and portfolio oversight per DGA direction.", "tags": ["governance", "portfolio"], "evidence": ["Portfolio governance", "EA standards"]},
            {"id": "DGA-SVC-01", "text": "Define service design and performance management for digital services.", "tags": ["service", "kpi"], "evidence": ["Service catalog", "SLA/KPI"]},
        ],
        "mapping_hints": {
            "Unified.DT.GOV": ["governance", "portfolio"],
            "Unified.DT.SVC": ["service", "kpi"]
        },
    },
    "COBIT 2019": {
        "framework_id": "COBIT_2019",
        "version": "2019",
        "authority": "ISACA",
        "domain": "dt",
        "obligations": [
            {"id": "COBIT-EDM-01", "text": "Ensure governance objectives are evaluated, directed, and monitored.", "tags": ["governance", "portfolio"], "evidence": ["Board minutes", "Metrics packs"]},
        ],
        "mapping_hints": {
            "Unified.DT.GOV": ["governance", "portfolio"]
        },
    },
    "TOGAF": {
        "framework_id": "TOGAF",
        "version": "10",
        "authority": "The Open Group",
        "domain": "dt",
        "obligations": [
            {"id": "TOGAF-EA-01", "text": "Maintain enterprise architecture standards and review processes.", "tags": ["architecture", "governance"], "evidence": ["EA standards", "ARB minutes"]},
        ],
        "mapping_hints": {
            "Unified.DT.GOV": ["architecture", "governance"]
        },
    },

    # ---------- GLOBAL FRAMEWORKS ----------
    "NIST CSF 2.0": {
        "framework_id": "NIST_CSF_2_0",
        "version": "2.0",
        "authority": "NIST",
        "domain": "global",
        "obligations": [
            {"id": "CSF-GV-01", "text": "Establish cybersecurity governance roles, responsibilities, and oversight.", "tags": ["governance", "risk", "policy"], "evidence": ["Charter", "RACI", "Meeting minutes"]},
            {"id": "CSF-ID-01", "text": "Maintain inventory of assets and associated risk context.", "tags": ["asset", "inventory"], "evidence": ["Asset register", "CMDB export"]},
            {"id": "CSF-PR-01", "text": "Implement IAM including MFA for privileged access.", "tags": ["iam", "pam"], "evidence": ["IAM configs", "PAM reports"]},
            {"id": "CSF-DE-01", "text": "Centralize logging and monitor security events.", "tags": ["logging", "monitoring", "soc"], "evidence": ["SIEM dashboards", "Use-case list"]},
            {"id": "CSF-RS-01", "text": "Maintain incident response playbooks and conduct exercises.", "tags": ["ir", "exercise"], "evidence": ["IR plan", "Exercise reports"]},
            {"id": "CSF-RC-01", "text": "Define recovery objectives and procedures for critical services.", "tags": ["bcdr", "resilience"], "evidence": ["DR plan", "RTO/RPO"]},
        ],
        "mapping_hints": {
            "Unified.GOV": ["governance", "policy", "risk"],
            "Unified.ASSET": ["asset", "inventory"],
            "Unified.IAM": ["iam", "pam"],
            "Unified.LOG": ["logging", "monitoring", "soc"],
            "Unified.IR": ["ir", "exercise"],
            "Unified.BCDR": ["bcdr", "resilience"],
        },
    },
    "ISO 27001:2022": {
        "framework_id": "ISO27001_2022",
        "version": "2022",
        "authority": "ISO/IEC",
        "domain": "global",
        "obligations": [
            {"id": "ISO-ISMS-01", "text": "Define ISMS scope, risk methodology, and maintain a risk treatment plan.", "tags": ["isms", "risk", "governance"], "evidence": ["ISMS scope", "Risk method", "RTP"]},
            {"id": "ISO-CTRL-01", "text": "Implement controls and maintain a Statement of Applicability.", "tags": ["controls", "soa", "evidence"], "evidence": ["SoA", "Control procedures"]},
        ],
        "mapping_hints": {
            "Unified.GOV": ["isms", "governance", "risk"],
            "Unified.CTRL": ["controls", "soa", "evidence"]
        },
    },
    "ISO 22301": {
        "framework_id": "ISO22301",
        "version": "2019",
        "authority": "ISO",
        "domain": "global",
        "obligations": [
            {"id": "BCMS-01", "text": "Perform BIA and define continuity strategies for critical services.", "tags": ["bia", "bcdr"], "evidence": ["BIA", "BC strategy"]},
            {"id": "BCMS-02", "text": "Maintain BC/DR plans and exercise them periodically.", "tags": ["plans", "exercise"], "evidence": ["BCP/DRP", "Exercise reports"]},
        ],
        "mapping_hints": {
            "Unified.BCDR": ["bia", "bcdr", "plans", "exercise"]
        },
    },
    "ISO 9001": {
        "framework_id": "ISO9001",
        "version": "2015",
        "authority": "ISO",
        "domain": "global",
        "obligations": [
            {"id": "QMS-01", "text": "Maintain quality management processes and continuous improvement.", "tags": ["quality", "governance"], "evidence": ["QMS procedures", "Management review"]},
        ],
        "mapping_hints": {
            "Unified.GOV": ["governance"],
            "Unified.CTRL": ["quality"]
        },
    },
    "ITIL 4": {
        "framework_id": "ITIL4",
        "version": "4",
        "authority": "AXELOS",
        "domain": "global",
        "obligations": [
            {"id": "ITIL-SVC-01", "text": "Maintain service management practices for delivery and continual improvement.", "tags": ["service", "kpi"], "evidence": ["Service catalog", "ITSM reports"]},
        ],
        "mapping_hints": {
            "Unified.DT.SVC": ["service", "kpi"]
        },
    },
}


def get_framework_pack(framework_name: str) -> Dict[str, Any]:
    """
    Get framework pack by name.
    
    Args:
        framework_name: Name of the framework
        
    Returns:
        Framework pack dictionary
    """
    if framework_name in LOCAL_FRAMEWORK_PACKS:
        return LOCAL_FRAMEWORK_PACKS[framework_name]
    
    # Return placeholder for unknown frameworks
    return {
        "framework_id": framework_name.replace(" ", "_"),
        "version": "unknown",
        "authority": "unknown",
        "domain": "global",
        "obligations": [
            {
                "id": f"{framework_name[:10]}-01",
                "text": "Placeholder obligation. Add real obligations to LOCAL_FRAMEWORK_PACKS.",
                "tags": ["placeholder"],
                "evidence": ["N/A"]
            }
        ],
        "mapping_hints": {"Unified.GOV": ["placeholder"]},
    }


def get_all_framework_names() -> List[str]:
    """Get list of all framework names."""
    return list(LOCAL_FRAMEWORK_PACKS.keys())


def get_frameworks_by_domain(domain_code: str) -> List[str]:
    """Get frameworks filtered by domain."""
    return [
        name for name, pack in LOCAL_FRAMEWORK_PACKS.items()
        if pack.get("domain") == domain_code
    ]
