import telebot
from telebot import types

bot = telebot.TeleBot("7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4")  # <-- Bu ýere öz tokeniňi ýaz

# Açarsöz
ADMIN_PASSWORD = "ADNİOBERTİ61"

# Admin panel menu

def admin_paneli():
    panel = types.ReplyKeyboardMarkup(resize_keyboard=True)
    panel.add("⚙️ Sazlamalar", "📊 Statistika")
    panel.add("📰 Awto Poster", "📤 Bildiriş ugrat")
    panel.add("🔙 Çyk")
    return panel

# /start komanda
@bot.message_handler(commands=['start'])
def start_handler(message):
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu.add("📲 Admin panel")
    bot.send_message(message.chat.id, "👋 Hoş geldiňiz! Menýudan saýlaň:", reply_markup=menu)

# Admin panel komanda düwme bilen
@bot.message_handler(func=lambda msg: msg.text == "📲 Admin panel")
def admin_panel_start(message):
    bot.send_message(message.chat.id, "🔐 Açarsözi giriziň:")
    bot.register_next_step_handler(message, barla_acarsöz)

# Açarsöz barlagy

def barla_acarsöz(message):
    if message.text == ADMIN_PASSWORD:
        bot.send_message(message.chat.id, "✅ Admin panel açyldy.", reply_markup=admin_paneli())
    else:
        bot.send_message(message.chat.id, "❌ Nädogry açarsöz.")

# Admin panel düwmeleri bilen işleýän funksiýalar

@bot.message_handler(func=lambda msg: msg.text == "⚙️ Sazlamalar")
def sazlamalar(message):
    sazlama = types.ReplyKeyboardMarkup(resize_keyboard=True)
    sazlama.add("📝 Menýu ýazgy üýtget", "🔑 VPN kod üýtget")
    sazlama.add("📣 Sponsor kanallary üýtget")
    sazlama.add("⬅ Yza")
    bot.send_message(message.chat.id, "⚙️ Sazlamalar bölümi:", reply_markup=sazlama)

@bot.message_handler(func=lambda msg: msg.text == "📊 Statistika")
def statika_handler(message):
    # Mysal üçin diňe san berilýär
    bot.send_message(message.chat.id, "👤 Ulanyjylar: 132")

@bot.message_handler(func=lambda msg: msg.text == "📰 Awto Poster")
def awto_poster(message):
    bot.send_message(message.chat.id, "🛠 Awto poster funksiýasy heniz işlenilýär.")

@bot.message_handler(func=lambda msg: msg.text == "📤 Bildiriş ugrat")
def bildirish_ugrat(message):
    bot.send_message(message.chat.id, "🛠 Bildiriş ugratma funksiýasy heniz işlenilýär.")

@bot.message_handler(func=lambda msg: msg.text == "🔙 Çyk" or msg.text == "⬅ Yza")
def cyk_handler(message):
    start_handler(message)

# Boty başlat
print("🤖 Bot işläp başlady...")
bot.infinity_polling()
