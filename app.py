import telebot
from telebot import types

# Bot tokeniňizi şu ýere giriziň:
TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'

bot = telebot.TeleBot(TOKEN)

# Admin açar sözi
ADMIN_KEYWORD = "ADNİOBERTİ61"

# Agzalygy bar bolmaly kanallar (kanal atlary '@' bilen)
channels = ['@DM_SERVERS', '@DM_404CHAT']

# Ulanyjylaryň agzalyk statusy (chat_id -> bool)
user_subscriptions = {}

# Admin panel açan ulanyjylar (chat_id set)
admin_sessions = set()
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    if user_subscriptions.get(user_id):
        bot.send_message(user_id, f"🟢 Salam {message.from_user.first_name}! Boty ulanyp bilersiňiz.")
        show_main_menu(user_id)
    else:
        send_subscription_menu(user_id)

def send_subscription_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    for ch in channels:
        markup.add(types.InlineKeyboardButton(text=ch, url=f"https://t.me/{ch.strip('@')}"))
    markup.add(types.InlineKeyboardButton(text="✅ Agza boldum", callback_data="joined"))
    bot.send_message(chat_id, "Ilki aşakdaky kanallara agza boluň, soňra «Agza boldum» düwmesine basyň:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "joined")
def joined_callback(call):
    user_id = call.message.chat.id
    user_subscriptions[user_id] = True
    bot.answer_callback_query(call.id, "Agzalygyňyz tassyklanyldy!")
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                          text="🟢 Agzalygyňyz tassyklanyldy! Indi boty ulanyp bilersiňiz.")
    show_main_menu(user_id)
    def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("VPN kodlaryny almak", "Statika görmek")
    markup.row("Admin panel", "Köp soralanlar")
    bot.send_message(chat_id, "Hyzmatlary saýlaň:", reply_markup=markup)

@bot.message_handler(commands=['admin'])
def ask_admin_keyword(message):
    bot.send_message(message.chat.id, "Admin paneli açmak üçin açar sözüňizi ýazyň:")

@bot.message_handler(func=lambda m: m.text == ADMIN_KEYWORD)
def admin_login(message):
    admin_sessions.add(message.chat.id)
    show_admin_menu(message.chat.id)

@bot.message_handler(func=lambda m: m.chat.id in admin_sessions)
def admin_panel_handler(message):
    text = message.text
    chat_id = message.chat.id

    if text == "⬅️ Çykmak":
        admin_sessions.discard(chat_id)
        bot.send_message(chat_id, "Admin panelden çykdyňyz.", reply_markup=types.ReplyKeyboardRemove())
    elif text == "1. Menýu ýazgyny üýtgetmek":
        bot.send_message(chat_id, "Menýu ýazgyny üýtgetmek funksiýasy (iň soňky ýakyn wagtda goşulýar).")
    elif text == "2. VPN kody üýtgetmek":
        bot.send_message(chat_id, "VPN kodlaryny üýtgetmek funksiýasy (iň soňky ýakyn wagtda goşulýar).")
    elif text == "3. Sponsor kanallary üýtgetmek":
        bot.send_message(chat_id, "Sponsor kanallary üýtgetmek funksiýasy (iň soňky ýakyn wagtda goşulýar).")
    elif text == "4. Statika":
        count = len(user_subscriptions)
        bot.send_message(chat_id, f"Ulanyjy sany: {count}")
    elif text == "5. Awto poster sazlamalary":
        bot.send_message(chat_id, "Awto poster sazlamalary (iň soňky ýakyn wagtda goşulýar).")
    else:
        bot.send_message(chat_id, "Nädogry buýruk. Menýudan saýlaň.")

def show_admin_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("1. Menýu ýazgyny üýtgetmek", "2. VPN kody üýtgetmek")
    markup.row("3. Sponsor kanallary üýtgetmek", "4. Statika")
    markup.row("5. Awto poster sazlamalary", "⬅️ Çykmak")
    bot.send_message(chat_id, "🛠️ Admin paneliň menýusy:", reply_markup=markup)
    
    if __name__ == "__main__":
    print("Bot işläp başlady...")
    bot.polling(non_stop=True)
