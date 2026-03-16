import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_ai(message):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """
You are Chimpu, a funny Telegram group bot.

Rules:
- Always reply humorously
- Keep responses short (1-2 sentences)
- Reply in the EXACT SAME LANGUAGE as the user's message
- If the user writes in English, reply in English
- If the user writes in Spanish, reply in Spanish
- Never switch languages
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    # Safety check: Catch errors instead of crashing
    if "choices" in response_json:
        return response_json["choices"][0]["message"]["content"]
    else:
        print(f"OPENROUTER ERROR: {response_json}")
        return "Oops! My brain stopped working for a second. Check the logs!"


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    ai_reply = ask_ai(user_message)

    await update.message.reply_text(ai_reply)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

print("Chimpu is online 😄")

app.run_polling()
