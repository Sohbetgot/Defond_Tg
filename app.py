import telebot
from telebot import types
import time
import threading

TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'  # Bot tokeniňizi şu ýere goýuň
bot = telebot.TeleBot(TOKEN)

# Bot sazlamalar
sponsor_channels = ['@DM_SERVERS', '@DM_404CHAT']
vpn_codes = []
used_codes = []
admins = []
admin_keyword = "admin_gir"
custom_menu = "👋 Salam {username}! Hoş geldiňiz."
spam_protection = True
last_message_time = {}
auto_posts = []
auto_post_interval = 3600  # Default 1 sagat

# Awto poster funksiýasy
def auto_poster():
    while True:
        if auto_posts:
            for post in auto_posts:
                print(f"[BOT] Awto post: {post}")
        time.sleep(auto_post_interval)

threading.Thread(target=auto_poster, daemon=True).start()

# Abuna barlag
@bot.message_handler(commands=['start'])
def start_handler(message):
    if not check_subscription(message.chat.id):
        send_subscription_menu(message.chat.id)
    else:
        username = message.from_user.first_name
        bot.send_message(message.chat.id, custom_menu.format(username=username))
        bot.send_message(message.chat.id, "\u2705 Agzalygyňyz barlandy! Kodyňyz: \n`vpn-kod-example`", parse_mode='Markdown')

# Abuna barlag funksiyasy
def check_subscription(user_id):
    for channel in sponsor_channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'creator', 'administrator']:
                return False
        except:
            return False
    return True

def send_subscription_menu(user_id):
    markup = types.InlineKeyboardMarkup()
    for ch in sponsor_channels:
        btn = types.InlineKeyboardButton(text=ch.replace('@', ''), url=f'https://t.me/{ch[1:]}')
        markup.add(btn)
    markup.add(types.InlineKeyboardButton("✅ Agza Boldum", callback_data="check_sub"))
    bot.send_message(user_id, "Botdan peýdalanmak üçin aşakdaky kanallara agza boluň:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def handle_check_sub(call):
    if check_subscription(call.message.chat.id):
        username = call.from_user.first_name
        bot.send_message(call.message.chat.id, custom_menu.format(username=username))
        bot.send_message(call.message.chat.id, "\u2705 Agzalygyňyz barlandy! Kodyňyz: \n`vpn-kod-example`", parse_mode='Markdown')
    else:
        bot.answer_callback_query(call.id, "Ilki bilen ähli kanallara agza boluň!", show_alert=True)

# Admin panel komanda arkaly açylýar
@bot.message_handler(commands=['admin'])
def admin_command(message):
    bot.send_message(message.chat.id, "Açar sözi giriziň:")
    bot.register_next_step_handler(message, verify_admin)

def verify_admin(message):
    if message.text == admin_keyword:
        bot.send_message(message.chat.id, admin_commands, parse_mode='Markdown')
        if message.chat.id not in admins:
            admins.append(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Nädogry açar sözi.")

admin_commands = (
    "🛠 *Admin Panel*\n\n"
    "1. Post goşmak: 'Post goş'\n"
    "2. Postlary görmek: 'Postlary görkez'\n"
    "3. Postlary öçürmek: 'Postlary arassala'\n"
    "4. Aralyk (sekundda): 'Aralyk <sekund>'\n"
    "5. VPN kod goşmak: 'VPN goş <kod>'\n"
    "6. VPN kodlary görmek: 'VPN gör'\n"
    "7. VPN kodlary arassala: 'VPN arassala'\n"
    "8. Ulanylan kodlar: 'Ulanylan kodlar'\n"
    "9. Bildiriş ugratmak: 'Bildiriş <habar>'\n"
    "10. Admin goşmak: 'Admin goş <id>'\n"
    "11. Admin öçürmek: 'Admin öçür <id>'\n"
    "12. Admin sanawy: 'Adminler'\n"
    "13. Açar söz üýtgetmek: 'Açar üýtget <täze_söz>'\n"
    "14. Spamlardan goragy aç/ýap: 'Spam aç' / 'Spam ýap'\n"
    "15. Bot sazlamalary: 'Sazlama üýtget <ad>=<gymmat>'\n"
)

# Admin komandalar
@bot.message_handler(func=lambda m: m.chat.id in admins)
def handle_admin(message):
    text = message.text
    if text.startswith('Post goş'):
        post = text.replace('Post goş', '').strip()
        if post:
            auto_posts.append(post)
            bot.reply_to(message, "Post goşuldy")
    elif text == 'Postlary görkez':
        bot.reply_to(message, '\n'.join(auto_posts) or "Post ýok")
    elif text == 'Postlary arassala':
        auto_posts.clear()
        bot.reply_to(message, "Postlar arassalandy")
    elif text.startswith('Aralyk'):
        try:
            global auto_post_interval
            auto_post_interval = int(text.split()[1])
            bot.reply_to(message, f"Aralyk {auto_post_interval} sekunda goýuldy")
        except:
            bot.reply_to(message, "Aralyk nädogry formatda")
    elif text.startswith('VPN goş'):
        kod = text.replace('VPN goş', '').strip()
        vpn_codes.append(kod)
        bot.reply_to(message, "VPN kod goşuldy")
    elif text == 'VPN gör':
        bot.reply_to(message, '\n'.join(vpn_codes) or "Kod ýok")
    elif text == 'VPN arassala':
        vpn_codes.clear()
        bot.reply_to(message, "VPN kodlar arassalandy")
    elif text == 'Ulanylan kodlar':
        bot.reply_to(message, '\n'.join(used_codes) or "Ulanylan kod ýok")
    elif text.startswith('Bildiriş'):
        msg = text.replace('Bildiriş', '').strip()
        for admin_id in admins:
            bot.send_message(admin_id, f"📢 Bildiriş: {msg}")
    elif text.startswith('Admin goş'):
        try:
            uid = int(text.split()[2])
            admins.append(uid)
            bot.reply_to(message, "Admin goşuldy")
        except:
            bot.reply_to(message, "ID nädogry")
    elif text.startswith('Admin öçür'):
        try:
            uid = int(text.split()[2])
            admins.remove(uid)
            bot.reply_to(message, "Admin öçürildi")
        except:
            bot.reply_to(message, "ID ýok ýa nädogry")
    elif text == 'Adminler':
        bot.reply_to(message, '\n'.join(map(str, admins)))
    elif text.startswith('Açar üýtget'):
        global admin_keyword
        admin_keyword = text.split(' ', 2)[2]
        bot.reply_to(message, "Açar üýtgedildi")
    elif text == 'Spam aç':
        global spam_protection
        spam_protection = True
        bot.reply_to(message, "Spam goragy açyldy")
    elif text == 'Spam ýap':
        spam_protection = False
        bot.reply_to(message, "Spam goragy ýapyldy")
    elif text.startswith('Sazlama üýtget'):
        try:
            setting = text.split(' ', 2)[2]
            key, value = setting.split('=')
            if key.strip() == 'menu':
                global custom_menu
                custom_menu = value.strip()
                bot.reply_to(message, "Menýu sazlamasy üýtgedildi")
        except:
            bot.reply_to(message, "Ýalňyş format")

# Bot başlaýar
print("[BOT] Işleýär...")
bot.infinity_polling()
