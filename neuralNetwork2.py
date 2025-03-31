from nn import NeuralNetwork
import numpy as np
import os

if __name__ == "__main__":

    nn = NeuralNetwork()

    modelName = input("Enter the model name to load: ")

    if (os.path.exists(f"models/{modelName}.npz")):
        nn.loadModel("celcius_to_fahrenheit")
    else:
        training_inputs = np.arange(-40, 110, 10).reshape(-1, 1) / 100
        training_outputs =((1.8 * training_inputs * 100) + 32) /212
        nn.trainNetwork(training_inputs, training_outputs, num_iterations=1000000, learning_rate=0.08)
        nn.saveModel("celcius_to_fahrenheit")
    
    userInput = int(input("Enter data to predict the output: "))

    inputToPredict = np.array([[userInput]])/100

    print("\nPredicted output: ")
    output =(nn.forward(inputToPredict)*212)[0][0]
    print(round(output,1), "Degree Fahrenheit")