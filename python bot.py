pip install python-telegram-botfrom telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

#7942505805:AAHIql8FZisOgYK_zvWSBmhEx5L9McaxhTk
TOKEN = 'YOUR_BOT_TOKEN'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 مرحبا! أنا بوت إدارة المجموعة. استخدم /help لرؤية الأوامر.")

def help(update: Update, context: CallbackContext):
    help_text = """
    📜 **الأوامر المتاحة**:
    - /start: بدء البوت
    - /help: عرض هذه الرسالة
    - /ban <user_id>: حظر عضو
    - /unban <user_id>: إلغاء حظر عضو
    - /mute <user_id>: كتم عضو
    - /unmute <user_id>: إلغاء كتم عضو
    - /delete: حذف رسالة (رد على الرسالة)
    """
    update.message.reply_text(help_text)

def ban_user(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.id not in [admin.user.id for admin in update.effective_chat.get_administrators()]:
        update.message.reply_text("❌ أنت لست مشرفًا!")
        return
    try:
        user_id = int(context.args[0])
        update.effective_chat.ban_user(user_id)
        update.message.reply_text(f"🚫 تم حظر العضو {user_id}.")
    except:
        update.message.reply_text("⚠️ استخدام: /ban <معرف_العضو>")

# أضف دوال مشابهة لـ unban, mute, unmute, etc.

def delete_message(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        update.message.reply_to_message.delete()
        update.message.delete()

def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(f"🎉 أهلا بك {member.first_name} في المجموعة!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ban", ban_user))
    dp.add_handler(CommandHandler("delete", delete_message))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
