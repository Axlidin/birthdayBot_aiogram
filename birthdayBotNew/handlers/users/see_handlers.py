from aiogram import types

from aiogram.types import CallbackQuery

# from keyboards.default.menukeyboard import menu
# from keyboards.inline.cancel import cancel
from loader import dp, db

@dp.message_handler(text="info")
async def all_birthday(message: types.Message):
    datas = await db.select_all_birthday()
    for data in datas:
        id = data[0]
        ism = data[1]
        yil = data[2]
        oy = data[3]
        kun = data[4]
        telegram_id = data[5]
        await message.answer(f"<b>Tug'ilgan kunlar:</b>\n"
                             f"<b>♻️ №</b> {data[0]}\n"
                             f"<b>🔰 Ism:</b> {data[1]}\n"
                             f"<b>📆 yil:</b> {data[2]}\n"
                             f"<b>📅 oy:</b> {data[3]}\n"
                             f"<b>📅 kun:</b>{data[4]}\n"
                             f"<b>🖇 telegram_id:</b>{data[5]}")
    # await message.answer("Asosiy ekranga qaytish uchun tugmani bosing", reply_markup=cancel)

# @dp.callback_query_handler(text="cancel")
# async def cancelmenu(call: CallbackQuery):
#     await call.message.answer("<b>Asosiy bo'lim!</b>", reply_markup=menu)
#     await call.message.delete()
#     await call.answer(cache_time=30)

from _datetime import datetime

@dp.message_handler(text="happy")
async def all_birthday(message: types.Message):
    now = datetime.now()
    x = now.strftime("%d/%m/%y")
    # print(x)
    year = now.strftime("%y")
    year = int(year)
    month = now.strftime("%m")
    month = str(month)
    day = now.strftime("%d")
    day = str(day)
    # print(month)
    # print(day)
    datas1 = await db.happy_month(month)
    # print(datas1)
    for data in datas1:
        # print(data)
        # id = data[0]
        oy = data[0]
        print(oy)
        if oy == '01':
            print('tabrikleman')
        else:
            print("xozrida mavjuda emas")
        # print(id)
        # print(oy)
        # print(data[4])
        # if month and day == data[3] and data[4]:
        #     print('tabrikleman')
        #     await message.answer('tabrikelaman')
        # else:
        #     print('xali erta')
        #     await message.answer("erta xali")
        # await message.answer(f"<b>Tug'ilgan kunlar:</b>\n"
        #                      f"<b>♻️ №</b> {data[0]}\n"
        #                      f"<b>🔰 Ism:</b> {data[1]}\n")
    # datas2 = await db.happy_day(day)
    # for data in datas2:
    #     id = data[0]
    #     # ism = data[1]
    #     # yil = data[2]
    #     oy = data[3]
    #     kun = data[4]
    #     print(oy)
    #     print(kun)
    #     # if month and day == data[3] and data[4]:
    #     #     print('tabrikleman')
    #     #     await message.answer('tabrikelaman')
    #     # else:
    #     #     print('xali erta')
    #     #     await message.answer("erta xali")
    #     # await message.answer(f"<b>Tug'ilgan kunlar:</b>\n"
    #     #                      f"<b>♻️ №</b> {data[0]}\n"
    #     #                      # f"<b>🔰 Ism:</b> {data[1]}\n"
    #     #                      # f"<b>📆 yil:</b> {data[2]}\n"
    #     #                      f"<b>📅 oy:</b> {data[3]}\n"
    #     #                      f"<b>📅 kun:</b>{data[4]}\n")