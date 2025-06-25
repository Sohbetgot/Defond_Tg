import telebot
from telebot import types

TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'  # Özüňiz bilen çalyşyň
bot = telebot.TeleBot(TOKEN)

# Sponsor kanallaryň sanawy: (ad, kanal linki)
sponsor_channels = [
    ("KANAL 1 ✅", "https://t.me/DM_SERVERS"),
    ("KANAL 2 ✅", "https://t.me/DM_404CHAT")
]

# Admin paneliň açylmagy üçin açar söz
ADMIN_PASSWORD = "ADNİOBERTİ61"  # Üýtgedip bilersiňiz

# Agza bolan ulanyjylaryň IDs sanawy
subscribed_users = set()

# Admin panel açan ulanyjylaryň chat ID-leri
admin_sessions = set()

def check_subscription(user_id):
    # Agza bolan ulanyjylar üçin barlag funksiýasy, ýöne häzirki wagtda düwme bilen görkezýäris.
    return user_id in subscribed_users

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.from_user.first_name or message.from_user.username or "Ulanyjy"

    markup = types.InlineKeyboardMarkup()
    for name, url in sponsor_channels:
        btn = types.InlineKeyboardButton(text=name, url=url)
        markup.add(btn)

    welcome_text = f"👋🏻 Hoş geldiňiz, {username}!\n\n" \
                   "📢 VPN kody almak üçin aşakdaky kanallara agza boluň👇🏻"

    bot.send_message(user_id, welcome_text, reply_markup=markup)

    # Ýönekeý admin panel açmak üçin ulanyja habar bermek
    bot.send_message(user_id, "Admin panel açmak üçin /admin komandasyny ulanyň.")

@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Admin panel açmak üçin açar sözi ýazyň:")

    # Ulanyjydan admin açar söz almagy üçin režim girizýäris
    bot.register_next_step_handler(message, process_admin_password)

def process_admin_password(message):
    user_id = message.chat.id
    text = message.text.strip()

    if text == ADMIN_PASSWORD:
        admin_sessions.add(user_id)
        show_admin_panel(user_id)
    else:
        bot.send_message(user_id, "Açar söz ýalňyş! Täzeden synanyşyň ýa-da /start bilen başlaň.")

def show_admin_panel(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Menýu ýazgyny üýtget", "VPN kodlaryny dolandyr")
    markup.row("Çykmak")
    bot.send_message(user_id, "Admin panel açyldy. Haýsy funksiýany isleýärsiňiz?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in admin_sessions)
def admin_panel_handler(message):
    user_id = message.chat.id
    text = message.text

    if text == "Menýu ýazgyny üýtget":
        bot.send_message(user_id, "Täze menýu ýazgyny ýazyň (Ulanyjy ady üçin {username} ulanyň):")
        bot.register_next_step_handler(message, update_menu_text)
    elif text == "VPN kodlaryny dolandyr":
        bot.send_message(user_id, "VPN kodlary dolandyryş bölümi (bu ýere kodlary goşup bilersiňiz).")
        # Bu ýerde VPN kodlary dolandyryş koduny goşup bilersiňiz
    elif text == "Çykmak":
        admin_sessions.discard(user_id)
        bot.send_message(user_id, "Admin panelden çykdyňyz.", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, "Nädogry saýlaw. Täzeden saýlaň.")

menu_text = "👋🏻 Hoş Geldiňiz !  {username}\n📢 VPN kodyny 🎮 almak üçin aşakdaky kanallara agza boluň!"

def update_menu_text(message):
    global menu_text
    user_id = message.chat.id
    new_text = message.text
    menu_text = new_text
    bot.send_message(user_id, "Menýu ýazgy üstünlikli üýtgedildi.")

# VPN kody bermek üçin mysal funksiýa
@bot.message_handler(commands=['getvpn'])
def send_vpn_code(message):
    user_id = message.chat.id
    if not check_subscription(user_id):
        bot.send_message(user_id, "Ilki bilen ähli sponsor kanallara agza boluň.")
        return
    # Mysal VPN kody, has çylşyrymly ulanmak üçin kody dolandyrmak gerek
    vpn_code = "VPN-KODY-123"
    bot.send_message(user_id, f"🎉 VPN kodyňyz: {vpn_code}")

bot.infinity_polling()
