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
    def get_deepseek_api_key() -> Optional[str]:
        """Get DeepSeek API key from environment."""
        return os.environ.get("DEEPSEEK_API_KEY")
    
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
