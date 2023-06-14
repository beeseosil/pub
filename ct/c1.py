import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
from sklearn.multiclass import OneVsRestClassifier

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from collections import Counter
import matplotlib.pyplot as plt

df=pd.read_csv("c:/code/ct/mental_health.csv")

df.isna().any()
if not df.text.nunique()==df.shape[0]:
    df=df.drop_duplicates()

df.label.value_counts().plot.barh()
plt.title("Label Classes Number"),plt.xlabel("Number"),plt.ylabel("Label Class")
plt.show()

print("regex")
df["text_"]=df.text.str.lower()
if df.text.isin(("#","@")).any():
    def sanitize_(text):
        text=re.sub(r"@\S+","",text)
        text=re.sub(r"#\S+","",text)
        return text
    df["text_"]=df.text_.apply(sanitize_)

print("stopwords")
def sanitize__(text,stopwords=stopwords.words("english")):
    text=nltk.word_tokenize(text)
    text=[word for word in text if not word in stopwords]
    return text
df["text__"]=df.text_.apply(sanitize__)

print("lemmatise")
def sanitize___(text,lemma=WordNetLemmatizer()):
    text=[lemma.lemmatize(word) for word in text]
    return " ".join(text)
df["text___"]=df.text__.apply(sanitize___)

df.to_csv("a.csv",index=False,encoding="utf-8")

word=Counter([ val for sublst in df.text__ for val in sublst ]).most_common(50)
word=pd.DataFrame(word,columns=["word","count"])
word.plot.barh(x="word"),plt.title("Words Count"),plt.show()

#Tf-Idf vectorise of x_
print("tf-idf vectorise")
tfidf=TfidfVectorizer()
x_train=tfidf.fit_transform(df.text___)
y_train=df.label

lr_param={
    "estimator__penalty":["l1","l2","elasticnet"],
    "estimator__max_iter":[int(q) for q in (1e4,1e6,1e8)],
    "estimator__verbose":[0],
    "estimator__n_jobs":[-1]
}
lr=BaggingClassifier(LogisticRegression())
lr_=GridSearchCV(lr,param_grid=lr_param)
lr_.fit(x_train,y_train)
y_pred_lr=lr_.best_estimator_.predict(x_train)
ac_lr=accuracy_score(y_train,y_pred_lr)

svc=BaggingClassifier(SVC())
svc.fit(x_train,y_train)
y_pred_svc=svc.predict(x_train)
ac_svc=accuracy_score(y_train,y_pred_svc)

rf_param={
    "estimator__min_samples_leaf":[10,40,100],
    "estimator__n_estimators":[100,400],
    "estimator__verbose":[0],
    "estimator__n_jobs":[-1],
}
rf=BaggingClassifier(RandomForestClassifier())
rf_=GridSearchCV(rf,param_grid=rf_param)
rf_.fit(x_train,y_train)
y_pred_rf=rf_.best_estimator_.predict(x_train)
ac_rf=accuracy_score(y_train,y_pred_rf)

cm=confusion_matrix(y_train,y_pred,labels=lr_.classes_)
disp=ConfusionMatrixDisplay(cm,display_labels=lr_.classes_)
disp.plot(),plt.show()

# test
from sklearn.linear_model import Perceptron

pcp_param={
    "estimator__penalty":["l1","l2"],
    "estimator__max_iter":[1000,2000,5000],
    "estimator__verbose":[1],
    "estimator__n_jobs":[-1],
    "n_jobs":[-1]
}
pcp=OneVsRestClassifier(Perceptron())
pcp_=GridSearchCV(pcp,param_grid=pcp_param)
pcp_.fit(x_train,y_train)
pcp_.best_estimator_
pcp_.best_score_