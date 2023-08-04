import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.types import Message, ContentType
from environs import Env

env = Env()            # Создаём эземпляр класса Env
env.read_env()         # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

BOT_TOKEN = env('BOT_TOKEN')    # Сохраняем значение перменной окружения в переменную bot_token

# Создаём объекты бота и деспетчера
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 5

# Словарь, в котором будут храниться данные пользователей
users: dict = {}

# Функция, возвращающая случайное целое число от 1 до 100
def get_randon_number() -> int:
    return random.randint(1, 100)

# Хэндлер для команды "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message) -> None:
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')
    # Если пользователь только запустил бота и его нет в словаре
    # users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}

# Хэндлер для команды "/help"
@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message) -> None:
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем?')

# Хэндлер для команды "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message) -> None:
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}')

# Хэндлер для команды "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message) -> None:
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом.')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы и так с Вами не играем. '
                             'Может, всё-таки, сыграем разок?')

# Хэндлер для обработки согласия пользователя сыграть в игру
@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть', 'ok', 'ок'],
                 ignore_case=True))
async def process_positive_answer(message: Message) -> None:
    if not users[message.from_user.id]['in_game']:
        await message.answer('Урраа!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать его!')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_randon_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру, я могу реагировать только '
                             'на числа от 1 до 100 и команды /cancel и /stat')

# Хэндлер для обработки отказа пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду', 'Отказ'], ignore_case=True))
async def process_negative_answer(message: Message) -> None:
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите сыграть - просто напишите об этом.')
    else:
        await message.answer('Мы жк сейчас с Вами играем. Присылайте, пожалуйста, числа от 1 до 100.')

# Хэндлер для обработки присылаемых пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message) -> None:
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Вы угадали число!\n\n'
                                 'Может, может сыграем ещё раз?')
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            users[message.from_user.id]['in_game'] = False
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Моё число меньше')
            users[message.from_user.id]['attempts'] -= 1
        else:
            await message.answer('Моё число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'К сожалению, у Вас больше не осталось попыток. Вы проиграли :(\n\n'
                                 f'Моё число было {users[message.from_user.id]["secret_number"]}\n\n'
                                 f'Давайте сыграем ещё раз?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Мы ещё не играем. Хотите сыграть?')


# Хэндлер для обработки любых других текстовых сообщений
@dp.message(F.content_type == ContentType.TEXT)
async def process_other_text_answer(message: Message) -> None:
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы сейчас с Вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я - довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')

if __name__ == '__main__':
    dp.run_polling(bot)