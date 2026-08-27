import os, yfinance as yf, requests
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NY = pytz.timezone('America/New_York')

def send(m):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=15)
    except: pass

def check():
    tickers = ["AAPL","NVDA","MSFT","TSLA","SPY","QQQ"]
    msg = f"📊 تقرير {datetime.now(NY).strftime('%I:%M %p')}\n\n"
    for t in tickers:
        try:
            tk = yf.Ticker(t)
            price = tk.fast_info.last_price
            prev = tk.fast_info.previous_close
            ch = ((price-prev)/prev)*100 if prev else 0
            msg += f"{t}: ${price:.2f} ({ch:+.2f}%)\n"
        except:
            msg += f"{t}: --\n"
    send(msg)

if __name__ == "__main__":
    check()     emoji="🟢" if direction=="CALL" else "🔴"
     msg=f"{emoji} ${t} - {direction} {int(r['strike'])} {exp} (${last}) | Stock ${curr:.1f} EMA20 ${ema20:.1f}"
     send(msg)
     break
   break
 except: continue
