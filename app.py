import telebot
from telebot import types

TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'  # <-- Şu ýere bot tokeniňizi goýuň
bot = telebot.TeleBot(TOKEN)

# Agza bolmaly kanallaryň sanawy (name + link)
channels = [
    ("DM CHANEL", "https://t.me/dm_servers"),
    ("DM 404 CHAT", "https://t.me/dm_404chat"),
]

# Ulanyjylaryň ID sanawy — adatça maglumat bazasy ulanýarsyňyz
users = set()

# Admin açar sözi
ADMIN_PASSWORD = "ADNİOBERTİ61"  # <-- Şu açar sözi üýtgedip goýuň

# Statika habary üçin funksiýa (agza sanyny görkezýär)
def get_statika_text():
    return f"📊 Statika:\n— Agza bolan ulanyjylar: {len(users)}"


# Agza bolmaly kanallar üçin düwmeler döredýär
def get_channels_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    for name, link in channels:
        # Düwmeler "name - link" görnüşinde, '+' ýa-da başga belgi goşulmaýar
        keyboard.add(types.InlineKeyboardButton(text=name, url=link))
    return keyboard


# Baş menýu ýazgy
menu_text = (
    "Salam, {username}!\n\n"
    "🌟 Menýu:\n"
    "1. Menýu ýazgyny üýtgetmek\n"
    "2. VPN kody üýtgetmek\n"
    "3. Sponsor kanallary üýtgetmek\n"
    "4. Statika\n"
    "5. Awto poster\n"
    "6. Çykmak\n"
)


@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)  # Her gezek start basylanda agza sanyna goşulýar
    username = message.from_user.first_name or "Ulanyjy"
    
    # Ilki agza bolmaly kanallary görkezýäris
    bot.send_message(message.chat.id, "📢 Agza bolmaly kanallar:", reply_markup=get_channels_keyboard())
    
    # Soň baş menýu görkezilýär
    bot.send_message(message.chat.id, menu_text.format(username=username))


# Admin paneli açmak üçin ulanyjydan açar söz soralýar
@bot.message_handler(commands=['admin'])
def admin_login(message):
    msg = bot.send_message(message.chat.id, "🔑 Admin panel açmak üçin açar sözüňizi ýazyň:")
    bot.register_next_step_handler(msg, check_admin_password)


def check_admin_password(message):
    if message.text == ADMIN_PASSWORD:
        # Dogry açar söz girizilende admin panel menýusyny görkez
        show_admin_panel(message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ Ýalňyş açar söz. Ýene synanyşyň.")


def show_admin_panel(chat_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📝 Menýu ýazgyny üýtgetmek")
    keyboard.add("🔐 VPN kody üýtgetmek")
    keyboard.add("📢 Sponsor kanallary üýtgetmek")
    keyboard.add("📊 Statika")
    keyboard.add("⏰ Awto poster")
    keyboard.add("🚪 Çykmak")
    
    bot.send_message(chat_id, "🛠️ Admin panel:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def admin_panel_actions(message):
    text = message.text
    
    if text == "📝 Menýu ýazgyny üýtgetmek":
        bot.send_message(message.chat.id, "Menýu ýazgyny şu ýere ýazyň:")
        bot.register_next_step_handler(message, save_menu_text)
    
    elif text == "🔐 VPN kody üýtgetmek":
        bot.send_message(message.chat.id, "VPN kodlaryny şu ýere ýazyň:")
        bot.register_next_step_handler(message, save_vpn_codes)
        
    elif text == "📢 Sponsor kanallary üýtgetmek":
        bot.send_message(message.chat.id, "Sponsor kanallary şu formatda ýazyň (her setiri: Ady - Link):")
        bot.register_next_step_handler(message, save_sponsor_channels)
        
    elif text == "📊 Statika":
        bot.send_message(message.chat.id, get_statika_text())
        
    elif text == "⏰ Awto poster":
        bot.send_message(message.chat.id, "Awto poster üçin ýazgy we aralygy ýazyň (mysal: Hat, 60):")
        bot.register_next_step_handler(message, save_auto_poster)
        
    elif text == "🚪 Çykmak":
        bot.send_message(message.chat.id, "Admin panelden çykdyňyz.", reply_markup=types.ReplyKeyboardRemove())
        
    else:
        # Admin panelde däl-de, başga zat ýazylsa
        bot.send_message(message.chat.id, "❓ Nädip kömek edip bilerin? Admin panelde bolmadyk bu buýruk ýa ýazgy.")


# Ýadyňyzda saklaň, bu funksiýalar ýönekeý nusga üçin. Siz özüňize görä maglumatlary saklamak we okamak koduny goşmaly.

def save_menu_text(message):
    global menu_text
    menu_text = message.text
    bot.send_message(message.chat.id, "✅ Menýu ýazgy üstünlikli üýtgedildi.")
    show_admin_panel(message.chat.id)


def save_vpn_codes(message):
    # Bu ýerde VPN kodlaryny saklamak üçin logika goşuň
    bot.send_message(message.chat.id, "✅ VPN kodlary üstünlikli kabul edildi.")
    show_admin_panel(message.chat.id)


def save_sponsor_channels(message):
    global channels
    lines = message.text.strip().split('\n')
    new_channels = []
    for line in lines:
        if '-' in line:
            name, link = line.split('-', 1)
            new_channels.append((name.strip(), link.strip()))
    channels = new_channels
    bot.send_message(message.chat.id, "✅ Sponsor kanallary üstünlikli üýtgedildi.")
    show_admin_panel(message.chat.id)


def save_auto_poster(message):
    # Bu ýerde awto poster ýazgy we wagtyny saklamak üçin logika goşuň
    bot.send_message(message.chat.id, "✅ Awto poster sazlamalary kabul edildi.")
    show_admin_panel(message.chat.id)


bot.polling(none_stop=True)
