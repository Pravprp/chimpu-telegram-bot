import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

def ask_ai(message):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://chimpu.bot",
        "X-Title": "Chimpu Telegram Bot"
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

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        result = response.json()

        # Print full response to Railway logs for debugging
        print("OpenRouter Response:", result)

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        # If OpenRouter returns an error
        if "error" in result:
            print("OpenRouter Error:", result["error"])
            return "Chimpu's joke engine broke for a second 🤖"

        return "Chimpu is thinking too hard 🤔"

    except Exception as e:
        print("Request failed:", str(e))
        return "Chimpu tripped over a banana peel 🍌"


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is None or update.message.text is None:
        return

    user_message = update.message.text

    ai_reply = ask_ai(user_message)

    await update.message.reply_text(ai_reply)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

print("Chimpu is online 😄")

app.run_polling()
