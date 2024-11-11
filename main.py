import os
import time

import requests
from dotenv import load_dotenv

START_COMMAND = '/start'
HELP_COMMAND = '/help'
HELP_COMMAND_ALIAS = 'Помощь'
SEND_TO_ADMIN_COMMAND = 'Связаться с администратором'
ABOUT_BOT_MESSAGE = "Я бот для обмена сообщениями с администратором."
HELP_MESSAGE = f"{ABOUT_BOT_MESSAGE}\n\n" \
               f"{START_COMMAND} - Перезапуск бота\n" \
               f"{HELP_COMMAND}- Показать справку\n\n" \
               "Используйте меню, чтобы связаться с администратором или получить помощь."
GREETING_MESSAGE = f'Добро пожаловать! {ABOUT_BOT_MESSAGE} Выберите действие из меню ниже.'
INVITE_MESSAGE = "Ваше сообщение будет передано администратору. Пожалуйста, напишите свой вопрос."
CONFIRM_MESSAGE = 'Ваше сообщение передано администратору.'

# Загрузка переменных из .env
load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not API_TOKEN or not ADMIN_CHAT_ID:
    raise ValueError("API_TOKEN и ADMIN_CHAT_ID должны быть заданы в файле .env")

BOT_URL = f'https://api.telegram.org/bot{API_TOKEN}'


def get_updates(offset=None):
    url = f'{BOT_URL}/getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()


def send_message(chat_id, text, reply_markup=None):
    """Функция для отправки сообщений с кнопками"""

    url = f'{BOT_URL}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup
    }
    try:
        if reply_markup:
            requests.post(url, json=data)
        else:
            requests.post(url, data=data)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка отправки сообщения: {e}")


def handle_command(text, chat_id) -> bool:
    """Функция обработки текста, как команды. Возвращает False, если текст не является командой"""

    is_command = True

    if text == START_COMMAND:
        reply_markup = {
            "keyboard": [
                [{"text": SEND_TO_ADMIN_COMMAND}],
                [{"text": HELP_COMMAND_ALIAS}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False  # Клавиатура будет постоянно видна
        }
        send_message(chat_id, GREETING_MESSAGE, reply_markup=reply_markup)
    elif text in [HELP_COMMAND, HELP_COMMAND_ALIAS]:
        send_message(chat_id, HELP_MESSAGE)
    elif text == SEND_TO_ADMIN_COMMAND:
        send_message(chat_id, INVITE_MESSAGE)
    else:
        is_command = False
    return is_command


def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            update_id = update['update_id']
            message = update.get('message')
            user_id = message['chat']['id']
            message_text = message['text']

            # Обработка команд
            if not handle_command(message_text, user_id):
                if str(user_id) != ADMIN_CHAT_ID:
                    # Пересылаем сообщение администратору
                    send_message(ADMIN_CHAT_ID, f'User {user_id}: {message_text}')
                    send_message(user_id, CONFIRM_MESSAGE)
                else:
                    # Ответ от админа отправляем обратно пользователю
                    user_chat_id = message['reply_to_message']['chat']['id'] if 'reply_to_message' in message else None
                    if user_chat_id:
                        send_message(user_chat_id, message_text)
            # Обновляем offset для следующего запроса
            offset = update_id + 1

        time.sleep(1)  # Задержка перед следующим запросом


if __name__ == '__main__':
    main()
