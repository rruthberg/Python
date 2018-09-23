# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 16:16:46 2017

@author: Ruthberg
"""

#Regression with keras

"""
Regression on house prices in Boston suburbs


"""

#Import packages

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor

import pandas
import numpy

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

#Import house price data

dataframe = pandas.read_csv("housing.csv", delim_whitespace=True, header = None)
dataset = dataframe.values

X = dataset[:,0:13]
Y = dataset[:,13]

#1. Define #2. Compile
#model speciied as a function for sk wrappers

def baseline_model():
    model = Sequential()
    model.add(Dense(13, input_dim = 13, kernel_initializer = 'normal', activation='relu'))
    model.add(Dense(1, kernel_initializer = 'normal'))
    model.compile(loss='mean_squared_error', optimizer = 'adam')
    return model
#3. Fit
seed = 7
numpy.random.seed(seed)

estimator = KerasRegressor(build_fn=baseline_model, nb_epoch = 100, batch_size=5, verbose=1)
kfold=KFold(n_splits=10, random_state=seed)
results= cross_val_score(estimator, X, Y, cv=kfold)

print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


numpy.random.seed(seed)
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasRegressor(build_fn=baseline_model, epochs=50, batch_size=5, verbose=0)))
pipeline = Pipeline(estimators)
kfold = KFold(n_splits=10, random_state=seed)
results = cross_val_score(pipeline, X, Y, cv=kfold)
print("Standardized: %.2f (%.2f) MSE" % (results.mean(), results.std()))



#4. Evaluate


#5. Predict