import os
import numpy as np
import pandas as pd
import secrets

# citation: cafe.naver.com/dmisimportant/

# variables
ornament="-"*10
hangul="가나다라마바사아자차카파타하"
ext=(".sas7bdat",".xport")
path_crf="C:/code/CUBEDEMO2017/CUBEDEMO_2017_dc_or_fmt.xlsx"
path_lab="C:/code/CUBEDEMO2017/CUBEDEMO_2017_dc_or_lar.xlsx"
path_set="C:/code/CUBEDEMO2017/SASSET/"

# aggregate files, tables
form_crf=pd.read_excel(path_crf)
form_lab=pd.read_excel(path_lab)
print(ornament,"domain formats:",os.linesep,form_crf.DOMAIN.unique())

sasobj=[obj for obj in os.scandir(path_set) if any(map(obj.path.lower().__contains__,ext)) and obj.is_file()]
sasbad=[obj for obj in sasobj if obj.stat().st_size<3]
if len(sasbad)>1:raise Exception("exotic file exists")

def _decode(filepath):
    data=pd.read_sas(filepath)
    nas=data.notna().value_counts().sum()
    bytecol=data.select_dtypes("object").columns
    data[bytecol]=data[bytecol].apply(lambda q:q.str.decode("utf-8"))
    if nas==data.notna().value_counts().sum():
        return data
    else:
        print(ornament,"error:",filepath)
        return None

data={os.path.splitext(obj.name)[0].upper():_decode(obj.path) for obj in sasobj}
print(ornament,"domain:",os.linesep,data.keys(),os.linesep,len(data),"domains")

# SN
def _aname(name,n=2,chars=hangul):
    surffix="".join([secrets.choice(chars) for q in range(n)])
    return name[:n]+surffix

sn=data["SN"]
sn_snname_mapper={name:_aname(name) for name in sn.SNNAME.unique()}
sn.SNNAME.replace(sn_snname_mapper,inplace=True)
ix=sn.SUBJID.unique()
print(ornament,"total subjects:",len(ix))

# DM
dm=data["DM"]

# AE
ae_=form_crf[form_crf.DOMAIN=="AE"]
ae=data["AE"]

# VS
vs=data["VS"]

def _get_label(form,var="VARNAME",kvp=["END","LABEL"]):
    label={}
    for varname in form[var].unique():
        kv=form[form[var]==varname].loc[:,kvp].values
        label[varname]={k:v for k,v in kv}
    return label

lb=data["LB"]
lb.info()
lb.groupby(["LBTEST"])["LBORRES"].agg(["mean","std","min","max","sum"])

def _gen_mockup_value(desc,count):
    print(ornament,"generating values")
    return {q:np.random.normal(desc.loc[q]["mean"],desc.loc[q]["std"],count) for q in desc.index}

def _gen_mockup(desc,ix,count=10):
    data=_gen_mockup_value(desc,count=len(ix)*count)
    ix=pd.MultiIndex.from_product([ix,[q for q in range(1,count+1,1)]],names=["SUBJID","VISIT"])
    return pd.DataFrame(data,ix).reset_index()

mock.merge(dm,on="SUBJID")
# join은 index-based
