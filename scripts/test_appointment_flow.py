import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.appointments import check_availability, book_appointment
from src.core.config import Config

def test_availability():
    print("\n--- Testing Availability Check ---")
    # Check tomorrow
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Checking availability for {tomorrow}...")
    
    slots = check_availability(tomorrow)
    if slots:
        print(f"Available slots: {slots}")
    else:
        print("No slots available (or error/full day).")
        
    return tomorrow, slots

def test_booking(date_str, time_str):
    print("\n--- Testing Booking Simulation ---")
    if not time_str:
        print("No time slot available to test booking.")
        return

    print(f"Attempting to book {date_str} at {time_str}...")
    
    # Use a dummy email for testing to avoid spamming real people too much, 
    # but we want to see if the system TRIES to send.
    # ideally we mock the email sender, but here we are doing an integration test.
    # If config is set, it will try to send.
    
    user_name = "Test User"
    user_email = "test@example.com"
    
    result = book_appointment(date_str, time_str, user_name, user_email, "Test Treatment")
    print("Booking Result:")
    print(result)
    
    # Check if ICS file was created
    if "CALENDAR:" in result:
        ics_path = result.split("CALENDAR:")[1].strip().split()[0] # Extract path
        if os.path.exists(ics_path):
            print(f"SUCCESS: ICS file created at {ics_path}")
            
            # Verify organizer
            with open(ics_path, 'r') as f:
                content = f.read()
                if f"mailto:{Config.get_email_sender()}" in content:
                     print("SUCCESS: Organizer email is correct in ICS.")
                else:
                     print(f"WARNING: Organizer email might be incorrect in ICS. Content snippet:\n{content[:200]}...")
        else:
            print(f"FAILURE: ICS file not found at {ics_path}")

if __name__ == "__main__":
    try:
        date_str, slots = test_availability()
        if slots:
            test_booking(date_str, slots[0])
        else:
            print("Skipping booking test as no slots are available.")
            
    except Exception as e:
        print(f"Test failed with error: {e}")
