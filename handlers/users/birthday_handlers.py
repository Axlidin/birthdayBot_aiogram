from _datetime import datetime
import asyncpg
import pytz
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from data.config import ADMINS
from keyboards.default.menu import Main_menu
from keyboards.inline.buttons_inline import cancel, cancel_admin
from loader import bot, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states.birthday_states import Birthday, del_birthday


# /form komandasi uchun handler yaratamiz. Bu yerda foydalanuvchi hech qanday holatda emas, state=None
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup

from loader import dp
from states.birthday_states import Birthday


@dp.message_handler(text="Add birthday", state=None)
async def enter_test(message: types.Message):
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    await message.answer("Ism kiriting", reply_markup=Mk)
    await Birthday.FullName.set()

@dp.message_handler(text="🛑 To'xtatish", state=Birthday)
async def cancel_see_fan(message: types.Message, state: FSMContext):
    await message.answer("Siz Tug'ilgan kun qo'shishni bekor qildingiz", reply_markup=Main_menu)
    await state.reset_state()


@dp.message_handler(state=Birthday.FullName)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text.upper()

    await state.update_data(
        {"name": fullname}
    )
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    await message.answer("Tug'ilgan yil kiriting! (<b>1996</b>)", reply_markup=Mk)


    # await Birthday.email.set()
    await Birthday.next()
@dp.message_handler(lambda message: not message.text.isdigit(), state=Birthday.Year)
async def process_year(message: types.Message):
    """
    If year is invalid
    """
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    return await message.answer("yil faqat raqamlarda kiritilishi kerak!!<b>1996</b>", reply_markup=Mk)
@dp.message_handler(state=Birthday.Year)
async def answer_year(message: types.Message, state: FSMContext):
    year = int(message.text)

    await state.update_data(
        {"year": year}
    )
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    await message.answer("Tug'ilgan oyingizni kiriting (<b>12</b>)", reply_markup=Mk)

    await Birthday.next()
@dp.message_handler(lambda message: not message.text.isdigit(), state=Birthday.Month)
async def process_month(message: types.Message):
    """
    If month is invalid
    """
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    return await message.answer("oy faqat raqamlarda kiritilishi kerak!!<b>12</b>", reply_markup=Mk)

@dp.message_handler(lambda message: message.text not in ["01", "02", "03", "04", "05", "06", "07", "08", "09",
                                                         "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], state=Birthday.Month)
async def process_month_invalid(message: types.Message):
    """
    Foydalanuvchining tug'ilgan oyini oladi
    """
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    return await message.answer("Kechirasz, bunday oy mavjud emas", reply_markup=Mk)
@dp.message_handler(state=Birthday.Month)
async def answer_month(message: types.Message, state: FSMContext):
    month = int(message.text)
    # print(month)

    await state.update_data(
        {"month": month}
    )
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")

    await message.answer("Tug'ilgan kun kiriting (<b>13</b>)", reply_markup=Mk)

    await Birthday.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=Birthday.Day)
async def process_day(message: types.Message):
    """
    If day is invalid
    """
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    return await message.answer("kun faqat raqamlarda kiritilishi kerak!<b>13</b>", reply_markup=Mk)
@dp.message_handler(lambda message: message.text not in ["01", "02", "03", "04", "05", "06", "07", "08", "09",
                                                         "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                                                         "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
                                                         "24", "25", "26", "27", "28", "29", "30", "31"], state=Birthday.Day)
async def process_day_invalid(message: types.Message):
    """
    Foydalanuvchining tug'ilgan kunini oladi
    """
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    return await message.answer("Kechirasz, bunday kun mavjud emas", reply_markup=Mk)
@dp.message_handler(state=Birthday.Day)
async def answer_month(message: types.Message, state: FSMContext):
    day = int(message.text)
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    # print(day)

    await state.update_data(
        {"day": day}
    )
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    name = data.get("name")
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")


    msg = "Quyidai ma`lumotlar qabul qilindi:\n"
    msg += f"Ism - {name}\n"
    msg += f"Tug'ilgan yil - {year}\n"
    msg += f"Tug'ilgan oy: - {month}\n"
    msg += f"Tug'ilgan kun: - {day}\n"

    # await message.answer(msg)

    # State dan chiqaramiz
    # 1-variant
    await state.finish()

    # 2-variant
    # await state.reset_state()

    # 3-variant. Ma`lumotlarni saqlab qolgan holda
    # await state.reset_state(with_data=False)
    await message.answer(f"Tabriklaymiz,siz muvaffaqiyatli tug'ilgan kun kiritdingiz", reply_markup=Main_menu)
    # await bot.send_message(chat_id=ADMINS[0], text=msg)
    member_id = message.from_user.id
    await state.finish()  # malumotlar ochib ketadi

    try:
        Birthday = await db.add_birthday(telegram_id=member_id,
                                          full_name=data['name'],
                                          Year=data['year'],
                                          Month=data['month'],
                                          Day=data['day'],
                                         ),

        Birthday = await db.select_birthday(telegram_id=message.from_user.id)
        # print(Birthday)

        # counts = await db.count_birthday()
        # await bot.send_message(chat_id=ADMINS[0], text=f"Tug'ilgan kunlari soni --- {counts}")
    except asyncpg.exceptions.UniqueViolationError:
        await state.reset_state(with_data=True)
#############################################
# @dp.message_handler(text="📝My birthday")
# async def show_own(message: Message):
#     tg_id = message.from_user.id
#     my_birthday = await db.my_birthday(tg_id=tg_id)
#     if not my_birthday:
#         await message.answer("❌ Sizda Tug'ilgan kunlar hozirda mavjud emas.\n"
#                              "Tug'ilgan kun qo'shish uchun <i>Add birthday</i> tugmasini bosing", reply_markup=Main_menu)
#     else:
#         for name in my_birthday:
#             msg = f"<b>Sizning Tug'ilgan kunlar ro'yxatingiz:</b>\n"
#             msg += f"<b>🔰 Ism:</b>  <i>{name[1].upper()}</i>\n"
#             msg += f"<b>🗓 Tug'ilgan Yili<i> (faqat raqamlarda)</i>:</b> {name[2]}\n"
#             msg += f"<b>📅 Tug'ilgan Oyi<i> (faqat raqamlarda)</i>:</b> {name[3]}\n"
#             msg += f"<b>📆 Tug'ilgan Kuni<i> (faqat raqamlarda)</i>:</b>{name[4]}\n"
#             await message.answer(msg)
#
#         if message.from_user.id == 5419118871:
#             await message.answer(f"Admin panelga qaytish uchun tugmani bosing", reply_markup=cancel_admin)
#         else:
#             await message.answer("Asosiy ekranga qaytish uchun tugmani bosing", reply_markup=cancel)


@dp.callback_query_handler(text="cancel_admin")
async def cancelmenu(call: CallbackQuery):
    await call.message.answer("<b>Asosiy bo'lim!</b>", reply_markup=Main_menu)
    await call.message.delete()
    await call.answer(cache_time=30)

@dp.callback_query_handler(text="cancel")
async def cancelmenu(call: CallbackQuery):
    await call.message.answer("<b>Asosiy bo'lim!</b>", reply_markup=Main_menu)
    await call.message.delete()
    await call.answer(cache_time=30)

 ###delete
#Fan o'chirish
@dp.message_handler(text="Delete birthday")
async def delete_db_fan(message: types.Message):
    tg_id = message.from_user.id
    my_birthday = await db.my_birthday(tg_id=tg_id)
    if not my_birthday:
        await message.answer("❌ Sizda Tug'ilgan kunlar hozirda mavjud emas.\n"
                             "Tug'ilgan kun qo'shish uchun <i>Add birthday</i> tugmasini bosing", reply_markup=Main_menu)
    else:
        Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for menu in my_birthday:
            fan_name_menu = menu[1]
            Mk.insert(KeyboardButton(text=fan_name_menu, resize_keyboard=True))
        Mk.add("🛑 To'xtatish")
        await message.answer(f"Kerakli Odamni tanlang! yoki tugmani bosing", reply_markup=Mk)
        await del_birthday.next()

@dp.message_handler(commands=["🛑 To'xtatish"], state=del_birthday)
async def cancel_delete(message: types.Message, state: FSMContext):
    await message.answer("Siz Tug'ilgan o'chirishni bekor qildingiz", reply_markup=Main_menu)
    await state.reset_state()

@dp.message_handler(state=del_birthday.birhtday_del)
async def data_del(message: types.Message, state: FSMContext):
    del_birthday = message.text.upper()
    await state.update_data(
        {"del_birthday": del_birthday}
    )
    deletes = await db.delete_db_name(del_name=del_birthday)
    if not deletes:
        await message.answer("Hozirda bunday ismli odam yo'q.", reply_markup=Main_menu)
    else:
        await message.answer(f"Siz tug'ilgan kun o'chirding\n\nDelete: {del_birthday}", reply_markup=Main_menu)
        await state.reset_state(with_data=True)

###statistik
import datetime

@dp.message_handler(text="📊 Statistika")
async def show_Statistika(message: types.Message):
    timezone = pytz.timezone("Asia/Tashkent")

    today = datetime.datetime.now(timezone)
    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minut = today.minute
    user_count = await db.count_FIO_state()
    birthday_count = await db.count_birthday()
    msg = f"<b><i>@My_Birthday2023_bot</i></b>\n📆 {year}-{month}-{day} ⏰ {hour}:{minut}\n👥 Bot foydalanuvchilari: <b>{user_count}</b> ta\n" \
          f"🎁🎉 Tug'ilgan kunlar: <b>{birthday_count}</b> ta"
    await bot.send_message(chat_id=message.from_user.id, text=msg, reply_markup=Main_menu)