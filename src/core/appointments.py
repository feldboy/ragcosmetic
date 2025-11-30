import datetime
from datetime import timedelta
import pytz
from typing import List
from src.utils.google_calendar import GoogleCalendarManager

# Initialize calendar manager
calendar_manager = GoogleCalendarManager()

def check_availability(date_str: str) -> List[str]:
    """
    Check available appointment slots for a given date using Google Calendar API.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format.
        
    Returns:
        List of available time slots in "HH:MM" format.
    """
    # Define working hours (10:00 to 18:00)
    working_hours = [f"{h:02d}:00" for h in range(10, 19)]
    
    try:
        check_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return ["Error: Invalid date format."]

    available = []
    tz = pytz.timezone('Asia/Jerusalem')
    
    for slot in working_hours:
        # Construct datetime for this slot
        slot_dt_str = f"{date_str} {slot}"
        slot_start = datetime.datetime.strptime(slot_dt_str, "%Y-%m-%d %H:%M")
        slot_start = tz.localize(slot_start)
        slot_end = slot_start + timedelta(minutes=60) # Assume 1 hour slots
        
        # Check if this specific slot is free
        events = calendar_manager.list_events(slot_start, slot_end)
        if not events:
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
        requested_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
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

def book_appointment(date_str: str, time_str: str, user_name: str, email: str, treatment_name: str = "ייעוץ קוסמטי") -> str:
    """
    Book an appointment directly on Google Calendar.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format.
        time_str: Time in "HH:MM" format.
        user_name: Client name.
        email: Client email.
        treatment_name: Name of the treatment/service.
    
    Returns:
        Success message with link to event.
    """
    # Parse datetime
    try:
        dt_str = f"{date_str} {time_str}"
        start_dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        tz = pytz.timezone('Asia/Jerusalem')
        start_dt = tz.localize(start_dt)
        end_dt = start_dt + timedelta(minutes=60) # 1 hour appointment
    except ValueError:
        return f"Error: Invalid date/time format."

    # Double check availability
    events = calendar_manager.list_events(start_dt, end_dt)
    if events:
        # Find alternative slots
        alternatives = find_nearest_available_slots(date_str, time_str, 3)
        
        if alternatives:
            alt_text = "\n".join([f"  • {alt}" for alt in alternatives[:3]])
            return f"מצטערת, השעה {time_str} ב-{date_str} תפוסה. 😔\n\nהשעות הקרובות הפנויות:\n{alt_text}\n\nאשמח לקבוע לך באחת מהשעות האלה!"
        else:
            return f"מצטערת, השעה {time_str} ב-{date_str} תפוסה ואין תורים פנויים בימים הקרובים. אשמח אם תוכלי לנסות תאריך אחר."
        
    try:
        event = calendar_manager.create_event(
            summary=f"{treatment_name} - {user_name}",
            start_time=start_dt,
            end_time=end_dt,
            description=f"טיפול: {treatment_name}\nלקוחה: {user_name}\nאימייל: {email}",
            attendee_email=email
        )
        
        if event:
            event_link = event.get('htmlLink')
            msg = f"נקבע! {date_str} {time_str}. ✅"
            if email:
                msg += "\nInvite sent to your email! 📧"
            else:
                msg += "\n(No email provided for invite)"
            return msg
        else:
            return "Error: Failed to create calendar event."

    except Exception as e:
        return f"Error booking appointment: {str(e)}"
