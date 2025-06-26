import telebot
from telebot import types

TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4'
bot = telebot.TeleBot(TOKEN)

# Kanallar: [("DM CHANEL", "https://t.me/dm_servers")]
channels = [("DM CHANEL", "https://t.me/dm_servers")]
menu_text = "\u2709 Menýu:\n1. Post goşmak\n2. Postlary görmek\n3. Postlary arassala\n4. Aralyk (sekundda): 'Aralyk <sekund>'"

admin_password = "ADNİOBERTİ61"
admins = set()

def check_subscribe_buttons():
    markup = types.InlineKeyboardMarkup()
    for name, link in channels:
        markup.add(types.InlineKeyboardButton(text=name, url=link))
    markup.add(types.InlineKeyboardButton("\u2705 AGZA BOLDUM", callback_data="check_subs"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in admins:
        text = "\u2709 Ilki bilen aşakdaky kanallara agza boluň:"
        bot.send_message(user_id, text, reply_markup=check_subscribe_buttons())
    else:
        bot.send_message(user_id, menu_text)

@bot.message_handler(commands=['admin_gir'])
def admin_gir(message):
    msg = bot.send_message(message.chat.id, "\ud83d\udd10 Açarsözi giriziň:")
    bot.register_next_step_handler(msg, check_password)

def check_password(message):
    if message.text == admin_password:
        admins.add(message.chat.id)
        bot.send_message(message.chat.id, "\u2705 Admin paneline üstünlikli girildi!", reply_markup=admin_panel_buttons())
    else:
        bot.send_message(message.chat.id, "\u274c Nädogry açarsöz!")

def admin_panel_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("\ud83d\udd27 Sazlamalar")
    markup.add("\ud83d\udcca Statika", "\ud83d\udd22 Awto Poster")
    markup.add("\u274e Çyk")
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subscriptions(call):
    user_id = call.from_user.id
    not_subscribed = []

    for _, channel_link in channels:
        try:
            channel_username = channel_link.split("/")[-1]
            member = bot.get_chat_member(f"@{channel_username}", user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel_username)
        except Exception:
            not_subscribed.append(channel_username)

    if not_subscribed:
        bot.answer_callback_query(call.id, "\ud83d\udeab Käbir kanallara heniz agza bolan dälsiňiz!", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "\u2705 Ulgama üstünlikli girildi!")
        bot.send_message(call.message.chat.id, menu_text)

bot.infinity_polling()
