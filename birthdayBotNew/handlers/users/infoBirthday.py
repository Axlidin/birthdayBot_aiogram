import psycopg2
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import Bot, Dispatcher, types

# Set up database connection
from data import config
# from keyboards.default.menukeyboard import Admin_menu, menu
from keyboards.default.menu import Main_menu
from loader import bot, dp

conn = psycopg2.connect(
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    database=config.DB_NAME
)
# Set up bot and dispatcher

# Konstantalarni o'rnating
PAGE_SIZE = 2

# Ma'lumotlar bazasidan mahsulotlarni olish funktsiyasini aniqlang
def get_products(page):
    offset = (page - 1) * PAGE_SIZE
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM birthday ORDER BY id LIMIT %s OFFSET %s",
            (PAGE_SIZE, offset)
        )
        products = cur.fetchall()
    return products

# Orqaga va oldinga tugmalarini yaratish funksiyasini aniqlang
def create_page_buttons(page):
    back_button = InlineKeyboardButton(
        "⬅️",
        callback_data=f"back_{page-1}" if page > 1 else "back_1"
    )
    forward_button = InlineKeyboardButton(
        "➡️",
        callback_data=f"forward_{page+1}"
    )
    exit_button = InlineKeyboardButton(
        "❌", callback_data="page_exit"
    )
    return InlineKeyboardMarkup().row(back_button, exit_button, forward_button)

# Orqaga va oldinga tugmalarini yaratish funksiyasini aniqlang
def create_page_firts(page):
    forward_button = InlineKeyboardButton(
        "➡️",
        callback_data=f"forward_{page+1}"
    )
    exit_button = InlineKeyboardButton(
        "❌", callback_data="page_exit"
    )
    return InlineKeyboardMarkup().row(exit_button, forward_button)
@dp.callback_query_handler(text="cancel_admin")
async def cancelmenu_admin(call: CallbackQuery):
    await call.message.answer("<b>Asosiy bo'lim!</b>", reply_markup=Main_menu)
    await call.answer(cache_time=30)

@dp.callback_query_handler(text="cancel")
async def cancelmenu(call: CallbackQuery):
    await call.message.answer("<b>Asosiy bo'lim!</b>", reply_markup=Main_menu)
    await call.message.delete()
    await call.answer(cache_time=30)
# Handler for "exit" button
@dp.callback_query_handler(lambda c: c.data == 'page_exit')
async def exit_button_handler(callback_query: types.CallbackQuery):
    if callback_query.id == 5419118871:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="<b>Ma'lumotlar olish tugatildi.</b>",
                               reply_markup=Main_menu)
    else:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="<b>Ma'lumotlar olish tugatildi.</b>",
                               reply_markup=Main_menu)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

# Sahifani o'zgartirish uchun foydalanuvchi so'rovlarini bajarish uchun funktsiyani belgilang
@dp.callback_query_handler(lambda c: True)
async def process_page_callback(callback_query: types.CallbackQuery):
    action = callback_query.data
    page = int(callback_query.data.split("_")[1])
    if action == "back_1":
        page -= 1
        page = 1
        products = get_products(page)
        buttons = create_page_firts(page)
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=format_products(products),
            reply_markup=buttons
        )
    else:
        products = get_products(page)
        buttons = create_page_buttons(page)
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=format_products(products),
            reply_markup=buttons
        )


#Mahsulotlarni matn sifatida formatlash funksiyasini aniqlang
def format_products(products):
    if not products:
        return "Tug'ilgan kunlar topilmadi."


    lines = []
    for p in products:

        lines.append(f"<b>Sizning Tug'ilgan kunlar ro'yxatingiz:</b>\n"
                    f"<b>🔰 Ism:</b>  <i>{p[1].upper()}</i>\n"
                    f"<b>🗓 Tug'ilgan Yili<i> (faqat raqamlarda)</i>:</b> {p[2]}\n"
                    f"<b>📅 Tug'ilgan Oyi<i> (faqat raqamlarda)</i>:</b> {p[3]}\n"
                    f"<b>📆 Tug'ilgan Kuni<i> (faqat raqamlarda)</i>:</b>{p[4]}\n\n"
                    f"**********\n\n")
    return "\n".join(lines)

# Define function to handle user requests to start browsing products
@dp.message_handler(text="📝My birthday")
async def process_start_command(message: types.Message):
    page = 1
    products = get_products(page)
    buttons = create_page_buttons(page)
    await bot.send_message(
        chat_id=message.chat.id,
        text=format_products(products),
        reply_markup=buttons
    )


