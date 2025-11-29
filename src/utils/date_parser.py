from datetime import datetime, timedelta
from typing import Optional, Tuple
import dateparser
from dateutil.parser import parse as dateutil_parse
import re


def parse_datetime(text: str, reference_time: Optional[datetime] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse natural language date/time text in Hebrew or English.
    
    Args:
        text: Natural language text like "מחר בשעה 3", "tomorrow at 3pm", "ביום חמישי ב-14:00"
        reference_time: Reference datetime for relative dates (defaults to now)
    
    Returns:
        Tuple of (date_str, time_str) in formats ("YYYY-MM-DD", "HH:MM")
        Returns (None, None) if parsing fails
    
    Examples:
        >>> parse_datetime("מחר בשעה 3")
        ("2025-11-30", "15:00")
        
        >>> parse_datetime("tomorrow at 10am")
        ("2025-11-30", "10:00")
        
        >>> parse_datetime("ביום חמישי ב-14:00")
        ("2025-12-05", "14:00")
    """
    if reference_time is None:
        reference_time = datetime.now()
    
    # Try to parse with dateparser (supports Hebrew and many languages)
    settings = {
        'PREFER_DATES_FROM': 'future',  # Always prefer future dates
        'RELATIVE_BASE': reference_time,
        'RETURN_AS_TIMEZONE_AWARE': False,
        'TIMEZONE': 'Asia/Jerusalem'
    }
    
    # Parse the full text
    parsed_dt = dateparser.parse(text, languages=['he', 'en'], settings=settings)
    
    if not parsed_dt:
        # Try a more aggressive approach - extract any numbers and keywords
        return _fallback_parse(text, reference_time)
    
    # Extract date and time
    date_str = parsed_dt.strftime("%Y-%m-%d")
    time_str = parsed_dt.strftime("%H:%M")
    
    # Always try to extract time manually if there are time keywords or numbers
    # This gives us better control over 12-hour format handling
    time_match = re.search(r'(\d{1,2}):?(\d{2})?', text)
    if time_match and _has_time_component(text):
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        
        # Handle 12-hour format
        if 'אחה"צ' in text or 'אחרי הצהריים' in text or 'pm' in text.lower():
            if hour < 12:
                hour += 12
        elif 'בבוקר' in text or 'לפנה"צ' in text or 'am' in text.lower():
            if hour == 12:
                hour = 0
        elif hour <= 9:  # Assume afternoon/business hours if single digit without AM/PM
            # Common assumption: 1-9 without specification = afternoon (13:00-21:00)
            if not ('בבוקר' in text or 'לפנה"צ' in text or 'am' in text.lower()):
                hour += 12
        
        time_str = f"{hour:02d}:{minute:02d}"
    elif not _has_time_component(text):
        # No time specified at all
        time_str = None
    
    return (date_str, time_str)


def _has_time_component(text: str) -> bool:
    """Check if text contains a time component."""
    time_keywords = [
        'שעה', 'בשעה', 'ב-', 'at', 'am', 'pm',
        'בוקר', 'צהריים', 'ערב', 'לילה',
        'morning', 'afternoon', 'evening', 'night'
    ]
    
    # Check for explicit time patterns (HH:MM or just numbers)
    if re.search(r'\d{1,2}:\d{2}', text):
        return True
    
    # Check for time keywords
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in time_keywords)


def _fallback_parse(text: str, reference_time: datetime) -> Tuple[Optional[str], Optional[str]]:
    """
    Fallback parser for cases where dateparser fails.
    Handles common Hebrew patterns manually.
    """
    text_lower = text.lower()
    
    # Map Hebrew day names to numbers (0=Monday, 6=Sunday)
    hebrew_days = {
        'ראשון': 6,
        'שני': 0,
        'שלישי': 1,
        'רביעי': 2,
        'חמישי': 3,
        'שישי': 4,
        'שבת': 5,
    }
    
    # Map English day names to numbers (0=Monday, 6=Sunday)
    english_days = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }
    
    # Handle "tomorrow" / "מחר"
    if 'מחר' in text_lower or 'tomorrow' in text_lower:
        target_date = reference_time + timedelta(days=1)
    # Handle "today" / "היום"
    elif 'היום' in text_lower or 'today' in text_lower:
        target_date = reference_time
    # Handle specific day names
    else:
        target_date = None
        # Check Hebrew days
        for day_name, day_num in hebrew_days.items():
            if day_name in text_lower:
                # Calculate next occurrence of this day
                days_ahead = day_num - reference_time.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                target_date = reference_time + timedelta(days=days_ahead)
                break
        
        # Check English days if not found
        if not target_date:
            for day_name, day_num in english_days.items():
                if day_name in text_lower:
                    # Calculate next occurrence of this day
                    days_ahead = day_num - reference_time.weekday()
                    if days_ahead <= 0:  # Target day already happened this week
                        days_ahead += 7
                    target_date = reference_time + timedelta(days=days_ahead)
                    break
    
    if not target_date:
        return (None, None)
    
    date_str = target_date.strftime("%Y-%m-%d")
    
    # Extract time
    time_match = re.search(r'(\d{1,2}):?(\d{2})?', text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2)) if time_match.group(2) else 0
        
        # Handle 12-hour format
        if 'אחה"צ' in text or 'אחרי הצהריים' in text or 'pm' in text_lower:
            if hour < 12:
                hour += 12
        elif hour <= 9:  # Assume afternoon if hour is small without AM/PM
            # Common assumption: 1-9 without specification = afternoon
            if not ('בבוקר' in text or 'לפנה"צ' in text or 'am' in text_lower):
                hour += 12
        
        time_str = f"{hour:02d}:{minute:02d}"
    else:
        time_str = None
    
    return (date_str, time_str)


def parse_date_only(text: str, reference_time: Optional[datetime] = None) -> Optional[str]:
    """
    Parse only the date part from natural language text.
    
    Returns:
        Date string in "YYYY-MM-DD" format or None
    """
    date_str, _ = parse_datetime(text, reference_time)
    return date_str


def parse_time_only(text: str) -> Optional[str]:
    """
    Parse only the time part from natural language text.
    
    Returns:
        Time string in "HH:MM" format or None
    """
    # Look for time patterns
    time_match = re.search(r'(\d{1,2}):?(\d{2})?', text)
    if not time_match:
        return None
    
    hour = int(time_match.group(1))
    minute = int(time_match.group(2)) if time_match.group(2) else 0
    
    text_lower = text.lower()
    
    # Handle 12-hour format
    if 'אחה"צ' in text or 'אחרי הצהריים' in text or 'pm' in text_lower:
        if hour < 12:
            hour += 12
    elif 'בבוקר' in text or 'לפנה"צ' in text or 'am' in text_lower:
        if hour == 12:
            hour = 0
    elif hour <= 9:  # Assume afternoon if hour is small without AM/PM
        hour += 12
    
    return f"{hour:02d}:{minute:02d}"
