"""
Configuration management for the RAG Cosmetic application.
Loads environment variables and validates required settings.
"""
import os
from typing import Optional

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, environment variables must be set manually
    pass


class Config:
    """Central configuration management."""
    
    @staticmethod
    def get_telegram_token() -> str:
        """Get Telegram bot token from environment."""
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError(
                "TELEGRAM_BOT_TOKEN not set. "
                "Please set it in your .env file or environment variables."
            )
        return token
    
    @staticmethod
    def get_openrouter_api_key() -> Optional[str]:
        """Get OpenRouter API key from environment."""
        return os.environ.get("OPENROUTER_API_KEY")
    
    @staticmethod
    def get_gemini_api_key() -> Optional[str]:
        """Get Gemini API key from environment."""
        return os.environ.get("GEMINI_API_KEY")
    
    @staticmethod
    def get_deepseek_api_key() -> Optional[str]:
        """Get DeepSeek API key from environment."""
        return os.environ.get("DEEPSEEK_API_KEY")

    @staticmethod
    def get_calendar_id() -> str:
        """Get Google Calendar ID from environment."""
        return os.environ.get("CALENDAR_ID", "primary")

    @staticmethod
    def get_calendar_ics_url() -> str:
        """Get Google Calendar private ICS URL from environment."""
        url = os.environ.get("CALENDAR_ICS_URL")
        if not url:
            # Fallback to the hardcoded one for backward compatibility if not set, 
            # but ideally it should be in env. 
            # For now, I'll return the one found in the code to avoid breaking if user hasn't set env yet.
            return "https://calendar.google.com/calendar/ical/titigimad1%40gmail.com/private-aa02a633d6633fa3b980bf5abe849eb0/basic.ics"
        return url

    @staticmethod
    def get_email_sender() -> Optional[str]:
        """Get email sender address from environment."""
        return os.environ.get("EMAIL_SENDER")

    @staticmethod
    def get_email_password() -> Optional[str]:
        """Get email app password from environment."""
        return os.environ.get("EMAIL_PASSWORD")

    @staticmethod
    def get_business_owner_email() -> Optional[str]:
        """Get business owner email from environment."""
        return os.environ.get("BUSINESS_OWNER_EMAIL")
    
    @staticmethod
    def get_business_owner_email() -> Optional[str]:
        """Get business owner email from environment."""
        return os.environ.get("BUSINESS_OWNER_EMAIL")

    @staticmethod
    def get_google_credentials_path() -> str:
        """Get path to Google Service Account JSON."""
        # Default to service_account.json in project root
        return os.environ.get("GOOGLE_CREDENTIALS_PATH", "service_account.json")

    @staticmethod
    def validate_required_keys():
        """Validate that all required API keys are set."""
        errors = []
        
        if not os.environ.get("TELEGRAM_BOT_TOKEN"):
            errors.append("TELEGRAM_BOT_TOKEN is required")
        
        if not os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("GEMINI_API_KEY") and not os.environ.get("DEEPSEEK_API_KEY"):
            errors.append("At least one of OPENROUTER_API_KEY, GEMINI_API_KEY, or DEEPSEEK_API_KEY must be set")
        
        if errors:
            error_msg = "\n".join(errors)
            raise ValueError(
                f"Missing required environment variables:\n{error_msg}\n\n"
                "Please copy .env.example to .env and fill in your API keys."
            )


# Validate on import
try:
    Config.validate_required_keys()
except ValueError as e:
    print(f"Configuration Error: {e}")
    # Don't raise here, let individual modules handle it
