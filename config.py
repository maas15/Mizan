"""
Sentinel GRC - Configuration Module
All constants, settings, and configuration values.
"""

import os
import secrets
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path

# =============================================================================
# LOAD ENVIRONMENT VARIABLES FROM .env FILE
# =============================================================================

# Try to load .env file from the same directory as this config file
_config_dir = Path(__file__).parent
_env_file = _config_dir / ".env"

try:
    from dotenv import load_dotenv
    
    # Load from .env file if it exists
    if _env_file.exists():
        load_dotenv(_env_file)
        print(f"✅ Loaded environment from: {_env_file}")
    else:
        # Also try current working directory
        load_dotenv()
except ImportError:
    print("⚠️ python-dotenv not installed. Using system environment variables only.")
    print("   Install with: pip install python-dotenv")


@dataclass
class AppConfig:
    """Application-wide configuration settings."""
    
    # Application Info
    APP_NAME: str = "Mizan"
    APP_TITLE: str = "Mizan | Enterprise GRC Platform"
    APP_ICON: str = "⚖️"
    APP_VERSION: str = "3.0.0"
    APP_TAGLINE: str = "Governance • Risk • Compliance"
    LOGO_FILE: str = "logo.png"
    
    # Creator Info
    CREATOR_NAME: str = "Eng. Mohammad Abbas Alsaadon"
    CREATOR_TITLE: str = "GRC Solutions Architect"
    COPYRIGHT_YEAR: str = "2025"
    
    # Database
    DB_FILE: str = "sentinel.db"
    DB_TIMEOUT: int = 30
    
    # Security
    MIN_PASSWORD_LENGTH: int = 8
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    SESSION_TIMEOUT_SECONDS: int = 3600
    
    # AI Settings
    AI_MODEL: str = "gpt-4-turbo"
    AI_FALLBACK_DELAY: float = 1.5
    MAX_PROMPT_LENGTH: int = 10000
    MAX_CONTEXT_LENGTH: int = 3000
    
    # UI Settings
    DEFAULT_COMPLIANCE_SCORE: int = 85
    ROADMAP_COLUMNS: int = 6
    MAX_INPUT_LENGTH: int = 500
    MAX_TEXT_AREA_LENGTH: int = 2000
    
    # File Settings
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_UPLOAD_TYPES: List[str] = field(default_factory=lambda: ["pdf"])
    
    # Timeouts
    RERUN_DELAY: float = 1.0
    SPINNER_MIN_DURATION: float = 0.5


@dataclass
class SecurityConfig:
    """Security-specific configuration."""
    
    ADMIN_USERNAME: str = "admin"
    
    @staticmethod
    def get_admin_password() -> str:
        """
        Get admin password from environment or generate secure one.
        
        Returns:
            str: The admin password
        """
        admin_pass = os.getenv("SENTINEL_ADMIN_PASSWORD")
        if not admin_pass:
            # For development only - in production, always use env var
            admin_pass = "admin123"  # Default for backward compatibility
            import logging
            logging.warning(
                "⚠️ Using default admin password. "
                "Set SENTINEL_ADMIN_PASSWORD environment variable for production."
            )
        return admin_pass
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """Generate a cryptographically secure password."""
        return secrets.token_urlsafe(length)
    
    # Password requirements
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGIT: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = False


class DomainConfig:
    """Domain-specific configuration and mappings."""
    
    # Logic mapping for domain names (English and Arabic)
    LOGIC_MAP: Dict[str, str] = {
        "Cyber Security": "cyber",
        "Data Management": "data",
        "Artificial Intelligence": "ai",
        "Digital Transformation": "dt",
        "Global Standards": "global",
        "الأمن السيبراني": "cyber",
        "إدارة البيانات": "data",
        "الذكاء الاصطناعي": "ai",
        "التحول الرقمي": "dt",
        "المعايير العالمية": "global",
    }
    
    # Framework registry - available frameworks per domain
    FRAMEWORK_REGISTRY: Dict[str, List[str]] = {
        "cyber": [
            "NCA ECC (Essential Cybersecurity Controls)",
            "NCA CCC (Cloud Cybersecurity Controls)",
            "NCA DCC (Data Cybersecurity Controls)",
            "NCA OTCC (Operational Technology Cybersecurity Controls)",
            "NCA TCC (Telework Cybersecurity Controls)",
            "NCA OSMACC (Social Media Accounts Cybersecurity Controls)",
            "NCA CSCC (Critical Systems Cybersecurity Controls)",
            "NCA NCS (National Cryptographic Standards)",
            "NCA CGIoT (Cybersecurity Guidelines for IoT)",
            "SAMA CSF",
        ],
        "data": ["NDMO/SDAIA", "GDPR", "DGA Data Standards"],
        "ai": ["NIST AI RMF", "EU AI Act", "SDAIA AI Ethics"],
        "dt": ["DGA Digital Gov Policy", "COBIT 2019", "TOGAF"],
        "global": ["NIST CSF 2.0", "ISO 27001:2022", "ISO 22301", "ISO 9001", "ITIL 4"],
    }
    
    @classmethod
    def get_domain_code(cls, domain_name: str) -> str:
        """Get the logic code for a domain name."""
        return cls.LOGIC_MAP.get(domain_name, "global")
    
    @classmethod
    def get_domain_regulations(cls, domain_name: str) -> List[str]:
        """Get available regulations/frameworks for a domain."""
        logic_code = cls.get_domain_code(domain_name)
        return cls.FRAMEWORK_REGISTRY.get(logic_code, cls.FRAMEWORK_REGISTRY["global"])


class PathConfig:
    """File and directory path configuration."""
    
    BASE_DIR: Path = Path(__file__).parent
    STYLES_DIR: Path = BASE_DIR / "styles"
    DATA_DIR: Path = BASE_DIR / "data"
    
    @classmethod
    def get_css_path(cls) -> Path:
        return cls.STYLES_DIR / "main.css"
    
    @classmethod
    def get_env_path(cls) -> Path:
        return cls.BASE_DIR / ".env"


# Singleton instances
config = AppConfig()
security_config = SecurityConfig()
domain_config = DomainConfig()
path_config = PathConfig()
