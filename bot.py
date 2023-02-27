import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
from battery import Battery

load_dotenv()
allow_list = os.getenv('TELEGRAM_ALLOW_LIST').split(',')
battery = Battery()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) in allow_list:
        await update.message.reply_text("Willkommen im Strom-Kabuff der Lessingstraße 1! \nSchreib mir /pwrsys oder /pwr um den derzeitigen Stand der Batterien zu lesen.")
    else:
        await update.message.reply_text("Sorry, but you are not allowed to use this bot. Your ID is: " + update.effective_chat.id)

async def pwrsys_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) in allow_list:
        await update.message.reply_text(battery.exec('pwrsys'))

async def pwr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) in allow_list:
        await update.message.reply_text(battery.exec('pwr'))

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("pwrsys", pwrsys_command))
    application.add_handler(CommandHandler("pwr", pwr_command))

    application.run_polling()