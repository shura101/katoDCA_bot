import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
import datetime
import requests
import os

TOKEN = os.getenv("TOKEN")
START_DATE = datetime.date(2025, 5, 17)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo, aku Kato DCA Bot! Aku akan bantu ingatkan kamu beli BTC Rp100.000 dan ETH Rp50.000 setiap 2 minggu."
    )

async def jadwal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    delta_days = (today - START_DATE).days
    next_dca = today + datetime.timedelta(days=(14 - delta_days % 14))
    await update.message.reply_text(f"Jadwal DCA berikutnya: {next_dca.strftime('%A, %d %B %Y')}")

async def harga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=idr").json()
    btc = data['bitcoin']['idr']
    eth = data['ethereum']['idr']
    msg = f"Harga saat ini:\nBTC: Rp{btc:,}\nETH: Rp{eth:,}"
    await update.message.reply_text(msg)

async def reminder_dca(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=os.getenv("CHAT_ID"),
        text="[Pengingat DCA] Hari ini jadwal beli BTC Rp100.000 dan ETH Rp50.000."
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jadwal", jadwal))
    app.add_handler(CommandHandler("harga", harga))

    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(reminder_dca, interval=1209600, first=10)

    app.run_polling()

if __name__ == '__main__':
    main()
