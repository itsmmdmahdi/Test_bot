import asyncio
import sys
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8924529360:AAE04ukDwrdyqhT97N8WMBonru6s8YtqJaY"
GROUP_ID = -1003960957591  
GROUP_LINK = "https://t.me/SHOLEX_TEL"

ADMIN_LINKS = {
    "mahdi": "https://t.me/begoo?start=_3688788873410"
}
MY_FEEDBACK_LINK = "https://t.me/begoo?start=_3688788873410"

async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(GROUP_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# منوی اصلی (دکمه بازی حذف شد چون کاربر از دکمه Menu/Test_run پایین تلگرام وارد میشه)
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("ارتباط با ناشناس ادمین‌ها", callback_data="admins")],
        [InlineKeyboardButton("انتقاد و پیشنهاد", callback_data="feedback")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not await is_member(context.bot, user_id):
        keyboard = [
            [InlineKeyboardButton("عضویت در گروه", url=GROUP_LINK)],
            [InlineKeyboardButton("بررسی عضویت", callback_data="check")]
        ]
        await update.message.reply_text("اول باید عضو گروه بشی 👇", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text("خوش آمدید! یکی از گزینه‌ها رو انتخاب کن:", reply_markup=get_main_keyboard())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "check":
        if await is_member(context.bot, user_id):
            await query.edit_message_text(text="عضویت شما تایید شد ✅\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=get_main_keyboard())
        else:
            await query.answer(text="❌ هنوز عضو گروه نشدی! اول داخل گروه عضو شو.", show_alert=True)
        return

    if query.data == "back_to_main":
        await query.edit_message_text(text="یکی از گزینه‌ها رو انتخاب کن:", reply_markup=get_main_keyboard())
        return

    if query.data == "admins":
        keyboard = [
            [InlineKeyboardButton("Mahdi", url=ADMIN_LINKS["mahdi"])],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")]
        ]
        await query.edit_message_text(text="ادمین مورد نظرت رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "feedback":
        keyboard = [
            [InlineKeyboardButton("ارسال پیام ناشناس", url=MY_FEEDBACK_LINK)],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")]
        ]
        await query.edit_message_text(text="از طریق دکمه زیر می‌توانید پیام خود را بفرستید 👇", reply_markup=InlineKeyboardMarkup(keyboard))

def run_html_server():
    port = int(os.environ.get("PORT", 8000))
    class MyHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args): pass
    
    with TCPServer(("", port), MyHandler) as httpd:
        print(f"Serving HTML Game on port {port}")
        httpd.serve_forever()

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    print("Bot is running successfully...")
    
    try:
        while True: await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        await app.updater.stop()
        await app.stop()

if __name__ == '__main__':
    html_server_thread = Thread(target=run_html_server, daemon=True)
    html_server_thread.start()

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
