import requests
from icalendar import Calendar
from datetime import datetime, timedelta, date, time
import pytz
from typing import List, Dict

# The private ICS link provided by the user
ICS_URL = "https://calendar.google.com/calendar/ical/titigimad1%40gmail.com/private-aa02a633d6633fa3b980bf5abe849eb0/basic.ics"

# Mock database for new bookings (since we can't write to the ICS)
# Format: "YYYY-MM-DD": ["HH:MM", "HH:MM"]
local_bookings: Dict[str, List[str]] = {}

def get_booked_slots_from_ics(check_date: date) -> List[str]:
    """
    Fetch events from the ICS feed and return booked times for the given date.
    """
    try:
        response = requests.get(ICS_URL)
        response.raise_for_status()
        cal = Calendar.from_ical(response.content)
        
        booked_times = []
        
        for component in cal.walk():
            if component.name == "VEVENT":
                dtstart = component.get('dtstart').dt
                dtend = component.get('dtend').dt
                
                # Handle full-day events (date objects)
                if isinstance(dtstart, date) and not isinstance(dtstart, datetime):
                    # If the event covers our check_date
                    if dtstart <= check_date < dtend:
                        return ["FULL_DAY"] # Block the whole day
                    continue
                
                # Handle timezone awareness
                if isinstance(dtstart, datetime):
                    # Convert to UTC or local time as needed. 
                    # For simplicity, we'll try to match the date.
                    # Note: This is a basic implementation. Timezones can be tricky.
                    event_date = dtstart.date()
                    
                    if event_date == check_date:
                        # Extract time string "HH:MM"
                        # We assume the event blocks this slot
                        time_str = dtstart.strftime("%H:%M")
                        booked_times.append(time_str)
                        
        return booked_times
        
    except Exception as e:
        print(f"Error fetching ICS: {e}")
        return []

def check_availability(date_str: str) -> List[str]:
    """
    Check available appointment slots for a given date using ICS feed + local bookings.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format.
        
    Returns:
        List of available time slots in "HH:MM" format.
    """
    # Define working hours (10:00 to 18:00)
    working_hours = [f"{h:02d}:00" for h in range(10, 19)]
    
    try:
        check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return ["Error: Invalid date format."]

    # 1. Get slots from ICS
    ics_booked = get_booked_slots_from_ics(check_date)
    
    if "FULL_DAY" in ics_booked:
        return []

    # 2. Get slots from local mock DB
    local_booked = local_bookings.get(date_str, [])
    
    # 3. Filter available
    available = []
    for slot in working_hours:
        # Simple string matching for now. 
        # Real implementation would check time ranges overlap.
        if slot not in ics_booked and slot not in local_booked:
            available.append(slot)
            
    return available

def book_appointment(date_str: str, time_str: str, user_name: str, contact_info: str) -> str:
    """
    Book an appointment locally (Mock) and generate a calendar invite.
    
    Returns:
        Success message with ICS file marker for telegram bot to send.
    """
    # Check availability first
    available = check_availability(date_str)
    if time_str not in available:
        return f"Error: Slot {time_str} on {date_str} is not available."
        
    # Book locally
    if date_str not in local_bookings:
        local_bookings[date_str] = []
    local_bookings[date_str].append(time_str)
    
    # Generate calendar invite
    from calendar_utils import create_simple_ics
    
    try:
        ics_path = create_simple_ics(
            date_str=date_str,
            time_str=time_str,
            title=f"Beauty Consultation - {user_name}",
            description=f"Your beauty consultation appointment with our expert advisor.\nLooking forward to meeting you!",
            duration_minutes=15
        )
        
        return f"נקבע! {date_str} {time_str}. ICS: {ics_path} ✅ CALENDAR:{ics_path}"
    except Exception as e:
        return f"Booked {user_name} on {date_str} at {time_str}, but couldn't generate calendar invite: {str(e)}"

