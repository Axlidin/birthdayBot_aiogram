from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")





# ADMINS = 5419118871
# BOT_TOKEN = "5581665659:AAHwyQF0bdwL72NEEwx6qfnc9vX_oqoT0hM"
# ip = "localhost"
#
# #startdagi foydalanuvchilar uchun
# DB_USER = "postgres"
# DB_PASS = 5861
# DB_NAME = "Davomat"
# DB_HOST = "localhost"

support_ids = [
5419118871
]
