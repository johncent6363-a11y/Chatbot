import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from google import genai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

gemini_client = genai.Client(
    api_key=GEMINI_KEY
)
user_chats = {}

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    user_chats[user_id] = gemini_client.chats.create(
        model="gemini-2.5-flash"
    )
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hey {name}! I'm live from the cloud 24/7! 🚀"
    )

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    if user_id not in user_chats:
        user_chats[user_id] = gemini_client.chats.create(
            model="gemini-2.5-flash"
        )
    
    try:
        text = update.message.text
        response = user_chats[user_id].send_message(text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .build()
    )
    app.add_handler(
        CommandHandler("start", start_command)
    )
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )
    app.run_polling()


