from aiogram import types
from aiogram import Bot


async def set_bot_commands(bot: Bot):
    bot_c = [
        types.BotCommand(command='/start', description='Старт'),
    ]
    a = await bot.set_my_commands(bot_c)
    print(a, "commands was set")