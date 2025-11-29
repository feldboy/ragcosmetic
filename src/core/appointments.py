import requests
from icalendar import Calendar
from datetime import datetime, timedelta, date, time
import pytz
from typing import List, Dict
from src.utils.calendar_utils import generate_ics_file

from src.core.config import Config

# The private ICS link provided by the user
ICS_URL = Config.get_calendar_ics_url()

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
                    # Convert to local time (Asia/Jerusalem)
                    tz = pytz.timezone('Asia/Jerusalem')
                    if dtstart.tzinfo is None:
                        dtstart = tz.localize(dtstart)
                    else:
                        dtstart = dtstart.astimezone(tz)
                        
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
    Check available appointment slots for a given date using ICS feed.
    
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

    # Get booked slots from ICS
    booked_slots = get_booked_slots_from_ics(check_date)
    
    if "FULL_DAY" in booked_slots:
        return []
        
    available = []
    
    for slot in working_hours:
        if slot not in booked_slots:
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

def book_appointment(date_str: str, time_str: str, user_name: str, email: str, treatment_name: str = "ייעוץ קוסמטי") -> str:
    """
    Book an appointment by generating an ICS file.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format.
        time_str: Time in "HH:MM" format.
        user_name: Client name.
        email: Client email.
        treatment_name: Name of the treatment/service.
    
    Returns:
        Success message with CALENDAR: path or error with alternatives.
    """
    # Check availability first
    available_slots = check_availability(date_str)
    
    if time_str not in available_slots:
        # Find alternative slots
        alternatives = find_nearest_available_slots(date_str, time_str, 3)
        
        if alternatives:
            alt_text = "\n".join([f"  • {alt}" for alt in alternatives[:3]])
            return f"מצטערת, השעה {time_str} ב-{date_str} תפוסה. 😔\n\nהשעות הקרובות הפנויות:\n{alt_text}\n\nאשמח לקבוע לך באחת מהשעות האלה!"
        else:
            return f"מצטערת, השעה {time_str} ב-{date_str} תפוסה ואין תורים פנויים בימים הקרובים. אשמח אם תוכלי לנסות תאריך אחר."
        
    try:
        # Generate ICS file
        ics_path = generate_ics_file(
            date_str=date_str,
            time_str=time_str,
            user_name=user_name,
            email=email,
            duration_minutes=60, # Default 1 hour
            output_dir="data/calendar_invites" # Store in data directory
        )
        
        # Send confirmation email
        from src.utils.email_sender import EmailSender
        email_sender = EmailSender()
        
        details = f"טיפול: {treatment_name}\nתאריך: {date_str}\nשעה: {time_str}"
        email_sent = email_sender.send_appointment_confirmation(email, details, ics_path)
        
        msg = f"נקבע! {date_str} {time_str}. ✅\nשלחתי לך הזמנה ליומן.\nCALENDAR:{ics_path}"
        
        if email_sent:
            msg += "\nוגם שלחתי לך מייל אישור! 📧"
        else:
            # Don't show error to user if it's just a config issue, but log it (handled in EmailSender)
            pass
            
        # Notify the owner
        try:
            owner_email = Config.get_business_owner_email() or Config.get_email_sender()
            if owner_email:
                owner_details = f"לקוחה חדשה קבעה תור!\n\nשם: {user_name}\nאימייל: {email}\nטיפול: {treatment_name}\nתאריך: {date_str}\nשעה: {time_str}"
                email_sender.send_owner_notification(owner_email, owner_details, ics_path)
        except Exception as e:
            print(f"Failed to notify owner: {e}")

            
        return msg

    except Exception as e:
        return f"Error booking appointment: {str(e)}"


