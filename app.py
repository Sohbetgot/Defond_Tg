import telebot
from telebot import types

# Bot token
TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'
bot = telebot.TeleBot(TOKEN)

# Ilkinji sazlamalar
admin_password = 'ADNİOBERTİ61'  # Admin panel açar sözi
admin_users = set()  # Açar sözi giren ulanyjylar

# Bot sazlamalar
bot_settings = {
    "bot_name": "VPN BOT",
    "menu_text": "Salam, {username}!\nMen size VPN hyzmatlaryny hödürleýärin.",
    "vpn_text": "\u2705 Agzalygyňyz barlandy! Kodyňyz: \nvpn-kod-example",
    "sponsor_channels": [
        {"name": "@DM_SERVERS", "url": "https://t.me/DM_SERVERS"},
        {"name": "@DM_404CHAT", "url": "https://t.me/DM_404CHAT"}
    ]
}

# Start komandasy
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not check_subscription(user_id):
        send_subscription_menu(user_id)
    else:
        bot.send_message(user_id, bot_settings["menu_text"].format(username=message.from_user.first_name))

# Admin panel açmak üçin komanda
@bot.message_handler(commands=['admin_gir'])
def ask_password(message):
    msg = bot.send_message(message.chat.id, "Açar sözi giriziň:")
    bot.register_next_step_handler(msg, check_admin_password)

# Açar sözi barlamak
def check_admin_password(message):
    if message.text == admin_password:
        admin_users.add(message.chat.id)
        show_admin_panel(message.chat.id)
    else:
        bot.send_message(message.chat.id, "\u274C Nädogry açar sözi.")

# Admin panel menýusy
def show_admin_panel(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Bot ady üýtget", "Menýu ýazgy üýtget")
    markup.add("VPN ýazgy üýtget", "Sponsor kanallary üýtget")
    markup.add("Açar sözi üýtget", "\u274C Çyk")
    bot.send_message(user_id, "Admin paneline geldiňiz. Sazlama saýlaň:", reply_markup=markup)

# Admin düwmeleri
@bot.message_handler(func=lambda message: message.chat.id in admin_users)
def admin_panel_commands(message):
    if message.text == "Bot ady üýtget":
        msg = bot.send_message(message.chat.id, "Täze bot adyny giriziň:")
        bot.register_next_step_handler(msg, update_bot_name)
    elif message.text == "Menýu ýazgy üýtget":
        msg = bot.send_message(message.chat.id, "Täze menýu ýazgysyny giriziň. {username} ýerini goýuň:")
        bot.register_next_step_handler(msg, update_menu_text)
    elif message.text == "VPN ýazgy üýtget":
        msg = bot.send_message(message.chat.id, "Täze VPN ýazgysyny giriziň. (vpn-kod yerine kod girilýär):")
        bot.register_next_step_handler(msg, update_vpn_text)
    elif message.text == "Sponsor kanallary üýtget":
        msg = bot.send_message(message.chat.id, "Her kanal: Kanal ady|https://t.me/link görnüşinde giriz. Her biri täze setirde.")
        bot.register_next_step_handler(msg, update_sponsor_channels)
    elif message.text == "Açar sözi üýtget":
        msg = bot.send_message(message.chat.id, "Täze admin açar sözi giriziň:")
        bot.register_next_step_handler(msg, update_admin_password)
    elif message.text == "\u274C Çyk":
        admin_users.remove(message.chat.id)
        bot.send_message(message.chat.id, "Admin panelden çykdyňyz.", reply_markup=types.ReplyKeyboardRemove())

# Üýtgetme funksiýalar
def update_bot_name(message):
    bot_settings["bot_name"] = message.text
    bot.send_message(message.chat.id, "Bot ady üstünlikli üýtgedildi.")

def update_menu_text(message):
    bot_settings["menu_text"] = message.text
    bot.send_message(message.chat.id, "Menýu ýazgy üstünlikli üýtgedildi.")

def update_vpn_text(message):
    bot_settings["vpn_text"] = message.text
    bot.send_message(message.chat.id, "VPN ýazgysy üstünlikli üýtgedildi.")

def update_sponsor_channels(message):
    lines = message.text.strip().split('\n')
    new_channels = []
    for line in lines:
        if '|' in line:
            name, url = line.split('|', 1)
            new_channels.append({"name": name.strip(), "url": url.strip()})
    bot_settings["sponsor_channels"] = new_channels
    bot.send_message(message.chat.id, "Sponsor kanallary üstünlikli täzelendi.")

def update_admin_password(message):
    global admin_password
    admin_password = message.text
    bot.send_message(message.chat.id, "Açar sözi üstünlikli üýtgedildi.")

# Agza bolmagy barlaýan funksiýa
def check_subscription(user_id):
    for ch in bot_settings["sponsor_channels"]:
        try:
            member = bot.get_chat_member(ch["name"], user_id)
            if member.status not in ["member", "creator", "administrator"]:
                return False
        except:
            return False
    return True

# Agza bolmak üçin düwme
def send_subscription_menu(user_id):
    markup = types.InlineKeyboardMarkup()
    for ch in bot_settings["sponsor_channels"]:
        markup.add(types.InlineKeyboardButton(text=ch["name"], url=ch["url"]))
    markup.add(types.InlineKeyboardButton("\u2705 Agza boldum", callback_data="check_sub"))
    bot.send_message(user_id, "Botdan peýdalanmak üçin aşakdaky kanallara agza boluň:", reply_markup=markup)

# Inline düwme barlag
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check_sub(call):
    if check_subscription(call.message.chat.id):
        bot.send_message(call.message.chat.id, bot_settings["vpn_text"])
    else:
        bot.answer_callback_query(call.id, "\u274C Ilki kanallara agza boluň!", show_alert=True)

bot.infinity_polling()
