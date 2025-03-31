import numpy as np

class NeuralNetwork(object):
    def __init__(self):
        self.inputLayerSize = 1
        self.hiddenLayerSize = 3
        self.outputLayerSize = 1

        np.random.seed(5)

        self.W1 = np.random.randn(self.inputLayerSize, self.hiddenLayerSize)
        self.bias1 = np.random.randn(1, self.hiddenLayerSize)

        self.W2 = np.random.randn(self.hiddenLayerSize, self.outputLayerSize)
        self.bias2 = np.random.randn(1, self.outputLayerSize)

    def trainNetwork(self, input, output, num_iterations, learning_rate=0.01):
        for iteration in range(num_iterations):
            iterInput = input  # Use the entire dataset
            expectedOutput = output
            
            actualOutput = self.forward(iterInput)
            
            # Compute error
            error = actualOutput - expectedOutput
            MSE = np.mean(0.5 * error**2)

            # Backpropagation

            # For linear Data
            delta3 = error

            # For non-linear Data
            # delta3 = error * (self.a3 * (1 - self.a3)) 


            delta2 = np.dot(delta3, self.W2.T) * (self.a2 * (1 - self.a2))

            # Update weights and biases
            self.W2 -= learning_rate * np.dot(self.a2.T, delta3)
            self.bias2 -= learning_rate * np.sum(delta3, axis=0, keepdims=True)
            self.W1 -= learning_rate * np.dot(iterInput.T, delta2)
            self.bias1 -= learning_rate * np.sum(delta2, axis=0, keepdims=True)

            if iteration % 25000 == 0:
                print(f"Iteration {iteration}, MSE: {MSE}")

    def saveModel(self, name):
        np.savez(f"models/{name}.npz", W1=self.W1, bias1=self.bias1, W2=self.W2, bias2=self.bias2)
        print("Model saved successfully!")

    def loadModel(self, filename="trained_model.npz"):
        data = np.load(f"models/{filename}.npz")
        self.W1 = data["W1"]
        self.bias1 = data["bias1"]
        self.W2 = data["W2"]
        self.bias2 = data["bias2"]
        print(f"{filename} model loaded successfully!")

    def forward(self, input):
        # Forward pass
        self.z2 = np.dot(input, self.W1) + self.bias1
        self.a2 = self.sigmoid(self.z2)
        self.z3 = np.dot(self.a2, self.W2) + self.bias2

        # For linear Data
        self.a3 = self.z3
        # For non-linear Data
        # self.a3 = self.sigmoid(self.z3)

        return self.a3
            
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def sigmoidDerivative(self, a):
        return a * (1 - a)
