import asyncio
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8924529360:AAE04ukDwrdyqhT97N8WMBonru6s8YtqJaY"
GROUP_ID = 3960957591  # آیدی گروه

# لینک‌های ناشناس (نکته: دکمه‌های تلگرام نباید لینک خالی داشته باشند، موقتاً لینک مهدی رو گذاشتم تا خودت آپدیت کنی)
ADMIN_LINKS = {
    "mahdi": "https://t.me/begoo?start=_3688788873410",
    "admin2": "https://t.me/begoo?start=_3688788873410",
    "admin3": "https://t.me/begoo?start=_3688788873410"
}

MY_FEEDBACK_LINK = "https://t.me/begoo?start=_3688788873410"

# چک عضویت
async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(GROUP_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_member(context.bot, user_id):
        keyboard = [
            [InlineKeyboardButton("عضویت در گروه", url="https://t.me/SHOLEX_TEL")],
            [InlineKeyboardButton("بررسی عضویت", callback_data="check")]
        ]
        await update.message.reply_text(
            "اول باید عضو گروه بشی 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [InlineKeyboardButton("ارتباط با ناشناس ادمین‌ها", callback_data="admins")],
        [InlineKeyboardButton("انتقاد و پیشنهاد", callback_data="feedback")]
    ]

    await update.message.reply_text(
        "یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # بررسی عضویت دوباره
    if query.data == "check":
        if await is_member(context.bot, user_id):
            await query.message.reply_text("عضویت تایید شد ✅ /start رو بزن")
        else:
            await query.message.reply_text("هنوز عضو نشدی ❌")
        return

    # منوی ادمین‌ها
    if query.data == "admins":
        keyboard = [
            [InlineKeyboardButton("mahdi", url=ADMIN_LINKS["mahdi"])],
            [InlineKeyboardButton("ادمین 2", url=ADMIN_LINKS["admin2"])],
            [InlineKeyboardButton("ادمین 3", url=ADMIN_LINKS["admin3"])]
        ]
        await query.message.reply_text(
            "یکی از ادمین‌ها رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # انتقاد و پیشنهاد
    elif query.data == "feedback":
        keyboard = [
            [InlineKeyboardButton("ارسال پیام", url=MY_FEEDBACK_LINK)]
        ]
        await query.message.reply_text(
            "از اینجا پیام بده 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def main():
    # ساخت اپلیکیشن ربات
    app = Application.builder().token(TOKEN).build()

    # ثبت هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    # راه‌اندازی اصولی ربات سازگار با محیط‌های ابری سرور
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    print("Bot is running...")
    
    # روشن نگه داشتن اسکریپت در سرور
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        await app.updater.stop()
        await app.stop()

if __name__ == '__main__':
    # حل مشکل Event Loop روی سرورهای لینوکسی و رندر
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
