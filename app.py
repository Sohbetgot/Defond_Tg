import random
import time
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram.error import BadRequest

# ADMIN AÇAR SÖZI
ADMIN_PASSWORD = "ADNİOBERTİ61"
admin_mode = {}

# DEFAULT SAZLAMALAR
START_MESSAGE = "👋 **Hoş geldiňiz! VPN kody almak üçin kanallara agza boluň!**"
VPN_CODE_FORMAT = "ABCDEFGHIJKL0123456789"  # 12 simwol
REQUIRED_CHANNELS = ["@dm_servers", "@ikinci_kanal"]  # @username görnüşinde
AUTO_POST_INTERVAL = 3600  # 1 sagat (sekuntda)
AUTO_POST_MESSAGE = "📍 **Täze VPN kodlary elýeterli! /start basyp alyň!**"

# ------------------ USER FUNKSIÝALARY ------------------
def start(update: Update, context: CallbackContext):
    buttons = [
        [InlineKeyboardButton("KANAL 1 🇺🇸", url=f"https://t.me/{REQUIRED_CHANNELS[0][1:]}")],
        [InlineKeyboardButton("KANAL 2 🇬🇧", url=f"https://t.me/{REQUIRED_CHANNELS[1][1:]}")],
        [InlineKeyboardButton("✅ AGZA BOLDUM", callback_data="check_sub")]
    ]
    update.message.reply_text(
        START_MESSAGE,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown"
    )

def check_subscription(update: Update, context: CallbackContext):
    user = update.effective_user
    try:
        for channel in REQUIRED_CHANNELS:
            member = context.bot.get_chat_member(chat_id=channel, user_id=user.id)
            if member.status not in ["member", "administrator", "creator"]:
                update.callback_query.message.reply_text("❌ **Ähli kanallara agza bolmaly!**")
                return
        
        vpn_code = ''.join(random.choices(VPN_CODE_FORMAT, k=12))
        update.callback_query.message.reply_text(f"🛡 **Siziň VPN kodynyz:** `{vpn_code}`", parse_mode="Markdown")
    
    except BadRequest:
        update.callback_query.message.reply_text("❌ **Kanal tapylmady! Admin bilen habarlaşyň.**")

# ------------------ ADMIN PANEL ------------------
def admin_login(update: Update, context: CallbackContext):
    if context.args and context.args[0] == ADMIN_PASSWORD:
        admin_mode[update.effective_user.id] = True
        update.message.reply_text(
            "🔐 **Admin paneline giriňiz!**\n\n"
            "/set_start - Start mesajyny üýtget\n"
            "/set_vpn - VPN kod formatyny üýtget\n"
            "/set_channels - Kanallary üýtget\n"
            "/auto_post - Awto-posteri düz\n"
            "/change_pass - Açar sözi üýtget\n"
            "/exit_admin - Çyk",
            parse_mode="Markdown"
        )
    else:
        update.message.reply_text("❌ **Ýalňyş açar sözi!**")

def set_start(update: Update, context: CallbackContext):
    if admin_mode.get(update.effective_user.id):
        global START_MESSAGE
        START_MESSAGE = ' '.join(context.args)
        update.message.reply_text(f"✅ **Start mesajy üýtgedildi:**\n`{START_MESSAGE}`", parse_mode="Markdown")

def set_vpn_format(update: Update, context: CallbackContext):
    if admin_mode.get(update.effective_user.id):
        global VPN_CODE_FORMAT
        VPN_CODE_FORMAT = ' '.join(context.args)
        update.message.reply_text(f"✅ **VPN formaty üýtgedildi:**\n`{VPN_CODE_FORMAT}`", parse_mode="Markdown")

def auto_post(context: CallbackContext):
    while True:
        # Botuň özüne habar iberýär (ulanyjylara ýaýratmak üçin)
        for user_id in admin_mode:  # Adminleriň listi
            try:
                context.bot.send_message(
                    chat_id=user_id,
                    text=AUTO_POST_MESSAGE,
                    parse_mode="Markdown"
                )
            except BadRequest:
                continue  # Ulanyjy boty blok eden bolsa, geç
        time.sleep(AUTO_POST_INTERVAL)

# ------------------ BOT BAŞLATMA ------------------
def main():
    updater = Updater("7660064921:AAHAl0-wL7q5eGgHFlyPCMgW6ow1u4cS1f4", use_context=True)  # @BotFather-dan almaly
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("admin", admin_login))
    dp.add_handler(CommandHandler("set_start", set_start))
    dp.add_handler(CommandHandler("set_vpn", set_vpn_format))
    dp.add_handler(CallbackQueryHandler(check_subscription, pattern="check_sub"))

    # Auto-posteri işe giriz (Diňe botuň özüne)
    Thread(target=auto_post, args=(updater.job_queue,)).start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
