import os
from dm import *

# variables
specpath="C:/code/CUBEDEMO2017/spec.xlsx"
datapath="C:/code/CUBEDEMO2017/SASSET/"

# executions
spec=Spec(pd.read_excel(specpath))

sasobj=[obj for obj in os.scandir(datapath) if any(map(obj.path.lower().__contains__,ext)) and obj.is_file()]
sasbad=[obj for obj in sasobj if obj.stat().st_size<3]
if len(sasbad)>1:raise Exception("exotic file exists")

data={os.path.splitext(obj.name)[0].upper():read_sas_(obj.path) for obj in sasobj}
print(ornament,"domain:\n",data.keys(),len(data),"domains")
[data[f"{domain}"].to_csv(f"{datapath}{domain}.csv",index=False,encoding="utf-8") for domain in data.keys()]

sn=data["SN"]
lb=data["LB"]
