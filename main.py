import asyncio
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8924529360:AAE04ukDwrdyqhT97N8WMBonru6s8YtqJaY"
GROUP_ID = -1003960957591  # آیدی درست شده گروه شما

ADMIN_LINKS = {
    "mahdi": "https://t.me/begoo?start=_3688788873410",
    "admin2": "https://t.me/begoo?start=_3688788873410",
    "admin3": "https://t.me/begoo?start=_3688788873410"
}

MY_FEEDBACK_LINK = "https://t.me/begoo?start=_3688788873410"

# تابع چک عضویت
async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(GROUP_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# تابع کمکی برای تولید منوی اصلی (برای جلوگیری از تکرار کد)
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
            [InlineKeyboardButton("عضویت در گروه", url="https://t.me/your_group_link")],
            [InlineKeyboardButton("بررسی عضویت", callback_data="check")]
        ]
        await update.message.reply_text(
            "اول باید عضو گروه بشی 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # ارسال منوی اصلی در دستور start
    await update.message.reply_text(
        "یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=get_main_keyboard()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # بررسی عضویت
    if query.data == "check":
        if await is_member(context.bot, user_id):
            # اگر عضو بود، پیام قبلی ویرایش میشه به منوی اصلی و دیگه پیام اضافه ساخته نمیشه
            await query.edit_message_text(
                text="عضویت شما تایید شد ✅\nیکی از گزینه‌ها رو انتخاب کن:",
                reply_markup=get_main_keyboard()
            )
        else:
            # استفاده از alert برای اینکه پیام اضافی فرستاده نشه و فقط یک پیغام پاپ‌آپ باز بشه
            await query.answer(text="هنوز عضو نشدی ❌ اول داخل گروه عضو شو.", show_alert=True)
        return

    # بازگشت به منوی اصلی
    if query.data == "back_to_main":
        await query.edit_message_text(
            text="یکی از گزینه‌ها رو انتخاب کن:",
            reply_markup=get_main_keyboard()
        )
        return

    # منوی ادمین‌ها (ویرایش پیام قبلی + اضافه شدن دکمه بازگشت)
    if query.data == "admins":
        keyboard = [
            [InlineKeyboardButton("mahdi", url=ADMIN_LINKS["mahdi"])],
            [InlineKeyboardButton("ادمین 2", url=ADMIN_LINKS["admin2"])],
            [InlineKeyboardButton("ادمین 3", url=ADMIN_LINKS["admin3"])],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")] # دکمه بازگشت
        ]
        await query.edit_message_text(
            text="یکی از ادمین‌ها رو انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # انتقاد و پیشنهاد (ویرایش پیام قبلی + اضافه شدن دکمه بازگشت)
    elif query.data == "feedback":
        keyboard = [
            [InlineKeyboardButton("ارسال پیام", url=MY_FEEDBACK_LINK)],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")] # دکمه بازگشت
        ]
        await query.edit_message_text(
            text="از اینجا پیام بده 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    print("Bot is running...")
    
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        await app.updater.stop()
        await app.stop()

if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
