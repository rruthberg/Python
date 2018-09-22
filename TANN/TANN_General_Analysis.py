# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:27:10 2017

@author: Ruthberg

ANALYSIS OF DATA USED TO ANALYZE A TANN MODEL (Technical Analysis Neural Network Model)

MULTILAYER PERCEPTRON MODEL

1. Define
2. Compile
3. Fit
4. Evaluate
5. Predict

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
import os

#Inputs
#TODO: order of indicators is reversed when saved using pandas shit.. use: pdFrame.iloc[:, ::-1]

#File management:
filename = "BTCUSD_1_20180101_Y"
inpath = "output/"
outpath = "output/"
ftype = ".csv"

#Model settings:
calEpochs = 100
batchSize = 100


# load and prepare the dataset
#requires knowledge about the input dataset and the columns to use. 
#conventions will be to have Y first in the input, and the other after col startCol
startCol = 2
dataset = np.loadtxt(inpath + filename + ftype, delimiter=",", skiprows = 1, usecols = None)
numcols = int(dataset.size/len(dataset))
X = dataset[:,startCol:numcols] #Cols included: Vol-Indicator 4
numPredictors = int(X.size/len(X))
print("Fitting Network using " + str(numPredictors) + " input predictors:" )
Y = dataset[:,0] #Y-variable

# 1. define the network
model = Sequential() #Sequence class of layered model
model.add(Dense(numPredictors, input_dim=numPredictors, activation='sigmoid')) #dense layer 2 with X neurons (first number), and X input (layer 1) neurons that should match X
model.add(Dense(1, activation='sigmoid')) #add (final) layer with 1 output - should match Y

# 2. compile the network
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 3. fit the network
history = model.fit(X, Y, epochs=calEpochs)

# 4. evaluate the network
loss, accuracy = model.evaluate(X, Y)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))

# 5. make predictions
probabilities = model.predict(X)
predictions = [float(np.round_(x)) for x in probabilities]
accuracy = np.mean(predictions == Y)
print("Prediction Accuracy: %.2f%%" % (accuracy*100))

#Layer weights
lw1 = model.layers[0].get_weights()
lw2 = model.layers[1].get_weights()
#TODO: order of indicators is reversed when saved using pandas shit..
np.savetxt(outpath + "TANN_Weights_Layer_1" + ftype, lw1[0], delimiter=",")
np.savetxt(outpath + "TANN_Weights_Layer_2" + ftype, lw2[0], delimiter=",")
np.savetxt(outpath + "TANN_Bias_Layer_1" + ftype, lw1[1], delimiter=",")
np.savetxt(outpath + "TANN_Bias_Layer_2" + ftype, lw2[1], delimiter=",")

def sigmoid_array(x):
    return 1/(1+np.exp(-x))

tArr = np.asarray([1,1,1,1,1,1])
tX = np.asarray([tArr])
print("Test model output prediction is: " + str(model.predict(tX)))

sig_sum = 0
for i in range(0,6):
    outLay1 = sigmoid_array(sum(lw1[0][i]) + lw1[1][i])
    sig_sum = sig_sum + outLay1*lw2[0][i]

compSig = sigmoid_array(sig_sum+lw2[1][0])
print("Computed output prediction is: " + str(compSig)
    


    

print("Biases: " + str(lw1[1]) + " and " + str(lw2[1]))
