import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN =  "7627324071:AAHKCFmbGK69EDzgShJ_CCyNorjnYLsTK3A"  # O'zingizning bot tokeningizni kiriting
bot = telebot.TeleBot(TOKEN)

admin_id = 6938841786  # Admin ID sini kiriting
user_ids = set()  # Foydalanuvchi ID larini saqlash

# **Asosiy menyu**
def main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    btn_ovoz = InlineKeyboardButton("🗳️ OVOZ BERISH", callback_data="ovoz_berish")
    markup.add(btn_ovoz)
    if chat_id == admin_id:
        btn_admin = InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin")
        markup.add(btn_admin)
    bot.send_message(chat_id, "Tugmalardan birini bosing:", reply_markup=markup)

# **/start komandasi**
@bot.message_handler(commands=['start'])
def start(message):
    user_ids.add(message.chat.id)
    main_menu(message.chat.id)

# **Ovoz berish paneli**
@bot.callback_query_handler(func=lambda call: call.data == "ovoz_berish")
def ovoz_berish(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_telegram = InlineKeyboardButton("🗳️ OVOZ BERISH (TELEGRAM)", url="https://t.me/ochiqbudjet_4_bot")
    btn_sayt = InlineKeyboardButton("🗳️ OVOZ BERISH (SAYT)", url="https://openbudget.uz/boards/initiatives/initiative/50/6c36c055-dcd4-4a5b-abd0-08617eb3c19a")
    btn_berdim = InlineKeyboardButton("✅ OVOZ berdim", callback_data="ovoz_berdim")
    btn_ortga = InlineKeyboardButton("⬅️ Ortga", callback_data="ortga")
    
    markup.add(btn_telegram, btn_sayt, btn_berdim, btn_ortga)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                          text="❗ Agar Telegram bot orqali ovoz bera olmasangiz, sayt orqali ovoz bering. ✅", 
                          reply_markup=markup)

# **Ortga qaytish**
@bot.callback_query_handler(func=lambda call: call.data == "ortga")
def ortga(call):
    main_menu(call.message.chat.id)

# **Telefon raqamini qabul qilish**
@bot.message_handler(content_types=['text'])
def get_number(message):
    if message.chat.id == admin_id:
        return

    number = message.text.strip()
    if (number.startswith("+998") and number[1:].isdigit() and len(number) == 13) or \
       (number.startswith("90") and number.isdigit() and len(number) == 9):
        user_ids.add(message.chat.id)
        bot.send_message(message.chat.id, "✅ Raqamingiz qabul qilindi! Admin tekshiradi.")
        bot.send_message(admin_id, f"Yangi ovoz beruvchi raqami: {number}")
    else:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri format! +998 yoki 90 bilan boshlangan to‘g‘ri raqam yuboring.")

# **Admin panel**
@bot.callback_query_handler(func=lambda call: call.data == "admin" and call.message.chat.id == admin_id)
def admin_panel(call):
    markup = InlineKeyboardMarkup(row_width=2)
    btn_statistika = InlineKeyboardButton("📊 Statistika", callback_data="statistika")
    btn_xabar = InlineKeyboardButton("✉️ Xabar yuborish", callback_data="xabar_yuborish")
    btn_ortga = InlineKeyboardButton("⬅️ Ortga", callback_data="ortga")

    markup.add(btn_statistika, btn_xabar, btn_ortga)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="👤 Admin paneliga xush kelibsiz!\nQuyidagilardan birini tanlang:", 
                          reply_markup=markup)

# **Statistika ko‘rsatish**
@bot.callback_query_handler(func=lambda call: call.data == "statistika" and call.message.chat.id == admin_id)
def statistika(call):
    bot.send_message(admin_id, f"📊 Botga yozgan foydalanuvchilar soni: {len(user_ids)}")

# **Xabar yuborish**
@bot.callback_query_handler(func=lambda call: call.data == "xabar_yuborish" and call.message.chat.id == admin_id)
def xabar_yuborish(call):
    msg = bot.send_message(admin_id, "✍ Xabar yuboring. Barcha foydalanuvchilarga yetkaziladi.")
    bot.register_next_step_handler(msg, send_to_all)

# **Hamma foydalanuvchilarga xabar yuborish**
def send_to_all(message):
    text = message.text
    if message.chat.id != admin_id:
        bot.send_message(message.chat.id, "Siz buni bajara olmaysiz.")
        return

    if not user_ids:
        bot.send_message(admin_id, "⚠️ Hali hech qanday foydalanuvchi yozmagan.")
        return

    for user_id in user_ids:
        try:
            bot.send_message(user_id, f"{text}")
        except:
            pass
    bot.send_message(admin_id, "✅ Xabar barcha foydalanuvchilarga yuborildi.")

# **Botni ishga tushirish**
bot.polling(non_stop=True)