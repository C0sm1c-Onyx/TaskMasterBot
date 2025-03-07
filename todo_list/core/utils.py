from datetime import datetime
from asgiref.sync import sync_to_async


def generate_custom_id(string: str) -> str:
    dt = datetime.now()
    return str(hash(str(dt.timestamp()) + string))


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
    from models import Category
    category_obg = Category.objects.get(category_name=key_category)

    return category_obg


@sync_to_async
def get_category_by_id(id):
    from models import Category
    category_obg = Category.objects.get(category_id=id)

    return category_obg