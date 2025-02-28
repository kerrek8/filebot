import os
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from dotenv import load_dotenv
from fastapi import FastAPI
from aiogram.fsm.storage.memory import MemoryStorage

from db.base import create_tables
from misk.commands import set_bot_commands
from handlers import start

load_dotenv()

bot = Bot(os.getenv("TOKEN"))

webhook_uri = 'https://filebot-snif.onrender.com' + '/' + str(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
dp.include_routers(start.router)


async def start():
    await set_bot_commands(bot)
    await create_tables()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start()
    print(await bot.set_webhook(url=webhook_uri, allowed_updates=[]), 'webhook was set')
    yield


app = FastAPI(docs_url=None, lifespan=lifespan)


@app.post('/' + str(os.getenv("TOKEN")))
async def webhook_response(update: dict):
    return await dp.feed_update(bot=bot, update=Update(**update))


@app.head('/')
@app.get('/')
async def alive():
    return "Alive"
