import os
import numpy as np
import pandas as pd
import secrets

# variables
gen=np.random.default_rng(2330)
ornament="-"*10
hangul="가나다라마바사아자차카파타하"
ext=(".sas7bdat",".xport")
specpath="C:/code/CUBEDEMO2017/spec.xlsx"
datapath="C:/code/CUBEDEMO2017/SASSET/"

# methods
class Spec:
    def __init__(self,specfile):
        spec=specfile.dropna(how="all",axis=1)
        spec["CODE"]=[dict(q.split(":") for q in w.split("|")) if isinstance(w,str) else w for w in spec.CODE]
        self.data=spec.copy()
        self.map=spec.set_index(["DOMAIN","ITEMID"]).T.to_dict()
        return None

def _read_sas(filepath):
    data=pd.read_sas(filepath)
    nas=data.notna().value_counts().sum()
    bytecol=data.select_dtypes("object").columns
    data[bytecol]=data[bytecol].apply(lambda q:q.str.decode("utf-8"))
    if nas==data.notna().value_counts().sum():
        return data
    else:
        print(ornament,"error:",filepath)
        return None

def type_length(type_length):
    typechar=type_length[0]
    if typechar=="C":
        return str,int(type_length[1:])
    elif typechar=="N":
        lenchar=type_length[1:]
        if "." in lenchar:
            deci=lenchar.index(".")
            x0=lenchar[:deci]
            x1=lenchar[deci+1:]
            return float,sum(map(int,(x0,x1)))+1
        return float,int(lenchar)
    raise NotImplementedError("")

def _edit_check(data,ect):
    if isinstance(data,pd.Series):
        data=data.to_frame()
    data["_TYPE"]=[isinstance(q,ect[0]) for q in data.iloc[:,0]]
    if all(data._TYPE):
        if ect[1]==2:
            return True
        data["_LEN"]=data.iloc[:,0].str.len()==ect[1]
        if all(data._LEN):
            return True
    print(ornament,"ec failed")
    return data[~(data._TYPE+data._LEN)]

def edit_check(data,ect,key=None):
    if isinstance(data,pd.DataFrame):
        raise NotImplementedError(f"{data.name} is not a series")
    data_nan=pd.isna(data)
    if pd.isna(key):
        return _edit_check(data[~data_nan],ect)
    if any(data_nan):
        print(ornament,f"ec failed {key=}")
        return data[data_nan]
    return _edit_check(data,ect)

def _gen_mockup(desc,count):
    print(ornament,"generating values")
    return {q:gen.normal(desc.loc[q]["mean"],desc.loc[q]["std"],count) if pd.notna(desc.loc[q]["std"])
             else gen.binomial(1,.1,count) for q in desc.index}

def gen_mockup(desc,ix,count=10):
    data=_gen_mockup(desc,count=len(ix)*count)
    ix=pd.MultiIndex.from_product([ix,[q for q in range(1,count+1,1)]],names=["SUBJID","VISIT"])
    return pd.DataFrame(data,ix).reset_index()

def hide(name,n=2,chars=hangul):
    suffix="".join([secrets.choice(chars) for _ in range(n)])
    return name[:n]+suffix

# executions
spec=Spec(pd.read_excel(specpath))

sasobj=[obj for obj in os.scandir(datapath) if any(map(obj.path.lower().__contains__,ext)) and obj.is_file()]
sasbad=[obj for obj in sasobj if obj.stat().st_size<3]
if len(sasbad)>1:raise Exception("exotic file exists")

data={os.path.splitext(obj.name)[0].upper():_read_sas(obj.path) for obj in sasobj}
print(ornament,"domain:\n",data.keys(),"\n",len(data),"domains")
[data[f"{domain}"].to_csv(f"{datapath}{domain}.csv",index=False,encoding="utf-8") for domain in data.keys()]

sn=data["SN"]
ix=sn.SUBJID.unique()
sn_snname_map={name:hide(name) for name in ix}
sn.SNNAME.replace(sn_snname_map,inplace=True)
print(ornament,"total subjects:",len(ix))

lb=data["LB"]
lb_desc=lb.groupby(["LBTEST"])["LBORRES"].agg(["mean","std"])
mockup=gen_mockup(lb_desc,ix,count=100)
print(mockup.sample(10))

# spec_usecol=["DOMAIN","PAGE_LABEL","VISIT","ITEMID","ITEM_SEQ","ITEM_LABEL","CODE","TYPE_LENGTH","VIEW_TYPE"]
# spec[spec_usecol]

# import json
# spec_dict=json.loads(spec[spec_usecol].set_index("DOMAIN").to_json(orient="records",indent=2))

# spec=pd.read_excel(path_spec).loc[:,:"VIEW_TYPE"]
# spec["CODE"]=spec.CODE.apply(lambda q:dict(item.split(":") for item in q.split("|")) if pd.notna(q) else q).dropna()
# spec.CODE.sample(10)

# mh=data["MH"]
# mh.MHONGO
# print(ornament,"\nCRF Name: ",mh_MHONGO_spec[0],"\nForm Label: ",mh_MHONGO_spec[1],"\nCode: ",mh_MHONGO_spec[2])

