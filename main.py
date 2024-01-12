from discord.ext import commands
import discord as ds
import json
import tokens
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


intents = ds.Intents.all()
bot = commands.Bot(command_prefix="$$", intents=intents)

with open("synced.json", "r") as f:
    synced: list = json.load(f)

def save_dict():
    with open("synced.json", "w") as f:
        json.dump(synced, f, indent=2)


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

async def sync(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = get_current_message_content(update)

    try:
        command, id = text.split(" ")
    except:
        await send_message("Please send /sync [id]", update, context)
        return

    try:
        id = int(id)
    except:
        await send_message("Is not an id!", update, context)
        return
    
    current_id = get_current_channel_id(update)

    temp = {
        str(id): str(current_id),
        str(current_id): str(id) 
    }

    synced.append(temp)
    save_dict()

    await send_message("Succesfuly synced with [nom du channel discord]")

@bot.event
async def on_ready():

    application = ApplicationBuilder().token(tokens.telegram()).build()

    start_handler = CommandHandler('sync', sync)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == '__main__':
    bot.run(tokens.discord())