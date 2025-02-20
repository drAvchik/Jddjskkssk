import logging
import telebot
from telebot import types

API_TOKEN = "6897266627:AAHmZJsecF6I-3QtM7MFtuomga0VYYrXeKg"

bot = telebot.TeleBot(API_TOKEN)
logging.basicConfig(level=logging.INFO)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👱‍♂️Профиль", "📝Повідомити")
    markup.row("⤵️Отримати інформацію", "🗄Пошук профілю")
    markup.row("📊Статистика", "👨‍👩‍👧‍👧Про нас", "👑Топ-3")

    welcome_message = (
        f"⚡️ Привіт, {message.from_user.first_name}!\n\n"
        f"Бот призначений для відстеження скаму та поганих роботяг в різних сферах надання послуг.\n\n"
        f"Якщо у вас є що розповісти нам або ви хочете дізнатися більше про людину з якою збираєтесь провести угоду, "
        f"скористайтесь кнопками нижче.\n\nБазу даних поповнюють щодня, і всіх скамерів тут немає.\n"
        f"Але ви можете дізнатися статистику, натиснувши відповідну кнопку!\n\n"
        f"АДМІНІСТРАТОР - @CTPAX_CBATTUHGAA"
    )

    bot.send_message(message.chat.id, text=welcome_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👱‍♂️Профиль")
def profile(message):
    profile_info = (
        f"📋 ID: {message.from_user.id}\n"
        f"🚹 ЮзерНейм: {message.from_user.username}\n"
        f"📝 Реєстрація: {message.date}\n"  # Display the current date
        "✅ Статус: КОРИСТУВАЧ\n"
        "💬 Принятих заявок: 0\n"
        "👁 Гарант LZT: Ви не заблоковані"
    )
    bot.send_message(message.chat.id, text=profile_info)

@bot.message_handler(func=lambda message: message.text == "📝Повідомити")
def inform(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_button = types.KeyboardButton("Назад")
    markup.add(back_button)
    inform_message = (
        "🆔 Вкажіть актуальний на даний момент UID порушника, "
        "якщо ви не знаєте його - вкажіть 0\n\n"
        "Якщо ви потрапили сюди випадково - просто натисніть Назад."
    )
    bot.send_message(message.chat.id, text=inform_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "⤵️Отримати інформацію")
def get_information(message):
    info_message = (
        "🌏 За якими даними ви хочете знайти підозрюваного?\n\n"
        "Просто надішліть у чат відомі вам дані.\n\n"
        "Приклади:\n"
        "UID - 5233478398\n"
        "Username - @username\n"
        "Номер телефону/картки - +38099999999 (або ваше значення, можливі крипто-гаманці)\n"
        "Код заявки - egpdn4xiq"
    )
    bot.send_message(message.chat.id, text=info_message)

@bot.message_handler(func=lambda message: message.text == "🗄Пошук профілю")
def search_profile(message):
    search_result = "👁 Info: 🗄Пошук профілю\n\nСкарг не виявлено."
    bot.send_message(message.chat.id, text=search_result)

@bot.message_handler(func=lambda message: message.text == "📊Статистика")
def statistics(message):
    statistics_message = (
        "✨ На сьогоднішній день наш бот налічує 691 користувачів, з яких 5 є перевіреними нами!\n"
        "👮 Загальна кількість заявок про скаму: 780"
    )
    bot.send_message(message.chat.id, text=statistics_message)

@bot.message_handler(func=lambda message: message.text == "👨‍👩‍👧‍👧Про нас")
def about_us(message):
    markup = types.InlineKeyboardMarkup()
    admin_button = types.InlineKeyboardButton("Адміністратор", url="https://t.me/CTPAX_CBATTUHGAA")
    channel_button = types.InlineKeyboardButton("Наш канал (поки доступ закрито)", url="https://example.com/channel")
    markup.row(admin_button, channel_button)

    about_us_message = (
        "Привіт! Ми є звичайними роботягами, які вирішили допомогти людям зберегти їхні гроші при проведенні угод. "
        "Бот був розроблений з нуля. Всі дані в боті отримані власноруч чи за допомогою наших користувачів, які повідомляють про скамерів. "
        "Ми постійно поповнюємо базу даних та розробляємо нові функції для перевірки людини."
    )

    bot.send_message(message.chat.id, text=about_us_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "👑Топ-3")
def top_users(message):
    top_users_message = (
        "🤴 Топ користувачів:\n\n"
        "Applone - 13 принятих заявок\n"
        "WorkWolf - 9 принятих заявок\n"
        "u͓̽H͓̽o͓̽K͓̽ [ Work 8am - 8pm UTC | No-DM ] - 5 принятих заявок"
    )
    bot.send_message(message.chat.id, text=top_users_message)

@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    start(message)

if __name__ == '__main__':
    bot.polling()
