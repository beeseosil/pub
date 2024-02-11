import os
import json
import datetime
import pandas as pd
import gspread as gs

import warnings
warnings.simplefilter("ignore", UserWarning)

ornament=". . ."
datetimeFormat="%y%m%d%H%M%S"

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
        print(ornament,"updating datafile unconditionally")
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

def exec():
    cols=("BATCH","LOCALE","INPUT","OUTPUT","DATE","RESULT")
    
    key="c:/code/blkey.json"
    datafile="c:/code/bl.csv"

    bl=wks(key)
    bl.open("daily","bl")
    history=hx()

    data=[]
    successive=False

    while True:
        if not successive:
            if os.path.exists(datafile):
                prev=pd.read_csv(datafile,encoding="utf-8")
            else:
                print(ornament,"failed to locate bl.csv, creating")
                bl.get(datafile)
            successive=True

        answer=input("read clipboard: ").strip().lower()

        if not answer:
            continue

        elif answer in ("reset"):
            print(ornament,"resetting")
            bl.wks.resize(prev.shape[0],prev.shape[1])
            bl.set(prev)
            continue

        elif answer=="get":
            bl.get(datafile)
            successive=False
            continue

        elif answer=="y":
            try:
                this=pd.read_clipboard(header=None,usecols=(0,1,2,3,4,6))
            except Exception as err:
                print(ornament,f"{err}")
            else:
                data.append(this)
            finally:
                continue

        elif answer=="go":
            if len(data)==0:
                print(ornament,"Zero-length data")
                continue

            this=pd.concat(data).set_axis(cols,axis=1)

            this.DATE=pd.to_datetime(this.DATE.apply(lambda q:q[:8]),format="%m/%d/%y").astype("str")

            thisBatchMacLattice=this.BATCH.str.contains("Mac")
            this.BATCH[thisBatchMacLattice]="MAS"
            this.BATCH[~thisBatchMacLattice]="AAS"

            this.OUTPUT=this.OUTPUT.str.replace("<br>"," ")

            ima=pd.concat([prev,this])
            ima=ima.drop_duplicates(["BATCH","DATE","INPUT","OUTPUT"],keep="first",ignore_index=True).sort_values("DATE",ascending=False)
            ima.to_csv(datafile,index=None,encoding="utf-8")

            print(ima.DATE.value_counts(sort=False)[:5].to_string())

            print(ornament,"writing")
            # response=bl.set(ima)
            
            # response["datetime"]=datetime.datetime.now().strftime(datetimeFormat)
            # if not history.rowcursor is None:
            #     history.hx.append(response)
            # else:
            #     history.hx=[response]
            # history.save()
            
            data=[]
            successive=False
            continue

        elif answer=="exit":
            if len(data)==0:
                print(ornament,"Did nothing")
                break
            print(ornament,"There's unloaded data")
            continue

        else:
            print(ornament,f"No such method '{answer}'")
            continue

    return 