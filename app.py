import telebot
from telebot import types
import time
import threading

TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'  # Bot tokeniňizi şu ýere goýuň
bot = telebot.TeleBot(TOKEN)

# Admin açar sözi
ADMIN_PASSWORD = "ADNİOBERTİ61"
admins = set()  # şu wagtky sessiýadaky adminler

# Sponsor kanallar (duwme görnüşinde görkeziler)
SPONSOR_CHANNELS = [
    ("KANAL 1 ✅", "https://t.me/DM_SERVERS"),
    ("KANAL 2 ✅", "https://t.me/DM_404CHAT"),
]

# VPN kodlar (bazasy)
vpn_codes = []  # [{"code": "ABC123", "used": False}]

# Ulanyjy maglumatlary: user_id -> dict
users = {}

# Awto poster üçin
auto_post_interval = 0
auto_post_texts = []
auto_post_running = False

# Spam goragy
user_message_times = {}

# Menü ýazgy (üýtgedip bolýar admin panelde)
menu_text = ("👋🏻 Hoş Geldiňiz, @{username}!\n\n"
             "📢 VPN kodyny almak üçin aşakdaky kanallara agza boluň:")


# === Kömekçi Funksiýalar ===

def make_subscribe_buttons():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for name, link in SPONSOR_CHANNELS:
        markup.add(types.InlineKeyboardButton(text=name, url=link))
    return markup

def check_subscription(user_id):
    # API çäklendirmesi sebäpli şu wagt hemme ulanyjyny agza kabul edýäris
    return users.get(user_id, {}).get("subscribed", False)

def mark_vpn_code_used(code):
    for item in vpn_codes:
        if item["code"] == code and not item["used"]:
            item["used"] = True
            return True
    return False

def get_free_vpn_code():
    for item in vpn_codes:
        if not item["used"]:
            return item["code"]
    return None

def is_spam(user_id):
    now = time.time()
    times = user_message_times.get(user_id, [])
    times = [t for t in times if now - t < 10]
    user_message_times[user_id] = times
    if len(times) >= 5:
        return True
    times.append(now)
    user_message_times[user_id] = times
    return False

def send_subscription_menu(chat_id):
    text = ("👋🏻 Hoş geldiňiz!\n\n"
            "VPN kodyny almak üçin aşakdaky kanallara agza boluň:\n")
    bot.send_message(chat_id, text, reply_markup=make_subscribe_buttons())

def is_admin(user_id):
    return user_id in admins

def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Agza Boldum", "VPN Kodumy Al", "Admin Panel")
    return markup

# Awto poster üçin funksiýa
def auto_post_worker():
    global auto_post_running
    while auto_post_running:
        if auto_post_interval > 0 and auto_post_texts:
            for post_text in auto_post_texts:
                # Bu ýere kanalyň ID-sini goýuň ýa-da islendik kanala ugradyp bilersiňiz
                # Mysal üçin: bot.send_message(CHANNEL_ID, post_text)
                print(f"Awto post: {post_text}")  # diňe konsola ýazmak
                time.sleep(auto_post_interval)
        else:
            time.sleep(5)

def start_auto_post():
    global auto_post_running
    if not auto_post_running:
        auto_post_running = True
        threading.Thread(target=auto_post_worker, daemon=True).start()

def stop_auto_post():
    global auto_post_running
    auto_post_running = False

# === Komandalar we habarlara işjeňlikler ===

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name or "Ulanyjy"
    users.setdefault(user_id, {"username": username, "subscribed": False, "vpn_code": None, "is_admin": False})

    if not check_subscription(user_id):
        send_subscription_menu(user_id)
    else:
        text = menu_text.format(username=username)
        bot.send_message(user_id, text, reply_markup=main_menu_keyboard())

@bot.message_handler(commands=['admin'])
def admin_login(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, "Admin paneline girmek üçin açar sözüni ýazyň:")
    bot.register_next_step_handler(msg, process_admin_password)

def process_admin_password(message):
    user_id = message.chat.id
    text = message.text.strip()
    if text == ADMIN_PASSWORD:
        admins.add(user_id)
        users[user_id]["is_admin"] = True
        bot.send_message(user_id, "🎉 Admin paneline üstünlikli girdiňiz!")
        show_admin_panel(user_id)
    else:
        bot.send_message(user_id, "❌ Ýalňyş açar söz. Admin paneline girmek mümkin däl.")

def show_admin_panel(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "VPN Kodlary Dolandyrmak",
        "Menýu Üýtgetmek",
        "Bildiriş Ugratmak",
        "Ulanyjylar",
        "Awto Poster",
        "Admin Goşmak / Aýyrmak",
        "Bot Sazlamalary",
        "Çykmak"
    )
    bot.send_message(user_id, "Admin panel:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Çykmak")
def admin_logout(message):
    user_id = message.chat.id
    if user_id in admins:
        admins.remove(user_id)
        users[user_id]["is_admin"] = False
    bot.send_message(user_id, "Admin panelinden çykdyňyz.", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda m: m.text == "VPN Kodlary Dolandyrmak")
def vpn_code_management(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    text = "VPN kodlaryny goşmak üçin, kodlary hatara her setirde bir kod bolup giriziň:"
    msg = bot.send_message(user_id, text)
    bot.register_next_step_handler(msg, add_vpn_codes)

def add_vpn_codes(message):
    user_id = message.chat.id
    lines = message.text.strip().split("\n")
    added = 0
    for line in lines:
        code = line.strip()
        if code and not any(item["code"] == code for item in vpn_codes):
            vpn_codes.append({"code": code, "used": False})
            added += 1
    bot.send_message(user_id, f"Üstünlikli {added} sany VPN kody goşuldy.")

@bot.message_handler(func=lambda m: m.text == "Menýu Üýtgetmek")
def menu_edit(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    text = "Täze menýu ýazgyny ýazyň (Ulanyjy adyny `{username}` hökmünde goýuň):"
    msg = bot.send_message(user_id, text)
    bot.register_next_step_handler(msg, save_menu_text)

def save_menu_text(message):
    global menu_text
    user_id = message.chat.id
    new_text = message.text
    menu_text = new_text
    bot.send_message(user_id, "Menýu ýazgy üstünlikli üýtgedildi.")

@bot.message_handler(func=lambda m: m.text == "Bildiriş Ugratmak")
def start_broadcast(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    msg = bot.send_message(user_id, "Ugratjak habaryňyzy ýazyň:")
    bot.register_next_step_handler(msg, send_broadcast)

def send_broadcast(message):
    text = message.text
    sent_count = 0
    for user_id in users.keys():
        try:
            bot.send_message(user_id, text)
            sent_count += 1
            time.sleep(0.05)
        except Exception:
            pass
    bot.send_message(message.chat.id, f"Bildiriş {sent_count} adama ugradylyldy.")

@bot.message_handler(func=lambda m: m.text == "Ulanyjylar")
def user_list(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    count = len(users)
    bot.send_message(user_id, f"Ulanyjy sany: {count}")

@bot.message_handler(func=lambda m: m.text == "Awto Poster")
def auto_poster_settings(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    text = ("Awto poster sazlamalary:\n"
            "1. Post goşmak: 'Post goş'\n"
            "2. Postlary görmek: 'Postlary görkez'\n"
            "3. Postlary öçürmek: 'Postlary arassala'\n"
            "4. Aralyk (sekundda): 'Aralyk <sekund>'\n
    # Awto poster sazlamalary (dowam)
@bot.message_handler(func=lambda m: m.text == "Post goş")
def add_auto_post(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    msg = bot.send_message(user_id, "Goşmak isleýän postuňyzy ýazyň:")
    bot.register_next_step_handler(msg, save_auto_post)

def save_auto_post(message):
    text = message.text
    auto_post_texts.append(text)
    bot.send_message(message.chat.id, "Post awto poster üçin goşuldy.")

@bot.message_handler(func=lambda m: m.text == "Postlary görkez")
def show_auto_posts(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    if not auto_post_texts:
        bot.send_message(user_id, "Hiç hili post ýok.")
        return
    text = "Awto poster postlary:\n\n" + "\n\n".join(f"{i+1}. {p}" for i,p in enumerate(auto_post_texts))
    bot.send_message(user_id, text)

@bot.message_handler(func=lambda m: m.text == "Postlary arassala")
def clear_auto_posts(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    auto_post_texts.clear()
    bot.send_message(user_id, "Awto poster postlary arassalandy.")

@bot.message_handler(func=lambda m: m.text.startswith("Aralyk"))
def set_auto_post_interval(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    try:
        seconds = int(message.text.split()[1])
        global auto_post_interval
        auto_post_interval = seconds
        bot.send_message(user_id, f"Awto poster aralygy {seconds} sekunt boldy.")
        start_auto_post()
    except:
        bot.send_message(user_id, "Dogry san giriziň: Meselem: Aralyk 60")

# Agza Boldum düwmesi üçin
@bot.message_handler(func=lambda m: m.text == "Agza Boldum")
def agza_boldum_handler(message):
    user_id = message.chat.id
    # Elbetde, hakykatdan kanal agzalygy barlanmaly. Häzirki wagtda simulýasiýa.
    users[user_id]["subscribed"] = True
    bot.send_message(user_id, "👏🏼 Siz kanallara üstünlikli agza bolduňyz! Indi VPN koduny alyp bilersiňiz.")

# VPN Kodumy Al düwmesine basylanda
@bot.message_handler(func=lambda m: m.text == "VPN Kodumy Al")
def give_vpn_code(message):
    user_id = message.chat.id
    if not users.get(user_id, {}).get("subscribed", False):
        send_subscription_menu(user_id)
        return
    code = get_free_vpn_code()
    if code:
        mark_vpn_code_used(code)
        users[user_id]["vpn_code"] = code
        bot.send_message(user_id, f"🎉 Siziň VPN kodyňyz: {code}\n#Hyzmat üçin sag boluň!")
    else:
        bot.send_message(user_id, "Gynansak-da, elýeterli VPN kodlary gutardy. Administrator bilen habarlaşyň.")

# Admin goşmak / aýyrmak
@bot.message_handler(func=lambda m: m.text == "Admin Goşmak / Aýyrmak")
def admin_add_remove_menu(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Admin Goş", "Admin Aýyr", "Yza", "Çykmak")
    msg = bot.send_message(user_id, "Näme isleýärsiňiz?", reply_markup=markup)
    bot.register_next_step_handler(msg, process_admin_add_remove)

def process_admin_add_remove(message):
    user_id = message.chat.id
    text = message.text
    if text == "Admin Goş":
        msg = bot.send_message(user_id, "Goşmak isleýän adminiň user_id-ni giriziň:")
        bot.register_next_step_handler(msg, add_admin_by_id)
    elif text == "Admin Aýyr":
        msg = bot.send_message(user_id, "Aýyrmak isleýän adminiň user_id-ni giriziň:")
        bot.register_next_step_handler(msg, remove_admin_by_id)
    elif text == "Yza":
        show_admin_panel(user_id)
    else:
        bot.send_message(user_id, "Başga zat talap edilmedi.")

def add_admin_by_id(message):
    user_id = message.chat.id
    try:
        new_admin_id = int(message.text)
        admins.add(new_admin_id)
        if new_admin_id not in users:
            users[new_admin_id] = {"username": None, "subscribed": False, "vpn_code": None, "is_admin": True}
        else:
            users[new_admin_id]["is_admin"] = True
        bot.send_message(user_id, f"Ulanyjy {new_admin_id} admin hökmünde goşuldy.")
    except:
        bot.send_message(user_id, "User_id doly san bolmaly.")

def remove_admin_by_id(message):
    user_id = message.chat.id
    try:
        rem_admin_id = int(message.text)
        if rem_admin_id in admins:
            admins.remove(rem_admin_id)
            if rem_admin_id in users:
                users[rem_admin_id]["is_admin"] = False
            bot.send_message(user_id, f"Ulanyjy {rem_admin_id} adminlykdan aýryldy.")
        else:
            bot.send_message(user_id, "Bu ulanyjy admin däl.")
    except:
        bot.send_message(user_id, "User_id doly san bolmaly.")

# Her gezek ulanyjy /start ýazylanda ýa-da başda işledi
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    user_id = message.chat.id
    if is_spam(user_id):
        bot.send_message(user_id, "💢 Köp habar ýazmaň, wagt beriň.")
        return

    text = message.text.lower()
    if text == "agza boldum":
        agza_boldum_handler(message)
    elif text == "vpn kodumy al":
        give_vpn_code(message)
    elif text == "admin panel":
        if users.get(user_id, {}).get("is_admin"):
            show_admin_panel(user_id)
        else:
            bot.send_message(user_id, "Admin däl.")
    else:
        bot.send_message(user_id, "Näme isleýändigiňizi düşündirip bilersiňizmi?")

# Bot işledilýär
print("Bot işläp başlady...")
bot.infinity_polling()
