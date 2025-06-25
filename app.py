-- coding: utf-8 --

import telebot from telebot import types import time import threading

Bot tokenini şu ýere goý

TOKEN = '7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4' bot = telebot.TeleBot(TOKEN)

Admin ID'leriň sanawy (ulanyjy ID)

ADMINS = [8143084360]

Admin açar sözi

ADMIN_PASSWORD = 'HRTCEREGET'

Sponsor kanallary (üstünlikli barlamak üçin)

SPONSOR_CHANNELS = ["@DM_SERVERS", "@DM_404CHAT"]

Menýu ýazgysy (admin üýtgedip biler)

menu_text = "👋🏻 Hoş Geldiňiz ! {username}\n📢 VPN kodyny 🎮 Almak uçin Aşaky\ud83d\udc47\uFE0F kanallara Agza Boluň !"

Spamdan goramak (ulanyjy_id: wagt)

last_used = {}

Awto post listi we wagt

auto_posts = []  # [(tekst, sekundy)]

----------- START -----------

@bot.message_handler(commands=['start']) def start(message): if not check_subscription(message.chat.id): send_subscription_menu(message.chat.id) else: username = message.from_user.first_name bot.send_message(message.chat.id, menu_text.format(username=username)) bot.send_message(message.chat.id, "\u2705 Agzalygyňyz barlandy! Kodyňyz: \nvpn-kod-example", parse_mode='Markdown')

----------- KANAL BARLAG -----------

def check_subscription(user_id): for channel in SPONSOR_CHANNELS: try: status = bot.get_chat_member(channel, user_id).status if status not in ['member', 'creator', 'administrator']: return False except: return False return True

def send_subscription_menu(user_id): markup = types.InlineKeyboardMarkup() for ch in SPONSOR_CHANNELS: markup.add(types.InlineKeyboardButton(ch, url=f"https://t.me/{ch[1:]}")) markup.add(types.InlineKeyboardButton("\u2705 AGZA BOLDUM", callback_data='check')) bot.send_message(user_id, "Aşakdaky kanallara agza boluň:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'check') def check_cb(call): if check_subscription(call.from_user.id): username = call.from_user.first_name bot.send_message(call.message.chat.id, menu_text.format(username=username)) bot.send_message(call.message.chat.id, "\u2705 Agzalygyňyz barlandy! Kodyňyz: \nvpn-kod-example", parse_mode='Markdown') else: bot.answer_callback_query(call.id, "\u274C Ilki kanallara agza boluň!")

----------- ADMIN PANEL -----------

@bot.message_handler(commands=['admin']) def admin_start(message): if message.chat.id in ADMINS: send_admin_panel(message.chat.id) else: bot.send_message(message.chat.id, "Açar sözi giriziň:") bot.register_next_step_handler(message, check_password)

def check_password(message): if message.text == ADMIN_PASSWORD: ADMINS.append(message.chat.id) bot.send_message(message.chat.id, "\u2705 Admin panel açyldy") send_admin_panel(message.chat.id) else: bot.send_message(message.chat.id, "\u274C Nädogry açar sözi")

def send_admin_panel(chat_id): markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.add("1. Sponsorlar", "2. Menýu ýazgy") markup.add("3. Bildiriş ugrat", "4. Awto Poster") markup.add("5. Admin goş", "6. Spamlardan goramak") markup.add("❌ Çyk") bot.send_message(chat_id, "Admin panel saýla:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.chat.id in ADMINS) def admin_actions(message): if message.text == "1. Sponsorlar": bot.send_message(message.chat.id, "Täze sponsor kanallary giriziň (formaty: @kanal1 @kanal2):") bot.register_next_step_handler(message, update_sponsors) elif message.text == "2. Menýu ýazgy": bot.send_message(message.chat.id, "Täze menýu ýazgysyny giriziň ({{username}} bilen ulanyjynyň adyny görkezýär):") bot.register_next_step_handler(message, update_menu) elif message.text == "3. Bildiriş ugrat": bot.send_message(message.chat.id, "Ulanyjylara ugratjak habaryňyzy ýazyň:") bot.register_next_step_handler(message, broadcast_message) elif message.text == "4. Awto Poster": bot.send_message(message.chat.id, "Posty giriziň, soňra wagty (sekund):") bot.register_next_step_handler(message, get_autopost_text) elif message.text == "5. Admin goş": bot.send_message(message.chat.id, "Täze admin ID giriziň:") bot.register_next_step_handler(message, add_admin) elif message.text == "6. Spamlardan goramak": bot.send_message(message.chat.id, "Spamlardan goramak işjeň edildi") elif message.text == "❌ Çyk": bot.send_message(message.chat.id, "Panelden çykdy\u2026", reply_markup=types.ReplyKeyboardRemove())

def update_sponsors(message): global SPONSOR_CHANNELS SPONSOR_CHANNELS = message.text.split() bot.send_message(message.chat.id, "\u2705 Sponsorlar täzelendi")

def update_menu(message): global menu_text menu_text = message.text bot.send_message(message.chat.id, "\u2705 Menýu ýazgy täzelendi")

def broadcast_message(message): for user_id in last_used.keys(): try: bot.send_message(user_id, message.text) except: continue bot.send_message(message.chat.id, "Ugratdyk")

def get_autopost_text(message): post_text = message.text bot.send_message(message.chat.id, "Wagty giriziň (sekund):") bot.register_next_step_handler(message, lambda msg: schedule_post(msg, post_text))

def schedule_post(message, post): try: seconds = int(message.text) auto_posts.append((post, seconds)) bot.send_message(message.chat.id, "\u2705 Awto post goşuldy") except: bot.send_message(message.chat.id, "\u274C Nädogry wagt")

def add_admin(message): try: new_id = int(message.text) ADMINS.append(new_id) bot.send_message(message.chat.id, "\u2705 Admin goşuldy") except: bot.send_message(message.chat.id, "\u274C ID nädogry")

----------- AWTO POST MEHANIZMI -----------

def auto_post_worker(): while True: for post, delay in auto_posts: time.sleep(delay) for admin_id in ADMINS: try: bot.send_message(admin_id, post) except: continue

threading.Thread(target=auto_post_worker, daemon=True).start()

----------- POLLING -----------

print("Bot işleýär...") bot.infinity_polling()

