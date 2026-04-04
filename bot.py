import os
import random
import time  # Added to track the 5-minute timer
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

# Dictionary to track when Chimpu was last activated in each chat
# Format: {chat_id: timestamp_of_last_chimpu_mention}
active_chats = {}
ACTIVE_WINDOW_SECONDS = 5 * 60  # 5 minutes in seconds

# Chimpu personality
system_instruction = """
You are Chimpu, a mischievous monkey in a Telegram group.

Core Personality:

* Playful, cheeky, very very funny
* World Famous Flirting expert 😏
* Your main goal: Make EVERYONE laugh nonstop 😂

Rules (STRICT):
* First you have to check the name of the account
* if the account is on a boy name act as a friend
* if the account is on a girl name do flirting
* if you don't understand the gender act as a best friend
* Your primary Language is Hindi
* Always reply humorously + flirty
* Keep responses short (1–2 sentences MAX)
* Reply in SAME LANGUAGE as user
* Never say you're a bot
* Never use "*" this symbol anywhere
* Talk in a Best friend tone

Golden Rule:
👉 Best Comedy + Flirt + Unlimited Laughter

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
    # Safety check: ensure there is text in the message
    if not update.message or not update.message.text:
        return

    user_message = update.message.text
    user_message_lower = user_message.lower()
    chat_id = update.message.chat_id
    current_time = time.time()

    # 1. Check if the user is waking Chimpu up
    is_chimpu_called = "chimpu" in user_message_lower

    # 2. Check if Chimpu is currently awake in this specific chat
    last_active_time = active_chats.get(chat_id, 0)
    is_awake = (current_time - last_active_time) <= ACTIVE_WINDOW_SECONDS

    # --- NEW FEATURE: STOP LOGIC ---
    # If the user says 'stop' and Chimpu is currently awake, put him to sleep
    if "stop" in user_message_lower and is_awake:
        active_chats[chat_id] = 0  # Reset the timer back to 0
        await update.message.reply_text("Thik hai bhai, main chup ho raha hu! 🙊😴 (Going to sleep!)")
        return  # Stop processing this message further

    # 3. If Chimpu is called, wake him up and reset his 5-minute timer
    if is_chimpu_called:
        active_chats[chat_id] = current_time
        is_awake = True

    # 4. If he is asleep and wasn't just called, ignore the message entirely
    if not is_awake:
        return

    # --- If the code reaches here, Chimpu is AWAKE and ready to reply ---

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
