import yfinance as yf, requests
from datetime import datetime
import pytz

BOT_TOKEN="8594574378:AAEqZ3fbmElLqR2h7..."
CHAT_ID="13889370"
NY=pytz.timezone('America/New_York')

def send(m):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": m, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# رسالة اختبار
send(f"✅ البوت اشتغل! {datetime.now(NY).strftime('%H:%M NY')} - ببدأ فحص {datetime.now().strftime('%H:%M Medina')}")

WATCH=["NVDA","TSLA","AMD","PLTR","META","COIN","HOOD","MSTR"]
for t in WATCH:
 try:
  tk=yf.Ticker(t)
  curr=float(tk.fast_info['last_price'])
  daily=tk.history(period="20d")
  if daily.empty: continue
  daily['EMA20']=daily['Close'].ewm(20).mean()
  ema20=float(daily['EMA20'].iloc[-1])
  chg=(curr/float(daily['Open'].iloc[-1])-1)
  direction="CALL" if curr>ema20 and chg>-0.02 else "PUT" if curr<ema20 and chg<0.02 else None
  if not direction: continue
  today=datetime.now(NY).date()
  exps=[e for e in tk.options if 1<=(datetime.strptime(e,"%Y-%m-%d").date()-today).days<=10][:2]
  for exp in exps:
   days=(datetime.strptime(exp,"%Y-%m-%d").date()-today).days
   opts=tk.option_chain(exp).calls if direction=="CALL" else tk.option_chain(exp).puts
   for _,r in opts.iterrows():
    last=float(r['lastPrice'] or 0)
    if 1.0<=last<=5.0 and float(r['bid'] or 0)>0.3:
     emoji="🟢" if direction=="CALL" else "🔴"
     msg=f"{emoji} ${t} - {direction} {int(r['strike'])} {exp} (${last}) | Stock ${curr:.1f} EMA20 ${ema20:.1f}"
     send(msg)
     break
   break
 except: continue
