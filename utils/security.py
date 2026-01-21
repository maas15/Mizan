"""
Sentinel GRC - Security Utilities
Secure password hashing, validation, and authentication helpers.
"""

import hashlib
import hmac
import secrets
import re
import logging
from typing import Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


# =============================================================================
# PASSWORD HASHING (Using PBKDF2 - no external dependencies)
# =============================================================================

class PasswordHasher:
    """
    Secure password hashing using PBKDF2-HMAC-SHA256.
    
    This is a secure alternative that doesn't require bcrypt installation.
    Uses 100,000 iterations as recommended by OWASP.
    """
    
    ALGORITHM = 'sha256'
    ITERATIONS = 100_000
    SALT_LENGTH = 32
    HASH_LENGTH = 32
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Hash a password with a random salt using PBKDF2.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Format "salt$hash" (both hex encoded)
        """
        salt = secrets.token_bytes(cls.SALT_LENGTH)
        hash_bytes = hashlib.pbkdf2_hmac(
            cls.ALGORITHM,
            password.encode('utf-8'),
            salt,
            cls.ITERATIONS,
            dklen=cls.HASH_LENGTH
        )
        return f"{salt.hex()}${hash_bytes.hex()}"
    
    @classmethod
    def verify_password(cls, password: str, stored_hash: str) -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password: Plain text password to verify
            stored_hash: Previously stored hash in "salt$hash" format
            
        Returns:
            bool: True if password matches
        """
        try:
            # Handle legacy SHA256 hashes (64 char hex, no salt)
            if '$' not in stored_hash and len(stored_hash) == 64:
                return cls._verify_legacy_hash(password, stored_hash)
            
            salt_hex, hash_hex = stored_hash.split('$')
            salt = bytes.fromhex(salt_hex)
            stored_hash_bytes = bytes.fromhex(hash_hex)
            
            computed_hash = hashlib.pbkdf2_hmac(
                cls.ALGORITHM,
                password.encode('utf-8'),
                salt,
                cls.ITERATIONS,
                dklen=cls.HASH_LENGTH
            )
            
            # Use constant-time comparison to prevent timing attacks
            return hmac.compare_digest(computed_hash, stored_hash_bytes)
        
        except (ValueError, AttributeError) as e:
            logger.warning(f"Password verification error: {e}")
            return False
    
    @classmethod
    def _verify_legacy_hash(cls, password: str, legacy_hash: str) -> bool:
        """Verify against old SHA256 hash format for backward compatibility."""
        computed = hashlib.sha256(password.encode()).hexdigest()
        return hmac.compare_digest(computed, legacy_hash)
    
    @classmethod
    def needs_rehash(cls, stored_hash: str) -> bool:
        """Check if a hash needs to be upgraded to current format."""
        return '$' not in stored_hash


# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

@dataclass
class PasswordValidationResult:
    """Result of password validation."""
    is_valid: bool
    errors: list = field(default_factory=list)
    strength_score: int = 0  # 0-100


class PasswordValidator:
    """Validate password strength and requirements."""
    
    def __init__(
        self,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = False
    ):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
        self.special_chars = r"!@#$%^&*(),.?\":{}|<>"
    
    def validate(self, password: str) -> PasswordValidationResult:
        """
        Validate a password against all requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            PasswordValidationResult with validation status and errors
        """
        errors = []
        score = 0
        
        if not password:
            return PasswordValidationResult(False, ["Password is required"], 0)
        
        # Length check
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters")
        else:
            score += 25
        
        # Uppercase check
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        elif re.search(r'[A-Z]', password):
            score += 15
        
        # Lowercase check
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        elif re.search(r'[a-z]', password):
            score += 15
        
        # Digit check
        if self.require_digit and not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        elif re.search(r'\d', password):
            score += 20
        
        # Special character check
        if self.require_special and not re.search(f'[{re.escape(self.special_chars)}]', password):
            errors.append("Password must contain at least one special character")
        elif re.search(f'[{re.escape(self.special_chars)}]', password):
            score += 25
        
        # Bonus for length
        if len(password) >= 12:
            score = min(100, score + 10)
        if len(password) >= 16:
            score = min(100, score + 10)
        
        return PasswordValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            strength_score=score
        )


# =============================================================================
# RATE LIMITING
# =============================================================================

class RateLimiter:
    """
    Simple in-memory rate limiter for login attempts.
    
    In production, use Redis or database-backed rate limiting.
    """
    
    def __init__(self, max_attempts: int = 5, lockout_minutes: int = 15):
        self.max_attempts = max_attempts
        self.lockout_duration = timedelta(minutes=lockout_minutes)
        self._attempts: dict = defaultdict(list)
        self._lockouts: dict = {}
    
    def is_locked(self, identifier: str) -> Tuple[bool, Optional[int]]:
        """
        Check if an identifier is currently locked out.
        
        Args:
            identifier: Username or IP address
            
        Returns:
            Tuple of (is_locked, seconds_remaining)
        """
        if identifier in self._lockouts:
            lockout_end = self._lockouts[identifier]
            if datetime.now() < lockout_end:
                remaining = (lockout_end - datetime.now()).seconds
                return True, remaining
            else:
                # Lockout expired
                del self._lockouts[identifier]
                self._attempts[identifier] = []
        
        return False, None
    
    def record_attempt(self, identifier: str, success: bool) -> bool:
        """
        Record a login attempt.
        
        Args:
            identifier: Username or IP address
            success: Whether the attempt was successful
            
        Returns:
            bool: True if account is now locked
        """
        # Clean old attempts (older than lockout duration)
        cutoff = datetime.now() - self.lockout_duration
        self._attempts[identifier] = [
            t for t in self._attempts[identifier] if t > cutoff
        ]
        
        if success:
            # Clear attempts on successful login
            self._attempts[identifier] = []
            if identifier in self._lockouts:
                del self._lockouts[identifier]
            return False
        
        # Record failed attempt
        self._attempts[identifier].append(datetime.now())
        
        # Check if we should lock
        if len(self._attempts[identifier]) >= self.max_attempts:
            self._lockouts[identifier] = datetime.now() + self.lockout_duration
            logger.warning(f"Account locked due to too many failed attempts: {identifier}")
            return True
        
        return False
    
    def get_remaining_attempts(self, identifier: str) -> int:
        """Get the number of remaining attempts before lockout."""
        current_attempts = len(self._attempts.get(identifier, []))
        return max(0, self.max_attempts - current_attempts)


# =============================================================================
# INPUT SANITIZATION
# =============================================================================

class InputSanitizer:
    """Sanitize user inputs to prevent injection attacks."""
    
    @staticmethod
    def sanitize_text(
        text: str,
        max_length: int = 500,
        allow_newlines: bool = False,
        allow_html: bool = False
    ) -> str:
        """
        Sanitize text input.
        
        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            allow_newlines: Whether to preserve newlines
            allow_html: Whether to allow HTML tags (dangerous!)
            
        Returns:
            str: Sanitized text
        """
        if not text:
            return ""
        
        # Convert to string if necessary
        text = str(text)
        
        # Remove HTML tags unless explicitly allowed
        if not allow_html:
            text = re.sub(r'<[^>]*>', '', text)
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Handle newlines
        if not allow_newlines:
            text = text.replace('\n', ' ').replace('\r', '')
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Trim and limit length
        text = text.strip()[:max_length]
        
        return text
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename to prevent path traversal.
        
        Args:
            filename: Original filename
            
        Returns:
            str: Safe filename
        """
        if not filename:
            return "unnamed"
        
        # Remove path components
        filename = filename.replace('\\', '/').split('/')[-1]
        
        # Remove dangerous characters
        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', filename)
        
        # Limit length
        name, ext = (filename.rsplit('.', 1) + [''])[:2]
        name = name[:200]
        
        if ext:
            return f"{name}.{ext[:10]}"
        return name if name else "unnamed"
    
    @staticmethod
    def sanitize_username(username: str) -> str:
        """
        Sanitize a username.
        
        Args:
            username: Input username
            
        Returns:
            str: Sanitized username
        """
        if not username:
            return ""
        
        # Allow only alphanumeric, underscore, hyphen
        username = re.sub(r'[^a-zA-Z0-9_\-]', '', str(username))
        
        # Limit length
        return username[:50].lower()


# =============================================================================
# TOKEN GENERATION
# =============================================================================

class TokenGenerator:
    """Generate secure tokens for various purposes."""
    
    @staticmethod
    def generate_session_token(length: int = 32) -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_api_key(prefix: str = "sk") -> str:
        """Generate an API key with a prefix."""
        return f"{prefix}_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def generate_reset_token() -> Tuple[str, datetime]:
        """
        Generate a password reset token with expiry.
        
        Returns:
            Tuple of (token, expiry_datetime)
        """
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(hours=1)
        return token, expiry


# =============================================================================
# SINGLETON INSTANCES
# =============================================================================

password_hasher = PasswordHasher()
password_validator = PasswordValidator()
rate_limiter = RateLimiter()
input_sanitizer = InputSanitizer()
token_generator = TokenGenerator()
