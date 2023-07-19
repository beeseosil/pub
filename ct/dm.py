import numpy as np
import pandas as pd
import secrets

# variables
gen=np.random.default_rng(2330)
ornament="-"*10
hangul="가나다라마바사아자차카파타하"
ext=(".sas7bdat",".xport")

# methods
class Spec:
    def __init__(self,specfile):
        spec=specfile.dropna(how="all",axis=1)
        spec["CODE"]=[dict(q.split(":") for q in w.split("|")) if isinstance(w,str) else w for w in spec.CODE]
        self.data=spec
        self.map=spec.set_index(["DOMAIN","ITEMID"]).T.to_dict()
        return None

def read_sas_(filepath):
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
