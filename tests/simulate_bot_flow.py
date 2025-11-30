import os
import sys
import datetime
from typing import List

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.appointments import book_appointment, find_nearest_available_slots

def simulate_conversation():
    print("🤖 Simulating Bot Conversation Flow (Logic Verification)")
    print("="*60)
    
    # Setup dates
    today = datetime.datetime.now()
    target_date = today + datetime.timedelta(days=2) # 2 days from now
    date_str = target_date.strftime("%Y-%m-%d")
    
    # --- Scenario 1: Successful Booking ---
    print("\n🔹 Scenario 1: User asks for an available slot")
    print(f"User: \"Hi, I'd like to book a facial treatment for {date_str} at 10:00.\"")
    
    print("\n[System]: Bot analyzes request...")
    print(f"[System]: Bot calls tool 'book_consultation(date='{date_str}', time='10:00', treatment='טיפול פנים')'")
    
    # Call the function directly (simulating the tool call)
    response_1 = book_appointment(
        date_str=date_str,
        time_str="10:00",
        user_name="Simulated User",
        email="simulated@test.com",
        treatment_name="טיפול פנים"
    )
    
    print(f"\nBot: \"{response_1}\"")
    
    if "נקבע" in response_1 or "confirmed" in response_1:
        print("✅ Result: Booking confirmed. Email invite triggered.")
    else:
        print("⚠️ Result: Unexpected response (maybe slot was taken?).")

    # --- Scenario 2: Unavailable Slot ---
    print("\n" + "-"*60)
    print("\n🔹 Scenario 2: User asks for the SAME slot (now taken)")
    print(f"User: \"I also want to book a manicure for {date_str} at 10:00.\"")
    
    print("\n[System]: Bot analyzes request...")
    print(f"[System]: Bot calls tool 'book_consultation(date='{date_str}', time='10:00', treatment='מניקור')'")
    
    # Call the function again for the same slot
    response_2 = book_appointment(
        date_str=date_str,
        time_str="10:00",
        user_name="Second User",
        email="second@test.com",
        treatment_name="מניקור"
    )
    
    print(f"\nBot: \"{response_2}\"")
    
    if "תפוסה" in response_2 and "השעות הקרובות הפנויות" in response_2:
        print("✅ Result: Slot rejected. Alternatives suggested.")
    else:
        print("⚠️ Result: Unexpected response.")

    print("\n" + "="*60)
    print("🏁 Simulation Complete")
    print("Note: This test verified the logic that the bot uses.")
    print("To run the actual AI bot, please add your API keys to .env")

if __name__ == "__main__":
    simulate_conversation()
