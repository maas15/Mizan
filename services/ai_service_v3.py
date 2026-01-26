"""
Mizan GRC - AI Service V3
100% AI-generated content based on user input ONLY.
NO assumptions. NO hardcoded values. NO implementation timeline tables.
"""

import os
import logging
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ResponseType(Enum):
    STRATEGY = "strategy"
    POLICY = "policy"
    AUDIT = "audit"
    RISK = "risk"

@dataclass
class AIResponse:
    content: str
    success: bool
    source: str = "ai"
    model: str = "gpt-4-turbo"
    confidence: int = 85


class AIService:
    """AI-driven document generation based strictly on user input."""
    
    @property
    def is_available(self) -> bool:
        return self.api_key is not None and self.client is not None
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4-turbo"
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                logger.info("✅ AI Service V3 ready")
            except ImportError:
                try:
                    import requests
                    self.client = "requests"
                except:
                    self.client = None
            except Exception as e:
                logger.error(f"Init error: {e}")
    
    def _call_ai(self, system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        
        if self.client == "requests":
            import requests
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.8
                },
                timeout=180
            )
            if resp.status_code != 200:
                raise Exception(f"API error: {resp.text}")
            return resp.json()["choices"][0]["message"]["content"]
        else:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.8
            )
            return resp.choices[0].message.content
    
    def _check_has_technology(self, tech: str) -> bool:
        """Check if user has any existing technology."""
        if not tech:
            return False
        tech_lower = tech.lower().strip()
        no_tech_indicators = [
            "not specified", "none", "no", "nothing", "n/a", "na", 
            "لا يوجد", "لا شيء", "غير محدد", "لم يتم", ""
        ]
        return tech_lower not in no_tech_indicators and len(tech_lower) > 2
    
    def _get_current_state_text(self, context: Dict[str, Any], language: str) -> tuple:
        """Get current state description based on user input."""
        tech = context.get("tech", "")
        gap_data = context.get("gap_data", {})
        
        has_tech = self._check_has_technology(tech)
        has_score = gap_data.get("compliance_score") is not None
        
        if language in ["Arabic", "العربية"]:
            if has_score:
                score = gap_data['compliance_score']
                return (f"لدى المنظمة برنامج قائم بنسبة امتثال {score}%", "HAS_SCORE")
            elif has_tech:
                return (f"لدى المنظمة بعض التقنيات: {tech}", "HAS_TECH")
            else:
                return ("المنظمة تبدأ من الصفر - لا يوجد برنامج أو تقنيات حالية", "FROM_ZERO")
        else:
            if has_score:
                score = gap_data['compliance_score']
                return (f"Organization has existing program with {score}% compliance", "HAS_SCORE")
            elif has_tech:
                return (f"Organization has some technology: {tech}", "HAS_TECH")
            else:
                return ("Organization is starting from ZERO - no existing program or technology", "FROM_ZERO")
    
    def generate_strategy(self, context: Dict[str, Any]) -> AIResponse:
        """Generate strategy based strictly on user input. No assumptions."""
        
        org_name = context.get("org_name", "Organization")
        sector = context.get("sector", "General")
        domain = context.get("domain", "Cyber Security")
        language = context.get("language", "English")
        frameworks = context.get("frameworks", [])
        challenges = context.get("challenges", "")
        budget = context.get("budget", "")
        horizon = context.get("horizon", "")
        
        # Get current state based on actual user input
        current_state_text, state_type = self._get_current_state_text(context, language)
        
        # Build facts from user input
        fw_str = ', '.join(frameworks) if isinstance(frameworks, list) else frameworks if frameworks else "Not specified"

        if language in ["Arabic", "العربية"]:
            system_prompt = f"""أنت مستشار GRC في شركة Big4. أنشئ استراتيجية بناءً على معلومات المستخدم فقط.

قواعد صارمة:
1. الوضع الحالي للمنظمة: {current_state_text}
2. إذا كانت المنظمة تبدأ من الصفر:
   - لا تذكر أي نسبة امتثال
   - لا تقل "نسبة الامتثال" أو "مستوى الامتثال"
   - قل فقط "المنظمة تبدأ من الصفر بدون برنامج قائم"
3. لا تفترض أي شيء لم يقدمه المستخدم
4. لا تضف جدول زمني للتنفيذ
5. اكتب 6 أقسام مفصولة بـ |||"""

            if state_type == "FROM_ZERO":
                state_instruction = """في قسم تقييم الوضع الحالي، اكتب:
"المنظمة ليس لديها برنامج {domain} قائم وتبدأ البناء من الصفر. لا يوجد تقييم امتثال حالي."
لا تذكر أي نسب مئوية."""
            else:
                state_instruction = f"استخدم المعلومات المقدمة: {current_state_text}"

            user_prompt = f"""استراتيجية {domain} لـ {org_name} ({sector})

المعلومات المقدمة:
- الأطر المستهدفة: {fw_str}
- الميزانية: {budget or 'غير محدد'}
- المدة: {horizon or 'غير محدد'} شهر
- التحديات: {challenges or 'غير محدد'}

{state_instruction}

اكتب 6 أقسام مفصولة بـ ||| (بدون جدول تنفيذ تفصيلي):

1. الرؤية التنفيذية و5 أهداف استراتيجية
|||
2. تقييم الوضع الحالي والفجوات
|||
3. الركائز الاستراتيجية (4 ركائز، 3 مبادرات لكل ركيزة)
|||
4. ملخص الاستثمار والموارد
|||
5. مؤشرات الأداء (KPIs) ومؤشرات المخاطر (KRIs)
|||
6. التوصيات والخطوات التالية
|||"""

        else:
            system_prompt = f"""You are a Big4 GRC consultant. Create strategy based on user input ONLY.

Strict rules:
1. Organization's current state: {current_state_text}
2. If organization is starting from zero:
   - Do NOT mention any compliance percentage
   - Do NOT say "compliance rate" or "compliance level"
   - Say only "Organization is starting from zero with no existing program"
3. Do NOT assume anything not provided by user
4. Do NOT add implementation timeline table
5. Write 6 sections separated by |||"""

            if state_type == "FROM_ZERO":
                state_instruction = """In Current State Assessment section, write:
"The organization does not have an existing {domain} program and is building from scratch. No compliance assessment exists."
Do NOT mention any percentages."""
            else:
                state_instruction = f"Use provided information: {current_state_text}"

            user_prompt = f"""{domain} strategy for {org_name} ({sector})

Provided information:
- Target frameworks: {fw_str}
- Budget: {budget or 'Not specified'}
- Timeline: {horizon or 'Not specified'} months
- Challenges: {challenges or 'Not specified'}

{state_instruction}

Write 6 sections separated by ||| (NO detailed implementation timeline table):

1. Executive Vision and 5 Strategic Objectives
|||
2. Current State Assessment and Gaps
|||
3. Strategic Pillars (4 pillars, 3 initiatives each)
|||
4. Investment and Resource Summary
|||
5. KPIs and KRIs
|||
6. Recommendations and Next Steps
|||"""

        try:
            content = self._call_ai(system_prompt, user_prompt, 4000)
            return AIResponse(content=content, success=True, source="api", model=self.model)
        except Exception as e:
            logger.error(f"Strategy failed: {e}")
            return AIResponse(content=f"Error: {str(e)}", success=False, source="error", model="none")
    
    def generate_policy(self, policy_name: str, domain: str, framework: str, language: str = "English") -> AIResponse:
        """Generate policy based on domain and framework requirements."""
        
        if language in ["Arabic", "العربية"]:
            system_prompt = f"أنت مستشار GRC. أنشئ سياسة {domain} متوافقة مع {framework}. محتوى فريد 100%."
            user_prompt = f"""سياسة "{policy_name}" لـ {domain} وفق {framework}.

اكتب:
1. الغرض والنطاق
2. 6-8 متطلبات مرتبطة بـ {framework}
3. الأدوار والمسؤوليات
4. 8-10 ضوابط
5. الامتثال والمراقبة
6. المراجعة"""
        else:
            system_prompt = f"You are a GRC consultant. Create {domain} policy aligned with {framework}. 100% unique content."
            user_prompt = f""""{policy_name}" policy for {domain} per {framework}.

Write:
1. Purpose and Scope
2. 6-8 requirements linked to {framework}
3. Roles and Responsibilities
4. 8-10 controls
5. Compliance and Monitoring
6. Review"""
        
        try:
            content = self._call_ai(system_prompt, user_prompt, 3500)
            return AIResponse(content=content, success=True, source="api")
        except Exception as e:
            return AIResponse(content=f"Error: {str(e)}", success=False, source="error")
    
    def generate_audit_report(self, standard: str, evidence_text: str, language: str = "English", domain: str = "Cyber Security") -> AIResponse:
        """Generate audit report based on provided evidence only."""
        
        evidence = evidence_text[:3000] if evidence_text else ""
        has_evidence = bool(evidence.strip())
        
        if language in ["Arabic", "العربية"]:
            system_prompt = "أنت مدقق Big4. أنشئ تقرير تدقيق بناءً على الأدلة المقدمة فقط. لا تفترض أي نتائج."
            if has_evidence:
                user_prompt = f"""تقرير تدقيق {standard} في {domain}.

الأدلة: {evidence}

اكتب: 1. ملخص 2. النطاق 3. 3-5 نتائج من الأدلة 4. الإيجابيات 5. التوصيات 6. الخلاصة"""
            else:
                user_prompt = f"""تقرير تدقيق {standard} في {domain}.

لم تقدم أدلة. اكتب: 1. التدقيق يتطلب أدلة 2. قائمة الأدلة المطلوبة 3. خطوات التدقيق"""
        else:
            system_prompt = "You are a Big4 auditor. Create audit report based on provided evidence ONLY. Do not assume findings."
            if has_evidence:
                user_prompt = f"""Audit report for {standard} in {domain}.

Evidence: {evidence}

Write: 1. Summary 2. Scope 3. 3-5 findings from evidence 4. Positives 5. Recommendations 6. Conclusion"""
            else:
                user_prompt = f"""Audit report for {standard} in {domain}.

No evidence provided. Write: 1. Audit requires evidence 2. List of required evidence 3. Audit steps"""
        
        try:
            content = self._call_ai(system_prompt, user_prompt, 3500)
            return AIResponse(content=content, success=True, source="api")
        except Exception as e:
            return AIResponse(content=f"Error: {str(e)}", success=False, source="error")
    
    def generate_risk_analysis(self, domain: str, threat: str, asset: str, context: Dict = None, language: str = "English") -> AIResponse:
        """Generate risk analysis for specific threat scenario."""
        
        context = context or {}
        notes = context.get("notes", "")[:1000]
        
        if language in ["Arabic", "العربية"]:
            system_prompt = f"أنت مستشار مخاطر Big4. تحليل مخاطر {domain} للسيناريو المحدد فقط."
            user_prompt = f"""تحليل مخاطر {domain}: التهديد={threat}، الأصل={asset}
ملاحظات: {notes or 'لا يوجد'}

اكتب: 1. السيناريو 2. 5-7 مخاطر محددة 3. الأثر 4. 6-8 ضوابط 5. التخفيف 6. KRIs"""
        else:
            system_prompt = f"You are a Big4 risk consultant. {domain} risk analysis for the specific scenario only."
            user_prompt = f"""{domain} risk analysis: Threat={threat}, Asset={asset}
Notes: {notes or 'None'}

Write: 1. Scenario 2. 5-7 specific risks 3. Impact 4. 6-8 controls 5. Mitigation 6. KRIs"""
        
        try:
            content = self._call_ai(system_prompt, user_prompt, 3500)
            return AIResponse(content=content, success=True, source="api")
        except Exception as e:
            return AIResponse(content=f"Error: {str(e)}", success=False, source="error")


ai_service = AIService()
