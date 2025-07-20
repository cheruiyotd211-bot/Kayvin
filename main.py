import os
import time
import requests
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

DERIV_APP_ID = os.environ.get("DERIV_APP_ID")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def check_market():
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
                Bot(token=BOT_TOKEN).send_message(chat_id=CHAT_ID, text="Signal: UNDER 9")
            elif last_price < 5:
                Bot(token=BOT_TOKEN).send_message(chat_id=CHAT_ID, text="Signal: RECOVERY UNDER 5")

scheduler = BlockingScheduler()
scheduler.add_job(check_market, "interval", minutes=15)
scheduler.start()
