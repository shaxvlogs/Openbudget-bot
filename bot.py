import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '7627324071:AAGAUGl7hCPfw0FKMvwSct00V3lANzNrIk4'  # Tokeningizni shu yerga kiriting
bot = telebot.TeleBot(TOKEN)

admin_id = 6938841786  # Adminning chat ID

# **Asosiy menyu**
def main_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_ovoz_telegram = telebot.types.KeyboardButton("🗳️ OVOZ BERISH (TELEGRAM)")
    btn_ovoz_sayt = telebot.types.KeyboardButton("🗳️ OVOZ BERISH (SAYT)")
    btn_ovoz_berdim = telebot.types.KeyboardButton("✅ Ovoz berdim")
    btn_admin = telebot.types.KeyboardButton("⚙️ Admin Panel") if message.chat.id == admin_id else None
    btn_ortga = telebot.types.KeyboardButton("⬅️ Ortga")
    
    if btn_admin:
        markup.add(btn_ovoz_telegram, btn_ovoz_sayt, btn_ovoz_berdim, btn_admin, btn_ortga)
    else:
        markup.add(btn_ovoz_telegram, btn_ovoz_sayt, btn_ovoz_berdim, btn_ortga)
    
    bot.send_message(message.chat.id, "Tugmalardan birini tanlang:", reply_markup=markup)

# **/start komandasi**
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message)

# **Tugmalar bosilganda ishlovchi handler**
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id

    if message.text == "🗳️ OVOZ BERISH (TELEGRAM)":
        bot.send_message(chat_id, "Ovoz berish uchun ushbu havolaga kiring: https://t.me/ochiqbudjet_4_bot")

    elif message.text == "🗳️ OVOZ BERISH (SAYT)":
        bot.send_message(chat_id, "Ovoz berish uchun ushbu havolaga kiring: https://openbudget.uz/boards/initiatives/initiative/50/6c36c055-dcd4-4a5b-ab5b-abcd1234")

    elif message.text == "✅ Ovoz berdim":
        bot.send_message(chat_id, "📞 Ovoz bergan raqamingizni yuboring:\n\nMasalan: +998901234567")

    elif message.text == "⬅️ Ortga":
        main_menu(message)

    elif message.text == "⚙️ Admin Panel" and chat_id == admin_id:
        admin_menu(message)

    elif message.text == "📊 Statistika" and chat_id == admin_id:
        user_count = bot.get_chat_member_count(chat_id)  
        bot.send_message(admin_id, f"📊 Bot foydalanuvchilar soni: {user_count}")

    elif message.text == "✉️ Xabar yuborish" and chat_id == admin_id:
        msg = bot.send_message(admin_id, "📩 Xabar yuboring. Hamma foydalanuvchilarga yetkaziladi.")
        bot.register_next_step_handler(msg, send_to_all)

    elif message.text.startswith("+") or message.text.replace(" ", "").isdigit():
        bot.send_message(chat_id, "✅ Raqamingiz qabul qilindi! Admin tekshiradi.")
        bot.send_message(admin_id, f"Yangi ovoz beruvchi raqami: {message.text}")

    else:
        bot.send_message(chat_id, "⚠️ Tugmalardan birini tanlang!")

# **Admin panel menyusi**
def admin_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_statistika = telebot.types.KeyboardButton("📊 Statistika")
    btn_xabar = telebot.types.KeyboardButton("✉️ Xabar yuborish")
    btn_ortga = telebot.types.KeyboardButton("⬅️ Ortga")
    markup.add(btn_statistika, btn_xabar, btn_ortga)
    bot.send_message(message.chat.id, "👤 Admin paneliga xush kelibsiz!\nQuyidagilardan birini tanlang:", reply_markup=markup)

# **Xabarni barcha foydalanuvchilarga yuborish**
def send_to_all(message):
    users = bot.get_chat_administrators(message.chat.id)  # Foydalanuvchilarni olish
    for user in users:
        try:
            bot.send_message(user.user.id, f"📢 {message.text}")
        except:
            continue
    bot.send_message(admin_id, "✅ Xabar barcha foydalanuvchilarga yuborildi!")

# **Botni ishga tushirish**
bot.polling(none_stop=True)