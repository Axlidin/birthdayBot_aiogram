import datetime
import pytz
import psycopg2
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config
from data.config import ADMINS
from loader import bot, db

dp = Dispatcher(bot)

# Joylashuvingiz uchun vaqt mintaqasini sozlang
timezone = pytz.timezone("Asia/Tashkent")
# print(timezone)

# Ma'lumotlar bazasi ulanishini o'rnating
conn = psycopg2.connect(
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    database=config.DB_NAME
)


# Joriy sanaga mos keladigan tug'ilgan kunlarni olish uchun funktsiyani belgilang
def get_birthdays():
    today = datetime.datetime.now(timezone)
    month = today.month
    day = today.day
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM birthday WHERE Month = '{month}' AND Day = '{day}'")

    rows = cur.fetchall()
    for row in rows:
        # print(row)
        yield row[5]


# Define the message to send
# Belgilangan Telegram foydalanuvchisiga xabar yuborish funksiyasini belgilang
async def send_message(telegram_id):
    datas = await db.my_birthday(tg_id=telegram_id)
    my_birthday = await db.my_bithday_see(tg_id=telegram_id)

    for name in my_birthday:
        name = name[1]
    today = datetime.datetime.now(timezone)
    month = today.month
    day = today.day
    month_day = f"{month} {day}"
    for data in datas:
        # db_month = data[3]
        # db_day = data[4]
        today = datetime.datetime.now(timezone)
        year = today.year
        db_month_day = f"{data[3]} {data[4]}"
        if db_month_day == month_day:
            message = f"<b><i>{name.upper()}!</i></b> bugun siz kiritgan tug'ilgan kunlardan biri... \n🎉 🎉 🎉Tabriklaymiz\n" \
                      f"Tug'ilgan kuningiz bilan <b><i>{data[1].upper()}\n🎉 🎉 🎉" \
                      f"{year - int(data[2])}</i></b> yoshingiz muborak bo'lsin"
            try:
                await bot.send_message(chat_id=telegram_id, text=message)
            except exceptions.BotBlocked:
                pass
        else:
            pass



# Xabarlarni yuborish uchun ishni belgilang
async def send_messages_job():
    birthdays = get_birthdays()
    for telegram_id in birthdays:
        await send_message(telegram_id)

# Har kuni yarim tunda ishni bajarish uchun rejalashtiruvchini sozlang
scheduler = AsyncIOScheduler(timezone=timezone)
scheduler.add_job(send_messages_job, 'cron', hour=0, minute=0)

# Start the scheduler / Rejalashtiruvchini ishga tushiring
scheduler.start()
