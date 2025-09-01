import os
from flask import Flask, request
import telebot
from telebot import types

# --- Настройки ---
BOT_TOKEN = "8473490832:AAG3i471zHemKSrk52bb7S4Yx_SxC9grvH0"  # токен прямо в коде
WEBHOOK_URL = "https://твой-проект-на-railway.app"  # вставь ссылку на свой проект Railway

ADMINS = [8179965778, 8117502632, 8037207761]  # ID админов
CONSULTANT_USERNAME = "@Serg_help"  # юрист
REVIEW_CHANNEL_LINK = "@doc_of_service"  # канал с отзывами

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Главное меню ---
def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🚘 Международные права", "🧾 Проверка штрафов")
    markup.row("📜 Первичное получение прав", "⚖️ Помощь при лишении")
    markup.row("📢 Отзывы", "✅ Наши гарантии")
    markup.row("💬 Все вопросы к юристу")
    return markup

# --- Старт ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в *AutoLawBot* — ваш надёжный помощник по юридическим вопросам водителей!\n\n"
        "📌 Мы оформляем документы *только официально* и полностью сопровождаем каждый процесс.\n"
        "🛡️ Надёжность, конфиденциальность и качество — наш приоритет!",
        parse_mode="Markdown",
        reply_markup=main_menu_markup()
    )

# --- Международные права ---
@bot.message_handler(func=lambda m: m.text == "🚘 Международные права")
def intl_license(message):
    bot.send_message(message.chat.id,
                     "🌍 *Анкета для оформления международного ВУ:*\n\n"
                     "1. ФИО:\n2. Дата рождения:\n3. Гражданство:\n4. Адрес проживания:\n5. Фото паспорта и национального ВУ (если есть)\n\n"
                     "📩 Отправьте данные сюда — наш специалист свяжется с вами.",
                     parse_mode="Markdown")
    bot.register_next_step_handler(message, handle_intl_license)

def handle_intl_license(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id, f"Новая заявка на международные права от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "✅ Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_intl_license)

# --- Проверка штрафов ---
@bot.message_handler(func=lambda m: m.text == "🧾 Проверка штрафов")
def fines_form(message):
    bot.send_message(message.chat.id,
                     "🧾 *Анкета для проверки штрафов:*\n\n"
                     "1. ФИО:\n2. Номер ВУ:\n3. Госномер автомобиля:\n4. Регион регистрации\n\n"
                     "📩 Отправьте данные сюда — мы проверим и свяжемся с вами.",
                     parse_mode="Markdown")
    bot.register_next_step_handler(message, handle_fines_form)

def handle_fines_form(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id, f"Новая заявка на проверку штрафов от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "✅ Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_fines_form)

# --- Первичное получение прав ---
@bot.message_handler(func=lambda m: m.text == "📜 Первичное получение прав")
def primary_license(message):
    bot.send_message(message.chat.id,
                     "📜 *Анкета для первичного получения ВУ:*\n\n"
                     "1. ФИО\n2. Дата рождения\n3. Гражданство\n4. Адрес проживания\n5. Фото паспорта\n\n"
                     "📩 Отправьте данные сюда — начнем оформление.",
                     parse_mode="Markdown")
    bot.register_next_step_handler(message, handle_primary_license)

def handle_primary_license(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id, f"Новая заявка на первичное получение ВУ от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "✅ Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_primary_license)

# --- Помощь при лишении ---
@bot.message_handler(func=lambda m: m.text == "⚖️ Помощь при лишении")
def help_license(message):
    bot.send_message(message.chat.id,
                     "⚖️ *Анкета для помощи при лишении ВУ:*\n\n"
                     "1. ФИО\n2. Дата рождения\n3. Причина лишения (если известна)\n4. Дата лишения\n\n"
                     "📩 Отправьте данные сюда — юрист свяжется с вами.",
                     parse_mode="Markdown")
    bot.register_next_step_handler(message, handle_help_license)

def handle_help_license(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id, f"Новая заявка на помощь при лишении ВУ от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "✅ Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_help_license)

# --- Медиа ---
@bot.message_handler(content_types=['photo', 'document'])
def handle_media(message):
    for admin_id in ADMINS:
        if message.content_type == 'photo':
            bot.send_photo(admin_id, message.photo[-1].file_id, caption=f"Фото от @{message.from_user.username}")
        elif message.content_type == 'document':
            bot.send_document(admin_id, message.document.file_id, caption=f"Документ от @{message.from_user.username}")
    bot.send_message(message.chat.id, "✅ Фото/документ получены. Ожидайте ответа.")

# --- Отзывы ---
@bot.message_handler(func=lambda m: m.text == "📢 Отзывы")
def show_reviews(message):
    bot.send_message(message.chat.id, f"🗣 Ознакомьтесь с отзывами клиентов:\n👉 {REVIEW_CHANNEL_LINK}")

# --- Гарантии ---
@bot.message_handler(func=lambda m: m.text == "✅ Наши гарантии")
def show_guarantees(message):
    bot.send_message(message.chat.id,
                     "✅ *Наши гарантии:*\n"
                     "- Работаем официально и законно\n"
                     "- Полное сопровождение от подачи документов до готовности\n"
                     "- Быстрое оформление без очередей\n"
                     "- Проверенные юристы с опытом 5+ лет\n"
                     "- Полная прозрачность и доверие",
                     parse_mode="Markdown")

# --- Контакт с юристом ---
@bot.message_handler(func=lambda m: m.text == "💬 Все вопросы к юристу")
def contact_lawyer(message):
    bot.send_message(message.chat.id, f"👨‍⚖️ Свяжитесь с юристом: {CONSULTANT_USERNAME}")

# --- Фолбэк ---
@bot.message_handler(content_types=["text"])
def fallback(message):
    bot.send_message(message.chat.id, "⚠️ Пожалуйста, используйте меню бота.")

# --- Webhook для Railway ---
app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# --- Запуск webhook ---
bot.remove_webhook()
bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
