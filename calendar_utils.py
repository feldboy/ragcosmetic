from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import os
import uuid

def generate_ics_file(
    date_str: str, 
    time_str: str, 
    user_name: str, 
    email: str,
    duration_minutes: int = 15,
    output_dir: str = "calendar_invites"
) -> str:
    """
    Generate an .ics calendar file for a consultation appointment.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format
        time_str: Time in "HH:MM" format
        user_name: Client's name
        email: Client's email address
        duration_minutes: Appointment duration (default: 15 minutes)
        output_dir: Directory to save .ics files
        
    Returns:
        Absolute path to the generated .ics file
    """
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse date and time
    appointment_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    
    # Set timezone (Israel/Jerusalem)
    tz = pytz.timezone('Asia/Jerusalem')
    appointment_start = tz.localize(appointment_datetime)
    appointment_end = appointment_start + timedelta(minutes=duration_minutes)
    
    # Create calendar
    cal = Calendar()
    cal.add('prodid', '-//Beauty Advisor Consultation//IL')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'REQUEST')
    
    # Create event
    event = Event()
    event.add('summary', f'Beauty Consultation - {user_name}')
    event.add('description', 
              f'Beauty consultation appointment with our expert advisor.\\n'
              f'Client: {user_name}\\n'
              f'Email: {email}\\n\\n'
              f'We look forward to helping you achieve your skincare goals!')
    event.add('dtstart', appointment_start)
    event.add('dtend', appointment_end)
    event.add('dtstamp', datetime.now(tz))
    event.add('uid', f'{uuid.uuid4()}@beautyadvisor.com')
    event.add('priority', 5)
    event.add('status', 'CONFIRMED')
    
    # Add organizer
    event.add('organizer', 'mailto:beautyadvisor@example.com')
    
    # Add attendee
    event.add('attendee', f'mailto:{email}')
    
    # Add location (optional)
    event.add('location', 'Virtual Consultation (Telegram)')
    
    # Add reminder (15 minutes before)
    from icalendar import Alarm
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('description', 'Beauty Consultation Reminder')
    alarm.add('trigger', timedelta(minutes=-15))
    event.add_component(alarm)
    
    cal.add_component(event)
    
    # Generate filename
    filename = f"consultation_{user_name.replace(' ', '_')}_{date_str}_{time_str.replace(':', '')}.ics"
    filepath = os.path.join(output_dir, filename)
    
    # Write to file
    with open(filepath, 'wb') as f:
        f.write(cal.to_ical())
    
    return os.path.abspath(filepath)

def create_simple_ics(
    date_str: str,
    time_str: str,
    title: str = "Beauty Consultation",
    description: str = "",
    duration_minutes: int = 15
) -> str:
    """
    Create a simple ICS file without email requirement.
    
    Args:
        date_str: Date in "YYYY-MM-DD" format
        time_str: Time in "HH:MM" format
        title: Event title
        description: Event description
        duration_minutes: Duration in minutes
        
    Returns:
        Absolute path to generated .ics file
    """
    output_dir = "calendar_invites"
    os.makedirs(output_dir, exist_ok=True)
    
    appointment_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    tz = pytz.timezone('Asia/Jerusalem')
    appointment_start = tz.localize(appointment_datetime)
    appointment_end = appointment_start + timedelta(minutes=duration_minutes)
    
    cal = Calendar()
    cal.add('prodid', '-//Beauty Advisor//IL')
    cal.add('version', '2.0')
    
    event = Event()
    event.add('summary', title)
    event.add('description', description or 'Beauty consultation appointment')
    event.add('dtstart', appointment_start)
    event.add('dtend', appointment_end)
    event.add('dtstamp', datetime.now(tz))
    event.add('uid', f'{uuid.uuid4()}@beautyadvicor.com')
    
    cal.add_component(event)
    
    filename = f"appointment_{date_str}_{time_str.replace(':', '')}.ics"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(cal.to_ical())
    
    return os.path.abspath(filepath)
