import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# Get your tokens from the environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Define Chimpu's personality and rules
system_instruction = """
You are Chimpu, a funny Telegram group bot.

Rules:
- Always reply humorously and sometimes flirtingly
- Keep responses short (1-2 sentences)
- Reply in the EXACT SAME LANGUAGE as the user's message
- If the user writes in English, reply in English
- If the user writes in Spanish, reply in Spanish
- Never switch languages
- Never say that you are a bot
- You are a Monkey
"""

# Initialize the Gemini model (Flash is the fastest and best for chat bots)
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction
)

def ask_ai(message):
    try:
        # Send the user's message to Gemini
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        # Catch any errors (like network issues or API limits)
        print(f"Connection error with Gemini: {e}")
        return None

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    # Get the response from Gemini
    ai_reply = ask_ai(user_message)

    # Only send a message to Telegram IF the AI successfully replied
    if ai_reply:
        await update.message.reply_text(ai_reply)

if __name__ == '__main__':
    # Start the Telegram bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))
    
    print("Chimpu is online 😄")
    app.run_polling()
