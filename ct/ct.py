import datetime
import numpy as np
import pandas as pd

# 변수 모음
datetimeFormat="%Y%m%d%H%M%S"
a="https://clinicaltrials.gov/api/query/study_fields?expr="
b="&fields=NCTId%2CBriefTitle%2CCondition%2COverallStatus%2CLeadSponsorName%2CEligibilityCriteria"
c="&min_rnk=1&max_rnk=1000&fmt=csv"
BITGEN=np.random.default_rng()

# 클래스 모음
class ctFrame:
    def __init__(self,cond,local=True): # 웹 API 리절트 데이터프레임 만들기
        self.recvDate=datetime.datetime.now().strftime(datetimeFormat)
        self.cond=cond.replace(" ","%20")
        self.url=a+self.cond+b+c
        if local:
            self.df=pd.read_csv("./ct.csv",index_col="NCTId")
        else:
            self.df=pd.read_csv(self.url,skiprows=10).loc[:,"NCTId":].set_index("NCTId")
            self.df[pd.isna(self.df)]="none"
            print(self.df,f"by {self.recvDate}")
        self.df.to_csv("./ct.csv",index=True)
        self.status=list(set(self.df["OverallStatus"].values))
        return None
    def __repr__(self):
        __colNames=[q[:7] for q in self.df.columns]
        return f"query: {self.cond}, shape: {self.df.shape}, cols: {__colNames}"
    def validVal(self,colidx=None): # Categoricals 찾기
        if colidx is None:
            col="OverallStatus"
        else:
            col=self.df.columns[colidx]
        print(col)
        return list(set(self.df[col].values))
    def byStatus(self,status=None): # OverallStatus 따라 표시하기
        if status is None:
            status=self.status[0]
        __viewport=self.df.loc[:,"OverallStatus"]
        __viewportIndex=__viewport[__viewport==status].index
        return self.df.loc[__viewportIndex]
    def byCond(self,cond): # Condition 따라 표시하기
        __viewport=self.df.loc[:,"Condition"]
        __viewportIndex=__viewport[__viewport.str.contains(cond)].index
        return self.df.loc[__viewportIndex]

# 명령 모음
def genId_(): # 시리얼 넘버 생성
    pass
def mesh(df,n=500,proportion=.6): # 뽑기
    viewportIndex=sorted(df.index)
    meshedIndex=BITGEN.choice(viewportIndex,size=n,replace=False)
    expArmSize=np.random.binomial(n,proportion)
    expArm=BITGEN.choice(meshedIndex,size=expArmSize,replace=False)
    conArm=list(set(meshedIndex)-set(expArm))
    expArmLen=len(expArm)
    conArmLen=len(conArm)
    if expArmLen+conArmLen!=n:
        raise ValueError(f"overlapping result {expArmLen=}, {conArmLen=}")
    return (expArm,conArm)
def decorate_col_(df): # 장식하기
    viewCols=df.columns
    return [f"{w} (N={len(q.df[w])})" for w in viewCols]

# 실행
q=ctFrame("cml")
q.byStatus()
idx=mesh(q.df)