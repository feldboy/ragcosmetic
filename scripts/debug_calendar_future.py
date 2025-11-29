import requests
from icalendar import Calendar
from datetime import datetime, date, timedelta
import pytz

ICS_URL = "https://calendar.google.com/calendar/ical/titigimad1%40gmail.com/private-aa02a633d6633fa3b980bf5abe849eb0/basic.ics"

def debug_feed_future():
    print(f"Fetching ICS from: {ICS_URL}")
    try:
        response = requests.get(ICS_URL)
        response.raise_for_status()
        
        cal = Calendar.from_ical(response.content)
        
        print("\n--- Searching for Future Events (2025+) ---")
        count = 0
        future_count = 0
        
        cutoff = datetime(2025, 1, 1, tzinfo=pytz.utc)
        
        for component in cal.walk():
            if component.name == "VEVENT":
                count += 1
                dtstart = component.get('dtstart').dt
                
                # Normalize to UTC
                if isinstance(dtstart, datetime):
                    if dtstart.tzinfo is None:
                        dtstart = pytz.utc.localize(dtstart)
                    else:
                        dtstart = dtstart.astimezone(pytz.utc)
                        
                    if dtstart > cutoff:
                        print(f"FUTURE EVENT: {component.get('summary')} | {dtstart}")
                        future_count += 1
                elif isinstance(dtstart, date):
                    if dtstart > cutoff.date():
                        print(f"FUTURE EVENT (All Day): {component.get('summary')} | {dtstart}")
                        future_count += 1
                        
        print(f"\nTotal events found: {count}")
        print(f"Future events found: {future_count}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_feed_future()
