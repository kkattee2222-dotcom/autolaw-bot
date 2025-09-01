import telebot
from telebot import types
from flask import Flask, request

# =========================
BOT_TOKEN = "8473490832:AAG3i471zHemKSrk52bb7S4Yx_SxC9grvH0"
WEBHOOK_URL = "https://autolaw-bot-production.up.railway.app"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Админы
ADMINS = [8179965778, 8117502632, 8037207761]

# Юрист и канал отзывов
CONSULTANT_USERNAME = "@Serg_help"
REVIEW_CHANNEL_LINK = "@doc_of_service"

# =========================
# Главное меню
def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚘 Международные права", "🧾 Проверка штрафов")
    markup.add("📜 Первичное получение прав", "⚖️ Помощь при лишении")
    markup.add("📢 Отзывы", "✅ Наши гарантии")
    markup.add("💬 Все вопросы к юристу")
    return markup

# =========================
# Старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в *AutoLawBot* — юридическая помощь водителям!\n\n"
        "📌 Мы оформляем документы только официально, без очередей и лишней бюрократии.\n"
        "⚖️ Наши юристы проверены и имеют опыт работы.",
        parse_mode="Markdown",
        reply_markup=main_menu_markup()
    )

# =========================
# Универсальная функция отправки заявок админам
def send_to_admins(user, data, title):
    for admin_id in ADMINS:
        bot.send_message(
            admin_id,
            f"💼 *{title}*\nОт @{user.username} (ID: {user.id}):\n\n{data}",
            parse_mode="Markdown"
        )
    bot.send_message(user.id, "✅ Спасибо! Ваша заявка отправлена. Ожидайте ответа.")

def handle_text_form(message, title):
    if message.content_type == 'text':
        send_to_admins(message.from_user, message.text, title)
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, lambda m: handle_text_form(m, title))

# =========================
# Разделы меню
@bot.message_handler(func=lambda m: m.text == "🚘 Международные права")
def intl_license(message):
    bot.send_message(
        message.chat.id,
        "🌍 *Анкета для оформления международного ВУ:*\n"
        "1. ФИО:\n2. Дата рождения:\n3. Гражданство:\n4. Адрес проживания:\n5. Фото паспорта и национального ВУ (если есть):",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Заявка на международные права"))

@bot.message_handler(func=lambda m: m.text == "🧾 Проверка штрафов")
def fines_form(message):
    bot.send_message(
        message.chat.id,
        "🧾 *Анкета для проверки штрафов и ограничений:*\n"
        "1. ФИО:\n2. Номер ВУ:\n3. Госномер автомобиля:\n4. Регион регистрации:",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Проверка штрафов"))

@bot.message_handler(func=lambda m: m.text == "📜 Первичное получение прав")
def primary_license(message):
    bot.send_message(
        message.chat.id,
        "📜 *Анкета для первичного получения ВУ:*\n"
        "1. ФИО:\n2. Дата рождения:\n3. Гражданство:\n4. Адрес проживания:\n5. Фото паспорта:",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Первичное получение ВУ"))

@bot.message_handler(func=lambda m: m.text == "⚖️ Помощь при лишении")
def help_license(message):
    bot.send_message(
        message.chat.id,
        "⚖️ *Анкета для помощи при лишении ВУ:*\n"
        "1. ФИО:\n2. Дата рождения:\n3. Причина лишения (если известна):\n4. Дата лишения:",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Помощь при лишении ВУ"))

# =========================
# Фото и документы
@bot.message_handler(content_types=['photo', 'document'])
def handle_media(message):
    for admin_id in ADMINS:
        if message.content_type == 'photo':
            bot.send_photo(admin_id, message.photo[-1].file_id, caption=f"Фото от @{message.from_user.username}")
        elif message.content_type == 'document':
            bot.send_document(admin_id, message.document.file_id, caption=f"Документ от @{message.from_user.username}")
    bot.send_message(message.chat.id, "Фото/документ получены, спасибо! Ожидайте ответа.")

# =========================
# Отзывы и гарантии
@bot.message_handler(func=lambda m: m.text == "📢 Отзывы")
def show_reviews(message):
    bot.send_message(message.chat.id, f"🗣 Ознакомьтесь с отзывами клиентов:\n👉 {REVIEW_CHANNEL_LINK}")

@bot.message_handler(func=lambda m: m
