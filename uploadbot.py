from pyrogram import Client , filters
from pyrogram.types import Message
import os

bot = Client(
    "bot",
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    bot_token=os.environ['BTOKEN']
)

CHANNEL_ID = -1001797893141
BOT_USERNAME = "dynastyanimeuploaderbot" #WITOUT @

@bot.on_message(filters.document & filters.user([2114972069, 5704299476, 6713194639]))
def main(_,m : Message):
    x = bot.send_document(CHANNEL_ID,m.document.file_id)
    msg_id = x.id
    m.reply(f"https://t.me/{BOT_USERNAME}?start={msg_id}")

@bot.on_message(filters.command("start"))
def start(_,m : Message):
    if len(m.text.split(" ")) == 2:
        msg_id = m.text.split(" ")[1]
        msg_id = int(msg_id)
        doc = bot.get_messages(CHANNEL_ID , msg_id)
        doc.copy(m.chat.id)
    else:
        m.reply("Hello there, only admins can use me")


bot.run()
