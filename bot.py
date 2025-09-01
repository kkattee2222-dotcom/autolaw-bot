import os
import telebot
from flask import Flask, request
from telebot import types

BOT_TOKEN = "8473490832:AAG3i471zHemKSrk52bb7S4Yx_SxC9grvH0"
WEBHOOK_URL = "https://autolaw-bot-production.up.railway.app"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

ADMINS = [8179965778, 8117502632, 8037207761]
CONSULTANT_USERNAME = "@Serg_help"
REVIEW_CHANNEL_LINK = "@doc_of_service"

def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚘 Международные права", "🧾 Проверка штрафов")
    markup.add("📜 Первичное получение прав", "⚖️ Помощь при лишении")
    markup.add("📢 Отзывы", "✅ Наши гарантии")
    markup.add("💬 Все вопросы к юристу")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в *AutoLawBot* — юридическая помощь водителям!\n\n"
        "📌 Мы оформляем документы только официально, без очередей.\n"
        "⚖️ Наши юристы проверены и имеют опыт работы.",
        parse_mode="Markdown",
        reply_markup=main_menu_markup()
    )

def send_to_admins(user, data, title):
    for admin_id in ADMINS:
        bot.send_message(admin_id, f"💼 *{title}*\nОт @{user.username} (ID: {user.id}):\n\n{data}", parse_mode="Markdown")
    bot.send_message(user.id, "✅ Спасибо! Ваша заявка отправлена. Ожидайте ответа.")

def handle_text_form(message, title):
    if message.content_type == 'text':
        send_to_admins(message.from_user, message.text, title)
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, lambda m: handle_text_form(m, title))

@bot.message_handler(func=lambda m: m.text == "🚘 Международные права")
def intl_license(message):
    bot.send_message(message.chat.id, "🌍 *Анкета для международного ВУ:*\n1. ФИО\n2. Дата рождения\n3. Гражданство\n4. Адрес\n5. Фото паспорта и ВУ", parse_mode="Markdown")
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Заявка на международные права"))

@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Бот работает!", 200

# Установка webhook перед запуском Flask
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
