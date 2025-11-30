import os
from dotenv import load_dotenv

print("Loading .env file...")
load_dotenv()

print("\n=== Checking API Keys ===")
deepseek = os.environ.get("DEEPSEEK_API_KEY")
gemini = os.environ.get("GEMINI_API_KEY")
openrouter = os.environ.get("OPENROUTER_API_KEY")
telegram = os.environ.get("TELEGRAM_BOT_TOKEN")

print(f"DEEPSEEK_API_KEY: {'✅ Present' if deepseek else '❌ Missing'}")
if deepseek:
    print(f"  Length: {len(deepseek)} characters")
    print(f"  Starts with: {deepseek[:10]}...")
    
print(f"GEMINI_API_KEY: {'✅ Present' if gemini else '❌ Missing'}")
if gemini:
    print(f"  Length: {len(gemini)} characters")
    
print(f"OPENROUTER_API_KEY: {'✅ Present' if openrouter else '❌ Missing'}")
if openrouter:
    print(f"  Length: {len(openrouter)} characters")
    
print(f"TELEGRAM_BOT_TOKEN: {'✅ Present' if telegram else '❌ Missing'}")
if telegram:
    print(f"  Length: {len(telegram)} characters")

print("\n=== Diagnosis ===")
if not (deepseek or gemini or openrouter):
    print("❌ No LLM API key found!")
    print("Please check your .env file format:")
    print("  - No spaces around =")
    print("  - No quotes needed")
    print("  - Example: DEEPSEEK_API_KEY=sk-xxxxx")
elif not telegram:
    print("❌ Telegram token missing!")
else:
    print("✅ Configuration looks good!")
