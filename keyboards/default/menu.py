from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Add birthday"),
            KeyboardButton(text="📝My birthday"),
        ],
        [
            KeyboardButton(text="Delete birthday"),
            KeyboardButton(text="📊 Statistika"),
        ],
        [
            KeyboardButton(text="Support service")
        ]
    ],
    resize_keyboard=True, one_time_keyboard=True
)