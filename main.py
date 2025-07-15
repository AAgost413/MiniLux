import telebot
import io
import sys
import os
from telebot import types
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
ALLOWED_USER_ID = 880913516

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот мини Люкс онлайн! 🛸"

@app.route('/' + TOKEN, methods=['POST'])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "⛔ Доступ запрещён.")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🚀 Запуск"), types.KeyboardButton("🧊 Состояние фронта"))
    bot.send_message(message.chat.id, "🏁 Мини Люкс к бою готов", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_code(message):
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "⛔ Нет доступа.")
        return

    if message.text == "🚀 Запуск":
        bot.reply_to(message, "Тачка заведена 🏎️")
        return
    elif message.text == "🧊 Состояние фронта":
        bot.reply_to(message, "Фронт держим! ❄️")
        return

    if any(x in message.text.lower() for x in ['import os', 'subprocess', 'eval(', '__import__']):
        bot.reply_to(message, "Ноу-ноу, командирка.")
        return

    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        exec(message.text)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        if not output.strip():
            output = "✅ Код выполнен, но молчит"
        bot.reply_to(message, output)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка:\n{e}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN)
    app.run(host='0.0.0.0', port=10000)
