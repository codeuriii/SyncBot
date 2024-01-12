from discord.ext import commands
import discord as ds
import tokens
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def send_message(msg: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=get_current_channel_id(update), text=msg)
def get_current_user_name(update: Update):
    return update.effective_user.name
def get_current_user_id(update: Update):
    return update.effective_user.id
def get_current_message_content(update: Update):
    return update.effective_message.text
def get_current_message_id(update: Update):
    return update.effective_message.id
def get_current_channel_name(update: Update):
    return update.effective_chat.full_name
def get_current_channel_id(update: Update):
    return update.effective_chat.id
async def send_file(filepath: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(chat_id=get_current_channel_id(update), document=filepath)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def sync(test: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(test, update, context)

if __name__ == '__main__':
    application = ApplicationBuilder().token(tokens.telegram()).build()
    
    start_handler = CommandHandler('sync', sync)
    application.add_handler(start_handler)
    
    application.run_polling()