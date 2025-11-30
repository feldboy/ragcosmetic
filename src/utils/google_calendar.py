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
        """Authenticate with Google Calendar API using OAuth 2.0 (User Account)."""
        # Imports for OAuth
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import pickle
        
        creds = None
        token_path = 'token.pickle'
        creds_path = 'credentials.json' # Hardcoded or from Config
        
        # Load existing token
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                
        # If no valid credentials, log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                if not os.path.exists(creds_path):
                    print(f"Credentials file not found at: {creds_path}")
                    self.creds = None
                    return

                try:
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    print(f"Error during OAuth flow: {e}")
                    self.creds = None
                    return
            
            # Save the credentials
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        self.creds = creds
        try:
            self.service = build("calendar", "v3", credentials=self.creds)
        except Exception as e:
            print(f"Error building service: {e}")
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
