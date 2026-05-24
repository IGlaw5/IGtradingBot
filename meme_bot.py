
import requests,time,json,os                            from datetime import datetime
P=5.0;T=0.18;S=0.08;M=4;I=30
TOKEN="7723336160:AAGyVIvzbVpYaTH1sHmhov-YzKDFZnvLRB8"
CID="6731899091"                                        O={}
def tg(m):                                               try:requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage",json={"chat_id":CID,"text":str(m)},timeout=5)
 except:pass
def log(m):
 print("["+datetime.now().strftime("%H:%M:%S")+"] "+str(m))
 tg(m)                                                  def lw():
 try:return json.load(open("w.json"))
 except:return {}                                       def sw(w):json.dump(w,open("w.json","w"))
def go():
 try:return json.load(open("o.json"))
 except:return 0                                        def so(o):json.dump(o,open("o.json","w"))
def gd(mint):                                            try:
  r=requests.get("https://api.dexscreener.com/latest/dex/tokens/"+mint,timeout=10).json()
  s=[p for p in r.get("pairs",[]) if p.get("chainId")=="solana"]
  if not s:return None
  p=sorted(s,key=lambda x:float(x.get("liquidity",{}).get("usd",0)or 0),reverse=True)[0]
  return{"price":float(p.get("priceUsd",0)or 0),"p5":float(p.get("priceChange",{}).get("m5",0)or 0),"p1":float(p.get("priceChange",{}).get("h1",0)or 0),"v5":float(p.get("volume",{}).get("m5",0)or 0),"v1":float(p.get("volume",{}).get("h1",0)or 0),"liq":float(p.get("liquidity",{}).get("usd",0)or 0),"name":p.get("baseToken",{}).get("symbol","")}
 except:return None
def ok(d):
 if not d or d["price"]<=0:return False                  if d["liq"]<5000:return False
 if d["p5"]<5:return False
 a=d["v1"]/12 if d["v1"]>0 else 0
 if a>0 and d["v5"]<a*2:return False
 if d["p1"]>60:return False
 return True
def ctg(W):
 try:
  off=go()
  r=requests.get("https://api.telegram.org/bot"+TOKEN+"/getUpdates?offset="+str(off),timeout=5).json()
  for u in r.get("result",[]):
   off=u["update_id"]+1;so(off)
   msg=u.get("message",{}).get("text","")
   if not msg:continue
   pts=msg.strip().split();cmd=pts[0].lower()
   if cmd=="/add" and len(pts)>=2:
    mint=pts[1];d=gd(mint)
    if d:
     nm=d["name"] if d["name"] else "COIN"+str(len(W)+1)
     W[nm]=mint;sw(W)
     tg("Added "+nm+" Price:$"+str(d["price"])+" Liq:$"+str(round(d["liq"])))
    else:tg("Coin not found!")
   elif cmd=="/remove" and len(pts)>=2:                     nm=pts[1].upper()
    if nm in W:del W[nm];sw(W);tg("Removed "+nm)
    else:tg(nm+" not found!")                              elif cmd=="/list":
    if W:tg("Watchlist:\n"+"\n".join([n+" | "+m[:8]+"..." for n,m in W.items()]))
    else:tg("Empty! Send /add CONTRACT")                   elif cmd=="/status":
    if O:                                                    msg="Trades:\n"
     for t,pos in O.items():                                  d=gd(W.get(t,""))
      if d:                                                    pnl=(d["price"]-pos["e"])/pos["e"]*100
       msg+=t+" "+str(round(pnl,1))+"%\n"                    tg(msg)
    else:tg("No open trades!")                             elif cmd=="/stop":tg("Stopping...");os._exit(0)
   elif cmd=="/help":tg("Commands:\n/add CONTRACT\n/remove NAME\n/list\n/status\n/stop")
 except:pass                                             return W
def run():                                               W=lw()
 log("IGtrading BOT STARTED")                            tg("IGtrading STARTED. Send /help")
 while True:                                              try:
   W=ctg(W)                                                if not W:time.sleep(I);continue
   for t,m in list(W.items()):                              d=gd(m)                                                 if not d:continue
    pr=d["price"]                                           if t in O:
     pos=O[t];pnl=(pr-pos["e"])/pos["e"]*100;pu=(pr-pos["e"])/pos["e"]*P
     if pr>=pos["tp"]:log("TAKE PROFIT "+t+" +"+str(round(pnl,1))+"% +$"+str(round(pu,2)));del O[t]
     elif pr<=pos["sl"]:log("STOP LOSS "+t+" "+str(round(pnl,1))+"% $"+str(round(pu,2)));del O[t]
     else:log("HOLDING "+t+" "+str(round(pnl,1))+"% $"+str(round(pu,2)))
     continue                                               if len(O)>=M:continue
    if ok(d):O[t]={"e":pr,"tp":pr*(1+T),"sl":pr*(1-S)};log("ENTRY "+t+" $"+str(pr))
   time.sleep(I)                                          except KeyboardInterrupt:log("Stopped.");break
  except Exception as e:log("Err:"+str(e));time.sleep(10)
if __name__=="__main__":run()
