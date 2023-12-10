from aiogram import types


kb_start = [
    [
        types.KeyboardButton(text='Мой профиль🏚️', resize_keyboard=True),
        types.KeyboardButton(text="Смотреть анкеты 🚀", resize_keyboard=True)
    ]
]


kb_sex = [
    [
        types.KeyboardButton(text='Я парень', resize_keyboard=True),
        types.KeyboardButton(text="Я девушка", resize_keyboard=True)
    ]
]


kb_f_reg = [
    [
        types.KeyboardButton(text="Смотреть анкеты 🚀", resize_keyboard=True)
    ]
]


kb_next = [
    [
        types.KeyboardButton(text='💤', resize_keyboard=True),
        types.KeyboardButton(text='❤', resize_keyboard=True),
        types.KeyboardButton(text="👎", resize_keyboard=True)
    ]
]


kb_registration = [
    [
        types.KeyboardButton(text='Зарегистрироваться', resize_keyboard=True)
    ]
]


kb_profile = [
    [
        types.KeyboardButton(text='1✏️', resize_keyboard=True),  # изменить профиль
        types.KeyboardButton(text='2📸', resize_keyboard=True),  # изменить фото
        types.KeyboardButton(text='3📜', resize_keyboard=True),  # изменить текст
        types.KeyboardButton(text="4 🚀", resize_keyboard=True)  # смотреть анкеты
    ]
]


kb_main_page = [
    [
        types.KeyboardButton(text='🚀', resize_keyboard=True, ),
        types.KeyboardButton(text='🏚️', resize_keyboard=True),
        types.KeyboardButton(text='⛔', resize_keyboard=True),
        types.KeyboardButton(text='🗑️', resize_keyboard=True),
    ]
]


kb_skip_about = [
    [
        types.KeyboardButton(text='Оставить без описания', resize_keyboard=True, ),
    ]
]

kb_change_activity = [
    [
        types.KeyboardButton(text='Смотреть анкеты 🚀', resize_keyboard=True, ),
    ]
]

kb_save_img = [
    [
        types.KeyboardButton(text='Это всё, сохранить фото', resize_keyboard=True, ),
    ]
]
