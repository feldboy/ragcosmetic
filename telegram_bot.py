import os
import asyncio
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from agent import beauty_advisor_agent, BeautyAdvisorDependencies

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Store conversation history: chat_id -> List[Message]
# Note: In production, use a persistent database (Redis, Postgres).
# For this prototype, in-memory is fine, but it will be lost on restart.
conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    deps = BeautyAdvisorDependencies()
    
    # Reset history on /start
    conversations[chat_id] = []
    
    # Trigger the agent's welcome message
    trigger_msg = "הלקוחה הגיעה כרגע. התחילי את השיחה לפי ההוראות שלך."
    try:
        result = await beauty_advisor_agent.run(trigger_msg, deps=deps)
        conversations[chat_id].extend(result.new_messages())
        await send_response(context, chat_id, result.output)
    except Exception as e:
        logging.error(f"Error in start: {e}")
        await context.bot.send_message(chat_id=chat_id, text="סליחה, יש לי קצת בעיה להתעורר עכשיו. 😴")

async def send_response(context: ContextTypes.DEFAULT_TYPE, chat_id: int, response_text: str):
    """
    Parse the response and send text with images/calendar files if needed.
    Supports IMAGE:path and CALENDAR:path syntax in responses.
    """
    # Check for image markers
    image_pattern = r'IMAGE:([^\s]+)'
    images = re.findall(image_pattern, response_text)
    
    # Check for calendar markers
    calendar_pattern = r'CALENDAR:([^\s]+)'
    calendars = re.findall(calendar_pattern, response_text)
    
    # Remove markers from text
    clean_text = re.sub(image_pattern, '', response_text)
    clean_text = re.sub(calendar_pattern, '', clean_text).strip()
    
    # Send images first
    for image_path in images:
        if os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as photo:
                    await context.bot.send_photo(chat_id=chat_id, photo=photo)
            except Exception as e:
                logging.error(f"Error sending image {image_path}: {e}")
    
    # Send text message
    if clean_text:
        await context.bot.send_message(chat_id=chat_id, text=clean_text)
    
    # Send calendar files last
    for calendar_path in calendars:
        if os.path.exists(calendar_path):
            try:
                filename = os.path.basename(calendar_path)
                # Send file with HTML formatted caption that makes it clickable
                with open(calendar_path, 'rb') as calendar_file:
                    await context.bot.send_document(
                        chat_id=chat_id, 
                        document=calendar_file,
                        filename=filename,
                        caption="📅 הזמנה ליומן - לחצי להוסיף ליומן שלך!",
                        parse_mode='HTML'
                    )
            except Exception as e:
                logging.error(f"Error sending calendar {calendar_path}: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text
    deps = BeautyAdvisorDependencies()
    
    # Retrieve history
    if chat_id not in conversations:
        conversations[chat_id] = []
    history = conversations[chat_id]
    
    try:
        result = await beauty_advisor_agent.run(user_text, deps=deps, message_history=history)
        conversations[chat_id].extend(result.new_messages())
        await send_response(context, chat_id, result.output)
    except Exception as e:
        logging.error(f"Error in handle_message: {e}")
        await context.bot.send_message(chat_id=chat_id, text="אופס! משהו השתבש. בבקשה נסי שוב.")

if __name__ == '__main__':
    # Use the provided token or env var
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8501173127:AAFrxLECyhd8_yoHSEgQsnOIgaXLpl0RGso")
    
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set.")
        exit(1)
        
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("הבוט רץ...")
    application.run_polling()
