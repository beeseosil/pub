import os
import json
import time
import numpy as np
import pandas as pd
import seaborn as sns
from collections import Counter

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

CP="utf-8"

os.chdir("c:/code/ct")

# visual check
train=pd.read_json("input/train.json",encoding=CP).set_index("id")
test=pd.read_json("input/test.json",encoding=CP).set_index("id")

# load data
train_=json.load(open("input/train.json",encoding=CP))
x_=[",".join(q["ingredients"]) for q in train_]
y_=[q["cuisine"] for q in train_]

# encode y_
lb=LabelEncoder()
y_=lb.fit_transform(y_)

#Tf-Idf binary vectorise of x_
tfidf=TfidfVectorizer(binary=True)
x_=tfidf.fit_transform(x_)

x_train,y_train=x_,y_
test_=json.load(open("input/test.json",encoding=CP))
x_test=[",".join(q["ingredients"]) for q in test_]
x_test=tfidf.transform(x_test) # Tf-Idf vectorise of x in x_ vectors

t0=time.time()
svc=OneVsRestClassifier(SVC(verbose=1))
svc.fit(x_train,y_train)
print(f"{time.time()-t0:.1f}s")
y_pred=svc.predict(x_train)
svc_acc=accuracy_score(y_train,y_pred)

t0=time.time()
lr=OneVsRestClassifier(LogisticRegression(penalty="l2",max_iter=int(1e8),verbose=1),n_jobs=-1)
lr.fit(x_train,y_train)
print("elasped:",f"{time.time()-t0:.1f}s")
y_pred=lr.predict(x_train)
lr_acc=accuracy_score(y_train,y_pred)



y_test=svc.predict(x_test) # prediction
y_cuisine=lb.inverse_transform(y_test) # code to label
y_id=[q["id"] for q in test_]
y_result=pd.DataFrame({"id":y_id,"cuisine":y_cuisine},columns=["id","cuisine"])
y_result.to_csv("answer.csv",index=False)