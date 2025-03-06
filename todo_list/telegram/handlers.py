import aiohttp
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from .keyboards import main_kb

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('''Привет!
                            Я твой помощник по управлению задачами. 
                            С помощью меня ты сможешь создавать задачи,
                            добавлять к ним комментарии и получать уведомления на электронную почту,
                            когда приходит время их выполнения.''',
                         reply_markup=main_kb)


@router.message(Command('task-list'))
async def cmd_get_tasks(message: Message):
    pass


@router.message(Command('add-task'))
async def cmd_add_task(message: Message):
    pass


@router.message(Command('add-comment-task'))
async def cmd_add_comment(message: Message):
    pass


@router.message(Command('task-comment-list'))
async def cmd_get_comment(message: Message):
    pass