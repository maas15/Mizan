"""
Sentinel GRC - Text Processing Utilities
PDF extraction, text manipulation, and formatting helpers.
"""

import re
import logging
from typing import Optional, List, Tuple
from io import BytesIO

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract text content from PDF files."""
    
    @staticmethod
    def extract_text(file) -> Optional[str]:
        """
        Extract text from a PDF file.
        
        Args:
            file: File-like object or path to PDF
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        try:
            import pdfplumber
            
            text_parts = []
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text_parts.append(extracted)
            
            # Combine and clean
            text = "\n".join(text_parts)
            # Remove null bytes
            text = text.replace("\x00", "")
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)
            
            return text.strip() if text.strip() else None
            
        except ImportError:
            logger.error("pdfplumber not installed")
            return None
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return None
    
    @staticmethod
    def get_page_count(file) -> int:
        """Get the number of pages in a PDF."""
        try:
            import pdfplumber
            with pdfplumber.open(file) as pdf:
                return len(pdf.pages)
        except Exception:
            return 0


class TextProcessor:
    """General text processing utilities."""
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate text to maximum length with suffix.
        
        Args:
            text: Input text
            max_length: Maximum length (including suffix)
            suffix: Suffix to append when truncated
            
        Returns:
            str: Truncated text
        """
        if not text or len(text) <= max_length:
            return text or ""
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def clean_markdown(text: str) -> str:
        """
        Remove markdown formatting from text.
        
        Args:
            text: Text with markdown
            
        Returns:
            str: Plain text
        """
        if not text:
            return ""
        
        # Remove headers
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # Remove bold/italic
        text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
        text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
        # Remove links
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        # Remove code blocks
        text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        return text.strip()
    
    @staticmethod
    def extract_sections(text: str, delimiter: str = "|||") -> List[str]:
        """
        Split text into sections by delimiter.
        
        Args:
            text: Input text
            delimiter: Section delimiter
            
        Returns:
            list: List of section strings
        """
        if not text:
            return []
        
        parts = text.split(delimiter)
        return [p.strip() for p in parts if p.strip()]
    
    @staticmethod
    def clean_section_header(text: str) -> str:
        """
        Remove section headers from text content.
        
        Args:
            text: Section text that may include its header
            
        Returns:
            str: Text with header removed
        """
        if not text:
            return ""
        
        # Remove markdown headers at start
        text = re.sub(r'^#{1,6}\s+.*$', '', text, flags=re.MULTILINE)
        # Remove bold headers at start
        text = re.sub(r'^\*\*.{1,50}\*\*$', '', text, flags=re.MULTILINE)
        
        return text.strip()


class RoadmapParser:
    """Parse roadmap data from various formats."""
    
    @staticmethod
    def parse_markdown_table(text: str) -> List[List[str]]:
        """
        Parse a markdown table into rows.
        
        Args:
            text: Markdown table text
            
        Returns:
            list: List of row lists (excluding header and separator)
        """
        rows = []
        lines = text.split("\n")
        
        for line in lines:
            # Skip non-table lines
            if "|" not in line:
                continue
            # Skip separator lines
            if "---" in line:
                continue
            
            # Parse cells
            parts = [p.strip() for p in line.split("|") if p.strip()]
            
            # Skip header row (check for known headers)
            if len(parts) >= 6 and "Phase" not in parts[0]:
                rows.append(parts[:6])
        
        return rows
    
    @staticmethod
    def validate_roadmap_row(row: List[str]) -> bool:
        """
        Validate a roadmap row has required data.
        
        Args:
            row: List of cell values
            
        Returns:
            bool: True if valid
        """
        if len(row) < 6:
            return False
        
        # Check phase is not empty
        if not row[0].strip():
            return False
        
        # Check initiative is not empty
        if not row[1].strip():
            return False
        
        return True


class ArabicTextProcessor:
    """Arabic-specific text processing utilities."""
    
    @staticmethod
    def is_arabic(text: str) -> bool:
        """
        Check if text contains Arabic characters.
        
        Args:
            text: Input text
            
        Returns:
            bool: True if contains Arabic
        """
        if not text:
            return False
        return any("\u0600" <= c <= "\u06FF" for c in text)
    
    @staticmethod
    def reverse_for_display(text: str) -> str:
        """
        Reverse Arabic text lines for proper display in some contexts.
        
        Args:
            text: Arabic text
            
        Returns:
            str: Reversed text
        """
        if not text:
            return ""
        return "\n".join([line[::-1] for line in text.split("\n")])
    
    @staticmethod
    def reshape_arabic(text: str) -> str:
        """
        Reshape Arabic text for proper display.
        
        Args:
            text: Arabic text
            
        Returns:
            str: Reshaped text suitable for display
        """
        try:
            import arabic_reshaper
            from bidi.algorithm import get_display
            
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
        except ImportError:
            logger.warning("Arabic reshaping libraries not available")
            return text
        except Exception as e:
            logger.error(f"Arabic reshaping error: {e}")
            return text


class TranslationMapper:
    """Maps English terms to Arabic for Big-4 style translations."""
    
    # Comprehensive translation dictionary
    TRANSLATIONS = {
        # Strategic Pillars
        "Governance & Risk": "الحوكمة وإدارة المخاطر المؤسسية",
        "Foundational Controls": "الضوابط الأمنية الأساسية والبنية التحتية",
        "Detection & Response": "الرصد السيبراني والاستجابة للحوادث",
        "Third-Party & Cloud": "أمن الأطراف الثالثة والحوسبة السحابية",
        "Resilience": "المرونة السيبرانية واستمرارية الأعمال",
        "AI Governance": "حوكمة الذكاء الاصطناعي المسؤول",
        "Use-case & Risk Mapping": "تحليل حالات الاستخدام وتقييم المخاطر",
        "Secure MLOps": "تأمين عمليات تعلم الآلة (Secure MLOps)",
        "Data Governance": "حوكمة البيانات الوطنية والمؤسسية",
        "Digital Governance": "الحوكمة الرقمية الذكية",
        
        # Initiatives
        "Establish governance, policies, and compliance operating rhythm": 
            "تأسيس إطار الحوكمة والسياسات وتفعيل إيقاع الامتثال التشغيلي",
        "Implement IAM/PAM/MFA and access review process": 
            "تطبيق منظومة إدارة الهوية والوصول (IAM) والمصادقة متعددة العوامل",
        "Centralize logging + SIEM use-cases + monitoring KPIs": 
            "مركزية السجلات وتفعيل حالات استخدام SIEM ومؤشرات الرصد",
        "Incident response playbooks + exercises + escalation model": 
            "تطوير أدلة الاستجابة للحوادث وتنفيذ تمارين المحاكاة ونمذجة التصعيد",
        "Build authoritative asset/service inventory and classification": 
            "بناء سجل موحد وشامل للأصول والخدمات وتصنيف البيانات",
        "Third-party risk lifecycle + supplier criticality + contracts": 
            "إدارة دورة حياة مخاطر الأطراف الثالثة وتصنيف الموردين والعقود",
        "BIA + DR tiers + testing program for critical services": 
            "تحليل الأثر (BIA) وتصنيف مستويات التعافي واختبار الخدمات الحرجة",
        
        # Roles
        "GRC Lead": "قائد الحوكمة والمخاطر",
        "Owner": "مالك الإجراء",
        "IAM Lead": "مسؤول إدارة الهوية",
        "SOC Lead": "قائد المركز الأمني",
        "IR Manager": "مدير الاستجابة للحوادث",
        "IT Ops": "العمليات التقنية",
        "Vendor Risk": "مسؤول مخاطر الموردين",
        "BCM Lead": "قائد استمرارية الأعمال",
        "CDO/DMO": "رئيس البيانات / مكتب البيانات",
        "Data Quality": "فريق جودة البيانات",
        "AI Governance": "مكتب حوكمة الذكاء الاصطناعي",
        "Data Science Lead": "قائد علوم البيانات",
        "DT PMO": "مكتب إدارة المشاريع الرقمية",
        "Service Owner": "مالك الخدمة",
        
        # Phases
        "0–3 months": "المدى القريب (٠-٣ أشهر)",
        "3–12 months": "المدى المتوسط (٣-١٢ شهر)",
        "12–36 months": "المدى الاستراتيجي (١-٣ سنوات)",
        
        # KPIs
        "Policy coverage % / Committee cadence": "نسبة تغطية السياسات / انتظام اللجان",
        "Control completion %": "نسبة اكتمال الضوابط",
        "MFA coverage % / Access review completion": "تغطية المصادقة الثنائية / اكتمال مراجعة الوصول",
        "MTTD / alert quality": "متوسط وقت الاكتشاف / جودة التنبيهات",
        "MTTR / exercise pass rate": "متوسط وقت التعافي / نسبة نجاح التمارين",
        
        # Section Headers
        "Executive Vision & Strategic Objectives": "الرؤية التنفيذية والأهداف الاستراتيجية",
        "Current State Assessment (Gap Analysis)": "تقييم الوضع الحالي (تحليل الفجوات)",
        "Strategic Pillars & Initiatives": "الركائز الاستراتيجية والمبادرات",
        "Implementation Roadmap": "خارطة طريق التنفيذ",
        "Measuring Success (KPIs & KRIs)": "قياس النجاح (مؤشرات الأداء)",
        "AI Confidence & Validation": "مستوى الثقة والتحقق",
        "Visual Roadmap (Gantt)": "الخارطة الزمنية (جانت)",
        
        # Table Headers
        "Phase": "المرحلة",
        "Initiative": "المبادرة",
        "Duration": "المدة",
        "Cost": "التكلفة",
        "Role": "الدور",
        "KPI": "مؤشر الأداء",
    }
    
    @classmethod
    def translate(cls, text: str) -> str:
        """
        Translate text using the dictionary.
        
        Args:
            text: English text to translate
            
        Returns:
            str: Arabic translation or original if not found
        """
        return cls.TRANSLATIONS.get(text.strip(), text)
    
    @classmethod
    def translate_dataframe(cls, df, columns: List[str] = None):
        """
        Translate specific columns in a DataFrame.
        
        Args:
            df: pandas DataFrame
            columns: List of columns to translate (default: all string columns)
            
        Returns:
            DataFrame with translated content
        """
        import pandas as pd
        
        df_copy = df.copy()
        
        if columns is None:
            columns = ["Phase", "Initiative", "Role", "KPI"]
        
        for col in columns:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].apply(
                    lambda x: cls.translate(str(x).strip()) if pd.notna(x) else x
                )
        
        return df_copy


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

pdf_extractor = PDFExtractor()
text_processor = TextProcessor()
roadmap_parser = RoadmapParser()
arabic_processor = ArabicTextProcessor()
translation_mapper = TranslationMapper()
