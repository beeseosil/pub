import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Get dataset
## Data is longitudinal and having absolute time values
indices=["user_id","phq.day"]
datafile="c:/code/x.csv"

## Drop the unnecessaries
data=pd.read_csv(datafile).drop(["Unnamed: 0","id"],axis=1).dropna(subset=["phq1","phq2","phq9"])

# Convert absolute times to relative time values (longitudinal indices)
## Ordering data by user_id, phq.day
data=data.sort_values(indices)

## Min-max scaling phq.day per user_id
mms=MinMaxScaler()
data["timedelta"]=data.groupby("user_id")["phq.day"].transform(
    lambda q:mms.fit_transform(q.to_numpy().reshape(-1,1)).reshape(-1)
)

# PHQ Evaluation
## Essential PHQ
phqEssential=data.loc[:,["phq1","phq2"]].gt(1).all(axis=1)

## Self-harm PHQ
phqZasal=data.loc[:,["phq9"]].gt(0).all(axis=1)

## Shaded PHQ
phqShaded=data.loc[phqEssential,[f"phq{q}" for q in range(1,9)]].gt(1).sum(axis=1)+phqZasal
phqShaded=phqShaded.fillna(0)
data["phqShaded"]=phqShaded

## Total Score
phq=data.loc[:,[q for q in data.columns if q[-1].isdigit() and q[:3]=="phq"]].sum(axis=1)
data["phq"]=phq

## idd: Initial Diagnosed Depression
idd=data[data.index.isin(data.groupby("user_id")["phq.day"].idxmin())].phqShaded.gt(3)
idd=data.user_id.isin(data[data.index.isin(idd.index)].user_id).rename("idd")

## mdd
mdd=data.phqShaded.gt(4).rename("mdd")

## odd
odd=((1<data.phqShaded) * (data.phqShaded<5)).rename("odd")

data=pd.concat([data,idd,mdd,odd],axis=1)



