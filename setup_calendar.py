import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.utils.google_calendar import GoogleCalendarManager

def setup():
    print("📅 Setting up Google Calendar Integration...")
    print("="*50)
    
    if not os.path.exists('credentials.json'):
        print("❌ Error: 'credentials.json' not found!")
        print("Please download your OAuth 2.0 Client ID JSON from Google Cloud Console")
        print("and save it as 'credentials.json' in this folder.")
        return

    print("Requesting access... A browser window should open.")
    
    try:
        manager = GoogleCalendarManager()
        if manager.service:
            print("\n✅ Authentication successful!")
            print("Token saved to 'token.pickle'")
            
            # Verify by listing events
            print("\nVerifying connection by listing upcoming events...")
            import datetime
            now = datetime.datetime.now(datetime.timezone.utc)
            end = now + datetime.timedelta(days=7)
            events = manager.list_events(now, end)
            
            if events:
                print(f"Found {len(events)} upcoming events:")
                for event in events[:3]:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(f"- {start}: {event.get('summary', 'No Title')}")
            else:
                print("No upcoming events found (but connection is working).")
                
        else:
            print("\n❌ Authentication failed.")
            
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")

if __name__ == "__main__":
    setup()
