import streamlit as st
from datetime import datetime
from da import *

# ornament
dff_next_bp=.25
dff_after_decision=4.58
st.set_page_config(page_title="Product Snapshot",layout="centered")
print(f"{datetime.now()}::initialized")

# yielding st.experimental_memo
def getdata_(path="c:/code/f.csv"):
    return pd.read_csv(path,index_col="date",converters={"date":pd.to_datetime})
f=getdata_()

# head
st.header("Product Snapshot")
prods=["Indices","Commodities","Utilities","Citations"]
t0,t1,t2,t3=st.tabs(prods)

# cache
pr=f.pr.dropna().diff().reindex(f.index)
ic=f.ic.resample("d").mean()
cb=f.cb.resample("d").mean()
ahe=f.ahe.dropna().pct_change()

# tab
with t0:
    # row
    st.subheader("Latest Quotes")
    cols=["us02y","iy","cb","fr"]
    cols_nm=["U.S.02Y","U.S.10Y-I","C.B.Y.S.","F.F.R."]
    data={q:f[q].dropna().iloc[-2:] for q in cols}
    for q in enumerate(st.columns(len(cols))):
        q[1].metric(
            label=f"{cols_nm[q[0]]} ({data[cols[q[0]]].index.max().strftime('%m-%d')})",
            value=f"{data[cols[q[0]]][-1]:.3f}",
            delta=f"{data[cols[q[0]]].diff()[-1]:.3f} ({data[cols[q[0]]].pct_change()[-1]*100:.2f}%)")
    # row
    st.subheader("NTFYS + 5YIE")
    st.markdown("log us02y-ffr, 5yie, normalized")
    spread=(f.us02y-f.fr).dropna()
    spread_log=pd.Series(scipy.stats.yeojohnson(spread)[0],index=spread.index)
    spread_zscore=scipy.stats.zscore(spread_log)
    data=pd.concat([spread_zscore,scipy.stats.zscore(f.ie.dropna())],axis=1).set_axis(["spread","ie"],axis=1).dropna()
    fg,ax=plt.subplots(figsize=(8,4))
    data.loc["2008":].plot(alpha=.8,ax=ax)
    ax.axhline(color="orange",linestyle="dotted",alpha=.7,y=data.ie[-1])
    ax.axhline(color="blue",linestyle="dotted",alpha=.7,y=data.spread[-1])
    ax.margins(x=0)
    st.pyplot(fg)
    # row
    st.subheader("U.S.02Y, F.F.R.")
    st.markdown("us02y, dff+upcoming bp")
    data=f[["fr","us02y"]].loc["2022":]
    if pd.isna(f.fr[-1]):
        data["fr"][-1]=dff_after_decision
    else:
        data=data.ffill(limit=3).dropna()
    fg,ax=plt.subplots(figsize=(8,4))
    data.us02y.plot(alpha=.8,ax=ax)
    ax.axhline(color="red",linestyle="dotted",alpha=.7,y=data.iloc[-1,0]+dff_next_bp)
    ax.margins(x=0)
    st.pyplot(fg)
    # row
    st.subheader("Corporate Yield Spread, ICSA, NFP")
    ur=f.ur
    ys=(spread_log*-1).rename("ys_inv")
    data=pd.concat([pr,ic,cb],axis=1)
    dur=st.slider("Duration (year)",min_value=data.index.min().year,max_value=data.index.max().year,value=(2022,2023),step=1,key="2")
    data_=data.apply(lambda q:scipy.stats.zscore(q,nan_policy="omit")).loc[f"{dur[0]}":f"{dur[1]}"].interpolate(limit_area="inside")
    trim=2
    data_.pr[data_.pr>=trim]=trim
    data_.pr[data_.pr<=-trim]=-trim
    data_.ic[data_.ic>=trim]=trim
    data_.ic[data_.ic<=-trim]=-trim
    data_.cb[data_.cb>=trim]=trim
    data_.cb[data_.cb<=-trim]=-trim
    fg,ax=plt.subplots(figsize=(8,4))
    targets=["cb","ic","pr"] # control
    data_[targets].plot(alpha=.7,ax=ax)
    ax.margins(x=0)
    ax.set_ylabel("MoM diff. or pct. change")
    plt.xticks(rotation=60)
    st.pyplot(fg)
    # row
    st.subheader("Price Indices")
    cols=["cci","ii"]
    cols_name=["CCPI","CPCE","PR"]
    data=pd.concat([(f[cols].dropna(how="all").pct_change()[1:]),pr.resample("m").mean()],axis=1).apply(lambda q:scipy.stats.zscore(q,nan_policy="omit"))
    dur=st.slider("Duration (year)",min_value=data.index.min().year,max_value=data.index.max().year,value=(2021,2023),step=1,key="1")
    data_=data.loc[f"{dur[0]}":f"{dur[1]}"]
    fg,ax=plt.subplots(figsize=(8,4))
    ax.plot(data_,alpha=.8)
    ax.set_ylabel("MoM diff. or pct. change")
    ax.legend(cols_name)
    plt.xticks(rotation=60)
    st.pyplot(fg)
    # row
    from_=2008
    freq="d"
    f_cols=["sp","ndx","hs","ks"]
    f0=f[f_cols][f"{from_}":]
    f1=f0.resample(freq).mean().pct_change().dropna()
    fg,ax=plt.subplots(figsize=(6,6))
    hm(f1.corr(),ax=ax)
    st.subheader("Correleation")
    st.markdown("몇 가지 계열의 1차 변화율의 Pearson 상관계수 "+f"({from_}~).")
    st.pyplot(fg)
with t1:
    # param
    cols=["cl","ng","si","hg","zs"]
    cols_nm=["W.T.I.","Nat-Gas","Silver","Copper","Soybean"]
    # row 0
    st.subheader("Latests")
    st.markdown("주요 원자재의 가격, 명목 가격의 상위 %.")
    ie=deflator(f)
    data={q:act(f[q],ie).dropna().iloc[-5:] for q in cols}
    for q in enumerate(st.columns(len(cols))):
        data_=data[cols[q[0]]]
        data_name=cols_nm[q[0]]+f" ({data_.index.max().strftime('%m-%d')})"
        data_vals=data_.iloc[-2:]
        q[1].metric(
            label=f"{data_name}",
            value=f"{data_vals.iat[-1,0]:.2f}",
            delta=None,delta_color="off")
    # row 1
    for q in enumerate(st.columns(len(cols))):
        data_=data[cols[q[0]]]
        data_name=cols_nm[q[0]]
        data_vals=data_.iloc[-2:]
        q[1].metric(
            label=f"{data_name} LP",
            value=f"{data_vals.iat[-1,2]*100:.2f}%",
            delta=None,delta_color="off")
    # row 2
    # st.subheader("Rolled Standard Deviation")
    # st.markdown("x일 변화율 평균의 표준편차의 1,2 표준점수(σ). BSM (60)")
    # dur=st.slider(
    #     "Duration (days)",
    #     min_value=5,
    #     max_value=200,
    #     value=60,
    #     step=5,)
    # cols=["cl","ng","si","hg","zs"]
    # for q in enumerate(cols):
    #     st.pyplot(roll_pct(f,q[1],dur=dur,figsize=(8,4),title=f"{cols_nm[q[0]]}"))
with t2:
    # params
    examplars=[("cb","fs"),("cb","ic"),("cl","ie"),("ng","fert")]
    # row
    st.subheader("Linregress")
    st.markdown("단선형회귀.")
    # q0,q1=st.columns(2)
    # x0_=q0.selectbox("x",f.columns)
    # y0_=q1.selectbox("y",f.columns)
    # if not x0_==y0_:
    #     # prepare
    #     data=f[[x0_,y0_]].dropna()
    #     obs_num=round(len(data)*.85)
    #     x0y0=data.sample(obs_num)
    #     x0,y0=x0y0.iloc[:,0],x0y0.iloc[:,1]
    #     x1y1=data.sample(len(data)-obs_num)
    #     x1=x1y1.iloc[:,0]
    #     # get equatation
    #     slope,intercept,rval,pval,stderr=scipy.stats.linregress(x0,y0)
    #     y1_guess=[(slope*x)+intercept for x in x1]
    #     y1_answer=x1y1.iloc[:,1]
    #     # plot guesses
    #     fg,ax=plt.subplots(2,1,figsize=(8,8))
    #     ax[0].scatter(x0.values,y0.values,
    #         color="tomato",alpha=.8)
    #     ax[0].plot(x1,y1_guess,
    #         color="navy",alpha=1,linewidth=2)
    #     # plot residues
    #     residue=y1_guess-y1_answer
    #     residue_devi=np.std(residue)*.5
    #     ax[1].scatter(y1_guess,y1_guess-y1_answer,
    #         color="tomato",alpha=.8)
    #     ax[1].hlines(
    #         y=0,
    #         xmin=min(y1_guess)-residue_devi,
    #         xmax=max(y1_guess)+residue_devi,
    #         color="navy",alpha=1)
    #     # render
    #     linreg_params=list(zip(
    #         ("slope","intercept","r-value","p-value"),
    #         (slope,intercept,rval,pval,stderr)))
    #     for q in enumerate(st.columns(len(linreg_params))):
    #         q[1].metric(
    #             linreg_params[q[0]][0],
    #             f"{linreg_params[q[0]][1]:.3f}")
    #     st.pyplot(fg)
    # else:
    #     st.error("Select x (enobs, causes), y (exobs, results)")
    ### testing
    # with st.container():
    #     st.subheader("Tests")
    #     st.markdown("This section is solely for testing purpose.")
    #     imgs={q.name:Image.open(f"asset/{q.name}") for q in os.scandir("asset") if q.name.endswith(".png") or q.name.endswith(".jpg")}
    #     if not len(imgs)==0:
    #         img_sel=st.radio("images",imgs.keys(),label_visibility="hidden")
    #         for img_label in imgs.keys():
    #             if img_label==img_sel:
    #                 st.image(imgs[img_label],)
    #     else:
    #         st.markdown(f"No imagefiles")
with t3:
    st.subheader("Citations")
    with open(f"asset/cite.txt",encoding="utf-8-sig") as citefile:
        sents=citefile.readlines()
    for q in sents:
        st.markdown(q)
        