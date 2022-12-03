import asyncio
import os
from pyrogram import Client
import pyrogram.types
from loguru import logger
from pyrogram.types import Message

api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']
phone_number = os.environ['PNONE_NUMBER']

app = Client('user', api_id=api_id, api_hash=api_hash, phone_number=phone_number)
chats: dict[int] = {}


@app.on_message(pyrogram.filters.command('Djony') & pyrogram.filters.me)
def register_chat(_: Client, message: Message):
    emoji = message.text.split()[-1]
    chats[message.chat.id] = emoji
    logger.info(f"Added {message.chat.title} (id: {message.chat.id}) to allowed chats {emoji}")


@app.on_message(pyrogram.filters.command('Cancel') & pyrogram.filters.me)
def register_chat(_: Client, message: Message):
    chats.pop(message.chat.id)
    logger.info(f"Removed {message.chat.title} (id: {message.chat.id}) from allowed chats ")


@app.on_message()
async def main(client: Client, message: pyrogram.types.Message):
    try:
        logger.info(f"FOUND NEW MESSAGE - {message.chat.id} | {message.from_user.id}")
        await client.send_reaction(message_id=message.id, chat_id=message.chat.id,
                                   emoji=chats[message.chat.id])
    except KeyError:
        logger.error(f"Chat is not allowed | id: {message.chat.id}")
    except Exception as e:
        logger.exception(e)


app.run()
