import os
import smtplib
from dotenv import load_dotenv

def check_email_config():
    print("Loading .env file...")
    load_dotenv()
    
    email = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")
    
    print(f"EMAIL_SENDER: {'[SET]' if email else '[MISSING]'}")
    if email:
        print(f"Value: {email}")
        
    print(f"EMAIL_PASSWORD: {'[SET]' if password else '[MISSING]'}")
    
    if password:
        # Check format
        clean_pass = password.replace(" ", "")
        print(f"Password length (ignoring spaces): {len(clean_pass)}")
        if len(clean_pass) != 16:
            print("WARNING: Google App Passwords are usually 16 characters long.")
        else:
            print("Format looks correct for an App Password (16 chars).")
            
        # Try connection
        print("\nAttempting SMTP login...")
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(email, password)
            print("SUCCESS: Login successful! Credentials are valid.")
            server.quit()
        except Exception as e:
            print(f"FAILURE: Login failed.\nError: {e}")
            print("\nTroubleshooting tips:")
            print("1. Ensure you are using an 'App Password', NOT your regular Gmail password.")
            print("2. Check if 2-Step Verification is enabled (required for App Passwords).")
            print("3. Verify there are no extra spaces or quotes in the .env file.")

if __name__ == "__main__":
    check_email_config()
