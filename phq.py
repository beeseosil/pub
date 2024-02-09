import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

from matplotlib.font_manager import fontManager, FontProperties
fontManager.addfont("./Pretendard-Light.otf")
fontProp=FontProperties(fname="./Pretendard-Light.otf")
sns.set(font=fontProp.get_name(),style="whitegrid",palette="muted")

pd.set_option("display.max_rows",6)
pd.set_option("display.max_columns",10)
pd.set_option("display.expand_frame_repr",False)

# Get dataset
## Data is longitudinal and having absolute time values
datafile="./Dataset_14-day_AA_depression_symptoms_mood_and_PHQ-9.csv"
indices=["user_id","phq.day"]
gomi=["Unnamed: 0","id","start.time","time"]

## Drop unnecessaries
data=pd.read_csv(datafile).drop(gomi,axis=1).dropna(subset=["phq1","phq9"])

# Convert absolute times to relative time values
## Ordering by user_id, phq.day
data=data.sort_values(indices)

## Min-max scaling phq.day per user_id
mms=MinMaxScaler()
data["timedelta"]=data.groupby("user_id")["phq.day"].transform(
    lambda q:mms.fit_transform(q.to_numpy().reshape(-1,1)).reshape(-1)
)

# PHQ Ex. results per user_id
'''Handling PHQ-9 score at the enrollment 
as longitudinal endpoints in the trial are 
[q for q in data.columns if q.startswith("q")].'''

longitudinalQs=[q for q in data.columns if q.startswith("q")]

phqEssential=data.loc[:,["phq1","phq2"]].gt(1).all(axis=1)

phqZasal=data.loc[:,["phq9"]].gt(0).all(axis=1)

phqShaded=data.loc[phqEssential,[f"phq{q}" for q in range(1,9)]].gt(1).sum(axis=1)+phqZasal
phqShaded=phqShaded.fillna(0)
data["phqShaded"]=phqShaded

phq=data[[q for q in data.columns if q[-1].isdigit() and q[:3]=="phq"]].sum(axis=1)
data["phq"]=phq

## idd: Initial Diagnosed Depression
idd=data[data.index.isin(data.groupby("user_id")["phq.day"].idxmin())].phqShaded.gt(3)
idd=data.user_id.isin(data[data.index.isin(idd.index)].user_id).rename("idd").apply(lambda q:"idd" if q else "")
idd.value_counts()

## mdd
mdd=data.phqShaded.gt(4).rename("mdd").apply(lambda q:"mdd" if q else "")

## odd
odd=((1<data.phqShaded) * (data.phqShaded<5)).rename("odd").apply(lambda q:"odd" if q else "")

## Dx Total
diag=(mdd+odd).rename("diag")
diag.loc[diag==""]=None

data=pd.concat([ 
    data.drop("phq.day",axis=1),
    diag
],axis=1)

# Take a Look
## Get more samples per spot, and spot would be an index for most values
data["spot"]=pd.qcut(data.timedelta,10,[q for q in range(1,11)])
perSpot=data.groupby("spot")[longitudinalQs].mean()

grp=sns.lineplot(perSpot,alpha=.8)
grp.set_title("Per Spot Score Changes")
grp.set_xlabel("Spot")
grp.set_ylabel("Score")
sns.move_legend(
    grp,
    title="ICD-10 Depression Questions",
    loc="lower left",
    ncols=4,
)
sns.despine()

## Happiness Score per Spot

## Dx Cat.
perSpotDiag=data.melt(["spot","diag"],longitudinalQs)

grp=sns.lineplot(
    perSpotDiag,
    x="spot",
    y="value",
    hue="diag",
    alpha=.8
)
grp.set_title("Score Changes")
grp.set_xlabel("Time Spot")
grp.set_ylabel("Score")
sns.move_legend(
    grp,
    title="Dx per PHQ-9",
    loc="lower left",
    ncols=4,
)
sns.despine()

## Spot Score Volatility per Crucial PHQ-9 Question



## Spot Score Volatility per Sex, Age, q-mean




