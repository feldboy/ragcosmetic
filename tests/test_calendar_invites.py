#!/usr/bin/env python3
"""
Test calendar invite generation.
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.calendar_utils import create_simple_ics, generate_ics_file

def test_calendar_generation():
    print("📅 Testing Calendar Generation...")
    print("-" * 50)
    
    # Test 1: Simple ICS generation
    print("\n1. Testing create_simple_ics():")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        ics_path = create_simple_ics(
            date_str=tomorrow,
            time_str="14:00",
            title="Test Beauty Consultation",
            description="This is a test appointment",
            duration_minutes=15
        )
        
        if os.path.exists(ics_path):
            print(f"   ✅ ICS file created: {ics_path}")
            print(f"   ✅ File size: {os.path.getsize(ics_path)} bytes")
            
            # Check content
            with open(ics_path, 'r') as f:
                content = f.read()
                if "BEGIN:VCALENDAR" in content and "BEGIN:VEVENT" in content:
                    print("   ✅ ICS format looks valid")
                else:
                    print("   ❌ ICS format seems invalid")
        else:
            print(f"   ❌ ICS file not found at {ics_path}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Full ICS with email
    print("\n2. Testing generate_ics_file():")
    try:
        ics_path = generate_ics_file(
            date_str=tomorrow,
            time_str="15:30",
            user_name="Test User",
            email="test@example.com",
            duration_minutes=15
        )
        
        if os.path.exists(ics_path):
            print(f"   ✅ Full ICS file created: {ics_path}")
        else:
            print(f"   ❌ ICS file not found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Calendar Tests Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_calendar_generation()
