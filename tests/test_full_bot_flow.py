import os
import sys
import asyncio
import datetime
from typing import Optional

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.agent import beauty_advisor_agent, BeautyAdvisorDependencies
from src.core.config import Config

# Mock dependencies
deps = BeautyAdvisorDependencies()

async def run_agent_test():
    print("🤖 Starting Full Bot Flow Test")
    print("="*50)

    # Calculate a test time for tomorrow
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    # Round to next hour to avoid "past time" issues if running at xx:59
    test_hour = 12
    date_str = tomorrow.strftime("%Y-%m-%d")
    time_str = f"{test_hour}:00"
    
    print(f"📅 Test Target: {date_str} at {time_str}")
    
    # --- Scenario 1: Successful Booking ---
    print("\n🔹 Scenario 1: Booking an Available Slot")
    user_msg_1 = f"Hi, I want to book a facial treatment for {date_str} at {time_str}. My name is BotTester and email is omer.dayan1999@gmail.com"
    print(f"User: {user_msg_1}")
    
    try:
        result_1 = await beauty_advisor_agent.run(user_msg_1, deps=deps)
        print(f"Agent: {result_1.data}")
        
        # Verify success keywords
        if "נקבע" in result_1.data or "confirmed" in result_1.data.lower() or "scheduled" in result_1.data.lower():
            print("✅ Scenario 1 Passed: Booking confirmed.")
        else:
            print("⚠️ Scenario 1 Warning: Response didn't explicitly confirm booking. Check output.")
            
    except Exception as e:
        print(f"❌ Scenario 1 Failed: {e}")

    # --- Scenario 2: Booking Unavailable Slot (Same time) ---
    print("\n🔹 Scenario 2: Booking an Unavailable Slot (The one we just booked)")
    user_msg_2 = f"I want to book a manicure for {date_str} at {time_str}. Name: AnotherUser, Email: other@test.com"
    print(f"User: {user_msg_2}")
    
    try:
        result_2 = await beauty_advisor_agent.run(user_msg_2, deps=deps)
        print(f"Agent: {result_2.data}")
        
        # Verify rejection and alternatives
        if "תפוסה" in result_2.data or "taken" in result_2.data.lower() or "unavailable" in result_2.data.lower():
            print("✅ Scenario 2 Passed: Slot identified as taken.")
            if "השעות הקרובות הפנויות" in result_2.data or "available" in result_2.data.lower():
                 print("✅ Scenario 2 Passed: Alternatives suggested.")
            else:
                 print("⚠️ Scenario 2 Warning: Alternatives NOT suggested.")
        else:
            print("❌ Scenario 2 Failed: Agent didn't reject the booking.")
            
    except Exception as e:
        print(f"❌ Scenario 2 Failed: {e}")

    print("\n" + "="*50)
    print("🏁 Test Complete")

if __name__ == "__main__":
    asyncio.run(run_agent_test())
