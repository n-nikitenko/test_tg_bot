# Telegram Bot для передачи сообщений администратору

## Пример использования

После запуска бота пользователь может начать диалог, нажав команду ***/start***.

В меню пользователю доступны команды:

- Связаться с администратором — отправить сообщение администратору.
- Помощь — получить справочную информацию.
-

Администратор видит сообщения пользователей и может ответить на них, отправляя сообщения через бота.
Ответы автоматически пересылаются соответствующему пользователю.

## Функции

- Обработка команд:
    - `/start`: Перезапуск бота и вывод приветственного сообщения.
    - `/help`: Показывает справочную информацию о доступных командах.
    - **Связаться с администратором**: Отправляет сообщение администратору.

- Основное меню с кнопками для выбора действия (доступно постоянно).
- Автоматическая пересылка сообщений от пользователей к администратору и ответов администратора пользователю.

## Установка и настройка

1. Склонируйте репозиторий или загрузите исходный код.
2. Установите зависимости:
   ```
   poetry install
   ```
3. Создайте файл .env в корневом каталоге и добавьте в него следующие переменные:

  ```commandline
    API_TOKEN=<ваш_токен_бота>
    ADMIN_CHAT_ID=<ID_администратора>
  ```

4. Запустите бота:

  ```commandline
    python bot.py
  ```