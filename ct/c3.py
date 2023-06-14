import numpy as np 
import pandas as pd 
import re, string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from imblearn.over_sampling import RandomOverSampler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

data=pd.read_json("c:/code/ct/input/train.json",encoding="utf-8")

def stopword(obj):
    obj=" ".join([word for word in obj if not word in stopwords.words("english")])
    return obj

x=data.ingredients.apply(stopword)

le=LabelEncoder()

y=le.fit_transform(data.cuisine)
print(le.classes_)

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=2330)

tfidf=TfidfVectorizer()
x_train=tfidf.fit_transform(x_train)
x_test=tfidf.transform(x_test)

x_train,y_train=RandomOverSampler(random_state=2330).fit_resample(x_train,y_train)

x_train=pd.DataFrame.sparse.from_spmatrix(x_train)
x_test=pd.DataFrame.sparse.from_spmatrix(x_test)

model_param={
    "learning_rate":[.001,.01,.1,1],
    "reg_alpha":[1e-5, 1e-2, 0.1, 1, 10],
    "reg_lambda":[1e-5, 1e-2, 0.1, 1, 10],
    "tree_method":["gpu_hist"]
}

{'tree_method': 'gpu_hist', 'reg_lambda': 10, 'reg_alpha': 0.1, 'missing': 0, 'learning_rate': 1}

model=XGBClassifier()
cv=RandomizedSearchCV(model,model_param)
cv.best_estimator_.score(x_train,y_train)
