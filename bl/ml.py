import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

def _truncate(data,n=3):
    '''Get words from series object for n-th'''
    return [q[:n] for q in data]

def _tokenize(data):
    '''Tokenise, encode, vectorise'''
    print("-"*10,"tokenising")
    _x=data[["INPUT","OUTPUT"]].apply(lambda q:q.str.findall(r"[\w]+")).apply(_truncate).apply(lambda q:q.str.join(" "))
    _x=data.INPUT+" "+data.OUTPUT
    _y=data.RESULT
    
    print("-"*10,"encoding")
    tfidf=TfidfVectorizer()
    lb=LabelEncoder()
    _x=tfidf.fit_transform(_x)
    _y=lb.fit_transform(_y)

    return (_x,_y),(tfidf,lb)

def _todf(data):
    '''spmatrix to dataframe'''
    return pd.DataFrame.sparse.from_spmatrix(data)

def _split(data):
    '''Splitting and oversampling'''
    if not isinstance(data,tuple):
        raise TypeError
    
    x,x_,y,y_=train_test_split(data[0],data[1],test_size=.2,random_state=3)
    x,y=RandomOverSampler(random_state=3).fit_resample(x,y)

    return {"x":x,"y":y,"x_":x_,"y_":y_}

# 
data=pd.read_csv("c:/code/bl.csv")
data,obj=_tokenize(data)
data=_split(data)

# param={
#     "estimator__learning_rate":[.001,.01,.1,1],
#     "estimator__reg_alpha":[1e-5, 1e-2, 0.1, 1, 10, 100],
#     "estimator__reg_lambda":[1e-5, 1e-2, 0.1, 1, 10, 100],
#     "estimator__tree_method":["gpu_hist"]
# }

{'estimator__tree_method': 'gpu_hist', 'estimator__reg_lambda': 0.1, 'estimator__reg_alpha': 0.1, 'estimator__learning_rate': 1}
{'estimator__tree_method': 'gpu_hist', 'estimator__reg_lambda': 1e-05, 'estimator__reg_alpha': 1, 'estimator__learning_rate': 1}
{'estimator__tree_method': 'gpu_hist', 'estimator__reg_lambda': 1, 'estimator__reg_alpha': 0.1, 'estimator__learning_rate': 0.1}
{'estimator__tree_method': 'gpu_hist', 'estimator__reg_lambda': 10, 'estimator__reg_alpha': 1e-05, 'estimator__learning_rate': 0.1}

model=BaggingClassifier(XGBClassifier())
cv=RandomizedSearchCV(model,param)
print('''cv.fit(_todf(data["x"]),data["y"])''')
rslt=pd.DataFrame(cv.cv_results_).sort_values(["mean_test_score","std_test_score"],ascending=False)
y__=cv.best_estimator_.predict(data["x_"])
acc=accuracy_score(data["y_"],y__) # 0.355
