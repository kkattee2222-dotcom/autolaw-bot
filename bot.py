import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

REVIEW_CHANNEL_LINK = "https://t.me/doc_of_service"
CONSULTANT_USERNAME = "@Serg_help"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚘 Анкета на международные права", "🧾 Проверка штрафов и арестов")
    markup.add("📢 Отзывы", "💬 Связаться с юристом")
    bot.send_message(message.chat.id,
        "👋 Добро пожаловать в AutoLawBot — юридическая помощь водителям!\n\n"
        "Выберите нужный раздел:",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🚘 Анкета на международные права")
def vudoc_form(message):
    bot.send_message(message.chat.id,
        "🌍 Анкета для оформления международного ВУ:\n\n"
        "1. ФИО:\n"
        "2. Дата рождения:\n"
        "3. Гражданство:\n"
        "4. Адрес проживания:\n"
        "5. Фото паспорта и национального ВУ (если есть):\n\n"
        "📩 Отправьте эти данные сюда — наш специалист свяжется с вами.")

@bot.message_handler(func=lambda m: m.text == "🧾 Проверка штрафов и арестов")
def fines_form(message):
    bot.send_message(message.chat.id,
        "🧾 Анкета для проверки штрафов и административных ограничений:\n\n"
        "1. ФИО:\n"
        "2. Номер ВУ:\n"
        "3. Госномер автомобиля:\n"
        "4. Регион регистрации:\n\n"
        "📩 Отправьте эти данные сюда — мы всё проверим и свяжемся с вами.")

@bot.message_handler(func=lambda m: m.text == "📢 Отзывы")
def show_reviews(message):
    bot.send_message(message.chat.id,
        f"🗣 Ознакомьтесь с отзывами наших клиентов:\n👉 {REVIEW_CHANNEL_LINK}")

@bot.message_handler(func=lambda m: m.text == "💬 Связаться с юристом")
def contact_lawyer(message):
    bot.send_message(message.chat.id,
        f"👨‍⚖️ Свяжитесь с нашим консультантом напрямую:\n{CONSULTANT_USERNAME}")

@bot.message_handler(content_types=["text"])
def fallback(message):
    bot.send_message(message.chat.id, "⚠️ Пожалуйста, выберите нужный раздел с клавиатуры.")

bot.polling(none_stop=True)
