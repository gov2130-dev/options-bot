import os, yfinance as yf, requests
from datetime import datetime
import pytz
BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
NY=pytz.timezone('America/New_York')
def send(m):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",data={"chat_id":CHAT_ID,"text":m})
def check():
    msg=""
    for t in ["AAPL","NVDA","TSLA"]:
        try:
            tk=yf.Ticker(t)
            p=tk.fast_info.last_price
            msg+=f"{t}: {p}\n"
        except: pass
    send(msg)
if __name__=="__main__":
    check()
