import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot tokeni
TOKEN = '7627324071:AAGAUGl7hCPfw0FKMvwSct00V3lANzNrIk4'
bot = telebot.TeleBot(TOKEN)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    btn_ovoz = InlineKeyboardButton("🗳️ OVOZ BERISH", callback_data="ovoz_berish")
    markup.add(btn_ovoz)
    bot.send_message(message.chat.id, "🎁 Har bir ovoz uchun 30.000 so'mdan pul mukofoti va qo'shimcha sovrinlar yutib olish uchun ovoz bering.\n2TA OVOZ UCHUN 70.000 SO'M\n\n👉 Ovoz berish uchun tugmani bosing.", reply_markup=markup)

# Ovoz berish paneli
@bot.callback_query_handler(func=lambda call: call.data == "ovoz_berish")
def ovoz_berish(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_telegram = InlineKeyboardButton("🗳️ OVOZ BERISH (TELEGRAM)", url="https://t.me/ochiqbudjet_007_bot")
    btn_sayt = InlineKeyboardButton("🗳️ OVOZ BERISH (SAYT)", url="https://openbudget.uz/boards/initiatives/initiative/50/6c36c055-dcd4-4a5b-abd0-08617eb3c19a")
    btn_berdim = InlineKeyboardButton("✅ OVOZ BERDIM", callback_data="ovoz_berdim")
    btn_ortga = InlineKeyboardButton("⬅️ Ortga", callback_data="ortga")
    
    markup.add(btn_telegram, btn_sayt, btn_berdim, btn_ortga)
    
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id, 
                          text="❗ AGAR TELEGRAM BOT ORQALI OVOZ BERA OLMASANGIZ SAYT ORQALI OVOZ BERING. Omad ✅", 
                          reply_markup=markup)

# Ovoz berdim tugmasi
@bot.callback_query_handler(func=lambda call: call.data == "ovoz_berdim")
def ovoz_berdim(call):
    markup = InlineKeyboardMarkup(row_width=1)
    btn_ortga = InlineKeyboardButton("⬅️ Ortga", callback_data="ortga")
    markup.add(btn_ortga)
    
    bot.send_message(call.message.chat.id, "📞 Ovoz bergan raqamingizni yuboring:\n\nMasalan: +998901234567", reply_markup=markup)

# Ortga qaytish
@bot.callback_query_handler(func=lambda call: call.data == "ortga")
def ortga(call):
    start(call.message)

# Telefon raqamini qabul qilish
@bot.message_handler(content_types=['text'])
def get_number(message):
    if message.text.startswith('+998') and message.text[1:].isdigit() and len(message.text) == 13:
        bot.send_message(message.chat.id, "✅ Raqamingiz qabul qilindi! Adminlar tekshirib chiqadi.")
    else:
        bot.send_message(message.chat.id, "❌ Noto'g'ri format! Iltimos, +998 bilan boshlanadigan to'g'ri raqam yuboring.")

# Botni ishga tushirish
bot.polling(non_stop=True)