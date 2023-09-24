import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv
from lib.battery import Battery
from systemd import journal
from datetime import datetime, timedelta

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

async def log_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.effective_chat.id) in allow_list:
        j = journal.Reader()
        j.add_match('CODE_FILE=/home/strompi/battery/daemon.py')
        j.seek_realtime(datetime.now() - timedelta(hours=8))
        response = ''
        for entry in j:
            response = response.join([entry['_SOURCE_REALTIME_TIMESTAMP'].strftime('%H:%M:%S'), ' ', entry['MESSAGE'], '\n'])

        await update.message.reply_text(response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).read_timeout(30).write_timeout(30).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("pwrsys", pwrsys_command))
    application.add_handler(CommandHandler("pwr", pwr_command))
    application.add_handler(CommandHandler("log", log_command))

    application.run_polling()