"""
Document Validation Utility for Mizan GRC
Validates that uploaded documents are relevant to the selected domain.
"""

from typing import Tuple, List
import re


# Domain-specific keywords for validation
DOMAIN_KEYWORDS = {
    "Cyber Security": {
        "strong": [
            "cybersecurity", "cyber security", "information security", "infosec",
            "nca", "sama", "ecc", "ccc", "csf", "iso 27001", "iso27001",
            "firewall", "intrusion", "malware", "ransomware", "phishing",
            "siem", "soc", "incident response", "vulnerability", "penetration test",
            "access control", "authentication", "encryption", "endpoint",
            "threat", "attack", "breach", "security awareness",
            "الأمن السيبراني", "أمن المعلومات", "الهيئة الوطنية للأمن السيبراني"
        ],
        "weak": [
            "security", "protection", "risk", "control", "policy", "compliance",
            "audit", "assessment", "framework"
        ],
        "exclude": [
            "food safety", "physical security only", "building security"
        ]
    },
    "Artificial Intelligence": {
        "strong": [
            "artificial intelligence", "ai governance", "machine learning", "ml model",
            "deep learning", "neural network", "algorithm", "sdaia", "ai ethics",
            "model risk", "bias", "fairness", "explainability", "xai",
            "training data", "inference", "prediction", "classification",
            "llm", "large language model", "generative ai", "chatbot",
            "computer vision", "nlp", "natural language",
            "الذكاء الاصطناعي", "التعلم الآلي", "سدايا", "أخلاقيات الذكاء الاصطناعي"
        ],
        "weak": [
            "model", "automation", "intelligent", "smart", "data science"
        ],
        "exclude": [
            "traditional software", "rule-based only"
        ]
    },
    "Data Management": {
        "strong": [
            "data governance", "data management", "pdpl", "personal data protection",
            "ndmo", "data privacy", "data quality", "data catalog", "metadata",
            "data classification", "data retention", "data lifecycle",
            "master data", "mdm", "data steward", "data owner",
            "consent management", "data subject rights", "dsar",
            "gdpr", "data protection", "pii", "personally identifiable",
            "حماية البيانات الشخصية", "حوكمة البيانات", "خصوصية البيانات"
        ],
        "weak": [
            "data", "database", "information", "records", "privacy"
        ],
        "exclude": [
            "cybersecurity only", "network security"
        ]
    },
    "Digital Transformation": {
        "strong": [
            "digital transformation", "digitization", "digitalization",
            "cloud migration", "cloud adoption", "saas", "paas", "iaas",
            "agile", "devops", "microservices", "api", "digital customer",
            "omnichannel", "mobile app", "user experience", "ux",
            "rpa", "robotic process automation", "workflow automation",
            "low-code", "no-code", "digital strategy", "vision 2030",
            "التحول الرقمي", "الرقمنة", "الحوسبة السحابية"
        ],
        "weak": [
            "digital", "technology", "innovation", "modernization", "automation"
        ],
        "exclude": [
            "cybersecurity policy", "security controls"
        ]
    },
    "Global Standards": {
        "strong": [
            "iso 27001", "iso 22301", "iso 9001", "iso 31000", "iso 27002",
            "itil", "cobit", "management system", "isms", "bcms", "qms",
            "certification", "audit", "non-conformity", "corrective action",
            "internal audit", "management review", "continual improvement",
            "document control", "records management", "competence",
            "نظام الإدارة", "الأيزو", "الاعتماد", "التدقيق الداخلي"
        ],
        "weak": [
            "standard", "framework", "compliance", "process", "procedure"
        ],
        "exclude": [
            "only cybersecurity", "only data privacy"
        ]
    }
}


def validate_document_for_domain(text: str, domain: str) -> Tuple[bool, float, str]:
    """
    Validate if a document is relevant to the specified domain.
    
    Args:
        text: Document text content
        domain: Target domain to validate against
        
    Returns:
        Tuple of (is_valid, confidence_score, message)
    """
    if not text or len(text) < 50:
        return False, 0.0, "Document is too short or empty"
    
    text_lower = text.lower()
    
    keywords = DOMAIN_KEYWORDS.get(domain, DOMAIN_KEYWORDS["Cyber Security"])
    
    # Count strong keyword matches
    strong_matches = sum(1 for kw in keywords["strong"] if kw.lower() in text_lower)
    
    # Count weak keyword matches
    weak_matches = sum(1 for kw in keywords["weak"] if kw.lower() in text_lower)
    
    # Check for exclusion keywords (wrong domain indicators)
    exclusion_matches = sum(1 for kw in keywords["exclude"] if kw.lower() in text_lower)
    
    # Calculate relevance score
    # Strong matches worth 3 points, weak worth 1 point, exclusions subtract 5 points
    score = (strong_matches * 3) + (weak_matches * 1) - (exclusion_matches * 5)
    
    # Normalize to 0-100
    max_possible = len(keywords["strong"]) * 3 + len(keywords["weak"])
    confidence = min(max(score / max_possible * 100, 0), 100) if max_possible > 0 else 0
    
    # Determine validity
    # Need at least 2 strong matches OR 5+ weak matches with no exclusions
    if strong_matches >= 2:
        is_valid = True
        message = f"Document appears relevant to {domain} ({strong_matches} strong indicators found)"
    elif strong_matches >= 1 and weak_matches >= 3 and exclusion_matches == 0:
        is_valid = True
        message = f"Document may be relevant to {domain} (moderate confidence)"
    elif weak_matches >= 5 and exclusion_matches == 0:
        is_valid = True
        message = f"Document has some relevance to {domain} (low confidence - please verify)"
    else:
        is_valid = False
        if exclusion_matches > 0:
            message = f"Document appears to be for a different domain, not {domain}"
        else:
            message = f"Document does not appear to be related to {domain}. Found {strong_matches} relevant indicators."
    
    return is_valid, confidence, message


def get_suggested_domain(text: str) -> Tuple[str, float]:
    """
    Suggest the most likely domain for a document.
    
    Returns:
        Tuple of (suggested_domain, confidence)
    """
    if not text:
        return "Cyber Security", 0.0
    
    text_lower = text.lower()
    scores = {}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        strong = sum(1 for kw in keywords["strong"] if kw.lower() in text_lower)
        weak = sum(1 for kw in keywords["weak"] if kw.lower() in text_lower)
        exclude = sum(1 for kw in keywords["exclude"] if kw.lower() in text_lower)
        
        scores[domain] = (strong * 3) + weak - (exclude * 5)
    
    # Get domain with highest score
    best_domain = max(scores, key=scores.get)
    best_score = scores[best_domain]
    
    # Calculate confidence
    total_score = sum(max(s, 0) for s in scores.values())
    confidence = (best_score / total_score * 100) if total_score > 0 else 0
    
    return best_domain, confidence
