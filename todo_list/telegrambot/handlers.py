from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .utils import AsyncIterator
from .services import (
    get_category_by_name,
    get_category_by_id,
    create_or_get_tg_user,
    create_category,
    create_task,
    get_user_tasks,
    create_comment,
    get_task_comments
)
from .keyboards import main_kb


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
    
    await create_or_get_tg_user(username, chat_id)
    await message.answer(
        '''Привет! Я твой помощник по управлению задачами.\nС помощью меня ты сможешь создавать задачи, добавлять к ним комментарии и получать уведомления, когда приходит время выполнения задачи.''',
        reply_markup=main_kb
    )


@router.message(F.text == 'Список задач')
async def cmd_get_tasks(message: Message):
    task_list = ''
    username = message.from_user.username
    
    data = await get_user_tasks(username)
    async_list = AsyncIterator(data['Tasks'])

    i = 1
    async for task in async_list:
        category = await get_category_by_id(task['task_category_id'])
        row = f"""Задача {i}:\nid: {task['task_id']}\nНазвание: {task['task_title']}\nОписание: {task['task_description']}\nКатегория: {category.category_name}\nДата начала исполнения: {task['start_date']}\nДата создания: {task['create_data']}\n\n"""
        task_list += row
        i += 1

    if task_list:
        await message.answer(task_list)
    else:
        await message.answer('У вас нет задач')


@router.message(F.text == 'Добавить задачу')
async def add_task(message: Message, state: FSMContext):
    await state.set_state(AddTask.category)
    await message.answer("Введите категорию")


@router.message(AddTask.category)
async def add_task_title(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(AddTask.task_title)
    await message.answer("Введите название задачи")


@router.message(AddTask.task_title)
async def add_task_description(message: Message, state: FSMContext):
    await state.update_data(task_title=message.text)
    await state.set_state(AddTask.task_description)
    await message.answer("Введите описание задачи")


@router.message(AddTask.task_description)
async def add_task_start_date(message: Message, state: FSMContext):
    await state.update_data(task_description=message.text)
    await state.set_state(AddTask.start_date)
    await message.answer("Введите дату начала исполнения задачи (формат: 2025-03-06)")


@router.message(AddTask.start_date)
async def add_task_on_db(message: Message, state: FSMContext):
    username = message.from_user.username
    await state.update_data(start_date=message.text)
    data = await state.get_data()

    # Create category first
    await create_category(data['category'])
    category_obj = await get_category_by_name(data['category'])
    
    # Then create task
    success = await create_task(username, data, category_obj.category_id)
    
    if success:
        await message.answer('Задача добавлена! Уведомлю когда наступит день исполнения')
    else:
        await message.answer('Произошла ошибка при создании задачи')
    
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

    success = await create_comment(username, str(abs(int(data["task_id"]))), data['comment'])
    
    if success:
        await message.answer('Комментарий к задаче добавлен')
    else:
        await message.answer('Произошла ошибка при добавлении комментария')
    
    await state.clear()


@router.message(F.text == 'Отобразить комментарии к задаче')
async def get_comment(message: Message, state: FSMContext):
    await state.set_state(GetTaskToShowComment.task_id)
    await message.answer("Введите id задачи у которой хотите увидеть комментарии")


@router.message(GetTaskToShowComment.task_id)
async def get_task_comment(message: Message, state: FSMContext):
    await state.update_data(task_id=message.text)
    data = await state.get_data()
    task_id = str(abs(int(data["task_id"])))

    json_data = await get_task_comments(task_id)
    
    comment_list = ''
    async_list = AsyncIterator(json_data['comments'])
    i = 1
    async for comment in async_list:
        row = f'Комментарий {i}:\n{comment["comment"]}\n\n'
        comment_list += row
        i += 1

    if comment_list:
        await message.answer(f"Комментарии к задаче {task_id}:\n\n{comment_list}")
    else:
        await message.answer(f'Комментариев к задаче {task_id} нету')

    await state.clear() 