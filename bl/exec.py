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
        print("_"*10,f"got:: sheet {shtname}:: {wksname}")
        return None
    def get(self):
        return self.wks.get_all_values()
    def set(self,data):
        return self.wks.update([data.columns.tolist()]+data.values.tolist())

class hx:
    def __init__(self,hxfile="c:/code/blhx.json"):
        self.hxfile=hxfile
        try:
            self.hx=json.load(open(hxfile,"r",encoding="utf-8"))
            self.rowcursor=self.hx[-1]["updatedRows"]
            self.datetime=self.hx[-1]["datetime"]
        except Exception as err:
            self.hx=[]
            self.rowcursor=None
            print(f"failed to open:: {err}")
        return None
    def show(self):
        return pd.DataFrame(self.hx)
    def save(self):
        json.dump(self.hx,open(self.hxfile,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        return None

# 
key="c:/code/blkey.json"
datafile="c:/code/bl.csv"
cols=("BATCH","LOCALE","INPUT","OUTPUT","DATE","RESULT")
BATCH_label={'Search - App Store v2': 'AAS','Search - Mac App Store': 'MAS'}

bl=wks(key)
bl.open("ap_daily","bl")
history=hx()

while True:
    if os.path.exists(datafile):
        print("-"*10,"found bl.csv")
        prev=pd.read_csv(datafile,encoding="utf-8")
    else:
        print("-"*10,"failed to locate bl.csv, creating one..")
        prev=pd.DataFrame(bl.get()).drop(0)
        prev.columns=cols
        prev.to_csv(datafile,index=False,encoding="utf-8")

    answer=input("read clipboard:: ")

    if not answer:
        print("-"*10,"did nothing")
        break
    if answer in ("reset","set"):
        print("-"*10,"resetting..")
        bl.wks.resize(prev.shape[0],prev.shape[1])
        bl.set(prev)
        continue
    if answer=="y":
        data=[]
        while answer=="y":
            try:
                this=pd.read_clipboard(header=None,usecols=[0,1,2,3,4,6])
            except Exception as err:
                print("failed::",err)
                continue
            else:
                data.append(this)
                answer=input("continue:: ")
                if answer=="y":
                    continue
                break
    
    this=pd.concat(data)
    print(f"got {this.shape[0]} rows")

    print("-"*10,"processing..")
    this=this.set_axis(cols,axis=1)
    this.DATE=pd.to_datetime(this.DATE.apply(lambda q:q[:8]),format="%m/%d/%y").astype("str")
    this.BATCH=this.BATCH.apply(lambda q:BATCH_label[q])
    this.OUTPUT=this.OUTPUT.str.replace("<br>"," ")

    ima=pd.concat([prev,this]).sort_values("DATE",ascending=False)
    ima.drop_duplicates(["BATCH","DATE","INPUT","OUTPUT"],keep="first",ignore_index=True,inplace=True)
    ima.to_csv(datafile,index=None,encoding="utf-8")

    print("-"*10,"writing..")
    response=bl.set(ima)
    response["datetime"]=datetime.datetime.now().strftime(datetimeFormat)
    if not history.rowcursor is None:
        history.hx.append(response)
    else:
        history.hx=[response]
    history.save()

    continue
