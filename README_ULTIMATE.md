# Mizan GRC | ميزان
## Enterprise Governance, Risk & Compliance Operating System

<div align="center">

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)
![License](https://img.shields.io/badge/license-MIT-orange)

**Big4-Quality GRC Platform for the Saudi Arabian Market**

[English](#features) | [العربية](#الميزات)

</div>

---

## Overview

Mizan (ميزان - Arabic for "Balance/Scale") is an enterprise-grade GRC operating system that delivers **McKinsey/Deloitte/PwC/EY/KPMG-level** strategic planning, policy drafting, audit assessment, and risk management capabilities.

Built specifically for the **Saudi Arabian market** with full bilingual Arabic-English support and compliance with local regulatory frameworks including NCA ECC, SAMA CSF, NDMO, and SDAIA guidelines.

---

## Features

### 🎯 Strategy Planning
- Big4-level strategic roadmaps with executive-grade deliverables
- Industry benchmarking with documented data sources
- CMMI-based maturity assessment (5-level model)
- Sector-specific analysis (Banking, Government, Healthcare, Energy, Telecom, Retail, Manufacturing)
- Cost estimates based on organization size

### 📋 Policy Drafting
- Regulatory-compliant policy documents
- Formal Arabic (فصحى) for Saudi government standards
- 9-section structured output
- Framework-aligned content

### 🔍 Audit Assessment
- Evidence-based compliance evaluation
- Gap analysis matrix
- Risk-prioritized recommendations
- Multi-framework support

### ⚠️ Risk Assessment
- Domain-specific risk radars
- Threat actor mapping
- Mitigation strategies (Immediate/Short-term/Long-term)
- Key Risk Indicators (KRIs)

### 📊 Supported Domains

| Domain | Description | Key Frameworks |
|--------|-------------|----------------|
| Cyber Security | الأمن السيبراني | NCA ECC, ISO 27001, NIST CSF |
| AI Governance | حوكمة الذكاء الاصطناعي | SDAIA AI Ethics, EU AI Act |
| Data Management | إدارة البيانات | NDMO, PDPL, GDPR |
| Digital Transformation | التحول الرقمي | TOGAF, COBIT, ISO 56000 |
| Global Standards | المعايير العالمية | ISO 9001, ISO 22301, ITIL |

---

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Quick Start

```bash
# Clone or download the project
cd mizan-grc

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your OpenAI API key

# Run the application
streamlit run app_ultimate.py
```

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Project Structure

```
mizan-grc/
├── app_ultimate.py              # Main application (consolidated)
├── config.py                    # Configuration
├── requirements.txt             # Dependencies
├── MIZAN_ULTIMATE_CONSOLIDATION.md  # Consolidation documentation
│
├── services/
│   ├── ai_service_v2.py         # Big4-level AI service
│   └── db_service.py            # Thread-safe database
│
├── data/
│   ├── benchmarks.py            # Industry benchmarks with sources
│   ├── frameworks.py            # Framework packs
│   ├── risk_data_v2.py          # Domain-specific risks
│   └── translations_v2.py       # Bilingual translations
│
├── utils/
│   ├── security.py              # Authentication & security
│   ├── text_processing.py       # PDF & text utilities
│   ├── validation.py            # Input validation
│   └── export_utils.py          # Export utilities
│
└── components/
    └── ui_components.py         # Streamlit UI components
```

---

## Benchmark Data Sources

All benchmark data is sourced from reputable industry reports:

- **Cybersecurity**: Gartner, SANS Institute, IBM/Ponemon, NCA, ISACA
- **Data Management**: DAMA-DMBOK, SDAIA, Gartner
- **AI Governance**: Stanford HAI, MIT Sloan, Deloitte
- **Digital Transformation**: McKinsey, IDC, Deloitte
- **Global Standards**: ISO Survey, AXELOS, BSI Group

---

## الميزات

### 🎯 التخطيط الاستراتيجي
- خرائط طريق استراتيجية بمستوى شركات الاستشارات الكبرى
- قياس الأداء مقارنة بالصناعة مع مصادر موثقة
- تقييم النضج القائم على نموذج CMMI (5 مستويات)
- تحليل خاص بالقطاع

### 📋 صياغة السياسات
- وثائق سياسات متوافقة مع المتطلبات التنظيمية
- اللغة العربية الفصحى لمعايير الجهات الحكومية السعودية
- هيكل من 9 أقسام

### 🔍 تقييم التدقيق
- تقييم الامتثال القائم على الأدلة
- مصفوفة تحليل الفجوات
- توصيات مرتبة حسب المخاطر

### ⚠️ تقييم المخاطر
- رادارات مخاطر خاصة بكل مجال
- تعيين الجهات الفاعلة التهديدية
- استراتيجيات التخفيف

---

## Author

**Eng. Mohammad Abbas Alsaadon**

---

## License

MIT License - See LICENSE file for details.

---

## Changelog

### Version 3.0.0 Ultimate (January 2026)
- Consolidated all versions (v1.0 - v2.4)
- Added dynamic benchmarks with documented sources
- Implemented confidence scoring on all outputs
- Enhanced Arabic output validation
- Full domain-specific risk contexts
- CMMI maturity model integration

### Version 2.x (January 2026)
- Big4 enhancements
- Arabic translation system
- Technology dropdowns
- Domain-specific risks

### Version 1.0 (January 2026)
- Initial release
- Basic GRC functionality
- Security fixes
