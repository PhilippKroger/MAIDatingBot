from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram import executor

from config import API_TOKEN, list_likov
from scripts import *
from keyboards import *

import logging
import os

from states_and_obj import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

flag = 0
flag_index = 0

# comment
@dp.message_handler(Text(equals=['Зарегистрироваться']))
async def registration(message: types.Message):
    await message.answer("Как тебя зовут?", reply_markup=types.ReplyKeyboardRemove())
    await Form.name.set()


# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if check_user_exists(user_id):
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_start, resize_keyboard=True)
        await message.answer("Чем займемся сегодня?", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_registration, resize_keyboard=True)
        await message.answer(
            f"Привет!\nЯ бот для знакомств студентов МАИ!😎✈️\nСистема взаимных лайков работает следующим образом: "
            f"\nEсли вы понравились другому пользователю, то его анкету вы увидите одной из первых!"
            f"\nРегистрируйся и начинай поиски своей второй половинки!", reply_markup=keyboard)
        await message.answer('Бота разработали: @lantafik и @PhilippKroger')


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Сколько тебе лет?\nНапиши число, например: 18", reply_markup=types.ReplyKeyboardRemove())
    await Form.age.set()


# Обработка сообщения с возрастом
@dp.message_handler(state=Form.age)
async def process_age(message: types.Message, state: FSMContext):
    x = message.text
    if not x.isdigit():
        await message.answer(f'Введите число')
    else:
        if 16 <= int(x) <= 75:
            age = message.text
            await state.update_data(age=age)
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb_sex, resize_keyboard=True)
            await message.answer("Какого ты пола?", reply_markup=keyboard)
            await Form.sex.set()
        else:
            await message.answer(
                f'Указан некорректный возраст. Тут присутствуют возрастные ограничения (от 16 до 75 лет)')


@dp.message_handler(state=Form.sex)
async def process_gender(message: types.Message, state: FSMContext):
    if message.text not in ['Я девушка', 'Я парень']:
        await message.answer('admin: бро нажми на кнопку...')
    else:
        gender = message.text
        await state.update_data(sex=gender)
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_skip_about, resize_keyboard=True)
        await message.answer("Расскажи о себе.", reply_markup=keyboard)  # types.ReplyKeyboardRemove()
        await Form.personal_data.set()


# Обработка сообщения с личными данными
@dp.message_handler(state=Form.personal_data)
async def process_personal_data(message: types.Message, state: FSMContext):
    personal_data = message.text
    user_id = message.from_user.id
    if personal_data == 'Оставить без описания':
        await state.update_data(personal_data="")
        user_data = await state.get_data()

        if get_user_by_id(user_id) is None:
            add_data(user_id, user_id, user_data, 0, 0, 1, 0)
        else:

            # os.remove(f'images/{user_id}/{user_id}.jpg')
            update_data(user_id, user_data)

        await message.answer("Добавь фотографию к профилю", reply_markup=types.ReplyKeyboardRemove())
        await Form.img.set()

    elif len(personal_data) <= 1000:
        await state.update_data(personal_data=personal_data)
        user_data = await state.get_data()

        if get_user_by_id(user_id) is None:
            add_data(user_id, user_id, user_data, 0, 0, 1, 0)
        else:
            # os.remove(f'images/{user_id}/{user_id}.jpg')
            update_data(user_id, user_data)

        await message.answer("Добавь фотографию к профилю", reply_markup=types.ReplyKeyboardRemove())
        await Form.img.set()
    else:
        await message.answer("Слишком большой текст, краткость сестра таланта! \n Расскажите о себе ещё раз."
                             , reply_markup=types.ReplyKeyboardRemove())
        await Form.personal_data.set()

    @dp.message_handler(content_types=types.ContentType.TEXT, state=Form.img)
    async def handle_message(message: types.Message):
        await message.answer('Вы отправили текстовое сообщение\nОтправьте фотографию📸')


# Обработчик приема изображения
@dp.message_handler(content_types=types.ContentType.PHOTO, state=Form.img)
async def handle_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    user_id = message.from_user.id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    save_photo(message.from_user.id, file_id)

    # await bot.download_file(file_path, f"images/{user_id}/{user_id}.jpg")
    await state.update_data(img=photo)
    await state.finish()

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_profile, resize_keyboard=True)
    await message.delete()
    await message.answer("Данные вашей анкеты были сохранены. Можете начинать знакомиться! \n Вот ваша анкета.",
                         reply_markup=keyboard)
    await send_profile(message.from_user.id, message.from_user.id, keyboard)
    msg = "1. Изменить анкету✏️\n2. Изменить фото📸 \n3. Изменить текст анкеты📜\n4. Смотреть анкеты🚀"
    await bot.send_message(message.from_user.id, msg)
    # file_test = await bot.get_file(file_id)
    # await bot.send_photo(message.from_user.id, file_test.file_id, reply_markup=keyboard)


# Обработчик команды /next для переключения на следующую анкету
@dp.message_handler(Text(equals=['👎']))
async def cmd_next(message: types.Message):
    global flag_index, list_likov
    await proverka_profile(message)
    user_list_id = all_users_id(user_sex(message.from_user.id))
    profile = User(message.from_user.id)
    index = profile.index
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_next, resize_keyboard=True)
    user_list_with_like = ankets_with_like(profile.user_id)
    if user_list_with_like == []:  # список людей лайкнувших
        if index < len(user_list_id):
            flag_index = 1
            profile_id = user_list_id[index]
            change_index(profile.user_id, profile.index + 1)
            await send_profile(message.from_user.id, profile_id, keyboard)
            if len(user_list_id) == index + 1:
                change_index(profile.user_id, 0)
    else:
        flag_index = 2
        if profile.index_like == 0:
            profile = User(message.from_user.id)
            await send_profile(profile.user_id, user_list_with_like[profile.index_like], keyboard)
            change_index_like(1, profile.user_id)
            list_likov = index_spiska(profile.user_id)
        elif profile.index_like == len(user_list_with_like):
            profile = User(message.from_user.id)
            change_index_like(0, profile.user_id)
            delete_all_like(profile.user_id)
            delete_for_liked(list_likov)
            await cmd_next(message)
        else:
            profile = User(message.from_user.id)
            await send_profile(profile.user_id, user_list_with_like[profile.index_like], keyboard)
            change_index_like(profile.index_like + 1, profile.user_id)


@dp.message_handler(Text(equals=['Смотреть анкеты 🚀', '4 🚀', '🚀']))
async def cmd_next2(message: types.Message):
    global flag, flag_index
    flag_index = 1
    await proverka_profile(message)
    profile = User(message.from_user.id)
    if profile.index_activity == 0:
        user_activity(1, message.from_user.id)
        msg = "Ваша анкета была активирована."
        await message.answer(msg)
    index = profile.index
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_next, resize_keyboard=True)
    user_list = all_users_id(user_sex(message.from_user.id))
    if index < len(user_list):
        if flag == 1:
            if index > 0:
                profile_id = user_list[index - 1]
                await send_profile(message.from_user.id, profile_id, keyboard)
            else:
                profile_id = user_list[0]
                change_index(profile.user_id, profile.index + 1)
                await send_profile(message.from_user.id, profile_id, keyboard)
            flag = 0
        else:
            profile_id = user_list[index]
            change_index(profile.user_id, profile.index + 1)
            await send_profile(message.from_user.id, profile_id, keyboard)
            if len(user_list) == index + 1:
                change_index(profile.user_id, 0)


# Функция для отображения анкет
async def send_profile(user_id, profile_id, keyboard):
    if type(profile_id) == int:
        profile = User(profile_id)
        profile_text = f"{profile.name}, {profile.age}\n{profile.personal_data}"
        await bot.send_photo(user_id, profile.photo, profile_text, reply_markup=keyboard)
    else:
        profile = User(profile_id[0])
        # if os.path.exists(f'images/{profile.user_id}') == False:
        #    profile_text = f"{profile.name}, {profile.age}\n{profile.personal_data}"
        #    await bot.send_message(user_id, profile_text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        # else:

        # photo = open(f'images/{profile.user_id}/{profile.user_id}.jpg', 'rb')
        profile_text = f"{profile.name}, {profile.age}\n{profile.personal_data}"
        await bot.send_photo(user_id, profile.photo, profile_text, reply_markup=keyboard)
        # await bot.send_photo(user_id, photo, profile_text, reply_markup=keyboard)


# Обработка сообщения с личными данными
@dp.message_handler(Text(equals='❤'))
async def process_personal_data(message: types.Message):
    global flag_index
    await proverka_profile(message)
    profile = User(message.from_user.id)
    user_list_with_like = ankets_with_like(profile.user_id)
    user_list_id = all_users_id(user_sex(profile.user_id))

    if flag_index == 2:
        profile_id = user_list_with_like[profile.index_like - 1]
        profile2 = User(profile_id[0])
    else:
        profile2 = User(user_list_id[profile.index - 1][0])
    if profile.index_like == len(user_list_with_like):
        profile = User(message.from_user.id)
        change_index_like(0, profile.user_id)

    if proverka_like2(profile.user_id, profile2.user_id):
        likes(profile.user_id, profile2.user_id)
    if proverka_like(profile.user_id, profile2.user_id):
        delete_like(profile.user_id, profile2.user_id)

        user = await bot.get_chat(profile.user_id)
        username = user.username
        user = await bot.get_chat(profile2.user_id)
        username2 = user.username
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_f_reg, resize_keyboard=True)
        await send_profile(profile.chat_id, profile2.chat_id, keyboard)
        await send_profile(profile2.chat_id, profile.chat_id, keyboard)
        await bot.send_message(profile.chat_id, f'У вас взаимная симпатия с @{username2}!', reply_markup=keyboard)
        await bot.send_message(profile2.chat_id, f'У вас взаимная симпатия с @{username}!', reply_markup=keyboard)

        await bot.send_message(profile.chat_id, 'Хорошо, идём дальше.', reply_markup=keyboard)
        await bot.send_message(profile2.chat_id, 'Хорошо, идём дальше.', reply_markup=keyboard)
    await cmd_next(message)


# Просмотр собственного профиля
@dp.message_handler(Text(equals=['Мой профиль🏚️', '🏚️']))
async def profile(message: types.Message):
    await proverka_profile(message)
    profile = User(message.from_user.id)
    profile_text = f"{profile.name}, {profile.age}\n{profile.personal_data}"
    # photo = open(f'images/{profile.user_id}/{profile.user_id}.jpg', 'rb')
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_profile, resize_keyboard=True)
    await bot.send_photo(profile.user_id, profile.photo, f'{profile_text}', reply_markup=keyboard)
    msg = "1. Изменить анкету✏️\n2. Изменить фото📸 \n3. Изменить текст анкеты📜\n4. Смотреть анкеты🚀"
    await bot.send_message(profile.user_id, msg)


@dp.message_handler(Text(equals='1✏️'))
async def change_profile(message: types.Message):
    user_id = message.from_user.id
    # delete_profile(message.from_user.id)
    await message.answer(f"Как тебя зовут?", reply_markup=types.ReplyKeyboardRemove())
    await Form.name.set()


@dp.message_handler(Text(equals='2📸'))
async def handle_photo(message: types.Message):
    await message.answer("Добавьте фотографию📸", reply_markup=types.ReplyKeyboardRemove())
    await Form1.image.set()

    @dp.message_handler(content_types=types.ContentType.TEXT, state=Form1.image)
    async def handle_message(message: types.Message):
        await message.answer('Вы отправили текстовое сообщение\nОтправьте фотографию📸')


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Form1.image)
async def handle_photo_1(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    profile = User(message.from_user.id)
    file_id, user_id = photo.file_id, message.from_user.id
    # os.remove(f'images/{user_id}/{user_id}.jpg')
    save_photo(message.from_user.id, file_id)
    file = await bot.get_file(file_id)
    file_path = file.file_path
    # await bot.download_file(file_path, f"images/{user_id}/{user_id}.jpg")
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_main_page, resize_keyboard=True)
    await message.answer("Данные успешно сохранены.",
                         reply_markup=keyboard)
    msg = "1. Изменить анкету✏️\n2. Изменить фото📸 \n3. Изменить текст анкеты📜\n4. Смотреть анкеты🚀"


@dp.message_handler(Text(equals='3📜'))
async def handle_photo(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_skip_about, resize_keyboard=True)
    await message.answer("📜 Измените описание вашей анкеты 📜", reply_markup=keyboard)
    await Form2.text.set()


@dp.message_handler(state=Form2.text)
async def process_personal_data_1(message: types.Message, state: FSMContext):
    personal_data = message.text
    if personal_data == 'Оставить без описания':
        await state.update_data(personal_data=personal_data)
        change_description(message.chat.id, "")
        await state.finish()
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_start, resize_keyboard=True)
        await message.answer("✨✨✨ Данные успешно сохранены ✨✨✨", reply_markup=keyboard)
    elif len(personal_data) <= 1000 and personal_data != 'Оставить без описания':
        await state.update_data(personal_data=personal_data)
        change_description(message.chat.id, personal_data)
        await state.finish()
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_start, resize_keyboard=True)
        await message.answer("✨✨✨ Данные успешно сохранены ✨✨✨", reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_skip_about, resize_keyboard=True)
        msg = "Слишком большой текст, краткость сеста таланта!\nРасскажите о себе ещё раз."
        await message.answer(msg, reply_markup=keyboard)


@dp.message_handler(Text(equals='💤'))
async def main_page(message: types.Message):
    global flag
    await proverka_profile(message)
    flag += 1
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_main_page, resize_keyboard=True)
    msg = ("Вы перешли в основное меню. \n"
           "1. Смотреть анкеты 🚀\n"
           "2. Мой профиль 🏚️\n"
           "3. Я больше не хочу никого искать ⛔\n"
           "4. Удалить анкету 🗑️")
    await message.answer(msg, reply_markup=keyboard)


@dp.message_handler(Text(equals=['Я больше не хочу никого искать', '⛔']))
async def off_profile(message: types.Message):
    await proverka_profile(message)
    profile = User(message.from_user.id)
    user_activity(0, profile.user_id)
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_change_activity, resize_keyboard=True)
    msg = "Ваша анкета была отключена. Надеемся вы нашли то, что искали!\nЕсли нет, то возвращайтесь"
    await message.answer(msg, reply_markup=keyboard)


@dp.message_handler(Text(equals=['Удалить анкету', '🗑️']))
async def delete_porfile(message: types.Message):
    await proverka_profile(message)
    user_id = message.from_user.id
    delete_profile(message.from_user.id)
    # os.remove(f'images/{user_id}/{user_id}.jpg')
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb_registration, resize_keyboard=True)
    msg = "Ваша анкета была удалена🗑.\nНадеемся вы нашли то, что искали!\nЕсли нет, то возвращайтесь."
    await message.answer(msg, reply_markup=keyboard)


async def proverka_profile(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_by_id(user_id)
    if user_data is None:
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb_registration)
        await message.answer('У вас нет профиля', reply_markup=keyboard)
    else:
        if message.text not in ['Мой профиль🏚️', "Смотреть анкеты 🚀", 'Я парень', "Я девушка", '💤', '❤', "👎",
                                'Зарегистрироваться', '1✏️', '2📸', '3📜', "4 🚀", '🚀', '⛔', '🗑️', 'Оставить без описания',
                                'Это всё, сохранить фото']:
            await message.answer('Используйте кнопку на клавиатуре')


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def proverka(message: types.message):
    await proverka_profile(message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
