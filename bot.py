import os, yfinance as yf, requests
from datetime import datetime
import pytz

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHAT_ID=os.getenv("CHAT_ID")
NY=pytz.timezone('America/New_York')

def send(m):
    if not m: return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def check():
    now = datetime.now(NY)
    # يشتغل بس وقت السوق 9:30 - 4:00 بتوقيت نيويورك
    if now.weekday() > 4:
        send(f"🐋 حيتان ابو راكان: السوق مقفل اليوم {now.date()}")
        return

    msg = f"🐋 *حيتان ابو راكان - فحص {now.strftime('%I:%M %p')} نيويورك*\n\n"
    found = False

    # نراقب SPX والاسهم الثقيلة
    for t in ["SPY","AAPL","NVDA","TSLA"]:
        try:
            tk = yf.Ticker(t)
            hist = tk.history(period="1d", interval="1m")
            if hist.empty: continue
            p = hist['Close'].iloc[-1]
            v = hist['Volume'].iloc[-1]
            # لو الفوليوم عالي نعتبره حركة حوت
            if v > 100000:
                found = True
                if t == "SPY":
                    # نحولها لتوصية SPX
                    direction = "CALL" if hist['Close'].iloc[-1] > hist['Open'].iloc[0] else "PUT"
                    msg += f"🔥 ${t} {direction} - دخول ${p:.1f} - حركة حوت\n"
                else:
                    msg += f"${t}: ${p:.2f} | Vol: {v}\n"
        except: pass

    if not found:
        msg += "لا يوجد حركة حيتان حاليا - السوق هادئ ✅"

    msg += f"\n⏰ {now.strftime('%Y-%m-%d %H:%M')} NY"
    send(msg)

if __name__=="__main__":
    check()
