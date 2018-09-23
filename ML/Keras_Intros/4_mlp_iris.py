# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 16:37:38 2017

@author: Ruthberg
"""

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

seed = 7
numpy.random.seed(seed)

#load data
dataframe = pandas.read_csv("iris.csv", header = None)
dataset = dataframe.values
X=dataset[:, 0:4].astype(float)
Y=dataset[:,4]

#encode class vals as ints
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y=encoder.transform(Y)
#convert to dummies / one-hot encoded
dummy_y=np_utils.to_categorical(encoded_Y)

#define model:
def baseline_model():
    #create model
    model = Sequential()
    model.add(Dense(8, input_dim=4, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    #compile
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

#estimate
#estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
#kfold = KFold(n_splits=10,shuffle=True,random_state=seed)

#results=cross_val_score(estimator, X, dummy_y, cv=kfold)

#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
    

#without KerasClassifier:
#create model
model = Sequential()
model.add(Dense(8, input_dim=4, activation='relu'))
model.add(Dense(3, activation='softmax'))
#compile
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(X, dummy_y, epochs=200, batch_size=5)


# 4. evaluate the network
loss, accuracy = model.evaluate(X, dummy_y)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))

# 5. make predictions
probabilities = model.predict(X)
#predictions = [float(numpy.round_(x)) for x in probabilities]
#accuracy = numpy.mean(predictions == dummy_y)
#print("Prediction Accuracy: %.2f%%" % (accuracy*100))
lw1 = model.layers[0].get_weights()
lw2 = model.layers[1].get_weights()

arr = lw1

numpy.savetxt("Output_weights" + str(0) + ".csv", arr[0], delimiter=",")
#arr.tofile('Output_weights.csv',sep=',',format='%10.5f')
#df = pandas.DataFrame(arr)
#df.to_csv("Output_weights.csv")

#csv_rows = ["{},{}".format(i, j) for i, j in arr]
#csv_text = "\n".join(csv_rows)

# write it to a file
##   f.write(csv_text)