import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default.menu import Main_menu
from loader import dp, bot
import datetime

# Get current month and day
from loader import db
from states.birthday_states import Check_fio


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    telegram_id = message.from_user.id
    db_fios = await db.my_bithday_see(tg_id=telegram_id)
    if not db_fios:
        await message.answer("Ismingizni kiriting!")
        await Check_fio.next()
    else:
        await message.answer("❕ Kerakli bo'limni tanlang.", reply_markup=Main_menu)


@dp.message_handler(state=Check_fio.Firstname)
async def firstname(message: types.Message, state: FSMContext):
    firstname = message.text.upper()
    await state.update_data(
        {"firstname": firstname}
    )
    await message.answer("Familiyangizni kiriting:")
    await Check_fio.next()
@dp.message_handler(state=Check_fio.Surname)
async def surname(message: types.Message, state: FSMContext):
    surname = message.text.upper()
    await state.update_data(
        {"surname": surname}
    )

    # ma'lumotlarni qayta o'qish
    data = await state.get_data()
    firstname = data.get("firstname")
    surname = data.get('surname')

    msg = "Quyidagi ma'lumotlar qabul qilindi:\n"
    msg += f"🔰 firstname ---- {firstname}\n"
    msg += f"🔰 surname ---- {surname}\n"


    await state.finish()
    #Admin_menu
    await message.answer("❕ Kerakli bo'limni tanlang.", reply_markup=Main_menu)
    try:
        user = await db.add_FIO_state(
            telegram_id=message.from_user.id,
            firstname=data["firstname"],
            surname=data["surname"],
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_FIO_state(telegram_id=message.from_user.id)
    # count = await db.count_FIO_state()
    # msg = f"{user[1]} {user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    # await bot.send_message(chat_id=ADMINS[0], text=msg)
