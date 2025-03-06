import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_list.settings')

import django
django.setup()

from telegram.handlers import router


load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    dp = Dispatcher(bot=bot)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())