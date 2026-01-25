"""
Mizan GRC - Realistic Maturity Assessment Engine
Based on actual controls in place, not self-reported scores.

For NCA ECC and other frameworks, we assess maturity based on:
1. Control coverage across domains
2. Process maturity indicators
3. Governance indicators
"""

from typing import Dict, List, Tuple, Optional
import re


# =============================================================================
# NCA ECC CONTROL DOMAINS AND WEIGHTS
# =============================================================================

NCA_ECC_DOMAINS = {
    "governance": {
        "name": "Cybersecurity Governance",
        "weight": 0.20,  # 20% of total score
        "controls": [
            "cybersecurity strategy",
            "cybersecurity policy",
            "roles and responsibilities",
            "risk management",
            "compliance program",
            "periodic review",
            "security committee",
            "ciso",
            "security charter"
        ],
        "minimum_for_managed": 5  # Need at least 5 for Level 4
    },
    "identity_access": {
        "name": "Identity & Access Management",
        "weight": 0.15,
        "controls": [
            "iam", "identity management", "access control",
            "mfa", "multi-factor", "2fa", "two-factor",
            "pam", "privileged access", "privileged account",
            "access review", "access certification",
            "sso", "single sign-on",
            "directory service", "active directory", "ldap",
            "password policy", "password management"
        ],
        "minimum_for_managed": 4
    },
    "network_security": {
        "name": "Network Security",
        "weight": 0.12,
        "controls": [
            "firewall", "next-gen firewall", "ngfw",
            "ips", "ids", "intrusion",
            "network segmentation", "vlan", "microsegmentation",
            "vpn", "remote access",
            "waf", "web application firewall",
            "ddos", "anti-ddos",
            "proxy", "web filter", "url filter",
            "nac", "network access control"
        ],
        "minimum_for_managed": 4
    },
    "endpoint_security": {
        "name": "Endpoint Security",
        "weight": 0.10,
        "controls": [
            "edr", "xdr", "endpoint detection",
            "antivirus", "anti-malware", "epp",
            "dlp", "data loss prevention",
            "mdm", "mobile device management",
            "encryption", "disk encryption", "bitlocker",
            "patch management", "wsus"
        ],
        "minimum_for_managed": 3
    },
    "security_operations": {
        "name": "Security Operations",
        "weight": 0.12,
        "controls": [
            "siem", "security monitoring", "log management",
            "soc", "security operations center",
            "incident response", "ir plan", "ir team",
            "threat intelligence", "threat hunting",
            "vulnerability management", "vulnerability scanner",
            "penetration testing", "pentest", "red team"
        ],
        "minimum_for_managed": 4
    },
    "data_protection": {
        "name": "Data Protection",
        "weight": 0.10,
        "controls": [
            "backup", "data backup", "backup solution",
            "drp", "disaster recovery", "dr site",
            "data classification", "data labeling",
            "encryption", "data encryption", "tde",
            "key management", "hsm", "kms",
            "data masking", "tokenization"
        ],
        "minimum_for_managed": 3
    },
    "awareness_training": {
        "name": "Security Awareness",
        "weight": 0.08,
        "controls": [
            "security awareness", "awareness training",
            "phishing simulation", "phishing test",
            "security training", "security education"
        ],
        "minimum_for_managed": 2
    },
    "third_party": {
        "name": "Third-Party Risk",
        "weight": 0.08,
        "controls": [
            "vendor management", "vendor assessment",
            "third-party risk", "tprm", "supply chain",
            "vendor security", "supplier assessment"
        ],
        "minimum_for_managed": 2
    },
    "business_continuity": {
        "name": "Business Continuity",
        "weight": 0.05,
        "controls": [
            "bcp", "business continuity", "continuity plan",
            "drp", "disaster recovery",
            "crisis management", "emergency response"
        ],
        "minimum_for_managed": 2
    }
}


# =============================================================================
# MATURITY INDICATORS (Process Maturity)
# =============================================================================

MATURITY_INDICATORS = {
    "level_1_initial": [
        "ad-hoc", "no formal", "reactive", "undefined"
    ],
    "level_2_developing": [
        "basic", "some", "partial", "developing", "in progress"
    ],
    "level_3_defined": [
        "documented", "defined", "standardized", "process", "procedure"
    ],
    "level_4_managed": [
        "measured", "monitored", "kpi", "metrics", "sla",
        "24x7", "24/7", "continuous", "automated"
    ],
    "level_5_optimizing": [
        "optimized", "continuous improvement", "predictive",
        "ai-driven", "machine learning", "advanced analytics"
    ]
}


def assess_maturity_from_controls(
    tech_stack: str,
    challenges: str = "",
    domain: str = "Cyber Security",
    self_reported_score: Optional[int] = None
) -> Dict:
    """
    Assess realistic maturity based on controls mentioned.
    
    Args:
        tech_stack: Technologies/controls in place (from UI input)
        challenges: Challenges mentioned (may indicate gaps)
        domain: Domain being assessed
        self_reported_score: Optional self-reported compliance score
        
    Returns:
        Dict with maturity level, calculated score, confidence, and details
    """
    
    tech_lower = tech_stack.lower() if tech_stack else ""
    challenges_lower = challenges.lower() if challenges else ""
    
    # Tokenize tech stack for matching
    # Replace common separators with spaces
    tech_normalized = tech_lower.replace(',', ' ').replace(';', ' ').replace('/', ' ').replace('-', ' ')
    tech_tokens = set(tech_normalized.split())
    
    # Assess each domain
    domain_scores = {}
    total_weighted_score = 0
    controls_found = []
    controls_missing = []
    
    for domain_key, domain_info in NCA_ECC_DOMAINS.items():
        controls_matched = []
        for control in domain_info["controls"]:
            control_lower = control.lower()
            
            # Strategy 1: Full phrase match
            if control_lower in tech_lower:
                if control not in controls_matched:
                    controls_matched.append(control)
                continue
            
            # Strategy 2: All significant words of control appear in tech
            control_words = [w for w in control_lower.split() if len(w) > 2]
            if len(control_words) >= 2:
                # Multi-word control - require at least 2 words match
                matches = sum(1 for w in control_words if w in tech_lower or w in tech_tokens)
                if matches >= 2:
                    if control not in controls_matched:
                        controls_matched.append(control)
                    continue
            else:
                # Single word control - must be exact token match
                if control_lower in tech_tokens:
                    if control not in controls_matched:
                        controls_matched.append(control)
        
        # Calculate domain coverage with realistic scoring curve
        # Having 1 control shows you've started = 20%
        # Having 2 controls shows basic capability = 35%  
        # Having 3+ controls shows good coverage = 50%+
        # Having minimum_for_managed = 70%
        # Having 5+ = 85%+
        
        n_matched = len(controls_matched)
        min_for_managed = domain_info.get("minimum_for_managed", 3)
        
        if n_matched == 0:
            domain_score = 0
        elif n_matched == 1:
            domain_score = 20
        elif n_matched == 2:
            domain_score = 35
        elif n_matched < min_for_managed:
            domain_score = 35 + (n_matched - 2) * 10  # 45, 55...
        elif n_matched == min_for_managed:
            domain_score = 70
        elif n_matched == min_for_managed + 1:
            domain_score = 80
        else:
            domain_score = min(85 + (n_matched - min_for_managed - 1) * 5, 100)
        
        # Weight the score
        weighted = domain_score * domain_info["weight"]
        total_weighted_score += weighted
        
        domain_scores[domain_key] = {
            "name": domain_info["name"],
            "controls_found": controls_matched,
            "controls_count": len(controls_matched),
            "total_controls": len(domain_info["controls"]),
            "coverage_pct": domain_score,
            "weighted_score": weighted,
            "meets_managed_threshold": len(controls_matched) >= min_for_managed
        }
        
        controls_found.extend(controls_matched)
        
        # Identify critical missing domains (0 coverage in important areas)
        if domain_score == 0 and domain_info["weight"] >= 0.10:
            controls_missing.append(domain_info["name"])
    
    # Base score adjustments:
    # - Having ANY technical controls means you've started (base 10%)
    # - Each domain with coverage adds credibility
    total_controls_found = len(controls_found)
    domains_with_coverage = sum(1 for d in domain_scores.values() if d["controls_count"] > 0)
    
    # Base score for having some security program
    base_score = 0
    if total_controls_found >= 2:
        base_score = 10  # Started security journey
    if domains_with_coverage >= 3:
        base_score += 5  # Breadth across domains
    if total_controls_found >= 8:
        base_score += 5  # Good depth of controls
    
    # Calculate overall score with base
    calculated_score = min(total_weighted_score + base_score, 100)
    
    # Determine maturity level based on calculated score
    if calculated_score < 20:
        maturity_level = 1
        maturity_name_en = "Initial"
        maturity_name_ar = "أولي"
    elif calculated_score < 40:
        maturity_level = 2
        maturity_name_en = "Developing"
        maturity_name_ar = "تطوير"
    elif calculated_score < 60:
        maturity_level = 3
        maturity_name_en = "Defined"
        maturity_name_ar = "محدد"
    elif calculated_score < 80:
        maturity_level = 4
        maturity_name_en = "Managed"
        maturity_name_ar = "مُدار"
    else:
        maturity_level = 5
        maturity_name_en = "Optimizing"
        maturity_name_ar = "تحسين مستمر"
    
    # Check for maturity level 4 prerequisites
    domains_meeting_managed = sum(
        1 for d in domain_scores.values() if d["meets_managed_threshold"]
    )
    
    # If claiming Level 4 but not enough domains meet threshold, cap at Level 3
    if maturity_level >= 4 and domains_meeting_managed < 6:
        maturity_level = 3
        maturity_name_en = "Defined"
        maturity_name_ar = "محدد"
        calculated_score = min(calculated_score, 59)  # Cap score
    
    # Calculate confidence based on data quality
    confidence = 75  # Base confidence
    
    # Reduce confidence if self-reported score differs significantly
    if self_reported_score is not None:
        score_diff = abs(self_reported_score - calculated_score)
        if score_diff > 30:
            confidence -= 20
        elif score_diff > 15:
            confidence -= 10
    
    # Reduce confidence if very few controls mentioned
    if len(controls_found) < 5:
        confidence -= 15
    
    # Increase confidence if many controls mentioned
    if len(controls_found) > 10:
        confidence += 5
    
    confidence = max(50, min(90, confidence))  # Keep between 50-90
    
    # Generate assessment notes
    assessment_notes = []
    
    if len(controls_found) < 5:
        assessment_notes.append(
            "Limited security controls identified. Score based on available information."
        )
    
    if controls_missing:
        assessment_notes.append(
            f"Critical gaps in: {', '.join(controls_missing[:3])}"
        )
    
    if self_reported_score and abs(self_reported_score - calculated_score) > 20:
        assessment_notes.append(
            f"Self-reported score ({self_reported_score}%) differs significantly from "
            f"control-based assessment ({calculated_score:.0f}%). Recommend detailed gap analysis."
        )
    
    return {
        "maturity_level": maturity_level,
        "maturity_name_en": maturity_name_en,
        "maturity_name_ar": maturity_name_ar,
        "calculated_score": round(calculated_score, 1),
        "self_reported_score": self_reported_score,
        "confidence": confidence,
        "controls_found": controls_found,
        "controls_count": len(controls_found),
        "critical_gaps": controls_missing,
        "domain_scores": domain_scores,
        "domains_meeting_managed_threshold": domains_meeting_managed,
        "assessment_notes": assessment_notes
    }


def get_maturity_assessment_summary(assessment: Dict, language: str = "English") -> str:
    """Generate human-readable maturity assessment summary."""
    
    if language in ["Arabic", "العربية"]:
        return f"""**تقييم مستوى النضج**

**المستوى:** {assessment['maturity_name_ar']} (المستوى {assessment['maturity_level']} من ٥)
**النتيجة المحسوبة:** {assessment['calculated_score']}%
**درجة الثقة:** {assessment['confidence']}/100

**الضوابط المكتشفة:** {assessment['controls_count']} ضابط
**الفجوات الحرجة:** {', '.join(assessment['critical_gaps'][:3]) if assessment['critical_gaps'] else 'لا توجد فجوات حرجة'}

**ملاحظات:**
{chr(10).join('- ' + note for note in assessment['assessment_notes']) if assessment['assessment_notes'] else '- التقييم مبني على الضوابط المذكورة'}
"""
    else:
        return f"""**Maturity Level Assessment**

**Level:** {assessment['maturity_name_en']} (Level {assessment['maturity_level']} of 5)
**Calculated Score:** {assessment['calculated_score']}%
**Confidence:** {assessment['confidence']}/100

**Controls Identified:** {assessment['controls_count']} controls
**Critical Gaps:** {', '.join(assessment['critical_gaps'][:3]) if assessment['critical_gaps'] else 'None identified'}

**Assessment Notes:**
{chr(10).join('- ' + note for note in assessment['assessment_notes']) if assessment['assessment_notes'] else '- Assessment based on controls mentioned'}
"""


# Quick test
if __name__ == "__main__":
    # Test case: User with only basic controls
    test_tech = "EDR/XDR, Next-Gen Firewall, WAF, Data Backup"
    
    result = assess_maturity_from_controls(
        tech_stack=test_tech,
        challenges="Legacy systems",
        self_reported_score=75
    )
    
    print("Test: Basic controls only")
    print(f"Tech: {test_tech}")
    print(f"Result: Level {result['maturity_level']} ({result['maturity_name_en']})")
    print(f"Score: {result['calculated_score']}%")
    print(f"Confidence: {result['confidence']}")
    print(f"Controls found: {result['controls_count']}")
    print(f"Gaps: {result['critical_gaps']}")
