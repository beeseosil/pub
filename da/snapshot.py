from da import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

nthread=12

f_=getdata(save=True)
f=f_.copy()

# x(cb, ic), y(pr)
cb=f.cb.resample("m").mean().dropna()
ic=f.ic.resample("m").mean()
pr=f.pr.dropna().diff().reindex(pd.date_range(start=cb.index.min(),end="2023-05-31",freq="d")).ffill().reindex(cb.index)
adp=f.adp.dropna().diff().reindex(pd.date_range(start=cb.index.min(),end="2023-05-31",freq="d")).ffill().reindex(cb.index)/1000

df_=pd.concat([cb,ic,pr],axis=1).dropna(thresh=2)[1:]
df=scipy.stats.zscore(df_)

x=df.iloc[:-1,[0,1]].apply(lambda q:scipy.stats.yeojohnson(q)[0])
x_=pd.DataFrame(df.iloc[-1,[0,1]]).T
y=df.iloc[:-1,2]

estimator=RandomForestRegressor()
param_grid={
    "max_depth":[8,16,32],
    "min_samples_leaf":[8,32,64],
    "min_samples_split":[8,32,64],
    "n_estimators":[100,200,400],
}

note=[]
while len(note)<=100:
    print("attempt #",len(note))
    estimator_grid=GridSearchCV(estimator=estimator,param_grid=param_grid,n_jobs=nthread,verbose=1)
    estimator_grid.fit(x,y)
    y_=estimator_grid.best_estimator_.predict(x_)
    note.append(y_[0])

print(estimator_grid.best_params_)
print(f'estimation: {x_.index[0].strftime("%Y-%m-%d")}:',pr.mean()+(pr.sem()*estimator_grid.best_estimator_.predict(x_))[0])
