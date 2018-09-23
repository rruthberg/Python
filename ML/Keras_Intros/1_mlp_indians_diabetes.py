"""
5 step model for modelling deep networks in keras

MULTILAYER PERCEPTRON MODEL

1. Define
2. Compile
3. Fit
4. Evaluate
5. Predict

"""

#Import statements
from keras.models import Sequential
from keras.layers import Dense
import numpy
import os

# load and prepare the dataset
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
X = dataset[:,0:8]
Y = dataset[:,8]

# 1. define the network
model = Sequential() #Sequence class of layered model
model.add(Dense(12, input_dim=8, activation='relu')) #dense layer 2 with 12 neurons, and 8 input neurons that should match X
model.add(Dense(1, activation='sigmoid')) #add (final) layer with 1 output - should match Y

# 2. compile the network
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 3. fit the network
history = model.fit(X, Y, epochs=100, batch_size=10)

# 4. evaluate the network
loss, accuracy = model.evaluate(X, Y)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))

# 5. make predictions
probabilities = model.predict(X)
predictions = [float(numpy.round_(x)) for x in probabilities]
accuracy = numpy.mean(predictions == Y)
print("Prediction Accuracy: %.2f%%" % (accuracy*100))

model_json = model.to_json()

with open("model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("model.h5")