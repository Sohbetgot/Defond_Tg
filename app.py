import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
import time

# TOKEN we ADMIN ID sazlamalary
TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'
ADMINS = [8143084360]  # Admin ID
SPONSOR_CHANNELS = ['@DM_SERVERS', '@DM_404CHAT']

bot = telebot.TeleBot(TOKEN)
scheduler = BackgroundScheduler()
scheduler.start()

# Awto post mesajy
auto_post_text = "\u2709\ufe0f Awto Post: Bu bot awtomat ugradylýan posta mysal."

def auto_poster():
    try:
        bot.send_message(chat_id=ADMINS[0], text=auto_post_text)
    except:
        pass

# 1 sagatda 1 gezek awto post
scheduler.add_job(auto_poster, 'interval', hours=1)

# Menýu ýazgysy
menu_text = """
👋️ Hoş Geldiňiz, {username} !
📢 VPN kodyny 🎮 Almak üçin aşakdaky kanallara agza boluň:

@DM_SERVERS
@DM_404CHAT
"""

# Spamlardan goramak
last_time = {}
def is_spam(user_id):
    now = time.time()
    if user_id in last_time and now - last_time[user_id] < 3:
        return True
    last_time[user_id] = now
    return False

# Kanal agzalygy barlamak
def check_subscription(user_id):
    for channel in SPONSOR_CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

# START komandasy
@bot.message_handler(commands=['start'])
def start(message):
    if is_spam(message.chat.id):
        bot.send_message(message.chat.id, "\u26d4\ufe0f Haýyş edilýär, gaýtadan synanyş! (Spam goralýşy)")
        return
    if not check_subscription(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("\u2705 Agza Boldum", callback_data="check_sub"))
        bot.send_message(message.chat.id, menu_text.format(username=message.from_user.first_name), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "\u2705 Agzalyğynyz barlandy! Kodyňyz: \n`vpn-kod-example`", parse_mode='Markdown')

# Admin panel
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id in ADMINS:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("\ud83d\udcc4 Menýu Ýazgyny Üýtgetmek", "\ud83d\udcf1 VPN Kody Üýtgetmek")
        markup.add("\u274c Çyk")
        bot.send_message(message.chat.id, "\ud83d\udd27 Admin Paneline Hoş Geldiňiz!", reply_markup=markup)

# Admin menýu duwmeleri
@bot.message_handler(func=lambda message: message.text == "\ud83d\udcc4 Menýu Ýazgyny Üýtgetmek")
def change_menu(message):
    if message.from_user.id in ADMINS:
        msg = bot.send_message(message.chat.id, "📄 Täze menýu ýazgysyny giriziň:")
        bot.register_next_step_handler(msg, save_menu_text)

def save_menu_text(message):
    global menu_text
    if message.from_user.id in ADMINS:
        menu_text = message.text
        bot.send_message(message.chat.id, "🌟 Menýu ýazgy üýtgedildi.")

@bot.message_handler(func=lambda message: message.text == "\ud83d\udcf1 VPN Kody Üýtgetmek")
def change_vpn_code(message):
    if message.from_user.id in ADMINS:
        msg = bot.send_message(message.chat.id, "🔑 VPN koduny giriziň:")
        bot.register_next_step_handler(msg, save_vpn_code)

def save_vpn_code(message):
    global vpn_code
    vpn_code = message.text
    bot.send_message(message.chat.id, "🔑 VPN kody üýtgedildi.")

# Agza boldum barlagy
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub_callback(call):
    if check_subscription(call.from_user.id):
        bot.send_message(call.message.chat.id, "\u2705 Agzalyğynyz barlandy! Kodyňyz: \n`vpn-kod-example`", parse_mode='Markdown')
    else:
        bot.send_message(call.message.chat.id, "\u26a0\ufe0f Ilki bilen kanallara agza boluň!")

# Çyk komanda
@bot.message_handler(func=lambda message: message.text == "\u274c Çyk")
def exit_panel(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "🚮 Panelden çykdyňyz.", reply_markup=markup)

# Boty hemişelik işledýäris
print("Bot işe başlady!")
bot.infinity_polling()
