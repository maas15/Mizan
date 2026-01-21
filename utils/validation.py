"""
Sentinel GRC - Validation Utilities
Input validation, form validation, and data validation helpers.
"""

import re
import logging
from typing import Optional, List, Tuple, Any, Dict
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    sanitized_value: Any = None
    
    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)


class InputValidator:
    """Validate and sanitize user inputs."""
    
    @staticmethod
    def validate_text(
        value: str,
        field_name: str = "Field",
        required: bool = True,
        min_length: int = 0,
        max_length: int = 500,
        pattern: str = None,
        allow_html: bool = False
    ) -> ValidationResult:
        """Validate text input."""
        result = ValidationResult(is_valid=True)
        
        if value is None:
            value = ""
        
        value = str(value).strip()
        
        if required and not value:
            result.add_error(f"{field_name} is required")
            return result
        
        if not value and not required:
            result.sanitized_value = ""
            return result
        
        if len(value) < min_length:
            result.add_error(f"{field_name} must be at least {min_length} characters")
        
        if len(value) > max_length:
            result.add_warning(f"{field_name} was truncated to {max_length} characters")
            value = value[:max_length]
        
        if pattern and not re.match(pattern, value):
            result.add_error(f"{field_name} format is invalid")
        
        if not allow_html:
            value = re.sub(r'<[^>]*>', '', value)
        
        value = value.replace('\x00', '')
        
        result.sanitized_value = value
        return result
    
    @staticmethod
    def validate_email(value: str, required: bool = True) -> ValidationResult:
        """Validate email address."""
        result = ValidationResult(is_valid=True)
        
        if not value and not required:
            result.sanitized_value = ""
            return result
        
        if not value and required:
            result.add_error("Email is required")
            return result
        
        value = str(value).strip().lower()
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            result.add_error("Invalid email format")
            return result
        
        result.sanitized_value = value
        return result
    
    @staticmethod
    def validate_username(value: str) -> ValidationResult:
        """Validate username."""
        result = ValidationResult(is_valid=True)
        
        if not value:
            result.add_error("Username is required")
            return result
        
        value = str(value).strip().lower()
        
        if len(value) < 3:
            result.add_error("Username must be at least 3 characters")
        
        if len(value) > 50:
            result.add_error("Username must be less than 50 characters")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            result.add_error("Username can only contain letters, numbers, underscores, and hyphens")
        
        if value and not value[0].isalpha():
            result.add_error("Username must start with a letter")
        
        result.sanitized_value = value
        return result
    
    @staticmethod
    def validate_number(
        value: Any,
        field_name: str = "Value",
        required: bool = True,
        min_value: float = None,
        max_value: float = None,
        allow_decimal: bool = True
    ) -> ValidationResult:
        """Validate numeric input."""
        result = ValidationResult(is_valid=True)
        
        if value is None or value == "":
            if required:
                result.add_error(f"{field_name} is required")
            else:
                result.sanitized_value = None
            return result
        
        try:
            if allow_decimal:
                num = float(value)
            else:
                num = int(value)
        except (ValueError, TypeError):
            result.add_error(f"{field_name} must be a valid number")
            return result
        
        if min_value is not None and num < min_value:
            result.add_error(f"{field_name} must be at least {min_value}")
        
        if max_value is not None and num > max_value:
            result.add_error(f"{field_name} must be at most {max_value}")
        
        result.sanitized_value = num
        return result
    
    @staticmethod
    def validate_selection(
        value: Any,
        allowed_values: List[Any],
        field_name: str = "Selection",
        required: bool = True
    ) -> ValidationResult:
        """Validate selection from allowed values."""
        result = ValidationResult(is_valid=True)
        
        if value is None or value == "":
            if required:
                result.add_error(f"{field_name} is required")
            else:
                result.sanitized_value = None
            return result
        
        if value not in allowed_values:
            result.add_error(f"Invalid {field_name}")
            return result
        
        result.sanitized_value = value
        return result


class FormValidator:
    """Validate entire forms with multiple fields."""
    
    def __init__(self):
        self.results: Dict[str, ValidationResult] = {}
        self.is_valid = True
    
    def add_result(self, field_name: str, result: ValidationResult):
        """Add a field validation result."""
        self.results[field_name] = result
        if not result.is_valid:
            self.is_valid = False
    
    def validate_text(self, field_name: str, value: str, **kwargs) -> str:
        """Validate text field and return sanitized value."""
        result = InputValidator.validate_text(value, field_name, **kwargs)
        self.add_result(field_name, result)
        return result.sanitized_value
    
    def get_errors(self) -> Dict[str, List[str]]:
        """Get all errors by field."""
        return {
            field: result.errors
            for field, result in self.results.items()
            if result.errors
        }
    
    def get_all_errors(self) -> List[str]:
        """Get flat list of all errors."""
        errors = []
        for field, result in self.results.items():
            for error in result.errors:
                errors.append(f"{field}: {error}")
        return errors


class DataValidator:
    """Validate data structures and business rules."""
    
    @staticmethod
    def validate_risk_score(probability: int, impact: int) -> Tuple[int, str]:
        """Calculate and validate risk score."""
        probability = max(1, min(5, probability))
        impact = max(1, min(5, impact))
        
        score = probability * impact
        
        if score >= 15:
            level = "CRITICAL"
        elif score >= 10:
            level = "HIGH"
        elif score >= 5:
            level = "MEDIUM"
        else:
            level = "LOW"
        
        return score, level
    
    @staticmethod
    def validate_roadmap_data(data: List[List[str]]) -> ValidationResult:
        """Validate roadmap data structure."""
        result = ValidationResult(is_valid=True)
        
        if not data:
            result.add_error("Roadmap data is empty")
            return result
        
        required_columns = 6
        validated_rows = []
        
        for i, row in enumerate(data):
            if len(row) < required_columns:
                result.add_warning(f"Row {i+1} has fewer than {required_columns} columns")
                row = row + [""] * (required_columns - len(row))
            
            phase = str(row[0]).strip()
            initiative = str(row[1]).strip()
            
            if not phase:
                result.add_warning(f"Row {i+1} has empty phase")
            
            if not initiative:
                result.add_warning(f"Row {i+1} has empty initiative")
            
            try:
                duration = float(row[2]) if row[2] else 3.0
            except ValueError:
                duration = 3.0
            
            try:
                cost = float(re.sub(r'[^\d.]', '', str(row[3]))) if row[3] else 0.0
            except ValueError:
                cost = 0.0
            
            validated_rows.append([
                phase,
                initiative,
                duration,
                cost,
                str(row[4]).strip() if len(row) > 4 else "",
                str(row[5]).strip() if len(row) > 5 else ""
            ])
        
        result.sanitized_value = validated_rows
        return result
    
    @staticmethod
    def validate_framework_selection(
        selected: List[str],
        available: List[str],
        min_selection: int = 1,
        max_selection: int = 10
    ) -> ValidationResult:
        """Validate framework selection."""
        result = ValidationResult(is_valid=True)
        
        if not selected:
            if min_selection > 0:
                result.add_error(f"At least {min_selection} framework(s) must be selected")
            result.sanitized_value = []
            return result
        
        if len(selected) < min_selection:
            result.add_error(f"At least {min_selection} framework(s) must be selected")
        
        if len(selected) > max_selection:
            result.add_warning(f"Selection limited to first {max_selection} frameworks")
            selected = selected[:max_selection]
        
        valid_selections = [fw for fw in selected if fw in available]
        
        if not valid_selections and min_selection > 0:
            result.add_error("No valid frameworks selected")
        
        result.sanitized_value = valid_selections
        return result


class FileValidator:
    """Validate uploaded files."""
    
    @classmethod
    def validate_file(
        cls,
        file,
        allowed_types: List[str] = None,
        max_size_mb: float = 10
    ) -> ValidationResult:
        """Validate an uploaded file."""
        result = ValidationResult(is_valid=True)
        
        if file is None:
            result.add_error("No file uploaded")
            return result
        
        filename = getattr(file, 'name', '')
        if not filename:
            result.add_error("Invalid file")
            return result
        
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        
        if allowed_types and ext not in allowed_types:
            result.add_error(f"File type '.{ext}' not allowed")
            return result
        
        try:
            file.seek(0, 2)
            size_bytes = file.tell()
            file.seek(0)
            
            size_mb = size_bytes / (1024 * 1024)
            if size_mb > max_size_mb:
                result.add_error(f"File too large ({size_mb:.1f}MB). Maximum: {max_size_mb}MB")
                return result
        except Exception as e:
            logger.warning(f"Could not check file size: {e}")
        
        result.sanitized_value = file
        return result


# Convenience instances
input_validator = InputValidator()
data_validator = DataValidator()
file_validator = FileValidator()
