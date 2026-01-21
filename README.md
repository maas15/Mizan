# 🛡️ Mizan

**Enterprise Governance, Risk & Compliance Operating System**

Version 2.0.0 (Refactored)

Created by: **Eng. Mohammad Abbas Alsaadon**

---

## 📋 Overview

Mizan GRC is an AI-powered platform for managing enterprise governance, risk, and compliance across multiple domains:

- **Cyber Security** - NCA, SAMA, NIST frameworks
- **Data Management** - NDMO, GDPR, DGA standards
- **Artificial Intelligence** - NIST AI RMF, EU AI Act, SDAIA Ethics
- **Digital Transformation** - DGA, COBIT, TOGAF
- **Global Standards** - ISO 27001, ISO 22301, ITIL

## ✨ Features

- 🎯 **Strategy Pipeline** - AI-generated strategic roadmaps
- 📝 **Policy Lab** - Automated policy document drafting
- 🔍 **Audit Module** - Evidence-based compliance auditing
- ⚠️ **Risk Radar** - Domain-specific risk analysis
- 📊 **Roadmap Visualization** - Gantt charts and Excel exports
- 🌐 **Bilingual Support** - English and Arabic interfaces

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone or download the project
cd Mizan

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings (especially OPENAI_API_KEY)

# Run the application
streamlit run app.py
```

### Default Credentials

- **Username:** admin
- **Password:** admin123 (⚠️ Change this in production!)

## 📁 Project Structure

```
Mizan/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── components/
│   ├── __init__.py
│   └── ui_components.py   # Reusable UI components
├── services/
│   ├── __init__.py
│   ├── db_service.py      # Database operations
│   └── ai_service.py      # AI/OpenAI integration
├── utils/
│   ├── __init__.py
│   ├── security.py        # Password hashing, rate limiting
│   ├── text_processing.py # PDF extraction, text utilities
│   └── validation.py      # Input validation
├── data/
│   ├── __init__.py
│   ├── frameworks.py      # Framework packs and obligations
│   ├── risk_data.py       # Risk knowledge bases
│   └── translations.py    # UI translations
└── styles/
    └── main.css           # Custom styles (optional)
```

## 🔐 Security Features

### Version 2.0 Security Improvements

1. **Secure Password Hashing**
   - PBKDF2-HMAC-SHA256 with 100,000 iterations
   - Random salts per password
   - Backward compatible with legacy SHA256 hashes

2. **Rate Limiting**
   - 5 failed attempts = 15-minute lockout
   - Per-user tracking

3. **Input Sanitization**
   - XSS prevention
   - SQL injection protection (parameterized queries)
   - Input length limits

4. **Session Management**
   - Namespaced session state
   - Secure session tokens

5. **Audit Logging**
   - Login/logout tracking
   - User actions logged
   - Admin activity monitoring

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | None (simulation mode) |
| `Mizan_ADMIN_PASSWORD` | Admin account password | admin123 |

### Application Config (config.py)

- `MIN_PASSWORD_LENGTH`: Minimum password length (default: 8)
- `MAX_LOGIN_ATTEMPTS`: Failed attempts before lockout (default: 5)
- `LOCKOUT_DURATION_MINUTES`: Lockout duration (default: 15)
- `AI_MODEL`: OpenAI model to use (default: gpt-4-turbo)

## 📊 Supported Frameworks

### Cyber Security
- NCA ECC (Essential Cybersecurity Controls)
- NCA CCC (Cloud Cybersecurity Controls)
- NCA DCC (Data Cybersecurity Controls)
- NCA OTCC (OT Cybersecurity Controls)
- NCA TCC (Telework Controls)
- SAMA CSF
- And more...

### Data Management
- NDMO/SDAIA
- GDPR
- DGA Data Standards

### AI Governance
- NIST AI RMF 1.0
- EU AI Act
- SDAIA AI Ethics

### Global Standards
- NIST CSF 2.0
- ISO 27001:2022
- ISO 22301
- ISO 9001
- ITIL 4

## 🛠️ Development

### Adding New Frameworks

Edit `data/frameworks.py` and add to `LOCAL_FRAMEWORK_PACKS`:

```python
"New Framework": {
    "framework_id": "NEW_FW_ID",
    "version": "1.0",
    "authority": "Authority Name",
    "domain": "cyber",  # or "data", "ai", "dt", "global"
    "obligations": [
        {
            "id": "NF-01",
            "text": "Obligation description",
            "tags": ["governance", "risk"],
            "evidence": ["Policy document", "Risk register"]
        }
    ],
    "mapping_hints": {
        "Unified.GOV": ["governance", "risk"]
    }
}
```

### Adding Risk Categories

Edit `data/risk_data.py`:

```python
NEW_RISK_DATA = {
    "Category Name": {
        "risks": ["Risk 1", "Risk 2"],
        "mitigations": "Mitigation strategies..."
    }
}
```

## 📝 License

Proprietary - All rights reserved.

## 🤝 Support

For support, contact the development team.

---

**Disclaimer:** This application provides AI-assisted recommendations. All outputs should be reviewed by qualified professionals before implementation. Do not use sensitive/PII data during testing.
