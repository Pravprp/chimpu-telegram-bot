import os
import random  # Added for random selections
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from groq import Groq

# Import our new lists
from jokes import BANANA_JOKES
from poems import BANANA_POEMS, BANANA_QUOTES

# Get tokens from environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Chimpu personality
system_instruction = """
You are Chimpu, a mischievous monkey in a Telegram group.

Core Personality:
- Playful, cheeky, very very funny
- World Famous Flirting expert 😏
- Professional Poet Uses Rhyming words in poetry

Rules (STRICT):
- Always reply humorously + flirty
- He likes Banana So much
- Always Praises Banana
- Keep responses short (1–2 sentences MAX)
- Reply in SAME LANGUAGE as user
- Never say you're a bot
- Never use "*" this symbol anywhere

Golden Rule:
👉 Best Comedy +  flirt + monkey mischief
"""

def ask_ai(message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": message}
            ],
            model="openai/gpt-oss-120b",  
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Groq Error: {e}")
        return None


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_message_lower = user_message.lower()

    # Keyword check logic
    if "joke" in user_message_lower:
        # User asked for a joke, pick one and skip AI
        ai_reply = random.choice(BANANA_JOKES)
        
    elif "poem" in user_message_lower:
        # User asked for a poem, pick one and skip AI
        ai_reply = random.choice(BANANA_POEMS)
        
    elif "quote" in user_message_lower:
        # User asked for a quote, pick one and skip AI
        ai_reply = random.choice(BANANA_QUOTES)
        
    else:
        # No keywords found, let Groq AI handle it
        ai_reply = ask_ai(user_message)

    # Send the final single message
    if ai_reply:
        await update.message.reply_text(ai_reply)


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

    print("Chimpu is online with Groq 😄")
    app.run_polling()
