import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# A list of 5 reliable, free AI models to cycle through
MODELS = [
    "qwen/qwen3-coder:free",
    "qwen/qwen3-next-80b-a3b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    "stepfun/step-3.5-flash:free",
    "nvidia/nemotron-3-super-120b-a12b:free"
]

def ask_ai(message):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Loop through our list of models one by one
    for model_name in MODELS:
        data = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": """
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
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()

            # If the response is good, return the text immediately
            if response.status_code == 200 and "choices" in response_json:
                return response_json["choices"][0]["message"]["content"]
            else:
                # If this specific model fails, print the error but let the loop try the next one
                print(f"Skipping {model_name} due to error: {response_json}")
                
        except Exception as e:
            # Catch internet connection issues so the bot doesn't crash
            print(f"Connection error with {model_name}: {e}")

    # If the loop finishes and all 5 models failed
    print("CRITICAL: All 5 fallback models failed!")
    return None


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    ai_reply = ask_ai(user_message)

    # Only send a message to Telegram IF the AI successfully replied
    if ai_reply:
        await update.message.reply_text(ai_reply)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

print("Chimpu is online 😄")

app.run_polling()
