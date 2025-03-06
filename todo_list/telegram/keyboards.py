from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Список задач")],
        [KeyboardButton(text="Добавить задачу")],
        [KeyboardButton(text="Добавить комментарий к задаче")],
        [KeyboardButton(text="Отобразить комментарии к задаче")],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие'
)