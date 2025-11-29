import os.path
import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.core.config import Config

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendarManager:
    def __init__(self):
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Google Calendar API using Service Account."""
        creds_path = Config.get_google_credentials_path()

        if not os.path.exists(creds_path):
            print(f"Service Account file not found at: {creds_path}")
            self.creds = None
            return

        try:
            self.creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
            self.service = build("calendar", "v3", credentials=self.creds)
        except Exception as e:
            print(f"Error authenticating with Service Account: {e}")
            self.creds = None
            self.service = None

    def list_events(self, start_time: datetime.datetime, end_time: datetime.datetime, calendar_id='primary'):
        """
        List events within a time range.
        
        Args:
            start_time: Start datetime (timezone aware)
            end_time: End datetime (timezone aware)
            calendar_id: Calendar ID (default: 'primary')
            
        Returns:
            List of events
        """
        if not self.service:
            return []

        try:
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=start_time.isoformat(),
                timeMax=end_time.isoformat(),
                singleEvents=True,
                orderBy="startTime"
            ).execute()
            events = events_result.get("items", [])
            return events
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def create_event(self, summary: str, start_time: datetime.datetime, end_time: datetime.datetime, 
                     attendee_email: str = None, description: str = "", calendar_id='primary'):
        """
        Create a new event in the calendar.
        
        Args:
            summary: Event title
            start_time: Start datetime
            end_time: End datetime
            attendee_email: Optional email to invite
            description: Event description
            calendar_id: Calendar ID (default: 'primary')
            
        Returns:
            Created event object or None
        """
        if not self.service:
            return None

        event = {
            "summary": summary,
            "description": description,
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "Asia/Jerusalem",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "Asia/Jerusalem",
            },
        }
        
        if attendee_email:
            event["attendees"] = [{"email": attendee_email}]

        try:
            event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"Event created: {event.get('htmlLink')}")
            return event
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
