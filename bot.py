import telebot
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Админы — сюда будут приходить заявки
ADMINS = [8051652564, 8037207761, 8117502632, 8179965778]

# Ссылки и контакты
REVIEW_CHANNEL_LINK = "https://t.me/doc_of_service"
CONSULTANT_USERNAME = "@Serg_help"

# --- Главное меню ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚘 Международные права", "🧾 Проверка штрафов")
    markup.add("📜 Первичное получение прав", "⚖️ Помощь при лишении")
    markup.add("📢 Отзывы", "✅ Наши гарантии")
    markup.add("💬 Все вопросы к юристу")
    bot.send_message(message.chat.id,
        "👋 Добро пожаловать в *AutoLawBot* — юридическая помощь водителям!",
        parse_mode="Markdown",
        reply_markup=markup)

# --- Международные права ---
@bot.message_handler(func=lambda m: m.text == "🚘 Международные права")
def intl_license(message):
    bot.send_message(message.chat.id,
        "🌍 *Анкета для оформления международного ВУ:*")
    bot.send_message(message.chat.id,
        "1. ФИО:\n"
        "2. Дата рождения:\n"
        "3. Гражданство:\n"
        "4. Адрес проживания:\n"
        "5. Фото паспорта и национального ВУ (если есть):\n\n"
        "📩 Отправьте эти данные сюда — наш специалист свяжется с вами.",
        parse_mode="Markdown")
    bot.register_next_step_handler(message, handle_intl_license)

def handle_intl_license(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id,
                f"Новая заявка на международные права от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "Спасибо! Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_intl_license)

# --- Проверка штрафов ---
@bot.message_handler(func=lambda m: m.text == "🧾 Проверка штрафов")
def fines_form(message):
    bot.send_message(message.chat.id,
        "🧾 *Анкета для проверки штрафов и ограничений:*\n\n"
        "1. ФИО:\n"
        "2. Номер ВУ:\n"
        "3. Госномер автомобиля:\n"
        "4. Регион регистрации:\n\n"
        "📩 Отправьте эти данные сюда — мы всё проверим и свяжемся с вами.",
        parse_mode="Markdown")
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

# --- Первичное получение прав ---
@bot.message_handler(func=lambda m: m.text == "📜 Первичное получение прав")
def primary_license(message):
    bot.send_message(message.chat.id,
        "📜 *Анкета для первичного получения водительского удостоверения:*\n\n"
        "1. ФИО:\n"
        "2. Дата рождения:\n"
        "3. Гражданство:\n"
        "4. Адрес проживания:\n"
        "5. Фото паспорта:\n\n"
        "📩 Отправьте эти данные сюда — и мы начнём процесс.",
        parse_mode="Markdown")
    bot.register_next_step_handler(message, handle_primary_license)

def handle_primary_license(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id,
                f"Новая заявка на первичное получение ВУ от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "Спасибо! Ваша заявка отправлена. Ожидайте ответа.")
    else:
        bot.send_message(message.chat.id, "⚠️ Пожалуйста, отправьте данные текстом.")
        bot.register_next_step_handler(message, handle_primary_license)

# --- Помощь при лишении прав ---
@bot.message_handler(func=lambda m: m.text == "⚖️ Помощь при лишении")
def help_license(message):
    bot.send_message(message.chat.id,
        "⚖️ *Анкета для помощи при лишении ВУ:*\n\n"
        "1. ФИО:\n"
        "2. Дата рождения:\n"
        "3. Причина лишения (если известна):\n"
        "4. Дата лишения:\n\n"
        "📩 Отправьте эти данные сюда — юрист свяжется с вами и подскажет дальнейшие шаги.",
        parse_mode="Markdown")
    bot.register_next_step_handler(message, handle_help_license)

def handle_help_license(message):
    if message.content_type == 'text':
        user_data = message.text
        for admin_id in ADMINS:
            bot.send_message(admin_id,
                f"Новая заявка на помощь при лишении ВУ от @{message.from_user.username} (ID: {message.from_user.id}):\n\n{user_data}")
        bot.send_message(message.chat.id, "Спасибо! Ваша заявка отправлена. Ожидайте ответа.")
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
    bot.send_message(message.chat.id, "Фото/документ получены, спасибо! Ожидайте ответа.")

# --- Отзывы ---
@bot.message_handler(func=lambda m: m.text == "📢 Отзывы")
def show_reviews(message):
    bot.send_message(message.chat.id,
        f"🗣 Ознакомьтесь с отзывами наших клиентов:\n👉 {REVIEW_CHANNEL_LINK}")

# --- Гарантии ---
@bot.message_handler(func=lambda m: m.text == "✅ Наши гарантии")
def show_guarantees(message):
    bot.send_message(message.chat.id,
        "✅ *Наши гарантии:*\n\n"
        "- Работаем официально и законно.\n"
        "- Оформление без очередей и лишних бюрократий.\n"
        "- Полная прозрачность и сопровождение каждого клиента.\n"
        "- Проверенные юристы с опытом.\n"
        "- Все детали можно уточнить у консультанта или в отзывах.",
        parse_mode="Markdown")

# --- Контакт с юристом ---
@bot.message_handler(func=lambda m: m.text == "💬 Все вопросы к юристу")
def contact_lawyer(message):
    bot.send_message(message.chat.id,
        f"👨‍⚖️ По всем вопросам свяжитесь с нашим юристом напрямую:\n{CONSULTANT_USERNAME}\n\n"
        "📌 Он ответит на любые вопросы и подскажет по вашей ситуации.")

# --- Фолбэк ---
@bot.message_handler(content_types=["text"])
def fallback(message):
    bot.send_message(message.chat.id, "⚠️ Пожалуйста, выберите нужный раздел с клавиатуры.")

bot.polling(none_stop=True)
