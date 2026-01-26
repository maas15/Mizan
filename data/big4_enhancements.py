"""
Mizan GRC - Big4 Quality Enhancements
Comprehensive additions to match Big4 consulting deliverable standards.
Includes: Resource Planning, Risk Heat Maps, Scenario Analysis, Enhanced Audit Details
"""

from typing import Dict, List, Any, Tuple

# =============================================================================
# RESOURCE PLANNING MATRICES
# =============================================================================

RESOURCE_REQUIREMENTS = {
    "Cyber Security": {
        "roles": [
            {"title": "CISO / Security Director", "fte": 1.0, "level": "Executive", "skills": ["Security strategy", "Risk management", "Regulatory compliance", "Team leadership"], "cost_sar_annual": 600000},
            {"title": "Security Architect", "fte": 1.0, "level": "Senior", "skills": ["Zero Trust", "Cloud security", "Network architecture", "Security frameworks"], "cost_sar_annual": 420000},
            {"title": "SOC Manager", "fte": 1.0, "level": "Senior", "skills": ["SIEM/SOAR", "Incident response", "Threat intelligence", "Team management"], "cost_sar_annual": 360000},
            {"title": "SOC Analyst L2/L3", "fte": 3.0, "level": "Mid", "skills": ["Threat hunting", "Malware analysis", "Forensics", "SIEM operations"], "cost_sar_annual": 240000},
            {"title": "SOC Analyst L1", "fte": 4.0, "level": "Junior", "skills": ["Alert triage", "Log analysis", "Ticket management", "Basic forensics"], "cost_sar_annual": 144000},
            {"title": "IAM Specialist", "fte": 2.0, "level": "Mid", "skills": ["Identity governance", "PAM", "MFA", "Access reviews"], "cost_sar_annual": 216000},
            {"title": "Vulnerability Manager", "fte": 1.0, "level": "Mid", "skills": ["Vulnerability scanning", "Patch management", "Risk prioritization", "Remediation tracking"], "cost_sar_annual": 216000},
            {"title": "Security Awareness Lead", "fte": 1.0, "level": "Mid", "skills": ["Training development", "Phishing simulations", "Communication", "Metrics"], "cost_sar_annual": 180000},
            {"title": "GRC Analyst", "fte": 2.0, "level": "Mid", "skills": ["NCA ECC", "ISO 27001", "Policy development", "Audit support"], "cost_sar_annual": 192000},
        ],
        "total_fte": 16.0,
        "total_annual_cost": 4524000,
        "external_support": [
            {"service": "Penetration Testing", "frequency": "Annual", "cost_sar": 150000},
            {"service": "Red Team Assessment", "frequency": "Annual", "cost_sar": 300000},
            {"service": "Threat Intelligence Feed", "frequency": "Annual", "cost_sar": 120000},
            {"service": "Security Awareness Platform", "frequency": "Annual", "cost_sar": 60000},
        ],
        "training_budget": 250000,
        "certification_requirements": ["CISSP", "CISM", "CEH", "OSCP", "GIAC", "NCA Certifications"]
    },
    
    "Artificial Intelligence": {
        "roles": [
            {"title": "Chief Data Officer / AI Lead", "fte": 1.0, "level": "Executive", "skills": ["AI strategy", "Data governance", "Ethics", "Stakeholder management"], "cost_sar_annual": 540000},
            {"title": "AI Ethics Officer", "fte": 1.0, "level": "Senior", "skills": ["AI ethics", "Bias detection", "Regulatory compliance", "Policy development"], "cost_sar_annual": 360000},
            {"title": "ML Engineering Lead", "fte": 1.0, "level": "Senior", "skills": ["MLOps", "Model deployment", "Pipeline automation", "Cloud ML"], "cost_sar_annual": 420000},
            {"title": "Data Scientist", "fte": 3.0, "level": "Mid", "skills": ["Model development", "Feature engineering", "Statistical analysis", "Python/R"], "cost_sar_annual": 300000},
            {"title": "ML Engineer", "fte": 2.0, "level": "Mid", "skills": ["Model deployment", "Monitoring", "API development", "Docker/K8s"], "cost_sar_annual": 288000},
            {"title": "AI Risk Analyst", "fte": 1.0, "level": "Mid", "skills": ["Model validation", "Risk assessment", "Documentation", "Testing"], "cost_sar_annual": 216000},
            {"title": "Data Engineer", "fte": 2.0, "level": "Mid", "skills": ["Data pipelines", "ETL", "Data quality", "Cloud platforms"], "cost_sar_annual": 264000},
        ],
        "total_fte": 11.0,
        "total_annual_cost": 3348000,
        "external_support": [
            {"service": "AI Audit / Assessment", "frequency": "Annual", "cost_sar": 200000},
            {"service": "Bias Testing Tools", "frequency": "Annual", "cost_sar": 80000},
            {"service": "MLOps Platform", "frequency": "Annual", "cost_sar": 150000},
        ],
        "training_budget": 200000,
        "certification_requirements": ["AWS ML Specialty", "Google ML Engineer", "Azure AI Engineer", "CDMP"]
    },
    
    "Data Management": {
        "roles": [
            {"title": "Chief Data Officer", "fte": 1.0, "level": "Executive", "skills": ["Data strategy", "Governance", "Regulatory", "Leadership"], "cost_sar_annual": 540000},
            {"title": "Data Protection Officer", "fte": 1.0, "level": "Senior", "skills": ["PDPL", "Privacy", "DSAR", "Compliance"], "cost_sar_annual": 360000},
            {"title": "Data Governance Manager", "fte": 1.0, "level": "Senior", "skills": ["Data governance", "Stewardship", "Policy", "Metadata"], "cost_sar_annual": 300000},
            {"title": "Data Steward", "fte": 4.0, "level": "Mid", "skills": ["Data quality", "Domain expertise", "Business rules", "Issue resolution"], "cost_sar_annual": 180000},
            {"title": "Data Quality Analyst", "fte": 2.0, "level": "Mid", "skills": ["DQ tools", "Profiling", "Monitoring", "Remediation"], "cost_sar_annual": 192000},
            {"title": "Data Architect", "fte": 1.0, "level": "Senior", "skills": ["Data modeling", "MDM", "Integration", "Cloud data"], "cost_sar_annual": 360000},
            {"title": "Privacy Analyst", "fte": 2.0, "level": "Mid", "skills": ["PDPL compliance", "PIA", "Consent management", "DSAR processing"], "cost_sar_annual": 180000},
        ],
        "total_fte": 12.0,
        "total_annual_cost": 3072000,
        "external_support": [
            {"service": "PDPL Compliance Audit", "frequency": "Annual", "cost_sar": 150000},
            {"service": "Data Catalog Platform", "frequency": "Annual", "cost_sar": 200000},
            {"service": "DQ Monitoring Tools", "frequency": "Annual", "cost_sar": 100000},
        ],
        "training_budget": 150000,
        "certification_requirements": ["CDMP", "CIPP/M", "CIPM", "DGSP"]
    },
    
    "Digital Transformation": {
        "roles": [
            {"title": "Chief Digital Officer", "fte": 1.0, "level": "Executive", "skills": ["Digital strategy", "Innovation", "Change management", "Stakeholder management"], "cost_sar_annual": 600000},
            {"title": "Digital Program Manager", "fte": 2.0, "level": "Senior", "skills": ["Program management", "Agile", "Stakeholder management", "Risk management"], "cost_sar_annual": 360000},
            {"title": "Enterprise Architect", "fte": 1.0, "level": "Senior", "skills": ["TOGAF", "Cloud architecture", "Integration", "Standards"], "cost_sar_annual": 420000},
            {"title": "Product Owner", "fte": 3.0, "level": "Mid", "skills": ["Product management", "Agile", "User research", "Roadmapping"], "cost_sar_annual": 264000},
            {"title": "UX/UI Designer", "fte": 2.0, "level": "Mid", "skills": ["User research", "Wireframing", "Prototyping", "Design systems"], "cost_sar_annual": 216000},
            {"title": "Full Stack Developer", "fte": 6.0, "level": "Mid", "skills": ["Frontend", "Backend", "APIs", "Cloud"], "cost_sar_annual": 240000},
            {"title": "DevOps Engineer", "fte": 2.0, "level": "Mid", "skills": ["CI/CD", "Kubernetes", "IaC", "Monitoring"], "cost_sar_annual": 264000},
            {"title": "Change Management Lead", "fte": 1.0, "level": "Senior", "skills": ["PROSCI", "Communication", "Training", "Adoption"], "cost_sar_annual": 300000},
            {"title": "Business Analyst", "fte": 2.0, "level": "Mid", "skills": ["Requirements", "Process mapping", "Documentation", "Testing"], "cost_sar_annual": 192000},
        ],
        "total_fte": 20.0,
        "total_annual_cost": 5532000,
        "external_support": [
            {"service": "Cloud Migration Support", "frequency": "Project", "cost_sar": 500000},
            {"service": "Digital Maturity Assessment", "frequency": "Annual", "cost_sar": 100000},
            {"service": "UX Research", "frequency": "Annual", "cost_sar": 150000},
        ],
        "training_budget": 300000,
        "certification_requirements": ["PMP", "SAFe", "TOGAF", "AWS/Azure/GCP", "Scrum"]
    },
    
    "Global Standards": {
        "roles": [
            {"title": "Management System Director", "fte": 1.0, "level": "Executive", "skills": ["ISO standards", "IMS", "Audit management", "Continuous improvement"], "cost_sar_annual": 420000},
            {"title": "ISMS Manager", "fte": 1.0, "level": "Senior", "skills": ["ISO 27001", "Risk assessment", "Controls", "Audit"], "cost_sar_annual": 300000},
            {"title": "BCM Manager", "fte": 1.0, "level": "Senior", "skills": ["ISO 22301", "BIA", "BCP", "Crisis management"], "cost_sar_annual": 300000},
            {"title": "Quality Manager", "fte": 1.0, "level": "Senior", "skills": ["ISO 9001", "Process improvement", "Metrics", "Customer focus"], "cost_sar_annual": 264000},
            {"title": "Internal Auditor", "fte": 2.0, "level": "Mid", "skills": ["ISO 19011", "Audit planning", "Evidence collection", "Reporting"], "cost_sar_annual": 192000},
            {"title": "Document Controller", "fte": 1.0, "level": "Junior", "skills": ["Document management", "Version control", "Records", "Distribution"], "cost_sar_annual": 120000},
            {"title": "IT Service Manager", "fte": 1.0, "level": "Senior", "skills": ["ITIL 4", "Service desk", "Change management", "SLA"], "cost_sar_annual": 288000},
            {"title": "Compliance Analyst", "fte": 2.0, "level": "Mid", "skills": ["Compliance monitoring", "Gap analysis", "Corrective actions", "Reporting"], "cost_sar_annual": 180000},
        ],
        "total_fte": 10.0,
        "total_annual_cost": 2616000,
        "external_support": [
            {"service": "Certification Audit (ISO 27001)", "frequency": "Annual", "cost_sar": 80000},
            {"service": "Certification Audit (ISO 22301)", "frequency": "Annual", "cost_sar": 60000},
            {"service": "Certification Audit (ISO 9001)", "frequency": "Annual", "cost_sar": 50000},
            {"service": "Pre-certification Gap Assessment", "frequency": "Once", "cost_sar": 100000},
        ],
        "training_budget": 180000,
        "certification_requirements": ["ISO 27001 LA", "ISO 22301 LA", "ISO 9001 LA", "ITIL 4", "CBCI", "CISA"]
    }
}

# =============================================================================
# SCENARIO ANALYSIS (Best/Expected/Worst Case)
# =============================================================================

SCENARIO_ANALYSIS = {
    "Cyber Security": {
        "best_case": {
            "timeline_months": 18,
            "budget_variance": -10,
            "compliance_achieved": 98,
            "assumptions": ["Full executive support", "No major incidents during implementation", "Skilled resources available", "Vendor delivery on time"],
            "probability": 20
        },
        "expected_case": {
            "timeline_months": 24,
            "budget_variance": 0,
            "compliance_achieved": 95,
            "assumptions": ["Normal executive engagement", "Minor incidents manageable", "Some resource gaps filled externally", "Minor vendor delays"],
            "probability": 60
        },
        "worst_case": {
            "timeline_months": 36,
            "budget_variance": 30,
            "compliance_achieved": 80,
            "assumptions": ["Leadership changes", "Major security incident diverts resources", "Key staff turnover", "Significant vendor issues"],
            "probability": 20
        }
    },
    "Artificial Intelligence": {
        "best_case": {
            "timeline_months": 14,
            "budget_variance": -15,
            "compliance_achieved": 100,
            "assumptions": ["Strong data science team", "Clear model inventory", "Executive AI champion", "Good data quality"],
            "probability": 15
        },
        "expected_case": {
            "timeline_months": 18,
            "budget_variance": 0,
            "compliance_achieved": 95,
            "assumptions": ["Normal team capacity", "Some legacy model challenges", "Standard stakeholder engagement", "Moderate data issues"],
            "probability": 55
        },
        "worst_case": {
            "timeline_months": 30,
            "budget_variance": 40,
            "compliance_achieved": 75,
            "assumptions": ["AI talent shortage", "Significant bias issues discovered", "Regulatory changes", "Data quality problems"],
            "probability": 30
        }
    },
    "Data Management": {
        "best_case": {
            "timeline_months": 14,
            "budget_variance": -10,
            "compliance_achieved": 100,
            "assumptions": ["Clear data ownership", "Good existing documentation", "Strong business engagement", "Modern data infrastructure"],
            "probability": 15
        },
        "expected_case": {
            "timeline_months": 18,
            "budget_variance": 5,
            "compliance_achieved": 95,
            "assumptions": ["Typical data silos", "Some ownership disputes", "Standard PDPL gaps", "Legacy system challenges"],
            "probability": 60
        },
        "worst_case": {
            "timeline_months": 28,
            "budget_variance": 35,
            "compliance_achieved": 80,
            "assumptions": ["Data chaos discovered", "Major PDPL violations found", "System integration failures", "Business resistance"],
            "probability": 25
        }
    },
    "Digital Transformation": {
        "best_case": {
            "timeline_months": 18,
            "budget_variance": -5,
            "compliance_achieved": 95,
            "assumptions": ["Strong change adoption", "Modern tech stack", "Agile organization", "Clear product vision"],
            "probability": 10
        },
        "expected_case": {
            "timeline_months": 24,
            "budget_variance": 10,
            "compliance_achieved": 85,
            "assumptions": ["Normal change resistance", "Some legacy constraints", "Standard integration effort", "Typical adoption curve"],
            "probability": 55
        },
        "worst_case": {
            "timeline_months": 42,
            "budget_variance": 50,
            "compliance_achieved": 60,
            "assumptions": ["Major change resistance", "Legacy system failures", "Vendor bankruptcy/issues", "Scope creep"],
            "probability": 35
        }
    },
    "Global Standards": {
        "best_case": {
            "timeline_months": 12,
            "budget_variance": -10,
            "compliance_achieved": 100,
            "assumptions": ["Existing documentation good", "Engaged process owners", "Experienced auditors", "No major NCs"],
            "probability": 20
        },
        "expected_case": {
            "timeline_months": 18,
            "budget_variance": 0,
            "compliance_achieved": 95,
            "assumptions": ["Some documentation gaps", "Normal engagement levels", "Minor NCs expected", "Standard audit findings"],
            "probability": 60
        },
        "worst_case": {
            "timeline_months": 30,
            "budget_variance": 25,
            "compliance_achieved": 80,
            "assumptions": ["Major documentation overhaul", "Process owner resistance", "Failed certification attempt", "Multiple major NCs"],
            "probability": 20
        }
    }
}

# =============================================================================
# RISK HEAT MAP DATA
# =============================================================================

RISK_HEAT_MAP = {
    "Cyber Security": {
        "risks": [
            {"id": "CS-R01", "name": "Ransomware Attack", "likelihood": 4, "impact": 5, "inherent_score": 20, "controls": "EDR, Backup, IR Plan", "residual_likelihood": 2, "residual_impact": 4, "residual_score": 8},
            {"id": "CS-R02", "name": "Data Breach", "likelihood": 3, "impact": 5, "inherent_score": 15, "controls": "DLP, Encryption, IAM", "residual_likelihood": 2, "residual_impact": 4, "residual_score": 8},
            {"id": "CS-R03", "name": "Insider Threat", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "PAM, UEBA, Access Reviews", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "CS-R04", "name": "Third-Party Compromise", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "TPRM, SLAs, Monitoring", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "CS-R05", "name": "DDoS Attack", "likelihood": 4, "impact": 3, "inherent_score": 12, "controls": "WAF, CDN, DDoS Protection", "residual_likelihood": 2, "residual_impact": 2, "residual_score": 4},
            {"id": "CS-R06", "name": "Phishing Attack", "likelihood": 5, "impact": 3, "inherent_score": 15, "controls": "Email Security, Awareness, MFA", "residual_likelihood": 3, "residual_impact": 2, "residual_score": 6},
            {"id": "CS-R07", "name": "Unpatched Vulnerabilities", "likelihood": 4, "impact": 4, "inherent_score": 16, "controls": "Patch Management, VM", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "CS-R08", "name": "Cloud Misconfiguration", "likelihood": 4, "impact": 4, "inherent_score": 16, "controls": "CSPM, IaC, Reviews", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
        ],
        "appetite": {"low": 4, "medium": 9, "high": 16},
        "scale": {"1": "Rare", "2": "Unlikely", "3": "Possible", "4": "Likely", "5": "Almost Certain"}
    },
    "Artificial Intelligence": {
        "risks": [
            {"id": "AI-R01", "name": "Biased Model Decisions", "likelihood": 4, "impact": 5, "inherent_score": 20, "controls": "Bias Testing, Monitoring", "residual_likelihood": 2, "residual_impact": 4, "residual_score": 8},
            {"id": "AI-R02", "name": "Model Drift", "likelihood": 4, "impact": 3, "inherent_score": 12, "controls": "MLOps, Monitoring, Alerts", "residual_likelihood": 2, "residual_impact": 2, "residual_score": 4},
            {"id": "AI-R03", "name": "Training Data Poisoning", "likelihood": 2, "impact": 5, "inherent_score": 10, "controls": "Data Validation, Access Controls", "residual_likelihood": 1, "residual_impact": 4, "residual_score": 4},
            {"id": "AI-R04", "name": "Adversarial Attack", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "Robustness Testing, Input Validation", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "AI-R05", "name": "Unexplainable Decisions", "likelihood": 4, "impact": 4, "inherent_score": 16, "controls": "XAI Framework, Documentation", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "AI-R06", "name": "Privacy Violation (Training Data)", "likelihood": 3, "impact": 5, "inherent_score": 15, "controls": "PETs, Data Anonymization", "residual_likelihood": 2, "residual_impact": 4, "residual_score": 8},
            {"id": "AI-R07", "name": "Regulatory Non-Compliance", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "SDAIA Alignment, Audits", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
        ],
        "appetite": {"low": 4, "medium": 9, "high": 16},
        "scale": {"1": "Rare", "2": "Unlikely", "3": "Possible", "4": "Likely", "5": "Almost Certain"}
    },
    "Data Management": {
        "risks": [
            {"id": "DM-R01", "name": "PDPL Non-Compliance", "likelihood": 4, "impact": 5, "inherent_score": 20, "controls": "PDPL Program, DPO, PIA", "residual_likelihood": 2, "residual_impact": 4, "residual_score": 8},
            {"id": "DM-R02", "name": "Data Quality Issues", "likelihood": 5, "impact": 3, "inherent_score": 15, "controls": "DQ Monitoring, Stewardship", "residual_likelihood": 3, "residual_impact": 2, "residual_score": 6},
            {"id": "DM-R03", "name": "Unauthorized Data Access", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "Access Controls, Classification", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "DM-R04", "name": "Data Loss", "likelihood": 2, "impact": 5, "inherent_score": 10, "controls": "Backup, DR, Encryption", "residual_likelihood": 1, "residual_impact": 4, "residual_score": 4},
            {"id": "DM-R05", "name": "DSAR Response Failure", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "DSAR Process, Automation", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "DM-R06", "name": "Cross-Border Transfer Violation", "likelihood": 3, "impact": 5, "inherent_score": 15, "controls": "Transfer Assessment, Safeguards", "residual_likelihood": 2, "residual_impact": 4, "residual_score": 8},
        ],
        "appetite": {"low": 4, "medium": 9, "high": 16},
        "scale": {"1": "Rare", "2": "Unlikely", "3": "Possible", "4": "Likely", "5": "Almost Certain"}
    },
    "Digital Transformation": {
        "risks": [
            {"id": "DT-R01", "name": "Project Failure/Delay", "likelihood": 4, "impact": 4, "inherent_score": 16, "controls": "PMO, Agile, Governance", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "DT-R02", "name": "Change Resistance", "likelihood": 5, "impact": 3, "inherent_score": 15, "controls": "Change Management, Communication", "residual_likelihood": 3, "residual_impact": 2, "residual_score": 6},
            {"id": "DT-R03", "name": "Integration Failure", "likelihood": 4, "impact": 4, "inherent_score": 16, "controls": "Architecture, Testing, APIs", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "DT-R04", "name": "Vendor Lock-in", "likelihood": 3, "impact": 3, "inherent_score": 9, "controls": "Multi-cloud, Standards, Contracts", "residual_likelihood": 2, "residual_impact": 2, "residual_score": 4},
            {"id": "DT-R05", "name": "Cybersecurity Gaps (New Systems)", "likelihood": 4, "impact": 4, "inherent_score": 16, "controls": "Security by Design, Testing", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "DT-R06", "name": "Budget Overrun", "likelihood": 4, "impact": 3, "inherent_score": 12, "controls": "Financial Controls, Monitoring", "residual_likelihood": 3, "residual_impact": 2, "residual_score": 6},
            {"id": "DT-R07", "name": "Skills Gap", "likelihood": 4, "impact": 3, "inherent_score": 12, "controls": "Training, Hiring, Partners", "residual_likelihood": 2, "residual_impact": 2, "residual_score": 4},
        ],
        "appetite": {"low": 4, "medium": 9, "high": 16},
        "scale": {"1": "Rare", "2": "Unlikely", "3": "Possible", "4": "Likely", "5": "Almost Certain"}
    },
    "Global Standards": {
        "risks": [
            {"id": "GS-R01", "name": "Certification Failure", "likelihood": 2, "impact": 5, "inherent_score": 10, "controls": "Pre-audit, Gap Closure, Preparation", "residual_likelihood": 1, "residual_impact": 4, "residual_score": 4},
            {"id": "GS-R02", "name": "Major Non-Conformity", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "Internal Audits, CAPA", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "GS-R03", "name": "Documentation Gaps", "likelihood": 4, "impact": 3, "inherent_score": 12, "controls": "Document Control, Reviews", "residual_likelihood": 2, "residual_impact": 2, "residual_score": 4},
            {"id": "GS-R04", "name": "BCP Test Failure", "likelihood": 3, "impact": 4, "inherent_score": 12, "controls": "Regular Testing, Updates", "residual_likelihood": 2, "residual_impact": 3, "residual_score": 6},
            {"id": "GS-R05", "name": "Management System Fatigue", "likelihood": 4, "impact": 3, "inherent_score": 12, "controls": "IMS Integration, Automation", "residual_likelihood": 2, "residual_impact": 2, "residual_score": 4},
            {"id": "GS-R06", "name": "Resource Constraints", "likelihood": 4, "impact": 3, "inherent_score": 12, "controls": "Planning, Prioritization", "residual_likelihood": 3, "residual_impact": 2, "residual_score": 6},
        ],
        "appetite": {"low": 4, "medium": 9, "high": 16},
        "scale": {"1": "Rare", "2": "Unlikely", "3": "Possible", "4": "Likely", "5": "Almost Certain"}
    }
}

# =============================================================================
# ENHANCED AUDIT DETAILS
# =============================================================================

AUDIT_EVIDENCE_TEMPLATES = {
    "evidence_types": [
        "Policy document review",
        "Procedure walkthrough",
        "Configuration screenshot",
        "System-generated report",
        "Interview notes",
        "Sample testing results",
        "Log file analysis",
        "Access control listing",
        "Training records",
        "Meeting minutes",
        "Third-party attestation",
        "Vulnerability scan report"
    ],
    "sample_sizes": {
        "small_population": {"population": "< 50", "sample": "All items or 25%", "confidence": "95%"},
        "medium_population": {"population": "50-500", "sample": "25-50 items", "confidence": "95%"},
        "large_population": {"population": "> 500", "sample": "Statistical sample (59 items)", "confidence": "95%", "error_margin": "10%"}
    },
    "root_cause_categories": [
        "People: Lack of training or awareness",
        "People: Resource constraints",
        "People: Unclear roles and responsibilities",
        "Process: Undocumented or unclear process",
        "Process: Process not followed",
        "Process: Process design flaw",
        "Technology: System limitation",
        "Technology: Misconfiguration",
        "Technology: Integration issue",
        "Governance: Policy gap",
        "Governance: Inadequate oversight",
        "External: Vendor/third-party issue"
    ],
    "management_response_template": {
        "fields": ["Agreed/Disagreed", "Action Plan", "Responsible Owner", "Target Date", "Resources Required", "Status"],
        "statuses": ["Not Started", "In Progress", "Completed", "Overdue", "Deferred"]
    }
}

ENHANCED_AUDIT_FINDINGS = {
    "Cyber Security": [
        {
            "id": "CS-F01",
            "title": "Privileged Access Management Gaps",
            "control_ref": "NCA ECC 2-3-1, ISO 27001 A.9.2.3",
            "priority": "HIGH",
            "observation": "Privileged accounts lack adequate controls. 23% of admin accounts have no MFA, PAM solution covers only 45% of privileged access, and quarterly access reviews are not performed consistently.",
            "evidence": ["AD privileged group listing (sample 50 accounts)", "PAM coverage report", "Access review records (last 12 months)", "Interview with IT Security Manager"],
            "sample_size": "50 privileged accounts from population of 187",
            "root_cause": "Process: Undocumented PAM onboarding process; Technology: Legacy systems not integrated with PAM",
            "risk_impact": "Unauthorized privileged access could lead to data breach, system compromise, or regulatory non-compliance (NCA ECC)",
            "recommendation": "1) Implement MFA for all privileged accounts within 30 days; 2) Expand PAM coverage to 100% within 90 days; 3) Establish monthly access review process with documented evidence",
            "management_response": "[To be completed by management]",
            "target_date": "Q1 2025",
            "estimated_effort": "Medium (2-3 months, 1.5 FTE)"
        },
        {
            "id": "CS-F02",
            "title": "Security Monitoring Coverage Gaps",
            "control_ref": "NCA ECC 2-7-1, ISO 27001 A.12.4.1",
            "priority": "HIGH",
            "observation": "SIEM coverage is incomplete with only 67% of critical systems sending logs. Alert rules have not been updated in 8 months, and there is no documented 24/7 monitoring procedure.",
            "evidence": ["SIEM data source inventory", "Alert rule configuration", "SOC shift schedule", "Incident ticket analysis (last 6 months)"],
            "sample_size": "All critical systems (45 systems), alert rules (234 rules)",
            "root_cause": "Technology: Integration challenges with legacy systems; People: SOC understaffing",
            "risk_impact": "Delayed threat detection increasing MTTD, potential for undetected breaches",
            "recommendation": "1) Complete SIEM integration for remaining critical systems; 2) Review and update alert rules quarterly; 3) Establish documented 24/7 SOC procedures; 4) Consider SOAR implementation for automation",
            "management_response": "[To be completed by management]",
            "target_date": "Q1-Q2 2025",
            "estimated_effort": "High (4-6 months, 2.0 FTE + vendor support)"
        }
    ],
    "Artificial Intelligence": [
        {
            "id": "AI-F01",
            "title": "AI Model Inventory Incomplete",
            "control_ref": "SDAIA AI Ethics Principle 3, NIST AI RMF MAP",
            "priority": "HIGH",
            "observation": "No centralized AI model registry exists. Through interviews, we identified 12 production ML models, but the organization could not provide a complete inventory. Model documentation is inconsistent.",
            "evidence": ["Stakeholder interviews (5 departments)", "Discovered model list", "Sample model documentation (3 models)", "Data science team assessment"],
            "sample_size": "All identified production models (12)",
            "root_cause": "Governance: No AI governance policy; Process: No model registration requirement",
            "risk_impact": "Unknown AI risk exposure, inability to demonstrate SDAIA compliance, potential for biased or harmful AI operating unmonitored",
            "recommendation": "1) Establish AI model registry within 60 days; 2) Conduct organization-wide AI model discovery; 3) Define mandatory model documentation standards; 4) Implement model lifecycle management process",
            "management_response": "[To be completed by management]",
            "target_date": "Q1 2025",
            "estimated_effort": "Medium (2-3 months, 1.0 FTE)"
        },
        {
            "id": "AI-F02",
            "title": "Bias Testing Not Performed",
            "control_ref": "SDAIA AI Ethics Principle 2 (Fairness), NIST AI RMF MEASURE",
            "priority": "HIGH",
            "observation": "None of the 3 customer-facing AI models sampled have documented bias testing. The credit scoring model shows potential demographic disparities but no formal fairness assessment has been conducted.",
            "evidence": ["Model documentation review", "Bias testing records (none found)", "Model output analysis (credit scoring)", "Interview with data science lead"],
            "sample_size": "3 customer-facing models from 5 identified",
            "root_cause": "People: Lack of bias testing expertise; Governance: No fairness requirements defined",
            "risk_impact": "Discriminatory outcomes affecting customers, regulatory violations, reputational damage, potential litigation",
            "recommendation": "1) Immediately assess credit scoring model for demographic bias; 2) Implement bias testing tools (e.g., AI Fairness 360); 3) Define fairness metrics and thresholds; 4) Establish ongoing fairness monitoring",
            "management_response": "[To be completed by management]",
            "target_date": "Immediate / Q1 2025",
            "estimated_effort": "High (3-4 months, 1.5 FTE + external expertise)"
        }
    ],
    "Data Management": [
        {
            "id": "DM-F01",
            "title": "PDPL Consent Management Gaps",
            "control_ref": "PDPL Article 6, 10",
            "priority": "HIGH",
            "observation": "Consent collection mechanisms do not meet PDPL requirements. 40% of sampled consent forms lack required disclosures, consent withdrawal process takes 15+ days vs. required reasonable timeframe.",
            "evidence": ["Consent form samples (25 forms)", "Consent database records", "Withdrawal request log", "Process walkthrough with DPO"],
            "sample_size": "25 consent forms from 3 channels, 15 withdrawal requests",
            "root_cause": "Process: Legacy consent forms not updated; Technology: Manual withdrawal process",
            "risk_impact": "PDPL non-compliance, regulatory fines up to SAR 5M, reputational damage, invalid processing activities",
            "recommendation": "1) Update all consent forms with PDPL-compliant language; 2) Implement consent management platform; 3) Automate withdrawal process to achieve < 72 hour response; 4) Conduct consent audit across all processing activities",
            "management_response": "[To be completed by management]",
            "target_date": "Q1 2025",
            "estimated_effort": "High (3-4 months, 2.0 FTE + legal support)"
        }
    ],
    "Digital Transformation": [
        {
            "id": "DT-F01",
            "title": "Change Management Process Gaps",
            "control_ref": "DGA Digital Standards, ITIL Change Management",
            "priority": "MEDIUM",
            "observation": "Digital transformation initiatives lack formal change management. User adoption rates for recent digital tools average 45% vs. 80% target. No change impact assessment process exists.",
            "evidence": ["Adoption metrics (3 recent initiatives)", "Change management documentation (none)", "User feedback surveys", "Interview with project managers"],
            "sample_size": "3 major digital initiatives from last 18 months",
            "root_cause": "Process: No change management framework; People: Change management skills gap",
            "risk_impact": "Failed digital adoption reducing ROI, employee frustration, project delays and cost overruns",
            "recommendation": "1) Establish change management framework (PROSCI/ADKAR); 2) Hire or train change management resources; 3) Mandate change impact assessment for all initiatives; 4) Implement adoption tracking and intervention process",
            "management_response": "[To be completed by management]",
            "target_date": "Q2 2025",
            "estimated_effort": "Medium (3 months, 1.0 FTE + training)"
        }
    ],
    "Global Standards": [
        {
            "id": "GS-F01",
            "title": "Internal Audit Program Deficiencies",
            "control_ref": "ISO 19011, ISO 27001 9.2, ISO 22301 9.2",
            "priority": "MEDIUM",
            "observation": "Internal audit program does not cover all ISO requirements. 2024 audit plan achieved only 60% completion. Auditor competency records are incomplete, and audit evidence is not consistently retained.",
            "evidence": ["2024 audit plan and status", "Auditor training records", "Sample audit reports (5)", "Evidence retention records"],
            "sample_size": "5 audit reports from 12 planned audits",
            "root_cause": "People: Insufficient internal auditor capacity; Process: No audit management tool",
            "risk_impact": "Certification risk if auditors identify incomplete internal audit program, missed improvement opportunities",
            "recommendation": "1) Complete remaining 2024 audits or document justified deferrals; 2) Establish auditor competency matrix and training plan; 3) Implement audit management tool; 4) Develop 2025 risk-based audit plan",
            "management_response": "[To be completed by management]",
            "target_date": "Q1 2025",
            "estimated_effort": "Medium (2-3 months, 0.5 FTE)"
        }
    ]
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_resource_requirements(domain: str) -> Dict:
    """Get resource requirements for a domain."""
    return RESOURCE_REQUIREMENTS.get(domain, RESOURCE_REQUIREMENTS["Cyber Security"])


def get_scenario_analysis(domain: str) -> Dict:
    """Get scenario analysis for a domain."""
    return SCENARIO_ANALYSIS.get(domain, SCENARIO_ANALYSIS["Cyber Security"])


def get_risk_heat_map(domain: str) -> Dict:
    """Get risk heat map data for a domain."""
    return RISK_HEAT_MAP.get(domain, RISK_HEAT_MAP["Cyber Security"])


def get_enhanced_audit_findings(domain: str) -> List[Dict]:
    """Get enhanced audit findings for a domain."""
    return ENHANCED_AUDIT_FINDINGS.get(domain, ENHANCED_AUDIT_FINDINGS["Cyber Security"])


def get_audit_evidence_templates() -> Dict:
    """Get audit evidence templates."""
    return AUDIT_EVIDENCE_TEMPLATES


def format_resource_table(domain: str, language: str = "English") -> str:
    """Format resource requirements as a table."""
    resources = get_resource_requirements(domain)
    
    if language in ["Arabic", "العربية"]:
        header = "| الدور | عدد الموظفين | المستوى | المهارات الأساسية | التكلفة السنوية (ريال) |"
        separator = "|-------|-------------|---------|-------------------|----------------------|"
        rows = []
        for role in resources["roles"]:
            skills = "، ".join(role["skills"][:2])
            rows.append(f"| {role['title']} | {role['fte']} | {role['level']} | {skills} | {role['cost_sar_annual']:,} |")
        
        total = f"\n**الإجمالي:** {resources['total_fte']} موظف | {resources['total_annual_cost']:,} ريال سنوياً"
        return header + "\n" + separator + "\n" + "\n".join(rows) + total
    else:
        header = "| Role | FTE | Level | Key Skills | Annual Cost (SAR) |"
        separator = "|------|-----|-------|------------|-------------------|"
        rows = []
        for role in resources["roles"]:
            skills = ", ".join(role["skills"][:2])
            rows.append(f"| {role['title']} | {role['fte']} | {role['level']} | {skills} | {role['cost_sar_annual']:,} |")
        
        total = f"\n**Total:** {resources['total_fte']} FTE | SAR {resources['total_annual_cost']:,} annually"
        return header + "\n" + separator + "\n" + "\n".join(rows) + total


def format_scenario_analysis(domain: str, language: str = "English") -> str:
    """Format scenario analysis."""
    scenarios = get_scenario_analysis(domain)
    
    if language in ["Arabic", "العربية"]:
        output = "**تحليل السيناريوهات**\n\n"
        output += "| السيناريو | المدة (شهر) | تباين الميزانية | الامتثال المتوقع | الاحتمالية |\n"
        output += "|----------|------------|----------------|-----------------|------------|\n"
        output += f"| الأفضل | {scenarios['best_case']['timeline_months']} | {scenarios['best_case']['budget_variance']}% | {scenarios['best_case']['compliance_achieved']}% | {scenarios['best_case']['probability']}% |\n"
        output += f"| المتوقع | {scenarios['expected_case']['timeline_months']} | {scenarios['expected_case']['budget_variance']}% | {scenarios['expected_case']['compliance_achieved']}% | {scenarios['expected_case']['probability']}% |\n"
        output += f"| الأسوأ | {scenarios['worst_case']['timeline_months']} | +{scenarios['worst_case']['budget_variance']}% | {scenarios['worst_case']['compliance_achieved']}% | {scenarios['worst_case']['probability']}% |\n"
    else:
        output = "**Scenario Analysis**\n\n"
        output += "| Scenario | Timeline (Months) | Budget Variance | Expected Compliance | Probability |\n"
        output += "|----------|-------------------|-----------------|---------------------|-------------|\n"
        output += f"| Best Case | {scenarios['best_case']['timeline_months']} | {scenarios['best_case']['budget_variance']}% | {scenarios['best_case']['compliance_achieved']}% | {scenarios['best_case']['probability']}% |\n"
        output += f"| Expected | {scenarios['expected_case']['timeline_months']} | {scenarios['expected_case']['budget_variance']}% | {scenarios['expected_case']['compliance_achieved']}% | {scenarios['expected_case']['probability']}% |\n"
        output += f"| Worst Case | {scenarios['worst_case']['timeline_months']} | +{scenarios['worst_case']['budget_variance']}% | {scenarios['worst_case']['compliance_achieved']}% | {scenarios['worst_case']['probability']}% |\n"
    
    return output


def format_risk_heat_map(domain: str, language: str = "English") -> str:
    """Format risk heat map as text table."""
    heat_map = get_risk_heat_map(domain)
    
    if language in ["Arabic", "العربية"]:
        output = "**مصفوفة المخاطر**\n\n"
        output += "| المعرف | الخطر | الاحتمال | الأثر | الدرجة الكامنة | الضوابط | الدرجة المتبقية |\n"
        output += "|--------|-------|---------|-------|---------------|---------|----------------|\n"
        for risk in heat_map["risks"]:
            output += f"| {risk['id']} | {risk['name']} | {risk['likelihood']} | {risk['impact']} | {risk['inherent_score']} | {risk['controls']} | {risk['residual_score']} |\n"
    else:
        output = "**Risk Heat Map**\n\n"
        output += "| ID | Risk | Likelihood | Impact | Inherent Score | Controls | Residual Score |\n"
        output += "|----|------|------------|--------|----------------|----------|----------------|\n"
        for risk in heat_map["risks"]:
            output += f"| {risk['id']} | {risk['name']} | {risk['likelihood']} | {risk['impact']} | {risk['inherent_score']} | {risk['controls']} | {risk['residual_score']} |\n"
    
    return output
