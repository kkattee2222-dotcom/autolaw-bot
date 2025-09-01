import os
import telebot
from flask import Flask, request
from telebot import types

# =========================
# Настройки бота
BOT_TOKEN = "8473490832:AAG3i471zHemKSrk52bb7S4Yx_SxC9grvH0"
WEBHOOK_URL = "https://autolaw-bot-production.up.railway.app"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Админы, которые получают заявки
ADMINS = [8179965778, 8117502632, 8037207761]

# Юрист и канал с отзывами
CONSULTANT_USERNAME = "@Serg_help"
REVIEW_CHANNEL_LINK = "https://t.me/doc_of_service"

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
        "📌 Мы оформляем документы только официально, без очередей.\n"
        "⚖️ Наши юристы проверены и имеют большой опыт работы.",
        parse_mode="Markdown",
        reply_markup=main_menu_markup()
    )

# =========================
# Универсальная отправка заявок админам
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
# Международные права
@bot.message_handler(func=lambda m: m.text == "🚘 Международные права")
def intl_license(message):
    bot.send_message(
        message.chat.id,
        "🌍 *Анкета для оформления международного ВУ:*\n"
        "1. ФИО\n"
        "2. Дата рождения\n"
        "3. Гражданство\n"
        "4. Адрес проживания\n"
        "5. Фото паспорта и национального ВУ (если есть)",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Заявка на международные права"))

# =========================
# Проверка штрафов
@bot.message_handler(func=lambda m: m.text == "🧾 Проверка штрафов")
def fines_form(message):
    bot.send_message(
        message.chat.id,
        "🧾 *Анкета для официальной проверки штрафов и ограничений:*\n"
        "1. ФИО\n"
        "2. Номер водительского удостоверения\n"
        "3. Госномер автомобиля\n"
        "4. Регион регистрации\n\n"
        "📌 Все данные обрабатываются официально и проверяются юристами.",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Проверка штрафов"))

# =========================
# Первичное получение прав
@bot.message_handler(func=lambda m: m.text == "📜 Первичное получение прав")
def primary_license(message):
    bot.send_message(
        message.chat.id,
        "📜 *Анкета для первичного получения водительского удостоверения:*\n"
        "1. ФИО\n"
        "2. Дата рождения\n"
        "3. Гражданство\n"
        "4. Адрес проживания\n"
        "5. Фото паспорта\n"
        "📌 Все документы оформляются официально, с полным сопровождением юриста.",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, lambda m: handle_text_form(m, "Первичное получение ВУ"))

# =========================
# Помощь при лишении
@bot.message_handler(func=lambda m: m.text == "⚖️ Помощь при лишении")
def help_license(message):
    bot.send_message(
        message.chat.id,
        "⚖️ *Анкета для помощи при лишении ВУ:*\n"
        "1. ФИО\n"
        "2. Дата рождения\n"
        "3. Причина лишения\n"
        "4. Дата лишения\n"
        "5. Были ли обжалования и решения суда?\n\n"
        "📌 Все обращения оформляются официально, юрист проверяет все документы и действия.",
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
    bot.send_message(message.chat.id, "✅ Фото/документ получены. Ожидайте ответа.")

# =========================
# Отзывы и гарантии
@bot.message_handler(func=lambda m: m.text == "📢 Отзывы")
def show_reviews(message):
    bot.send_message(message.chat.id, f"🗣 Ознакомьтесь с отзывами клиентов:\n👉 {REVIEW_CHANNEL_LINK}")

@bot.message_handler(func=lambda m: m.text == "✅ Наши гарантии")
def show_guarantees(message):
    bot.send_message(
        message.chat.id,
        "✅ *Наши гарантии:*\n"
        "- Работаем официально и законно.\n"
        "- Полное сопровождение каждого клиента.\n"
        "- Проверенные юристы с опытом.\n"
        "- Прозрачность и безопасность всех операций.\n"
        "- Все детали можно уточнить у консультанта или в отзывах.",
        parse_mode="Markdown"
    )

# =========================
# Контакт с юристом
@bot.message_handler(func=lambda m: m.text == "💬 Все вопросы к юристу")
def contact_lawyer(message):
    bot.send_message(
        message.chat.id,
        f"👨‍⚖️ Свяжитесь напрямую с юристом:\n{CONSULTANT_USERNAME}\n\n"
        "📌 Он ответит на любые вопросы и подскажет по вашей ситуации."
    )

# =========================
# Фолбэк
@bot.message_handler(content_types=["text"])
def fallback(message):
    bot.send_message(message.chat.id, "⚠️ Пожалуйста, выберите раздел с клавиатуры.")

# =========================
# Webhook для Railway
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Бот работает!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
