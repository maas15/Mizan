#!/usr/bin/env python3
"""
Verify AI service generates content based on user input only.
"""

import os
import sys
from pathlib import Path

APP_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(APP_DIR))

env_path = APP_DIR / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ No OPENAI_API_KEY found")
    sys.exit(1)

print(f"✅ API Key: {api_key[:15]}...{api_key[-4:]}")

from services.ai_service_v3 import ai_service

def test_no_technology():
    """Test: No technology = starting from zero, no partial compliance."""
    print("\n" + "=" * 80)
    print("TEST 1: No Technology = Starting from ZERO")
    print("=" * 80)
    
    context = {
        "org_name": "New Company",
        "sector": "Technology",
        "domain": "Cyber Security",
        "language": "English",
        "frameworks": ["NCA ECC", "NCA CCC"],
        "tech": "Not specified",
        "challenges": "Building security from scratch",
        "gap_data": {}
    }
    
    response = ai_service.generate_strategy(context)
    
    if not response.success:
        print(f"❌ Failed: {response.content}")
        return False
    
    content = response.content.lower()
    
    # Should NOT have these (assuming compliance with percentage)
    bad_patterns = [
        "partial compliance",
        "partially compliant", 
        "some compliance",
        "compliance score of",
        "compliance level of",
        "75%", "65%", "50%", "40%", "60%", "70%", "80%"
    ]
    
    found_bad = [p for p in bad_patterns if p in content]
    has_timeline_table = "| phase |" in content or "|phase|" in content
    
    print(f"Bad patterns found: {found_bad if found_bad else 'NONE ✅'}")
    print(f"Has timeline table: {'YES ❌' if has_timeline_table else 'NO ✅'}")
    
    if found_bad or has_timeline_table:
        return False
    
    print("✅ PASS: No assumptions, no timeline table")
    return True


def test_not_specified_arabic():
    """Test: Arabic - no assumed compliance percentages."""
    print("\n" + "=" * 80)
    print("TEST 2: Arabic - No Technology")
    print("=" * 80)
    
    context = {
        "org_name": "شركة جديدة",
        "sector": "Banking",
        "domain": "Data Management",
        "language": "Arabic",
        "frameworks": ["PDPL"],
        "tech": "غير محدد",
        "gap_data": {}
    }
    
    response = ai_service.generate_strategy(context)
    
    if not response.success:
        print(f"❌ Failed: {response.content}")
        return False
    
    content = response.content
    
    # Check for ASSUMED compliance percentages (the real problem)
    # "نسبة الامتثال" alone is OK if it says "لا يوجد نسبة امتثال"
    bad_patterns = [
        "75%", "65%", "50%", "40%", "60%", "70%", "80%",
        "امتثال جزئي",  # partial compliance
        "نسبة امتثال حالية",  # current compliance rate
        "مستوى الامتثال الحالي",  # current compliance level
    ]
    
    found_bad = [p for p in bad_patterns if p in content]
    
    # Check for good indicators
    good_patterns = ["من الصفر", "لا يوجد", "بدون برنامج", "تأسيس", "بناء"]
    found_good = [p for p in good_patterns if p in content]
    
    print(f"Bad patterns (percentages/partial): {found_bad if found_bad else 'NONE ✅'}")
    print(f"Good patterns: {found_good[:3]}..." if found_good else "None ⚠️")
    
    # Show relevant section
    sections = content.split("|||")
    if len(sections) > 1:
        print(f"\nSection 2 preview:\n{sections[1][:300]}...")
    
    if found_bad:
        print(f"❌ FAIL: Found assumption patterns: {found_bad}")
        return False
    
    print("✅ PASS: No assumed percentages in Arabic")
    return True


def test_with_actual_score():
    """Test: When user provides score, use that score."""
    print("\n" + "=" * 80)
    print("TEST 3: User Provides Score (45%)")
    print("=" * 80)
    
    context = {
        "org_name": "Existing Corp",
        "sector": "Healthcare",
        "domain": "Cyber Security",
        "language": "English",
        "tech": "Firewall, Antivirus",
        "gap_data": {"compliance_score": 45}
    }
    
    response = ai_service.generate_strategy(context)
    
    if not response.success:
        print(f"❌ Failed: {response.content}")
        return False
    
    content = response.content
    
    has_45 = "45%" in content or "45 %" in content
    has_75 = "75%" in content
    
    print(f"Has user's 45%: {'YES ✅' if has_45 else 'NO ⚠️'}")
    print(f"Has assumed 75%: {'YES ❌' if has_75 else 'NO ✅'}")
    
    if has_75:
        print("❌ FAIL: Used assumed 75% instead of user's 45%")
        return False
    
    print("✅ PASS: Respects user-provided data")
    return True


def test_six_sections():
    """Test: Output has 6 sections."""
    print("\n" + "=" * 80)
    print("TEST 4: Six Sections Format")
    print("=" * 80)
    
    context = {
        "org_name": "Test Org",
        "sector": "Retail",
        "domain": "Digital Transformation",
        "language": "English",
        "tech": "",
        "gap_data": {}
    }
    
    response = ai_service.generate_strategy(context)
    
    if not response.success:
        print(f"❌ Failed: {response.content}")
        return False
    
    sections = response.content.split("|||")
    section_count = len([s for s in sections if s.strip()])
    
    print(f"Sections found: {section_count}")
    
    if section_count < 6:
        print(f"❌ FAIL: Only {section_count} sections")
        return False
    
    print("✅ PASS: Has 6+ sections")
    return True


if __name__ == "__main__":
    print("=" * 80)
    print("VERIFICATION: No Assumptions, No Timeline Tables")
    print("=" * 80)
    
    results = []
    results.append(("No Technology Test", test_no_technology()))
    results.append(("Arabic No Tech Test", test_not_specified_arabic()))
    results.append(("User Score Test", test_with_actual_score()))
    results.append(("Six Sections Test", test_six_sections()))
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✅ ALL TESTS PASSED")
    else:
        print("\n❌ SOME TESTS FAILED")
    
    sys.exit(0 if all_passed else 1)
