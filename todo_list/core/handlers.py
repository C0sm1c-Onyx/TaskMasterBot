import aiohttp
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async

from core.models import Category, TGbotUser
from core.keyboards import main_kb


class AsyncIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.data):
            raise StopAsyncIteration

        value = self.data[self.index]
        self.index += 1
        return value


@sync_to_async
def get_category_by_name(key_category):
    category_obg = Category.objects.get(category_name=key_category)

    return category_obg


@sync_to_async
def get_category_by_id(id):
    category_obg = Category.objects.get(category_id=id)

    return category_obg


router = Router()


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
    chat_id = message.chat.id

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'http://taskmasterbot:8000/api/v1/get_user/{username}/',
            headers={
                'User-Agent': 'TelegramBot'
        }) as response:
            data = await response.json()
            if data['tg_user']:
                print(username, '-', 'exists')
            else:
                async with session.post(
                        'http://taskmasterbot:8000/api/v1/create_tg_user/',
                        data={'username_id': username, 'chat_id': chat_id},
                        headers={
                            'User-Agent': 'TelegramBot'
                        }
                ) as response:
                    print(response.status)

    await message.answer('''Привет! Я твой помощник по управлению задачами.\nС помощью меня ты сможешь создавать задачи, добавлять к ним комментарии и получать уведомления, когда приходит время выполнения задачи.''',
                         reply_markup=main_kb)


@router.message(F.text == 'Список задач')
async def cmd_get_tasks(message: Message):
    task_list = ''
    username = message.from_user.username
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'http://taskmasterbot:8000/api/v1/task-list/{username}/',
            headers={
                'User-Agent': 'TelegramBot'
            }
        ) as response:
            print(response.status)
            data = await response.json()

            async_list = AsyncIterator(data['Tasks'])

            i = 1
            async for task in async_list:
                category = await get_category_by_id(task['task_category_id'])
                print(task)
                row = f"""Задача {i}:\nid: {task['task_id']}\nНазвание: {task['task_title']}\nОписание: {task['task_description']}\nКатегория: {category.category_name}\nДата начала исполнения: {task['start_date']}\nДата создания: {task['create_data']}\n\n"""
                task_list += row
                i += 1

            if task_list:
                await message.answer(task_list)
            else:
                await message.answer('У вас нет задач')


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

    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://taskmasterbot:8000/api/v1/create-category/',
            data={
                'category_id': '1',
                'category_name': data['category']
            },
            headers={
                'User-Agent': 'TelegramBot'
            }
        ) as response:
            print(response.status)

            category_obj = await get_category_by_name(data['category'])

            async with session.post(
                'http://taskmasterbot:8000/api/v1/create-task/',
                data={
                    "user_id": username,
                    "task_id": "1",
                    "task_title": data['task_title'],
                    "task_description": data['task_description'],
                    "start_date": data['start_date'],
                    "task_category_id": category_obj.category_id
                },
                headers={
                    'User-Agent': 'TelegramBot'
                }
            ) as response:
                print(response.status)
                await message.answer('Задача добавлена! Уведомлю когда наступит день исполнения')
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
            f'http://taskmasterbot:8000/api/v1/create_comment/{abs(int(data["task_id"]))}/',
            data={
                "comment_id": "1",
                "comment": data['comment'],
                "username_id": username,
                "task_id": data['task_id']
            },
            headers={
                'User-Agent': 'TelegramBot'
            }
        ) as response:
            print(response.status)

            await message.answer('Комментарий к задаче добавлен')
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
        comment_list = ''
        async with session.get(
            f'http://taskmasterbot:8000/api/v1/list-comment/{abs(int(data["task_id"]))}/',
            headers={
                'User-Agent': 'TelegramBot'
            }
        ) as response:
            print(response.status)

            json_data = await response.json()

            async_list = AsyncIterator(json_data['comments'])
            i = 1
            async for comment in async_list:
                row = f'Комментарий {i}:\n{comment["comment"]}\n\n'
                comment_list += row
                i += 1

            if comment_list:
                await message.answer(f"Комментарии к задаче {data['task_id']}:\n\n{comment_list}")
            else:
                await message.answer(f'Комментариев к задаче {data["task_id"]} нету')

            await state.clear()
