from datetime import datetime


def generate_custom_id(string: str) -> str:
    dt = datetime.now()
    return str(hash(str(dt.timestamp()) + string))