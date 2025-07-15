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
        bot.reply_to(message, "тебя тут не ждали. выйди")
        return
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 Запускай эту лютую машину")
    btn2 = types.KeyboardButton("🧊 Как дела на северном фронте?")
    markup.add(btn1, btn2)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "⛔тебя тут не ждали. выйди.")
        return

    if message.text == "🚀 Запускай эту лютую машину":
        bot.reply_to(message, "🏎️ Учитель Люкс проверяет запуск.")
        return

    elif message.text == "🧊 Как дела на северном фронте?":
        bot.reply_to(message, "❄️ Всё под контролем.")
        return
        
    code = message.text
    if any(x in code.lower() for x in ['import os', 'subprocess', 'open(', 'eval(', '__import__']):
        bot.reply_to(message, "Ноу-ноу, свити. Это слишком опасно.")
        return

    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        exec(code)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        if not output.strip():
            output = "✅ Код выполнен, но тихо как северный фронт"
        bot.reply_to(message, output)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка:\n{e}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN)
    app.run(host='0.0.0.0', port=10000)
