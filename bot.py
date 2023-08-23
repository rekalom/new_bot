from config_bot.config import load_config

config = load_config()

# Выводим значения полей экземпляра класса Config на печать,
# чтобы убедиться, что все данные, получаемые из переменных окружения, доступны
print('BOT_TOKEN: ', config.tg_bot.token)
print('ADMINS_IDS: ', config.tg_bot.admins_id)
print()
print('DATABSE: ', config.db.database)
print('DB_HOST: ', config.db.db_host)
print('DB_USER: ', config.db.db_user)
print('DB_PASSWORD: ', config.db.db_password)
