import numpy as np

class NeuralNetwork(object):

    def __init__(self, modelName=None,inputLayerSize=1, hiddenLayerSize=3, hiddenLayer2Size = 3,outputLayerSize=1):
        if(modelName is not None):
            self.loadModel(modelName)
            return
        self.inputLayerSize = inputLayerSize
        self.hiddenLayerSize = hiddenLayerSize
        self.hiddenLayer2Size = hiddenLayer2Size
        self.outputLayerSize = outputLayerSize

        np.random.seed(5)

        self.W1 = np.random.randn(self.inputLayerSize, self.hiddenLayerSize) * np.sqrt(1.0 / self.inputLayerSize)
        self.W2 = np.random.randn(self.hiddenLayerSize, self.hiddenLayer2Size) * np.sqrt(1.0 / self.hiddenLayerSize)
        self.W3 = np.random.randn(self.hiddenLayer2Size, self.outputLayerSize) * np.sqrt(1.0 / self.hiddenLayer2Size)


        self.bias1 = np.zeros((1, self.hiddenLayerSize))
        self.bias2 = np.zeros((1, self.hiddenLayer2Size))
        self.bias3 = np.zeros((1, self.outputLayerSize))

        self.MSE = 1

   
    def trainNetwork(self, input, output, num_iterations, learning_rate=0.01, batch_size=128):
        num_samples = input.shape[0]

        for iteration in range(num_iterations):
           
           # Shuffle the dataset at the start of each epoch
           indices = np.arange(num_samples)
           np.random.shuffle(indices)
           input = input[indices]
           output = output[indices]

           for i in range(0, num_samples, batch_size):
                
            batch_input = input[i:i+batch_size]
            batch_output = output[i:i+batch_size]

            actualOutput = self.forward(batch_input)

              # Compute error
            error = actualOutput - batch_output
            MSE = np.mean(0.5 * error**2)

                # Backpropagation
            delta4 = error * self.relu_derivative(self.a4)
            delta3 = np.dot(delta4, self.W3.T) * self.relu_derivative(self.a3)
            delta2 = np.dot(delta3, self.W2.T) * self.relu_derivative(self.a2)

               # Update weights and biases
            self.W3 -= learning_rate * np.dot(self.a3.T, delta4)
            self.bias3 -= learning_rate * np.sum(delta4, axis=0, keepdims=True)
            self.W2 -= learning_rate * np.dot(self.a2.T, delta3)
            self.bias2 -= learning_rate * np.sum(delta3, axis=0, keepdims=True)
            self.W1 -= learning_rate * np.dot(batch_input.T, delta2)
            self.bias1 -= learning_rate * np.sum(delta2, axis=0, keepdims=True)

            self.MSE = MSE
            # if iteration % 10 == 0:

           print(f"Iteration {iteration}, MSE: {MSE}")

    def saveModel(self, name):
        np.savez(f"models/{name}.npz", W1=self.W1, bias1=self.bias1, W2=self.W2, bias2=self.bias2, W3=self.W3, bias3=self.bias3, MSE=self.MSE)
        print("Model saved successfully!")

    def loadModel(self, modelName="trained_model.npz"):
        data = np.load(f"models/{modelName}.npz")
        self.W1 = data["W1"]
        self.bias1 = data["bias1"]
        self.W2 = data["W2"]
        self.bias2 = data["bias2"]
        self.W3 = data["W3"]
        self.bias3 = data["bias3"]
        self.MSE = data["MSE"]
       

    def forward(self, input):
        # Forward pass
        self.z2 = np.dot(input, self.W1) + self.bias1
        self.a2 = self.relu(self.z2)
        self.z3 = np.dot(self.a2, self.W2) + self.bias2
        self.a3 = self.relu(self.z3)
        self.z4 = np.dot(self.a3, self.W3) + self.bias3
        self.a4 = self.softmax(self.z4)

        return self.a4
            
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500))) 

    
    def sigmoidDerivative(self, a):
     
        return a * (1 - a)
    
    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, a):
        return np.where(a > 0, 1, 0)

    def softmax(self, z):
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)