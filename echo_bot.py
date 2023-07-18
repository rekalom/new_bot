import requests
import time

API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = '5920847035:AAF1NcN2CSyfR_9X9UbcRZDJLnDNn7YCZ8g'
TEXT: str = 'УРААААААА! ПРИВЕТТТ!!!!!'
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int
while counter < MAX_COUNTER:
    print('попытка = ', counter)      # Номер попытки, чтобы видеть, что код живёт
    updates = request.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()