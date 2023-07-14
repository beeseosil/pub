import os
from time import time
from datetime import datetime
import numpy as np
import scipy.stats
import pandas as pd
import pandas_datareader as pdd
import yfinance
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
from tqdm import tqdm
from sklearn.impute import KNNImputer


rnd=np.random.RandomState(0)
pd.options.mode.copy_on_write = True
pd.options.display.max_rows=6
pd.options.display.max_columns=4
pd.options.display.precision=5
plt.rcParams['figure.figsize']=[12,5]
sns.set_theme(style="whitegrid",palette="bright",font="monospace")


intern={
"ci":"CPIAUCSL",
"pi":"PPIACO",
"ii":"PCEPILFE",
"pic":"PI",
"ahe":"CES0500000003",
"hi":"CSUSHPISA",
"cb":"BAMLH0A0HYM2",
"fs":"STLFSI4",
"ic":"ICSA",
"pr":"PAYEMS",
"fr":"DFF",
"nk":"NIKKEI225",
"fert":"PCU325311325311",
"iy":"DFII10",
"us10y":"DGS10",
"us02y":"DGS2",
"ur":"UNRATE",
"adp":"ADPMNUSNERSA",
"cci":"CPILFESL",
"ie":"T5YIE",
"djia":"DJIA"
}
extern={
"zs":"ZS=F",
"zc":"ZC=F",
"zw":"ZW=F",
"hg":"HG=F",
"si":"SI=F",
"ng":"NG=F",
"cl":"CL=F",
"uj":"JPY=X",
"uy":"CNY=X",
"ue":"EURUSD=X",
"hs":"^HSI",
"ks":"^KS11",
"vn":"VNM",
"sp":"^GSPC",
"ndx":"^IXIC",
"us10y":"^TNX"
}


class t:
    def __init__(self):
        self.t0_datetime=datetime.now().strftime("%m-%d %H:%M")
        self.t0=time()
        print(f"{self.t0_datetime} ({self.t0})")
    def __repr__(self):
        t0=self.t0
        t1=time()
        t1_in=datetime.now().strftime("%m-%d %H:%M")
        return f"{self.t0_datetime} ---> {t1_in} ({round((t1-t0)/60,1)})"


def ntfys(series:pd.DataFrame,target:list=["sp","ks","cb"])->pd.DataFrame:
    ntfys=series["us02y"]-series["fr"]
    ntfys.name="ntfys"
    s_=pd.concat([series[target],ntfys],axis=1)
    return s_


def v_range(series:pd.DataFrame,v:float,ticker:str="ks",target:str="sp",mod=.015):
    s_=series[[ticker,target]].loc["2020":].dropna()
    s_=s_[(s_[target] >= v * (1-mod))&(s_[target] <= v * (1+mod))][ticker]
    min_=s_.min()
    mid_=s_.mean()
    max_=s_.max()
    std_=s_.std()
    return [round(q) for q in (min_,mid_,max_,std_)]


def theta(v:float)->float: # results intraday decaying per minute
    decayingPerHour=(v/(6.5*60))*10
    return round(decayingPerHour,2)


def rtn_(ticker:str,f:pd.DataFrame,days:int=20)->float:
    rtn=round((f[ticker].dropna().pct_change()*100)[-1*days:].std(),2)
    print(rtn,"%")
    return rtn
# sp[(sp.pct_change()*100).round(2)>= 1*sp_]["2023"]
# sp[(sp.pct_change()*100).round(2)<=-1*sp_]["2023"]


def apnd(path:str)->pd.DataFrame:
	if not path.endswith("/"):path+="/"
	return pd.concat([pd.read_csv(f"{path}{q.name}") for q in os.scandir(path) if ".csv" in q.name],axis=0)


def index_full_range(f:pd.DataFrame):
    return pd.DataFrame(index=pd.date_range(f.index.min(),f.index.max(),freq="D"))


def getdata(days_visit=100,save=False):
    f=pd.read_csv("c:/code/f.csv",index_col="date",converters={"date":pd.to_datetime})
    
    renew_data_end=pd.Timestamp("today").floor("d")
    
    if days_visit<0:
        renew_data_start=pd.Timestamp("1980-01-01")
        f=pd.DataFrame(index=pd.date_range("1980-01-01",renew_data_end,freq="D"))
    else:
        renew_data_start=f.index.max()-pd.Timedelta(days=days_visit)

    with open("c:/code/fred.key",encoding="utf-8-sig") as fredkey:
        fredkey=fredkey.readline()
    renew_data_fred=(pdd.DataReader(list(intern.values()),"fred",start=renew_data_start,end=renew_data_end,api_key=fredkey)
        .rename({q:w for w,q in intern.items()},axis=1))

    yfinance.pdr_override()
    renew_data_yahoo=(pdd.data.get_data_yahoo(list(extern.values()),start=renew_data_start,end=renew_data_end)
        .loc[:,"Close"]
        .rename({q:w for w,q in extern.items()},axis=1))

    renew_data=renew_data_fred.combine_first(renew_data_yahoo)

    if days_visit<0:
        f=renew_data
    else:
        f=f.reindex(pd.date_range(f.index.min(),renew_data_end,freq="D")).combine_first(renew_data)
        f.update(renew_data)
    f.index.name="date"

    print(f[["us02y","uj","ks","sp"]].tail(3))
    
    if save:
        f.to_csv("c:/code/f.csv")
        return f
    else:
        ask=input("input to save above::")
        if ask in ["y","Y"]:
            f.to_csv("c:/code/f.csv")
    
    return f


def mon(f:pd.DataFrame,start,stop)->np.ndarray:
    return np.asarray(sum([f.index.month==q for q in range(start,stop,1)]),dtype="bool")


def dtr(arr,o=1):
    # ii-a-i
    if any(np.isnan(arr)):
        raise ValueError(f"nan in the array")
    a=arr.copy()
    x=np.arange(len(a))
    q=np.polyval(np.polyfit(x,a,deg=o),x)
    a-=q
    return a


def arigeo(a)->tuple:
    # pp. 479
    a=a.dropna()
    mean_ari=np.mean(a)
    mean_geo=np.exp(np.mean(np.log(a)))
    median_ari=np.median(a)
    return (mean_ari,mean_geo,median_ari)


def distrb(f:pd.Series):
    # pp. 467
    trs={
    "noop":lambda x:x,
    "log" :np.log,
    "sqrt":np.sqrt,
    "cbrt":np.cbrt,
    "inv" :lambda x:-1/x,
    "sq"  :lambda x:x*x,
    "cb"  :lambda x:x*x*x,
    "diff":np.diff}
    deta_cont=f.dropna()
    deta_name=deta_cont.name
    fg,ax=plt.subplots(1,len(trs),figsize=(23,4),layout="constrained")
    fg.suptitle(f"transformations::{deta_name}")
    for q in enumerate(trs):
        ax[q[0]].hist(trs[q[1]](deta_cont),edgecolor="black")
        ax[q[0]].set_title(q[1])

# todo #
def deflator(f):
    fa=pd.concat([f.ci.ffill(),f.ie.interpolate().ffill()],axis=1).dropna()
    fb=fa.ci * (1+(fa.ie/100))
    return fb


def act(t,i=None):
    # if deflator is None, just calculate lzp
    if t.name=="ng" or t.name=="spr":
        a=t.dropna()
        a_=t.dropna()
    elif not i is None:
        a=pd.concat([t,i],axis=1).dropna()
        a_=a.iloc[:,0] # i
        a=a.iloc[:,0] / a.iloc[:,1] # i_
    else:
        a=t.dropna()
        a_=t.dropna()
    # using yeo-johnson
    if not int(np.sign(a).sum())==len(a):
        a_l=scipy.stats.yeojohnson(a)[0]
    else:
        if t.name=="zs":
            a_l=np.log(np.log(a))
        else:
            a_l=np.log(a)
    # de-ta
    a_ls   =scipy.stats.zscore(a_l)
    a_lsp  =scipy.stats.norm.cdf(a_ls,loc=a_ls.mean(),scale=a_ls.std(ddof=1))
    a_lsp_f=pd.Series(a_lsp,index=a.index)
    return pd.concat([a_,a,a_lsp_f],axis=1).set_axis([f"{t.name}",f"{t.name}_",f"{t.name}lp"],axis=1)


def nav(f:pd.DataFrame,i:str,v:float):
    rowidx=np.abs(f[f"{i}"]-v).argmin()
    colidx=f.columns.get_indexer([f"{i}"])[0]
    viewport=f.iloc[rowidx,colidx:colidx+2]
    cdf_i=viewport[1]
    print(f"{cdf_i*100:.5f}%")
    return viewport


def roll_pct(f,i,dur=5,start="2022",ax=None,figsize=(8,8),title=""):
    d=f[i].dropna().rolling(dur).mean().pct_change().iloc[1:]
    d_std=np.std(d)
    if ax is None:
        # creating plt canvas
        fg,ax=plt.subplots(figsize=figsize)
    else:
        # mutating input ax
        fg=False
    ax.plot(d[f"{start}":])
    ax.set_title(title)
    [ax.axhline(y=d_std*q,linestyle="dotted",alpha=.7,color="red") for q in (-2,-1,1,2)]
    return fg or None


def rng(f:pd.DataFrame,i:str,
        rng=(.05,3),test=False)->pd.DataFrame:
    f=f.copy()
    if not i in f.columns:
        raise NameError(f"{i} does not exist")
    col=f"{i}lzp"
    if test:
        rng=np.delete(
            np.round(np.flip(
            np.geomspace(rng[0],1,rng[1])),2),2)
    else:
        rng=np.round(np.flip(
            np.percentile(f[col].dropna(),(2,15,30,100))),2)
    f.loc[:,f"{col}rng"]=None
    for q in range(len(rng)):
        f.loc[:,f"{col}rng"]=np.where(
        (~pd.isna(f[col])) & (f[col]<=rng[q]),
        rng[q],
        f[f"{col}rng"])
    f_=f.loc[:,f"{col}rng"].astype("category").copy()
    f.update(f_)
    return f


def ns(f:pd.DataFrame,x:str,y:str):
    f=f[[x,y]].dropna()
    rowidx=np.amin((f.count()[x],f.count()[y]))
    return f[f.shape[0]-rowidx:]


def cx(f:pd.DataFrame,x:str,y:str,d=180,
       normed=True,save=True,detrend=None,test=False):
    # pp. 261
    f=ns(f,y,x)
    freq=f.index.freq.freqstr
    if detrend is None:
        detrend=lambda q:q
    if save:
        plt.figure(figsize=(22,14))
        xc=plt.xcorr(f[y],f[x],
            detrend=detrend,maxlags=d,normed=normed)
        plt.suptitle(f"{freq} {y},{x},{d}")
        plt.savefig(f"e:/capt/{freq}_{y}_{x}_{d}.png")
        plt.cla(),plt.clf(),plt.close()
        idx=abs(xc[1]).argmax()
        return xc[0][idx],xc[1][idx]
    fg,ax=plt.subplots(1,2)
    ac=ax[0].acorr(f[x],
        detrend=detrend,maxlags=d)
    xc=ax[1].xcorr(f[y],f[x],
        detrend=detrend,maxlags=d,normed=normed)
    fg.suptitle(f"{freq}_{freq} {y},{x},{d}")
    ac_=ac[0][abs(ac[1]).argmax()]
    xc_=xc[0][abs(xc[1]).argmax()]
    if test:
        return (ac[0],ac[1]),(xc[0],xc[1])
    return ac_,xc_


def cx_(f:pd.DataFrame,x,d=12):
    f=f[x]
    cache=[]
    for col in tqdm(list(product(x,x)),desc=f"cx-rel"):
        if not col[0] is col[1]:
            rslt=cx(f[[col[0],col[1]]],
                col[0],col[1],d=d,save=True)
            cache.append((col[0],col[1],rslt[0],np.round(rslt[1],2)))
    rslt=(pd.DataFrame(cache,columns=["x","y","dur","coef"])
            .sort_values(by="coef",ascending=False)
            .set_index(keys=["x","y"])
            .sort_index())
    return rslt


def impt(f:pd.DataFrame,x,n=10)->pd.DataFrame:
    return (pd.DataFrame(
        KNNImputer(n_neighbors=n,weights="distance").fit_transform(f),
            index=f.index,columns=x))


# innermost visualisations
def hm(f,mm=(-1,1),ax=None,cbar=False,title=None):
    # pp.201
    if title is None:
        title=f"{', '.join(f.columns)}"
    mask=np.triu(np.ones_like(f,dtype=bool))[1:,:-1]
    f=f.iloc[1:,:-1]
    cmap=sns.diverging_palette(250,10,as_cmap=True)
    if ax is None:
        plt.subplots(figsize=(22,20))
    plt.title(title)
    sns.heatmap(f,
        mask=mask,cmap=cmap,ax=ax,cbar=cbar,
        vmin=mm[0],vmax=mm[1],
        annot=True,center=0,square=True,linewidths=.5,fmt=".2f")


def hm_(f):
    if len(f.columns)>20:
        q=input(f"{len(f.columns)} columns:: ")
        if not q:
            raise ValueError(f"{len(f.columns)} is too much")
    _,ax=plt.subplots(1,3,figsize=(22,16))
    hm(f,
        title=f"",ax=ax[0])
    ax[0].title.set_text("org")
    hm(f.dropna(),
        title=f"",ax=ax[1])
    ax[1].title.set_text("dropna")
    hm(impt(f,f.columns),
        title=f"",ax=ax[2])
    ax[2].title.set_text("impt")


def pp(f,vars=None,l=False,hue=None):
    (sns.pairplot(data=f,vars=vars,hue=hue,
        dropna=False,kind="scatter",diag_kind="hist")
        .map_diag(sns.histplot,log_scale=l,
        multiple="stack",element="step"))


def vs(f,x:str,y:str):
    fg,ax=plt.subplots()
    ax0=ax.twinx()
    ax.plot(f.loc[:,x],label=x,color="red")
    ax0.plot(f.loc[:,y],label=y,color="blue")
    ax.set_ylabel(x)
    ax0.set_ylabel(y)
    h,l=ax.get_legend_handles_labels()
    fg.legend(h,(),loc="upper center")


def rp(f,x,y,
    hue=None,size=None,sizes=(20,200)):
    sns.relplot(data=f,x=x,y=y,hue=hue,size=size,sizes=sizes)
