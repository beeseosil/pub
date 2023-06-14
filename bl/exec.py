import os
import json
import datetime
import pandas as pd
import gspread as gs

datetimeFormat="%y%m%d%H%M%S"

class wks:
    def __init__(self,key):
        self.key=key
        self.gs=gs.service_account(self.key)
    def open(self,shtname,wksname):
        self.sht=self.gs.open(shtname)
        self.wks=self.sht.worksheet(wksname)
        print(f"got:: sheet {shtname}:: {wksname}")
        return None
    def set(self,data):
        return self.wks.update([data.columns.tolist()]+data.values.tolist())

class hx:
    def __init__(self,hxfile="history.json"):
        self.hxfile=hxfile
        try:
            self.hx=json.load(open(hxfile,"r",encoding="utf-8"))
            self.rowcursor=self.hx[-1]["updatedRows"]
            self.datetime=self.hx[-1]["datetime"]
        except Exception as err:
            self.hx=[]
            self.rowcursor=None
            print(f"failed to opening history.json: {err}")
        return None
    def show(self):
        return pd.DataFrame(self.hx)
    def save(self):
        json.dump(self.hx,open(self.hxfile,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        return None
    
os.chdir("c:/code/misc/bl")
key="c:/code/gcapikey_bl.json"
cols=["BATCH","LOCALE","INPUT","OUTPUT","DATE","RESULT"]
BATCH_label={'Search - App Store v2': 'AAS','Search - Mac App Store': 'MAS'}

bl=wks(key)
bl.open("ap_daily","bl")
history=hx()

while True:
    prev=pd.read_csv("bl.csv",encoding="utf-8")

    answer=input("read clipboard:: ")
    if not answer:
        print(f"resetting.. {prev.shape}")
        bl.wks.resize(10,10)
        bl.set(prev)
        continue
    if answer in ("exit","quit"):
        break
    if answer=="y":
        try:
            this=pd.read_clipboard(header=None,usecols=[0,1,2,3,4,6])
        except Exception as err:
            print("failed::",err)
            continue

        this=this.set_axis(cols,axis=1).dropna()
        this.DATE=pd.to_datetime(this.DATE.apply(lambda q:q[:8]),format="%m/%d/%y").astype("str")
        this.BATCH=this.BATCH.apply(lambda q:BATCH_label[q])
        this.OUTPUT=this.OUTPUT.str.replace("<br>"," ")

        ima=pd.concat([prev,this]).sort_values("DATE",ascending=False).drop_duplicates(["DATE","INPUT","OUTPUT"],keep="first",ignore_index=True)
        ima.to_csv("bl.csv",index=None,encoding="utf-8")

        response=bl.set(ima)
    
    response["datetime"]=datetime.datetime.now().strftime(datetimeFormat)
    if not history.rowcursor is None:
        history.hx.append(response)
    else:
        history.hx=[response]
    history.save()
    continue
