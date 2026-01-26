#!/usr/bin/env python3
"""
Test script to verify AI-driven document generation.
Run this to confirm the app generates unique, domain-specific content.
"""

import os
import sys
from pathlib import Path

# Setup path
APP_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(APP_DIR))

# Load environment
from dotenv import load_dotenv
load_dotenv(APP_DIR / ".env")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY not found in .env file")
    print("Please ensure .env file exists with: OPENAI_API_KEY=your-key")
    sys.exit(1)

print(f"✅ API Key loaded: {api_key[:15]}...{api_key[-4:]}")

from services.ai_service_v3 import ai_service

def test_strategy_generation():
    """Test that different domains produce different content."""
    print("\n" + "=" * 80)
    print("TEST: Domain-Specific Strategy Generation")
    print("=" * 80)
    
    domains = [
        ("Data Management", "Arabic"),
        ("Artificial Intelligence", "Arabic"),
        ("Cyber Security", "Arabic"),
    ]
    
    results = {}
    
    for domain, lang in domains:
        print(f"\n📋 Generating {domain} strategy ({lang})...")
        
        context = {
            "org_name": "شركة اختبار" if lang == "Arabic" else "Test Company",
            "sector": "Banking",
            "domain": domain,
            "language": lang,
            "gap_data": {}  # No data provided - should NOT assume 75% vs 0%
        }
        
        response = ai_service.generate_strategy(context)
        
        if response.success:
            results[domain] = response.content
            
            # Check for domain-specific keywords
            content_lower = response.content.lower()
            
            if domain == "Data Management":
                has_data_keywords = any(kw in response.content for kw in ["PDPL", "بيانات", "خصوصية", "جودة البيانات"])
                has_cyber_keywords = any(kw in response.content for kw in ["SIEM", "SOC", "سيبراني", "تهديدات"])
                print(f"   ✅ Has Data Management keywords: {has_data_keywords}")
                print(f"   ⚠️ Has Cyber keywords (should be minimal): {has_cyber_keywords}")
                
            elif domain == "Artificial Intelligence":
                has_ai_keywords = any(kw in response.content for kw in ["ذكاء اصطناعي", "AI", "نماذج", "تحيز", "XAI"])
                print(f"   ✅ Has AI keywords: {has_ai_keywords}")
            
            # Check for forbidden phrases
            has_75_0 = "75%" in response.content and "0%" in response.content
            has_available_request = "متاح عند الطلب" in response.content or "available upon request" in content_lower
            
            print(f"   ❌ Has '75% vs 0%' phrase: {has_75_0}")
            print(f"   ❌ Has 'available upon request': {has_available_request}")
            
            # Show preview
            print(f"\n   Preview (first 300 chars):")
            print(f"   {response.content[:300]}...")
            
        else:
            print(f"   ❌ Failed: {response.content}")
    
    # Check uniqueness
    print("\n" + "=" * 80)
    print("UNIQUENESS CHECK")
    print("=" * 80)
    
    if len(results) >= 2:
        domains_list = list(results.keys())
        for i in range(len(domains_list)):
            for j in range(i+1, len(domains_list)):
                d1, d2 = domains_list[i], domains_list[j]
                # Compare first 500 chars
                similar = results[d1][:500] == results[d2][:500]
                status = "❌ IDENTICAL" if similar else "✅ UNIQUE"
                print(f"{d1} vs {d2}: {status}")


def test_policy_uniqueness():
    """Test that same policy generated twice is different."""
    print("\n" + "=" * 80)
    print("TEST: Policy Uniqueness (Same query, different results)")
    print("=" * 80)
    
    policies = []
    for i in range(2):
        print(f"\n📋 Generating Policy (attempt {i+1})...")
        response = ai_service.generate_policy(
            policy_name="سياسة حماية البيانات",
            domain="Data Management",
            framework="PDPL",
            language="Arabic"
        )
        if response.success:
            policies.append(response.content)
            print(f"   ✅ Generated ({len(response.content)} chars)")
        else:
            print(f"   ❌ Failed: {response.content}")
    
    if len(policies) == 2:
        # Compare
        identical = policies[0] == policies[1]
        similar = policies[0][:200] == policies[1][:200]
        
        if identical:
            print("\n❌ PROBLEM: Both policies are IDENTICAL")
        elif similar:
            print("\n⚠️ WARNING: Policies start the same (first 200 chars)")
        else:
            print("\n✅ SUCCESS: Policies are DIFFERENT (as expected)")


if __name__ == "__main__":
    print("=" * 80)
    print("MIZAN GRC - AI GENERATION TEST")
    print("=" * 80)
    
    test_strategy_generation()
    test_policy_uniqueness()
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
