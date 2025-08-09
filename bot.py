import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Твои админы — сюда будут приходить заявки
ADMINS = [8051652564, 8037207761, 8117502632, 8179965778]

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
    bot.register_next_step_handler(message, handle_vudoc_form)

def handle_vudoc_form(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id,
                f"Новая заявка на международные права от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "Спасибо! Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_vudoc_form)

@bot.message_handler(func=lambda m: m.text == "🧾 Проверка штрафов и арестов")
def fines_form(message):
    bot.send_message(message.chat.id,
        "🧾 Анкета для проверки штрафов и административных ограничений:\n\n"
        "1. ФИО:\n"
        "2. Номер ВУ:\n"
        "3. Госномер автомобиля:\n"
        "4. Регион регистрации:\n\n"
        "📩 Отправьте эти данные сюда — мы всё проверим и свяжемся с вами.")
    bot.register_next_step_handler(message, handle_fines_form)

def handle_fines_form(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id,
                f"Новая заявка на проверку штрафов от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "Спасибо! Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_fines_form)

@bot.message_handler(content_types=['photo', 'document'])
def handle_media(message):
    for admin_id in ADMINS:
        if message.content_type == 'photo':
            bot.send_photo(admin_id, message.photo[-1].file_id, caption=f"Фото от @{message.from_user.username}")
        elif message.content_type == 'document':
            bot.send_document(admin_id, message.document.file_id, caption=f"Документ от @{message.from_user.username}")
    bot.send_message(message.chat.id, "Фото/документ получены, спасибо! Ожидайте ответа.")

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
