import telebot
from telebot import types

# Bot tokeny giriziň
TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'
bot = telebot.TeleBot(TOKEN)

# Açarsöz
admin_password = "ADNİOBERTİ61"
admin_users = set()

# VPN kod sanawy (bir görnüşli)
vpn_code = "vpn-code-example"

# Sponsor kanallary
sponsor_channels = ["@examplechannel1", "@examplechannel2"]

# Menýu ýazgy
menu_text = "\U0001F44B Salam, {username}! VPN kody almak üçin aşakdaky kanallara agza boluň."

# Agzalyk barlaýjy
def check_subscription(user_id):
    for channel in sponsor_channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status in ['left']:
                return False
        except:
            return False
    return True

# Start komanda
def send_subscription_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    for ch in sponsor_channels:
        markup.add(types.InlineKeyboardButton(text=f"➕ {ch}", url=f"https://t.me/{ch[1:]}"))
    markup.add(types.InlineKeyboardButton(text="✅ AGZA BOLDUM", callback_data="check_member"))
    bot.send_message(chat_id, "VPN kody almak üçin aşakdaky kanallara agza boluň:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(message.chat.id):
        send_subscription_menu(message.chat.id)
    else:
        username = message.from_user.first_name
        bot.send_message(message.chat.id, menu_text.format(username=username))
        bot.send_message(message.chat.id, f"\u2705 Agzalygyňyz barlandy! Kodyňyz: \n{vpn_code}", parse_mode='Markdown')

# AGZA BOLDUM düwmesi üçin
@bot.callback_query_handler(func=lambda call: call.data == "check_member")
def callback_check(call):
    if check_subscription(call.message.chat.id):
        bot.send_message(call.message.chat.id, f"\u2705 Agzalygyňyz barlandy! Kodyňyz: \n{vpn_code}")
    else:
        bot.send_message(call.message.chat.id, "\u274C Ilki bilen ähli kanallara agza boluň!")

# Admin panel açmak üçin
@bot.message_handler(commands=['admin_gir'])
def ask_password(message):
    msg = bot.send_message(message.chat.id, "\U0001F511 Admin açarsözüni giriziň:")
    bot.register_next_step_handler(msg, check_password)

def check_password(message):
    if message.text == admin_password:
        admin_users.add(message.chat.id)
        show_admin_panel(message.chat.id)
    else:
        bot.send_message(message.chat.id, "\u274C Nädogry açarsöz!")

# Admin paneli

def show_admin_panel(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📝 Menýu üýtgetmek", "🔐 VPN kod üýtgetmek")
    markup.row("📢 Sponsor kanallary", "📊 STATIKA")
    markup.row("🤖 Awto Poster", "🚪 Panelden çyk")
    bot.send_message(chat_id, "\U0001F6E0 Admin paneline hoş geldiňiz:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id in admin_users)
def handle_admin(message):
    if message.text == "📝 Menýu üýtgetmek":
        msg = bot.send_message(message.chat.id, "Täze menýu ýazgyny giriziň:")
        bot.register_next_step_handler(msg, change_menu)

    elif message.text == "🔐 VPN kod üýtgetmek":
        msg = bot.send_message(message.chat.id, "Täze VPN kodyny giriziň:")
        bot.register_next_step_handler(msg, change_vpn)

    elif message.text == "📢 Sponsor kanallary":
        msg = bot.send_message(message.chat.id, "Sponsor kanallary (arasynda boşluk bilen):")
        bot.register_next_step_handler(msg, change_channels)

    elif message.text == "📊 STATIKA":
        bot.send_message(message.chat.id, "👤 user1 – 10/10\n👤 user2 – 5/10")

    elif message.text == "🤖 Awto Poster":
        msg = bot.send_message(message.chat.id, "Ugratyljak haty giriziň:")
        bot.register_next_step_handler(msg, get_post_text)

    elif message.text == "🚪 Panelden çyk":
        admin_users.discard(message.chat.id)
        bot.send_message(message.chat.id, "Admin panelden çykdyňyz.", reply_markup=types.ReplyKeyboardRemove())

# Menýu üýtgetmek

def change_menu(message):
    global menu_text
    menu_text = message.text
    bot.send_message(message.chat.id, "📝 Menýu täzelendi!")

# VPN kod üýtgetmek

def change_vpn(message):
    global vpn_code
    vpn_code = message.text
    bot.send_message(message.chat.id, "🔐 VPN kody täzelendi!")

# Sponsor kanallary üýtgetmek

def change_channels(message):
    global sponsor_channels
    sponsor_channels = message.text.split()
    bot.send_message(message.chat.id, "📢 Kanallar täzelendi!")

# Awto poster
post_data = {}

def get_post_text(message):
    post_data[message.chat.id] = {"text": message.text}
    msg = bot.send_message(message.chat.id, "Sekundda wagt giriziň:")
    bot.register_next_step_handler(msg, set_post_timer)

def set_post_timer(message):
    try:
        seconds = int(message.text)
        post = post_data.get(message.chat.id)
        bot.send_message(message.chat.id, f"✅ Post ýatda saklandy we her {seconds} sekuntdan botda görkeziler.")
        auto_post_loop(post['text'], seconds, message.chat.id)
    except:
        bot.send_message(message.chat.id, "❌ Nädogry wagt!")

def auto_post_loop(text, delay, chat_id):
    import threading, time
    def loop():
        while chat_id in admin_users:
            bot.send_message(chat_id, f"🟢 Awto post:\n{text}")
            time.sleep(delay)
    threading.Thread(target=loop).start()

# Boty işledýäris
print("Bot işe başlady...")
bot.infinity_polling()
