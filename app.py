import telebot
from telebot import types

TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'  # 🔐 Bot tokeniňi şu ýere goý
bot = telebot.TeleBot(TOKEN)

# 🔐 Admin açarsözi
ADMIN_PASSWORD = "ADNİOBERTİ61"

# 📢 Sponsor kanallar
sponsor_channels = {
    "📡 Kanal 1": "https://t.me/DM_SERVERS",
    "📡 Kanal 2": "https://t.me/DM_404CHAT"
}

# 🧠 Admin statusyny saklaýan sözlük
admin_users = set()

# 📋 Esasy menýu
menu_text = """
👋 Salam, {username}!

Botdan peýdalanmak üçin aşakdaky menýudan peýdalanyň:
✅ Agza boldum
🔑 admin_gir — Admin paneli açmak üçin
"""

# 🔐 Admin panel menýusy
admin_panel_text = """
👑 *Admin Panel*

1️⃣ Post goşmak
2️⃣ Postlary görmek
3️⃣ Postlary arassala
4️⃣ Aralyk (sekundda) üýtgetmek
5️⃣ Menýu ýazgysyny üýtgetmek
6️⃣ VPN kodyny üýtgetmek
🔚 Çykmak
"""

# ✅ Agzalyk barlagy
def check_subscription(user_id):
    for name, link in sponsor_channels.items():
        try:
            chat_member = bot.get_chat_member(link, user_id)
            if chat_member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

# 📩 Kanal barlag menýusy
def send_subscription_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    for name, link in sponsor_channels.items():
        markup.add(types.InlineKeyboardButton(text=name, url=link))
    markup.add(types.InlineKeyboardButton(text="✅ Agza boldum", callback_data="check_sub"))
    bot.send_message(chat_id, "➕ Ilki bilen aşakdaky kanallara agza boluň:", reply_markup=markup)

# ▶ /start komandasy
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not check_subscription(user_id):
        send_subscription_menu(user_id)
    else:
        username = message.from_user.first_name
        bot.send_message(user_id, menu_text.format(username=username))

# 🔘 Agza boldum düwmesini barla
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
    if check_subscription(call.message.chat.id):
        bot.send_message(call.message.chat.id, "✅ Agzalyk barlandy! VPN koduňyz: `vpn-kod-example`", parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, "⛔ Ilki kanallara agza bolmaly!")

# 🔑 Admin gir komandasy
@bot.message_handler(commands=['admin'])
def admin(message):
    msg = bot.send_message(message.chat.id, "🔑 Açarsözi giriziň:")
    bot.register_next_step_handler(msg, check_admin_password)

# 🔍 Açarsözi barla
def check_admin_password(message):
    if message.text == ADMIN_PASSWORD:
        admin_users.add(message.chat.id)
        bot.send_message(message.chat.id, admin_panel_text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Açarsöz ýalňyş!")

# 🧾 Admin komandasy
@bot.message_handler(func=lambda msg: msg.text in ['1', '2', '3', '4', '5', '6', 'Çykmak', 'çykmak'])
def admin_panel_handler(message):
    if message.chat.id not in admin_users:
        return bot.send_message(message.chat.id, "⛔ Admin panel üçin rugsat ýok!")
    
    if message.text == 'Çykmak' or message.text == 'çykmak':
        admin_users.remove(message.chat.id)
        return bot.send_message(message.chat.id, "🔒 Admin panelden çykdyňyz.")

    bot.send_message(message.chat.id, f"✳ Funksiýa {message.text} saýlandy. (Ýöne häzirki wagtda ýerine ýetirilmeýär.)")

# ▶ Bot işleýär
print("🤖 Bot işläp başlady...")
bot.infinity_polling()
