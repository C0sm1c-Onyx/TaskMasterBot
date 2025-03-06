import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_list.settings')

from telegram.keyboards import main_kb
from core.models import Category

router = Router()


@sync_to_async
def get_objects_db(key_category):
    category_obg = Category.objects.get(category_name=key_category)

    return category_obg


class AddTask(StatesGroup):
    category = State()
    task_title = State()
    task_description = State()
    start_date = State()


class GetTask(StatesGroup):
    task_id = State()
    comment = State()


class GetTaskToShowComment(StatesGroup):
    task_id = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    username = message.from_user.username
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/api/v1/get_user/{username}/') as response:
            data = await response.json()
            if data['tg_user']:
                print(username, '-', 'exists')
            else:
                async with session.post('http://127.0.0.1:8000/api/v1/create_tg_user/', data={'username_id': username}) as response:
                    print(response.status)

    await message.answer('''Привет! Я твой помощник по управлению задачами.\nС помощью меня ты сможешь создавать задачи, добавлять к ним комментарии и получать уведомления на электронную почту, когда приходит время их выполнения.''',
                         reply_markup=main_kb)


@router.message(F.text == 'Список задач')
async def cmd_get_tasks(message: Message):
    username = message.from_user.username
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/api/v1/task-list/{username}/') as response:
            print(response.status)
            data = await response.json()
            await message.answer(str(data))


@router.message(F.text == 'Добавить задачу')
async def add_task(
        message: Message, state: FSMContext
):
    await state.set_state(AddTask.category)
    await message.answer("Введите категорию")


@router.message(AddTask.category)
async def add_task_title(
        message: Message, state: FSMContext
):
    await state.update_data(category=message.text)
    await state.set_state(AddTask.task_title)
    await message.answer("Введите название задачи")


@router.message(AddTask.task_title)
async def add_task_description(
        message: Message, state: FSMContext
):
    await state.update_data(task_title=message.text)
    await state.set_state(AddTask.task_description)
    await message.answer("Введите описание задачи")


@router.message(AddTask.task_description)
async def add_task_start_date(
        message: Message, state: FSMContext
):
    await state.update_data(task_description=message.text)
    await state.set_state(AddTask.start_date)
    await message.answer("Введите дату начала исполнения задачи (формат: 2025-03-06)")


@router.message(AddTask.start_date)
async def add_task_on_db(
        message: Message, state: FSMContext
):
    username = message.from_user.username

    await state.update_data(start_date=message.text)

    data = await state.get_data()

    await message.answer(str(data))
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://127.0.0.1:8000/api/v1/create-category/',
            data={'category_id': '1', 'category_name': data['category']}
        ) as response:
            print(response.status)

            category_obj = await get_objects_db(data['category'])

            async with session.post(
                'http://127.0.0.1:8000/api/v1/create-task/',
                data={
                    "user_id": username,
                    "task_id": "1",
                    "task_title": data['task_title'],
                    "task_description": data['task_description'],
                    "start_date": data['start_date'],
                    "task_category_id": category_obj.category_id
                }
            ) as response:
                print(response.status)
                await state.clear()


@router.message(F.text == 'Добавить комментарий к задаче')
async def get_task(message: Message, state: FSMContext):
    await state.set_state(GetTask.task_id)
    await message.answer("Введите id задачи, к которой хотите написать комментарий")


@router.message(GetTask.task_id)
async def add_comment(message: Message, state: FSMContext):
    await state.update_data(task_id=message.text)
    await state.set_state(GetTask.comment)

    await message.answer("Введите комментарий")


@router.message(GetTask.comment)
async def create_comment_on_db(message: Message, state: FSMContext):
    username = message.from_user.username
    await state.update_data(comment=message.text)

    data = await state.get_data()

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'http://127.0.0.1:8000/api/v1/create_comment/{abs(int(data["task_id"]))}/',
            data={
                "comment_id": "1",
                "comment": data['comment'],
                "user_id": username,
                "task_id": data['task_id']
            }
        ) as response:
            print(response.status)

            data = await response.json()

            await message.answer(str(data))
            await state.clear()


@router.message(F.text == 'Отобразить комментарии к задаче')
async def get_comment(message: Message, state: FSMContext):
    await state.set_state(GetTaskToShowComment.task_id)
    await message.answer("Введите id задачи у которой хотите увидеть комментарии")


@router.message(GetTaskToShowComment.task_id)
async def get_task_comment(message: Message, state: FSMContext):
    await state.update_data(task_id=message.text)

    data = await state.get_data()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'http://127.0.0.1:8000/api/v1/list-comment/{abs(int(data["task_id"]))}/'
        ) as response:
            print(response.status)

            data = await response.json()

            await message.answer(str(data))
            await state.clear()
