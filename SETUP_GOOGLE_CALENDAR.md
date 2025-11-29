# How to Setup Google Calendar API

To enable the bot to manage your calendar, you need to create a Google Cloud Project and generate a `credentials.json` file.

## Option A: The "I just want to test it" Path (Mock Calendar)
If you don't want to go through the Google setup right now, I can switch the bot to use a **Mock Calendar**. This requires **zero setup** and works immediately for testing.
**Just tell me: "Switch to mock calendar"**

## Option B: The Real Deal (Google Calendar Setup)

### 1. Create a Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown (top left) and select **"New Project"**.
3. Name it `BeautyAdvisorBot` and click **Create**.

### 2. Enable the API
1. In the sidebar, go to **APIs & Services** > **Library**.
2. Search for **"Google Calendar API"**.
3. Click on it and click **Enable**.

### 3. Configure Consent Screen
1. Go to **APIs & Services** > **OAuth consent screen**.
2. Select **External** and click **Create**.
3. Fill in:
   - **App name**: BeautyAdvisor
   - **User support email**: Your email
   - **Developer contact information**: Your email
4. Click **Save and Continue** (you can skip Scopes).
5. Under **Test users**, click **Add Users** and add your own email address. (Crucial!)
6. Click **Save and Continue**.

### 4. Create Credentials
1. Go to **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **OAuth client ID**.
3. Application type: **Desktop app**.
4. Name: `Desktop Client`.
5. Click **Create**.

### 5. Download & Move File
1. You'll see a popup with "OAuth client created".
2. Click the **Download JSON** button (icon with a down arrow).
3. Rename the downloaded file to `credentials.json`.
4. Move this file to your project folder:
   `/Users/yaronfeldboy/Documents/ragcosmetic/credentials.json`

### 6. Authenticate
1. Run the setup script in your terminal:
   ```bash
   python3 setup_google_calendar.py
   ```
2. Follow the link in the terminal to log in with your Google account.

Once done, let me know!
