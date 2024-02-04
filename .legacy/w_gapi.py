import os
import json
import datetime
import pandas as pd
import gspread as gs
from app_store_scraper import AppStore


datetimeFormat="%y%m%d%H%M%S"
# bot account key
key="c:/code/gcapikey_bl.json"
gdf="ap_daily"

gc=gs.service_account(filename=key)
wks=gc.open(gdf).worksheet("bl")

# sht1 = gc.open_by_key('0BmgG')
# sht2 = gc.open_by_url('https://docs.google.com/spreadsheet/ccc?key=..')

with open("last","r",encoding="utf-8") as last:
    lastdata=json.load(last)
    lastrow=lastdata[0]["updatedRows"]

cols=["BATCH","LOCALE","INPUT","OUTPUT","DATE","none","RESULT"]
input("read clipboard")
this=pd.read_clipboard(header=None).set_axis(cols,axis=1).drop("none",axis=1).dropna()
this.OUTPUT=this.OUTPUT.str.replace("<br>"," ")
this.DATE=pd.to_datetime(this.DATE.apply(lambda q:q[:8]),format="%m/%d/%y").astype("str")

prev=pd.read_csv("aas.csv",encoding="utf-8")

response=wks.update([this.columns.tolist()]+this.values.tolist())
response["datetime"]=datetime.datetime.now().strftime(datetimeFormat)
with open("last","r+",encoding="utf-8") as last:
    lastdata=json.load(last)
    lastdata.append(response)
    json.dump(lastdata,last,indent=2)

for col in ("BATCH","LOCALE","RESULT"):
    bl[col]=pd.Categorical(bl[col])
bl.BATCH=bl.BATCH.cat.rename_categories(["ASV2","MAS"])

bluo=bl.OUTPUT.drop_duplicates()
bluoid=[]
blUniqueOutputIdsError=[]
for output in bluo:
    try:
        outputId=f'{AppStore(country="kr",app_name=output).app_id}'
    except Exception as e:
        outputId="fail"
        blUniqueOutputIdsError.append((output,e.args[0]))
    bluoid.append(outputId)

pd.merge(pd.DataFrame({"OUTPUT":bluo,"ID":bluoid,}),bl,on="OUTPUT")