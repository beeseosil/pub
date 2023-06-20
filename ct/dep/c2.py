import os
import pandas as pd
from sklearn.metrics import accuracy_score
from simpletransformers.classification import ClassificationModel,ClassificationArgs
from sklearn.model_selection import train_test_split

os.chdir("c:/code/ct")

# import torch
# https://pytorch.org/get-started/locally/
# torch.cuda.is_available(): Returns True if CUDA is supported by your system, else False
# torch.cuda.get_device_name(torch.cuda.current_device()): Returns name of the CUDA device with ID = ‘device_ID’

df=pd.read_csv("mt.csv").drop("Unnamed: 0",axis=1)

specialty=df.medical_specialty.value_counts()
specialtyOther=specialty[specialty<100]
df.loc[df.medical_specialty.isin(specialtyOther.index.values),"medical_specialty"]=" others"

klass=dict(zip(df.medical_specialty.unique(),list(range(len(df.medical_specialty.unique())))))
df["medical_specialty"]=df.medical_specialty.replace(klass)
df[["transcription","keywords"]]=df[["transcription","keywords"]].fillna(" ")

xy=pd.DataFrame({"text":df.transcription+" "+df.keywords,"labels":df.medical_specialty},columns=["text","labels"])

x_train=xy[["text"]]
y_train=xy[["labels"]]
xy.to_csv("xy.csv",index=False)

_x,x,_y,y=train_test_split(xy.text,xy.labels,stratify=xy.labels,test_size=.15)
_xy=pd.concat([_x,_y],axis=1)
xy=pd.concat([x,y],axis=1)

weight=[1]*len(df.medical_specialty.unique())

learning_rate=1e-5
epoch=3

clf_args=ClassificationArgs(num_train_epochs=epoch,learning_rate=learning_rate,reprocess_input_data=True,save_model_every_epoch=False,overwrite_output_dir=True)
clf=ClassificationModel("roberta","roberta-base",num_labels=len(klass),weight=weight,args=clf_args)
clf.train_model(_xy)
clf.save_model()

result,model_output,wrong_prediction=clf.eval_model(xy)

result,output=clf.predict(xy.text.tolist())
acc=accuracy_score(xy.labels,result)