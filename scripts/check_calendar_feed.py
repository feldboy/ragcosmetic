import requests
from icalendar import Calendar
from datetime import datetime, date
import pytz

ICS_URL = "https://calendar.google.com/calendar/ical/titigimad1%40gmail.com/private-aa02a633d6633fa3b980bf5abe849eb0/basic.ics"

def check_feed():
    print(f"Fetching ICS from: {ICS_URL}")
    try:
        response = requests.get(ICS_URL)
        response.raise_for_status()
        print("Successfully fetched ICS data.")
        
        cal = Calendar.from_ical(response.content)
        print("Successfully parsed ICS data.")
        
        print("\nUpcoming Events:")
        count = 0
        now = datetime.now(pytz.utc)
        
        for component in cal.walk():
            if component.name == "VEVENT":
                summary = component.get('summary')
                dtstart = component.get('dtstart').dt
                dtend = component.get('dtend').dt
                
                # Normalize to UTC for comparison if datetime
                if isinstance(dtstart, datetime):
                    if dtstart.tzinfo is None:
                        dtstart = pytz.utc.localize(dtstart)
                    else:
                        dtstart = dtstart.astimezone(pytz.utc)
                        
                    if dtstart > now:
                        print(f"- {summary}: {dtstart} to {dtend}")
                        count += 1
                        if count >= 10:
                            break
                elif isinstance(dtstart, date):
                    # Future dates
                    if dtstart >= now.date():
                        print(f"- {summary} (All Day): {dtstart}")
                        count += 1
                        if count >= 10:
                            break
                            
        if count == 0:
            print("No upcoming events found (or feed is empty).")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_feed()
