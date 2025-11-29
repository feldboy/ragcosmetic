import requests
from icalendar import Calendar
from datetime import datetime, date, timedelta
import pytz

ICS_URL = "https://calendar.google.com/calendar/ical/titigimad1%40gmail.com/private-aa02a633d6633fa3b980bf5abe849eb0/basic.ics"

def debug_feed():
    print(f"Fetching ICS from: {ICS_URL}")
    try:
        response = requests.get(ICS_URL)
        response.raise_for_status()
        print(f"Response size: {len(response.content)} bytes")
        
        # Print first 500 characters to verify format
        print("\n--- Raw Content Start ---")
        print(response.content[:500].decode('utf-8'))
        print("--- Raw Content End ---\n")
        
        cal = Calendar.from_ical(response.content)
        
        print("\n--- Parsing Events ---")
        count = 0
        now = datetime.now(pytz.utc)
        
        for component in cal.walk():
            if component.name == "VEVENT":
                summary = component.get('summary')
                dtstart = component.get('dtstart').dt
                dtend = component.get('dtend').dt
                
                print(f"Found event: {summary} | Start: {dtstart} | End: {dtend}")
                
                # Check if it's tomorrow
                tomorrow = date.today() + timedelta(days=1)
                
                if isinstance(dtstart, datetime):
                    event_date = dtstart.date()
                else:
                    event_date = dtstart
                    
                if event_date == tomorrow:
                    print(f"!!! FOUND EVENT FOR TOMORROW: {summary} !!!")
                
                count += 1
                if count >= 20:
                    print("... (limit reached)")
                    break
                            
        if count == 0:
            print("No events found in the feed.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_feed()
