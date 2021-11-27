import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import numpy as np
import pickle
new_train=pd.read_csv("new_train.csv")
new_test=pd.read_csv("new_test.csv")

#drop values
new_train.drop('femaleres',axis=1, inplace=True)
new_test.drop('femaleres',axis=1, inplace=True)

X=new_train[['edu','med_expenses_hh_ep','cons_alcohol','ed_expenses_perkid','fs_adwholed_often','fs_chwholed_often','med_sickdays_hhave','cons_tobacco']]
Y=new_train['depressed']
#create model
decision=DecisionTreeClassifier(min_samples_split=10,max_depth=15,random_state=1024)
decision.fit(X,Y)
decision.predict_proba(new_test)                             

pickle.dump(decision,open('dcmodel.pkl','wb'))

model=pickle.load(open('dcmodel.pkl','rb'))


