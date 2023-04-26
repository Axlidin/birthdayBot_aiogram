from aiogram.dispatcher.filters.state import StatesGroup, State


# Shaxsiy ma'lumotlarni yig'sih uchun PersonalData holatdan yaratamiz
class Birthday(StatesGroup):
    # Foydalanuvchi buyerda 4 ta holatdan o'tishi kerak
    FullName = State() # fio
    Year = State() # year
    Month = State() # month
    Day = State() # Day

class Check_fio(StatesGroup):
    Firstname = State()
    Surname = State()

class del_birthday(StatesGroup):
    birhtday_del = State()