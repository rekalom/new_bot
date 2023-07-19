from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN: str = 'BOT TOKEN HERE'

# Создаём объекты бота и деспетчера
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher()

# Хэндлер для команды "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message) -> None:
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь!')

# Хэндлер для команды "help"
@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message) -> None:
    await message.answer('Напиши мне что-нибуть, и я пришлю'
                         'тебе в ответ твоё же сообщение!')

# Хэндлер для любых текстовых сообщений,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message) -> None:
    await message.reply(text=message.text)

if __name__ == '__main__':
    dp.run_polling(bot)