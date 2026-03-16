import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "8756612174:AAE2YBkpMe9tvhvEULzNaQnDYsSGEGNMsf0"
OPENROUTER_API_KEY = "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"

def ask_ai(message):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/hunter-alpha",
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

    return response.json()["choices"][0]["message"]["content"]


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    ai_reply = ask_ai(user_message)

    await update.message.reply_text(ai_reply)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

print("Chimpu is online 😄")

app.run_polling()