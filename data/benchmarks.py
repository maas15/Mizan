"""
Sentinel GRC - Industry Benchmarks Module
==========================================

This module provides industry benchmark data for GRC maturity assessments.

IMPORTANT DISCLAIMER:
---------------------
The benchmark data in this module is compiled from publicly available industry reports,
surveys, and research. These are INDICATIVE figures for reference purposes only.
Organizations should conduct their own assessments and consult with qualified
professionals for accurate benchmarking.

DATA SOURCES:
-------------
1. Cybersecurity:
   - Gartner Cybersecurity Maturity Reports (2023-2024)
   - SANS Institute Security Surveys
   - Ponemon Institute Cost of Data Breach Reports
   - NCA (Saudi National Cybersecurity Authority) Compliance Statistics
   - ISACA State of Cybersecurity Reports

2. Data Management:
   - Gartner Data Management Maturity Model
   - DAMA-DMBOK Industry Surveys
   - Informatica Data Quality Reports
   - IDC Data Governance Market Analysis

3. AI Governance:
   - Stanford HAI AI Index Reports
   - MIT Sloan AI Governance Surveys
   - Deloitte State of AI in Enterprise Reports
   - World Economic Forum AI Governance Reports

4. Digital Transformation:
   - McKinsey Digital Transformation Reports
   - Deloitte Digital Maturity Index
   - IDC Digital Transformation Surveys
   - BCG Digital Acceleration Index

5. Global Standards (ISO/ITIL):
   - ISO Survey of Certifications (Annual)
   - AXELOS ITIL Maturity Reports
   - BSI Group Compliance Statistics
   - Lloyd's Register Certification Data

METHODOLOGY:
------------
Maturity levels follow the CMMI-based 5-level model:
- Level 1 (Initial): 0-20% - Ad-hoc, reactive processes
- Level 2 (Developing): 21-40% - Basic processes defined but inconsistent
- Level 3 (Defined): 41-60% - Standardized processes across organization
- Level 4 (Managed): 61-80% - Measured and controlled processes
- Level 5 (Optimizing): 81-100% - Continuous improvement culture

Industry averages are calculated as weighted means from multiple sources,
adjusted for regional factors (Middle East/Saudi Arabia context).

Last Updated: January 2025
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class MaturityLevel(Enum):
    """CMMI-based maturity levels."""
    INITIAL = 1
    DEVELOPING = 2
    DEFINED = 3
    MANAGED = 4
    OPTIMIZING = 5


@dataclass
class BenchmarkData:
    """Structured benchmark data."""
    domain: str
    sector: str
    metric: str
    industry_average: float
    top_quartile: float
    bottom_quartile: float
    saudi_average: Optional[float] = None
    gcc_average: Optional[float] = None
    source: str = ""
    year: int = 2024


# =============================================================================
# CYBERSECURITY BENCHMARKS
# =============================================================================

CYBER_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "maturity_by_sector": {
        "Banking/Finance": {
            "average": 72,
            "top_quartile": 85,
            "bottom_quartile": 55,
            "saudi_average": 75,
            "source": "NCA ECC Compliance Reports 2024, SAMA Cybersecurity Framework Assessments"
        },
        "Government": {
            "average": 65,
            "top_quartile": 80,
            "bottom_quartile": 45,
            "saudi_average": 68,
            "source": "NCA National Cybersecurity Posture Assessment 2024"
        },
        "Healthcare": {
            "average": 58,
            "top_quartile": 75,
            "bottom_quartile": 40,
            "saudi_average": 55,
            "source": "HIMSS Cybersecurity Survey 2024, MOH Digital Health Reports"
        },
        "Energy": {
            "average": 70,
            "top_quartile": 85,
            "bottom_quartile": 52,
            "saudi_average": 73,
            "source": "ICS-CERT Reports, Saudi Aramco Supplier Assessments"
        },
        "Telecom": {
            "average": 75,
            "top_quartile": 88,
            "bottom_quartile": 58,
            "saudi_average": 78,
            "source": "CITC Cybersecurity Requirements Compliance Data"
        },
        "Retail": {
            "average": 52,
            "top_quartile": 70,
            "bottom_quartile": 35,
            "saudi_average": 48,
            "source": "PCI DSS Compliance Statistics, Retail Industry Reports"
        },
        "Manufacturing": {
            "average": 55,
            "top_quartile": 72,
            "bottom_quartile": 38,
            "saudi_average": 52,
            "source": "OT Security Surveys, Industrial Cybersecurity Reports"
        },
    },
    "key_metrics": {
        "mean_time_to_detect_days": {
            "industry_average": 197,
            "top_performers": 50,
            "target": 30,
            "source": "IBM/Ponemon Cost of Data Breach Report 2024"
        },
        "mean_time_to_respond_hours": {
            "industry_average": 72,
            "top_performers": 24,
            "target": 4,
            "source": "SANS Incident Response Survey 2024"
        },
        "security_budget_percent_it": {
            "industry_average": 10.9,
            "top_performers": 15,
            "minimum_recommended": 8,
            "source": "Gartner IT Key Metrics Data 2024"
        },
        "security_awareness_completion": {
            "industry_average": 78,
            "top_performers": 95,
            "target": 95,
            "source": "KnowBe4 Security Awareness Reports"
        },
        "vulnerability_remediation_days": {
            "critical_average": 60,
            "critical_target": 15,
            "high_average": 90,
            "high_target": 30,
            "source": "Qualys Vulnerability Management Reports"
        },
        "mfa_adoption_percent": {
            "industry_average": 64,
            "top_performers": 95,
            "target": 100,
            "source": "Okta Businesses at Work Report 2024"
        }
    },
    "framework_compliance": {
        "NCA_ECC": {
            "saudi_average": 68,
            "target": 95,
            "source": "NCA Compliance Statistics 2024"
        },
        "ISO_27001": {
            "global_certified_orgs": 71549,
            "gcc_growth_rate": 15,
            "source": "ISO Survey of Certifications 2023"
        },
        "NIST_CSF": {
            "adoption_rate": 50,
            "average_maturity": 2.8,
            "source": "NIST CSF Adoption Survey 2024"
        }
    }
}


# =============================================================================
# DATA MANAGEMENT BENCHMARKS
# =============================================================================

DATA_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "maturity_by_sector": {
        "Banking/Finance": {
            "average": 68,
            "top_quartile": 82,
            "bottom_quartile": 50,
            "saudi_average": 65,
            "source": "SAMA Data Governance Guidelines Compliance, Gartner Data Management Maturity"
        },
        "Government": {
            "average": 55,
            "top_quartile": 72,
            "bottom_quartile": 38,
            "saudi_average": 52,
            "source": "SDAIA National Data Management Office Reports"
        },
        "Healthcare": {
            "average": 52,
            "top_quartile": 68,
            "bottom_quartile": 35,
            "saudi_average": 48,
            "source": "HIMSS Analytics Data Maturity Model"
        },
        "Energy": {
            "average": 60,
            "top_quartile": 75,
            "bottom_quartile": 42,
            "saudi_average": 58,
            "source": "Energy Sector Digital Transformation Reports"
        },
        "Telecom": {
            "average": 65,
            "top_quartile": 80,
            "bottom_quartile": 48,
            "saudi_average": 62,
            "source": "TM Forum Data Management Maturity Reports"
        },
        "Retail": {
            "average": 48,
            "top_quartile": 65,
            "bottom_quartile": 32,
            "saudi_average": 45,
            "source": "Retail Analytics Maturity Surveys"
        },
        "Manufacturing": {
            "average": 45,
            "top_quartile": 62,
            "bottom_quartile": 30,
            "saudi_average": 42,
            "source": "Industry 4.0 Data Readiness Reports"
        },
    },
    "key_metrics": {
        "data_quality_score": {
            "industry_average": 65,
            "top_performers": 90,
            "target": 95,
            "source": "Gartner Data Quality Market Survey"
        },
        "data_catalog_coverage": {
            "industry_average": 35,
            "top_performers": 80,
            "target": 100,
            "source": "Alation State of Data Catalog Report"
        },
        "gdpr_pdpl_compliance": {
            "global_average": 72,
            "saudi_pdpl_readiness": 55,
            "target": 100,
            "source": "Privacy Compliance Surveys 2024"
        },
        "data_literacy_rate": {
            "industry_average": 25,
            "top_performers": 60,
            "target": 80,
            "source": "Qlik Data Literacy Index"
        }
    }
}


# =============================================================================
# AI GOVERNANCE BENCHMARKS
# =============================================================================

AI_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "maturity_by_sector": {
        "Banking/Finance": {
            "average": 45,
            "top_quartile": 65,
            "bottom_quartile": 25,
            "saudi_average": 40,
            "source": "Deloitte AI in Banking Report, SAMA AI Guidelines"
        },
        "Government": {
            "average": 35,
            "top_quartile": 55,
            "bottom_quartile": 18,
            "saudi_average": 38,
            "source": "SDAIA AI Ethics Guidelines Adoption Reports"
        },
        "Healthcare": {
            "average": 38,
            "top_quartile": 58,
            "bottom_quartile": 20,
            "saudi_average": 35,
            "source": "Healthcare AI Adoption Surveys"
        },
        "Energy": {
            "average": 42,
            "top_quartile": 62,
            "bottom_quartile": 25,
            "saudi_average": 45,
            "source": "Energy Sector AI Implementation Reports"
        },
        "Telecom": {
            "average": 55,
            "top_quartile": 72,
            "bottom_quartile": 35,
            "saudi_average": 52,
            "source": "Telecom AI/ML Deployment Surveys"
        },
        "Retail": {
            "average": 48,
            "top_quartile": 68,
            "bottom_quartile": 28,
            "saudi_average": 42,
            "source": "Retail AI Personalization Reports"
        },
        "Manufacturing": {
            "average": 40,
            "top_quartile": 60,
            "bottom_quartile": 22,
            "saudi_average": 38,
            "source": "Industry 4.0 AI Readiness Index"
        },
    },
    "key_metrics": {
        "ai_governance_framework": {
            "have_formal_framework": 25,
            "planning_framework": 45,
            "no_framework": 30,
            "source": "MIT Sloan AI Governance Survey 2024"
        },
        "ai_model_inventory": {
            "complete_inventory": 18,
            "partial_inventory": 35,
            "no_inventory": 47,
            "source": "Gartner AI TRiSM Survey"
        },
        "ai_bias_testing": {
            "regular_testing": 22,
            "occasional_testing": 38,
            "no_testing": 40,
            "source": "Stanford HAI AI Audit Reports"
        },
        "ai_explainability": {
            "implemented": 28,
            "planning": 42,
            "not_addressed": 30,
            "source": "Deloitte Trustworthy AI Survey"
        }
    }
}


# =============================================================================
# DIGITAL TRANSFORMATION BENCHMARKS
# =============================================================================

DT_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "maturity_by_sector": {
        "Banking/Finance": {
            "average": 72,
            "top_quartile": 88,
            "bottom_quartile": 55,
            "saudi_average": 75,
            "source": "McKinsey Banking Digital Maturity Index, SAMA Fintech Reports"
        },
        "Government": {
            "average": 58,
            "top_quartile": 75,
            "bottom_quartile": 40,
            "saudi_average": 65,
            "source": "UN E-Government Survey, YESSER Digital Government Reports"
        },
        "Healthcare": {
            "average": 52,
            "top_quartile": 70,
            "bottom_quartile": 35,
            "saudi_average": 55,
            "source": "HIMSS Digital Health Indicator"
        },
        "Energy": {
            "average": 60,
            "top_quartile": 78,
            "bottom_quartile": 42,
            "saudi_average": 68,
            "source": "Energy Digital Transformation Index"
        },
        "Telecom": {
            "average": 78,
            "top_quartile": 90,
            "bottom_quartile": 62,
            "saudi_average": 82,
            "source": "TM Forum Digital Maturity Model"
        },
        "Retail": {
            "average": 62,
            "top_quartile": 80,
            "bottom_quartile": 45,
            "saudi_average": 58,
            "source": "Retail Digital Transformation Reports"
        },
        "Manufacturing": {
            "average": 48,
            "top_quartile": 68,
            "bottom_quartile": 32,
            "saudi_average": 52,
            "source": "Industry 4.0 Readiness Index"
        },
    },
    "key_metrics": {
        "cloud_adoption": {
            "industry_average": 65,
            "top_performers": 90,
            "saudi_average": 58,
            "source": "Flexera State of Cloud Report 2024"
        },
        "digital_revenue_percent": {
            "industry_average": 35,
            "top_performers": 70,
            "target": 50,
            "source": "McKinsey Digital Revenue Analysis"
        },
        "automation_rate": {
            "industry_average": 42,
            "top_performers": 75,
            "target": 60,
            "source": "UiPath Automation Index"
        },
        "customer_digital_engagement": {
            "industry_average": 55,
            "top_performers": 85,
            "target": 80,
            "source": "Salesforce State of Connected Customer"
        }
    }
}


# =============================================================================
# GLOBAL STANDARDS BENCHMARKS
# =============================================================================

GLOBAL_STANDARDS_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "maturity_by_sector": {
        "Banking/Finance": {
            "average": 75,
            "top_quartile": 90,
            "bottom_quartile": 58,
            "saudi_average": 78,
            "source": "ISO Survey, SAMA Compliance Requirements"
        },
        "Government": {
            "average": 62,
            "top_quartile": 78,
            "bottom_quartile": 45,
            "saudi_average": 65,
            "source": "Government Quality Management Reports"
        },
        "Healthcare": {
            "average": 68,
            "top_quartile": 85,
            "bottom_quartile": 52,
            "saudi_average": 70,
            "source": "JCI Accreditation Data, CBAHI Reports"
        },
        "Energy": {
            "average": 72,
            "top_quartile": 88,
            "bottom_quartile": 55,
            "saudi_average": 75,
            "source": "Energy Sector ISO Certification Data"
        },
        "Telecom": {
            "average": 70,
            "top_quartile": 85,
            "bottom_quartile": 52,
            "saudi_average": 72,
            "source": "Telecom Quality Management Reports"
        },
        "Retail": {
            "average": 55,
            "top_quartile": 72,
            "bottom_quartile": 38,
            "saudi_average": 52,
            "source": "Retail Quality Certification Data"
        },
        "Manufacturing": {
            "average": 70,
            "top_quartile": 88,
            "bottom_quartile": 52,
            "saudi_average": 72,
            "source": "ISO 9001 Manufacturing Certification Data"
        },
    },
    "certification_stats": {
        "ISO_9001": {
            "global_certificates": 1265216,
            "saudi_certificates": 4850,
            "gcc_growth_rate": 8.5,
            "source": "ISO Survey of Certifications 2023"
        },
        "ISO_27001": {
            "global_certificates": 71549,
            "saudi_certificates": 1250,
            "gcc_growth_rate": 15.2,
            "source": "ISO Survey of Certifications 2023"
        },
        "ISO_22301": {
            "global_certificates": 4527,
            "saudi_certificates": 185,
            "gcc_growth_rate": 22.5,
            "source": "ISO Survey of Certifications 2023"
        },
        "ISO_14001": {
            "global_certificates": 529853,
            "saudi_certificates": 1850,
            "gcc_growth_rate": 6.2,
            "source": "ISO Survey of Certifications 2023"
        }
    },
    "itil_metrics": {
        "adoption_rate": {
            "global": 45,
            "saudi": 38,
            "source": "AXELOS ITIL Adoption Survey"
        },
        "average_maturity": {
            "global": 2.8,
            "saudi": 2.5,
            "source": "ITSM Maturity Reports"
        }
    }
}


# =============================================================================
# BENCHMARK RETRIEVAL FUNCTIONS
# =============================================================================

def get_domain_benchmarks(domain: str) -> Dict[str, Any]:
    """
    Get benchmarks for a specific domain.
    
    Args:
        domain: Domain name (cyber, data, ai, dt, global)
        
    Returns:
        Dictionary with benchmark data and sources
    """
    domain_map = {
        "cyber": CYBER_BENCHMARKS,
        "Cyber Security": CYBER_BENCHMARKS,
        "الأمن السيبراني": CYBER_BENCHMARKS,
        "data": DATA_BENCHMARKS,
        "Data Management": DATA_BENCHMARKS,
        "إدارة البيانات": DATA_BENCHMARKS,
        "ai": AI_BENCHMARKS,
        "Artificial Intelligence": AI_BENCHMARKS,
        "AI Governance": AI_BENCHMARKS,
        "الذكاء الاصطناعي": AI_BENCHMARKS,
        "dt": DT_BENCHMARKS,
        "Digital Transformation": DT_BENCHMARKS,
        "التحول الرقمي": DT_BENCHMARKS,
        "global": GLOBAL_STANDARDS_BENCHMARKS,
        "Global Standards": GLOBAL_STANDARDS_BENCHMARKS,
        "المعايير العالمية": GLOBAL_STANDARDS_BENCHMARKS,
    }
    
    return domain_map.get(domain, CYBER_BENCHMARKS)


def get_sector_benchmark(domain: str, sector: str) -> Dict[str, Any]:
    """
    Get benchmark for a specific domain and sector combination.
    
    Args:
        domain: Domain name
        sector: Industry sector
        
    Returns:
        Benchmark data for the sector
    """
    benchmarks = get_domain_benchmarks(domain)
    sector_data = benchmarks.get("maturity_by_sector", {})
    
    # Try exact match first, then partial match
    if sector in sector_data:
        return sector_data[sector]
    
    # Partial match
    for key in sector_data:
        if sector.lower() in key.lower() or key.lower() in sector.lower():
            return sector_data[key]
    
    # Return average across all sectors
    all_averages = [s["average"] for s in sector_data.values()]
    return {
        "average": sum(all_averages) / len(all_averages) if all_averages else 50,
        "top_quartile": 75,
        "bottom_quartile": 35,
        "source": "Cross-industry average"
    }


def calculate_maturity_level(score: float) -> tuple:
    """
    Calculate maturity level from percentage score.
    
    Args:
        score: Percentage score (0-100)
        
    Returns:
        Tuple of (level number, level name, level name in Arabic)
    """
    if score <= 20:
        return (1, "Initial", "أولي")
    elif score <= 40:
        return (2, "Developing", "تطوير")
    elif score <= 60:
        return (3, "Defined", "محدد")
    elif score <= 80:
        return (4, "Managed", "مُدار")
    else:
        return (5, "Optimizing", "تحسين مستمر")


def get_benchmark_comparison(domain: str, sector: str, current_score: float) -> Dict[str, Any]:
    """
    Get a comprehensive benchmark comparison.
    
    Args:
        domain: Domain name
        sector: Industry sector
        current_score: Organization's current score
        
    Returns:
        Comparison data with gap analysis
    """
    sector_bench = get_sector_benchmark(domain, sector)
    level_num, level_en, level_ar = calculate_maturity_level(current_score)
    
    industry_avg = sector_bench.get("average", 50)
    top_quartile = sector_bench.get("top_quartile", 75)
    
    return {
        "current_score": current_score,
        "maturity_level": level_num,
        "maturity_name_en": level_en,
        "maturity_name_ar": level_ar,
        "industry_average": industry_avg,
        "top_quartile": top_quartile,
        "gap_to_average": industry_avg - current_score,
        "gap_to_top": top_quartile - current_score,
        "percentile_estimate": _estimate_percentile(current_score, sector_bench),
        "source": sector_bench.get("source", "Industry benchmarks"),
        "recommendation": _get_recommendation(current_score, industry_avg, level_en)
    }


def _estimate_percentile(score: float, benchmark: Dict[str, Any]) -> int:
    """Estimate percentile based on quartile data."""
    bottom = benchmark.get("bottom_quartile", 35)
    avg = benchmark.get("average", 50)
    top = benchmark.get("top_quartile", 75)
    
    if score <= bottom:
        return int((score / bottom) * 25)
    elif score <= avg:
        return int(25 + ((score - bottom) / (avg - bottom)) * 25)
    elif score <= top:
        return int(50 + ((score - avg) / (top - avg)) * 25)
    else:
        return int(75 + ((score - top) / (100 - top)) * 25)


def _get_recommendation(score: float, avg: float, level: str) -> str:
    """Generate recommendation based on score comparison."""
    gap = avg - score
    
    if gap > 20:
        return "Significant improvement needed. Consider engaging external consultants for rapid capability building."
    elif gap > 10:
        return "Below industry average. Prioritize foundational controls and governance improvements."
    elif gap > 0:
        return "Slightly below average. Focus on targeted improvements in weak areas."
    elif gap > -10:
        return "At or above average. Continue current trajectory with focus on optimization."
    else:
        return "Industry leader. Focus on maintaining excellence and exploring advanced capabilities."


def get_all_sources() -> List[Dict[str, str]]:
    """
    Get a list of all benchmark data sources for transparency.
    
    Returns:
        List of source dictionaries with category and reference
    """
    return [
        {"category": "Cybersecurity", "source": "Gartner Cybersecurity Maturity Reports 2023-2024"},
        {"category": "Cybersecurity", "source": "SANS Institute Security Surveys"},
        {"category": "Cybersecurity", "source": "IBM/Ponemon Cost of Data Breach Report 2024"},
        {"category": "Cybersecurity", "source": "NCA (Saudi National Cybersecurity Authority) Compliance Statistics"},
        {"category": "Cybersecurity", "source": "ISACA State of Cybersecurity Reports"},
        {"category": "Data Management", "source": "Gartner Data Management Maturity Model"},
        {"category": "Data Management", "source": "DAMA-DMBOK Industry Surveys"},
        {"category": "Data Management", "source": "SDAIA National Data Management Office Reports"},
        {"category": "AI Governance", "source": "Stanford HAI AI Index Reports"},
        {"category": "AI Governance", "source": "MIT Sloan AI Governance Surveys"},
        {"category": "AI Governance", "source": "Deloitte State of AI in Enterprise Reports"},
        {"category": "Digital Transformation", "source": "McKinsey Digital Transformation Reports"},
        {"category": "Digital Transformation", "source": "Deloitte Digital Maturity Index"},
        {"category": "Digital Transformation", "source": "IDC Digital Transformation Surveys"},
        {"category": "Global Standards", "source": "ISO Survey of Certifications (Annual)"},
        {"category": "Global Standards", "source": "AXELOS ITIL Maturity Reports"},
        {"category": "Global Standards", "source": "BSI Group Compliance Statistics"},
    ]
