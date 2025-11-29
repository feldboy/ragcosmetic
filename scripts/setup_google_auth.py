import os.path
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from src.core.config import Config

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    """Shows basic usage of the Google Calendar API."""
    creds = None
    token_path = Config.get_google_token_path()
    creds_path = Config.get_google_credentials_path()
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting new authentication flow...")
            if not os.path.exists(creds_path):
                print(f"ERROR: Could not find credentials file at {creds_path}")
                print("Please ensure you have downloaded the OAuth 2.0 Client ID JSON from Google Cloud Console")
                print("and saved it as 'credentials.json' in the project root.")
                return

            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            # Manual flow with localhost redirect (workaround for OOB deprecation)
            # 1. Generate URL with localhost redirect
            flow.redirect_uri = 'http://localhost'
            auth_url, _ = flow.authorization_url(prompt='consent')

            print("Please visit this URL to authorize this application:")
            print(auth_url)
            print("\nINSTRUCTIONS FOR FRIEND:")
            print("1. Open the link and authorize.")
            print("2. The browser will try to load a page starting with 'http://localhost' and FAIL.")
            print("3. THIS IS NORMAL! Copy the FULL URL from the address bar (it contains the code).")
            print("4. Send that full URL to me.")
            
            # 2. Get URL/code from user
            response = input("\nPaste the full redirect URL (or just the code): ")
            
            # Extract code if full URL is pasted
            if "code=" in response:
                code = response.split("code=")[1].split("&")[0]
            else:
                code = response
            
            # 3. Fetch token
            flow.fetch_token(code=code)
            creds = flow.credentials
            
        # Save the credentials for the next run
        print(f"Saving token to {token_path}...")
        with open(token_path, "w") as token:
            token.write(creds.to_json())
            
    print("Authentication successful! You can now run the bot.")

if __name__ == "__main__":
    main()
