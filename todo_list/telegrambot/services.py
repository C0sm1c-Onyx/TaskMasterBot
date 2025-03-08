from asgiref.sync import sync_to_async
import aiohttp
from core.models import Category, TGbotUser


@sync_to_async
def get_category_by_name(key_category: str) -> Category:
    return Category.objects.get(category_name=key_category)


@sync_to_async
def get_category_by_id(category_id: str) -> Category:
    return Category.objects.get(category_id=category_id)


async def create_or_get_tg_user(username: str, chat_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'http://taskmasterbot:8000/api/v1/get_user/{username}/',
            headers={'User-Agent': 'TelegramBot'}
        ) as response:
            data = await response.json()
            if data['tg_user']:
                return True
            
            async with session.post(
                'http://taskmasterbot:8000/api/v1/create_tg_user/',
                data={'username_id': username, 'chat_id': chat_id},
                headers={'User-Agent': 'TelegramBot'}
            ) as response:
                return response.status == 200


async def create_category(category_name: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://taskmasterbot:8000/api/v1/create-category/',
            data={
                'category_id': '1',
                'category_name': category_name
            },
            headers={'User-Agent': 'TelegramBot'}
        ) as response:
            return response.status == 200


async def create_task(username: str, task_data: dict, category_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://taskmasterbot:8000/api/v1/create-task/',
            data={
                "user_id": username,
                "task_id": "1",
                "task_title": task_data['task_title'],
                "task_description": task_data['task_description'],
                "start_date": task_data['start_date'],
                "task_category_id": category_id
            },
            headers={'User-Agent': 'TelegramBot'}
        ) as response:
            return response.status == 201


async def get_user_tasks(username: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'http://taskmasterbot:8000/api/v1/task-list/{username}/',
            headers={'User-Agent': 'TelegramBot'}
        ) as response:
            return await response.json()


async def create_comment(username: str, task_id: str, comment_text: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'http://taskmasterbot:8000/api/v1/create_comment/{task_id}/',
            data={
                "comment_id": "1",
                "comment": comment_text,
                "username_id": username,
                "task_id": task_id
            },
            headers={'User-Agent': 'TelegramBot'}
        ) as response:
            return response.status == 201


async def get_task_comments(task_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'http://taskmasterbot:8000/api/v1/list-comment/{task_id}/',
            headers={'User-Agent': 'TelegramBot'}
        ) as response:
            return await response.json() 