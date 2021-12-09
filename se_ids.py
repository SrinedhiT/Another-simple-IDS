# -*- coding: utf-8 -*-
"""SE-IDS.ipynb
Automatically generated by Colaboratory.
"""

import numpy as np
import pandas as pd
import sklearn.metrics
import sklearn.model_selection
import sklearn.linear_model
import sklearn.preprocessing
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('/content/UNSW_NB15_training-set.csv')
test = pd.read_csv('/content/UNSW_NB15_testing-set.csv')

#Information about Training data
data.head()
data.describe()

data.dropna(inplace = True)

data['service']
data.service.unique()

for col in data.columns:
  if data[col].dtypes == 'object':
    un = len(data[col].unique())
    print("Feature '{col}' has {un} categories".format(col=col, un=un))

data.attack_cat.unique()
data.drop(columns='attack_cat', inplace = True )
test.drop(columns = 'attack_cat', inplace = True)

data.label.value_counts()

#Splitting Datasets

x_train, y_train = data.drop(columns=['label']), data['label']
x_test, y_test = test.drop(columns=['label']), test['label']

categ = ['proto', 'service', 'state']
num = list(set(x_train.columns) - set(categ))

x_test.reset_index(drop=True, inplace=True)
x_train.head()

x_test.head()

#Normalizing Dataset using Min-Max Scaler
scaler = MinMaxScaler()
scaler = scaler.fit(x_train[num])
x_train[num] = scaler.transform(x_train[num])

scaler = scaler.fit(x_test[num])
x_test[num] = scaler.transform(x_test[num])

#Function for Encoding the categorical values using OneHotEncoding
serv = OneHotEncoder()
pro = OneHotEncoder()
sta = OneHotEncoder()

def encode(data):

    X = serv.fit_transform(data['service'].values.reshape(-1, 1))
    Xm = pro.fit_transform(data['proto'].values.reshape(-1, 1))
    Xmm = sta.fit_transform(data['state'].values.reshape(-1, 1))

    data = pd.concat([data,
                      pd.DataFrame(Xm.toarray(), columns=['proto_'+i for i in pro.categories_[0]]),
                      pd.DataFrame(X.toarray(), columns=['service_'+i for i in serv.categories_[0]]),
                      pd.DataFrame(Xmm.toarray(), columns=['state_'+i for i in sta.categories_[0]])],
                      axis=1)

    data.drop(['proto', 'service', 'state'], axis=1, inplace=True)

    return data

#before OneHotEncoding
x_train

x_test

#Applying OneHotEncoding
x_train = encode(x_train)
x_test = encode(x_test)

#After OneHotEncoding
x_train.shape, y_train.shape

x_test.shape, y_test.shape

x_test

x_train

#Aligning the sets
final_train, final_test = x_train.align(x_test, join='inner', axis=1)

final_test

final_train

#Using Naive Bayes Classifier

m1 = MultinomialNB()

m1.fit(final_train, y_train)
y_pred = m1.predict(final_test)

print("Accuracy Score for Naive Bayes Model is : ", accuracy_score(y_test, y_pred))

print("Classification Report for Naive Bayes Model: ")
print(classification_report(y_test, y_pred))