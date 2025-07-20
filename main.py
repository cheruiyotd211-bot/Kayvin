import os
import time
import requests
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import datetime

DERIV_APP_ID = os.environ.get("DERIV_APP_ID")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def check_market():
    tz = timezone('Africa/Nairobi')
    now = datetime.datetime.now(tz)
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    url = f"https://api.deriv.com/binary/websockets/v3?app_id={DERIV_APP_ID}"
    payload = {
        "ticks_history": "R_100",
        "adjust_start_time": 1,
        "count": 10,
        "end": "latest",
        "style": "ticks"
    }

    response = requests.post(url, json=payload)
    if response.ok:
        ticks = response.json().get("history", {}).get("prices", [])
        if ticks:
            last_price = float(ticks[-1])
            if last_price < 9:
                Bot(token=BOT_TOKEN).send_message(chat_id=CHAT_ID, text=f"🚨 Signal: UNDER 9 at {formatted_time}")
            elif last_price < 5:
                Bot(token=BOT_TOKEN).send_message(chat_id=CHAT_ID, text=f"✅ Recovery UNDER 5 at {formatted_time}")

scheduler = BlockingScheduler()
scheduler.add_job(check_market, "interval", minutes=15)
scheduler.start()
