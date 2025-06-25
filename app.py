import telebot
from telebot import types

bot = telebot.TeleBot("7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4")  # Bot tokeniňi şu ýere goý

ADMIN_PASSWORD = "ADNİOBERTİ61"  # Açarsöz şu ýerde

sponsor_channels = {
    "@DM_SERVERS": "https://t.me/DM_SERVERS",
    "@DM_404CHAT": "https://t.me/DM_404CHAT"
}

menu_text = "👋 Hoş geldiňiz, {username}!\nBotdan peýdalanmak üçin aşakdaky kanallara agza boluň."

# /start komandasy
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not check_subscription(user_id):
        send_subscription_menu(user_id)
    else:
        username = message.from_user.first_name
        bot.send_message(user_id, menu_text.format(username=username))

# Abuna barlagy
def check_subscription(user_id):
    for channel in sponsor_channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

# Kanallara agza bolmadyk bolsa
def send_subscription_menu(user_id):
    markup = types.InlineKeyboardMarkup()
    for name, url in sponsor_channels.items():
        btn = types.InlineKeyboardButton(text=name, url=url)
        markup.add(btn)
    markup.add(types.InlineKeyboardButton(text="✅ Agza boldum", callback_data="check_sub"))
    bot.send_message(user_id, "Botdan peýdalanmak üçin şu kanallara agza boluň:", reply_markup=markup)

# ✅ Agza boldum barlagy
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def handle_check_sub(call):
    user_id = call.message.chat.id
    if check_subscription(user_id):
        bot.send_message(user_id, "✅ Agzalygyňyz barlandy! Ulgama girildi.")
        username = call.from_user.first_name
        bot.send_message(user_id, menu_text.format(username=username))
    else:
        bot.send_message(user_id, "❌ Kanallara agza bolmadyk ýaly görünýär. Täzeden barlaň.")

# Admin giriş komandasy
@bot.message_handler(commands=['admin_gir'])
def admin_giris(message):
    bot.send_message(message.chat.id, "🔐 Açarsözi giriziň:")
    bot.register_next_step_handler(message, check_admin_password)

def check_admin_password(message):
    if message.text == ADMIN_PASSWORD:
        show_admin_panel(message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ Açarsöz nädogry!")

# Admin panel menýusy
def show_admin_panel(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📝 Menýuny üýtget", "🔑 VPN kodlaryny dolandyrmak")
    markup.add("📢 Bildiriş ugratmak", "❌ Çyk")
    bot.send_message(chat_id, "🛡 Admin Paneline hoş geldiňiz!", reply_markup=markup)

# Admin düwmeleri bilen iş
@bot.message_handler(func=lambda message: message.text == "❌ Çyk")
def exit_admin_panel(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "🔒 Admin panelden çykdyňyz.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📝 Menýuny üýtget")
def change_menu_text(message):
    bot.send_message(message.chat.id, "✏ Täze menýu ýazgyny giriziň:")
    bot.register_next_step_handler(message, save_new_menu)

def save_new_menu(message):
    global menu_text
    menu_text = message.text
    bot.send_message(message.chat.id, "✅ Menýu üstünlikli täzelendi.")

@bot.message_handler(func=lambda message: message.text == "📢 Bildiriş ugratmak")
def notify_all_users(message):
    bot.send_message(message.chat.id, "✉ Ugratmaly habary ýazyň:")
    bot.register_next_step_handler(message, broadcast_message)

def broadcast_message(message):
    text = message.text
    # Diňe mysal üçin, diňe özi alýar
    bot.send_message(message.chat.id, f"📣 Bildiriş ugradyldy:\n{text}")

# Boty işledýäris
bot.infinity_polling()
