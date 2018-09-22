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


filename = "GBPUSD_1_20171221_Y"
inpath = "output/"
outpath = "output/"
ftype = ".csv"




# load and prepare the dataset
#dataset = np.loadtxt(filename+".csv", delimiter=",", skiprows = 1, usecols = (8,9,10,11,12,14))

dataset = np.loadtxt(filename+".csv", delimiter=",", skiprows = 1, usecols = (0,1,2,3,4,6))
X = dataset[:,0:5] #Cols included: Vol-Indicator 4
Y = dataset[:,5] #Y-variable

# 1. define the network
model = Sequential() #Sequence class of layered model
model.add(Dense(5, input_dim=5, activation='sigmoid')) #dense layer 2 with 12 neurons, and 5 input (layer 1) neurons that should match X
model.add(Dense(1, activation='sigmoid')) #add (final) layer with 1 output - should match Y

# 2. compile the network
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 3. fit the network
history = model.fit(X, Y, epochs=100, batch_size=100)

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
np.savetxt("TANN_Weights_Layer_1" + ".csv", lw1[0], delimiter=",")
np.savetxt("TANN_Weights_Layer_2" + ".csv", lw2[0], delimiter=",")
np.savetxt("TANN_Bias_Layer_1" + ".csv", lw1[1], delimiter=",")
np.savetxt("TANN_Bias_Layer_2" + ".csv", lw2[1], delimiter=",")

print("Biases: " + str(lw1[1]) + " and " + str(lw2[1]))
