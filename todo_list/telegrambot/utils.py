class AsyncIterator:
    """Async iterator for processing data in chunks."""
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