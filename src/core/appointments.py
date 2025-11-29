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
    Check available appointment slots for a given date using Google Calendar API.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format.
        
    Returns:
        List of available time slots in "HH:MM" format.
    """
    from src.utils.google_calendar import check_is_slot_available
    
    # Define working hours (10:00 to 18:00)
    working_hours = [f"{h:02d}:00" for h in range(10, 19)]
    
    try:
        check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return ["Error: Invalid date format."]

    available = []
    tz = pytz.timezone('Asia/Jerusalem')
    
    for slot in working_hours:
        # Construct datetime for this slot
        slot_dt_str = f"{date_str} {slot}"
        slot_start = datetime.strptime(slot_dt_str, "%Y-%m-%d %H:%M")
        slot_start = tz.localize(slot_start)
        slot_end = slot_start + timedelta(minutes=60) # Assume 1 hour slots
        
        # Check if this specific slot is free
        if check_is_slot_available(slot_start, slot_end):
            available.append(slot)
            
    return available

def find_nearest_available_slots(date_str: str, time_str: str, num_alternatives: int = 3) -> List[str]:
    """
    Find nearest available time slots around a requested time.
    
    Args:
        date_str: Requested date in "YYYY-MM-DD" format.
        time_str: Requested time in "HH:MM" format.
        num_alternatives: Number of alternative slots to suggest.
        
    Returns:
        List of available time slots in "YYYY-MM-DD HH:MM" format.
    """
    try:
        requested_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        return []
    
    alternatives = []
    
    # Check same day first (later slots)
    available_today = check_availability(date_str)
    for slot in available_today:
        if slot > time_str:
            alternatives.append(f"{date_str} {slot}")
            if len(alternatives) >= num_alternatives:
                return alternatives
    
    # Check next few days
    for days_ahead in range(1, 7):
        next_date = requested_dt + timedelta(days=days_ahead)
        next_date_str = next_date.strftime("%Y-%m-%d")
        available_slots = check_availability(next_date_str)
        
        for slot in available_slots:
            alternatives.append(f"{next_date_str} {slot}")
            if len(alternatives) >= num_alternatives:
                return alternatives
    
    return alternatives

def book_appointment(date_str: str, time_str: str, user_name: str, contact_info: str, treatment_name: str = "ייעוץ קוסמטי") -> str:
    """
    Book an appointment directly on Google Calendar.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format.
        time_str: Time in "HH:MM" format.
        user_name: Client name.
        contact_info: Phone or email.
        treatment_name: Name of the treatment/service.
    
    Returns:
        Success message or error with alternatives.
    """
    from src.utils.google_calendar import create_calendar_event, check_is_slot_available
    
    # Parse datetime
    try:
        dt_str = f"{date_str} {time_str}"
        start_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        tz = pytz.timezone('Asia/Jerusalem')
        start_dt = tz.localize(start_dt)
        end_dt = start_dt + timedelta(minutes=60) # 1 hour appointment
    except ValueError:
        return f"Error: Invalid date/time format."

    # Double check availability
    if not check_is_slot_available(start_dt, end_dt):
        # Find alternative slots
        alternatives = find_nearest_available_slots(date_str, time_str, 3)
        
        if alternatives:
            alt_text = "\n".join([f"  • {alt}" for alt in alternatives[:3]])
            return f"מצטערת, השעה {time_str} ב-{date_str} תפוסה. 😔\n\nהשעות הקרובות הפנויות:\n{alt_text}\n\nאשמח לקבוע לך באחת מהשעות האלה!"
        else:
            return f"מצטערת, השעה {time_str} ב-{date_str} תפוסה ואין תורים פנויים בימים הקרובים. אשמח אם תוכלי לנסות תאריך אחר."
        
    # Extract client email if present
    import re
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', contact_info)
    client_email = email_match.group(0) if email_match else None
    
    try:
        event_link = create_calendar_event(
            summary=f"{treatment_name} - {user_name}",
            start_time=start_dt,
            end_time=end_dt,
            description=f"טיפול: {treatment_name}\nלקוחה: {user_name}\nיצירת קשר: {contact_info}",
            attendee_email=client_email
        )
        
        msg = f"נקבע! {date_str} {time_str}. ✅"
        if client_email:
            msg += "\nInvite sent to your email! 📧"
        else:
            msg += "\n(No email provided for invite)"
            
        return msg

    except Exception as e:
        return f"Error booking appointment: {str(e)}"

