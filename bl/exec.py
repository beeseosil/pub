import warnings
warnings.simplefilter("ignore", UserWarning)

import os
import json
import datetime
import pandas as pd
import gspread as gs

ornament="-"*10
datetimeFormat="%y%m%d%H%M%S"
cols=("BATCH","LOCALE","INPUT","OUTPUT","DATE","RESULT")

class wks:
    def __init__(self,key):
        self.key=key
        self.gs=gs.service_account(self.key)
    def open(self,shtname,wksname):
        self.sht=self.gs.open(shtname)
        self.wks=self.sht.worksheet(wksname)
        print(ornament,f"got {shtname}, {wksname}")
        return None
    def get(self,datafile):
        print(ornament,"updating datafile unconditionally..")
        _data=pd.DataFrame(self.wks.get_values()).drop(0)
        _data.columns=cols
        _data.to_csv(datafile,index=False,encoding="utf-8")
        return None
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
            print(ornament,f"failed to open ({err})")
        return None
    def show(self):
        return pd.DataFrame(self.hx)
    def save(self):
        json.dump(self.hx,open(self.hxfile,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        return None

key="c:/code/blkey.json"
datafile="c:/code/bl.csv"

bl=wks(key)
bl.open("daily","bl")
history=hx()

successive=False

while True:
    if not successive:
        if os.path.exists(datafile):
            print(ornament,"found bl.csv")
            prev=pd.read_csv(datafile,encoding="utf-8")
        else:
            print(ornament,"failed to locate bl.csv, creating one..")
            bl.get(datafile)

    answer=input("read clipboard: ").lower()

    if not answer:
        break
    elif answer in ("reset","set"):
        print(ornament,"resetting..")
        bl.wks.resize(prev.shape[0],prev.shape[1])
        bl.set(prev)
        continue
    elif answer=="get":
        bl.get(datafile)
        continue
    elif answer=="y":
        data=[]
        while answer=="y":
            try:
                this=pd.read_clipboard(header=None,usecols=(0,1,2,3,4,6))
            except Exception as err:
                print(ornament,f"{err}")
            else:
                data.append(this)
            finally:
                answer=input("continue: ").lower()
                if answer=="y":
                    continue
                break
    else:
        print(ornament,f"no such method '{answer}'")
        continue
    
    this=pd.concat(data)
    print(f"{ornament} got {this.shape[0]} rows")

    print(ornament,"processing..")
    this=this.set_axis(cols,axis=1)

    this.DATE=pd.to_datetime(this.DATE.apply(lambda q:q[:8]),format="%m/%d/%y").astype("str")
    
    thisBatchMacLattice=this.BATCH.str.contains("Mac")
    this.BATCH[thisBatchMacLattice]="MAS"
    this.BATCH[~thisBatchMacLattice]="AAS"
    
    this.OUTPUT=this.OUTPUT.str.replace("<br>"," ")

    ima=pd.concat([prev,this])
    ima=ima.drop_duplicates(["BATCH","DATE","INPUT","OUTPUT"],keep="first",ignore_index=True).sort_values("DATE",ascending=False)
    ima.to_csv(datafile,index=None,encoding="utf-8")

    print(ornament,"writing..")
    response=bl.set(ima)
    response["datetime"]=datetime.datetime.now().strftime(datetimeFormat)

    if not history.rowcursor is None:
        history.hx.append(response)
    else:
        history.hx=[response]
    history.save()

    continue
