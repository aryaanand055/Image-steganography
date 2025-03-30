import numpy as np

class DeepNeuralNetwork():
    def __init__(self):
        number_of_neurons = 8
        np.random.seed(2)  # Ensure reproducibility

        # Initialize weights and biases
        self.synaptic_weights1 = 2 * np.random.random((1, number_of_neurons)) - 1
        self.bias1 = np.random.random((1, number_of_neurons))

        self.synaptic_weights2 = 2 * np.random.random((number_of_neurons, number_of_neurons)) - 1
        self.bias2 = np.random.random((1, number_of_neurons))

        self.synaptic_weights3 = 2 * np.random.random((number_of_neurons, 1)) - 1
        self.bias3 = np.random.random((1, 1))

    def __relu(self, x):
        return np.maximum(0, x)

    def __relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def train(self, training_inputs, training_outputs, num_iterations, learning_rate=0.01):
        for iteration in range(num_iterations):
            # Forward propagation
            hidden_layer1 = self.__relu(np.dot(training_inputs, self.synaptic_weights1) + self.bias1)
            hidden_layer2 = self.__relu(np.dot(hidden_layer1, self.synaptic_weights2) + self.bias2)
            output_layer = np.dot(hidden_layer2, self.synaptic_weights3) + self.bias3  # No activation in output

            # Compute error
            output_error = training_outputs - output_layer
            output_delta = output_error  # No activation, so no derivative needed

            # Backpropagation
            hidden_layer2_error = output_delta.dot(self.synaptic_weights3.T)
            hidden_layer2_delta = hidden_layer2_error * self.__relu_derivative(hidden_layer2)

            hidden_layer1_error = hidden_layer2_delta.dot(self.synaptic_weights2.T)
            hidden_layer1_delta = hidden_layer1_error * self.__relu_derivative(hidden_layer1)

            # Update weights and biases
            self.synaptic_weights3 += learning_rate * hidden_layer2.T.dot(output_delta)
            self.bias3 += learning_rate * np.sum(output_delta, axis=0, keepdims=True)

            self.synaptic_weights2 += learning_rate * hidden_layer1.T.dot(hidden_layer2_delta)
            self.bias2 += learning_rate * np.sum(hidden_layer2_delta, axis=0, keepdims=True)

            self.synaptic_weights1 += learning_rate * training_inputs.T.dot(hidden_layer1_delta)
            self.bias1 += learning_rate * np.sum(hidden_layer1_delta, axis=0, keepdims=True)

    def think(self, inputs):
        hidden_layer1 = self.__relu(np.dot(inputs, self.synaptic_weights1) + self.bias1)
        hidden_layer2 = self.__relu(np.dot(hidden_layer1, self.synaptic_weights2) + self.bias2)
        output_layer = np.dot(hidden_layer2, self.synaptic_weights3) + self.bias3
        return output_layer

if __name__ == "__main__":
    # Initialize neural network
    dnn = DeepNeuralNetwork()

    # Normalized training data
    training_inputs = np.array([[-10], [-9], [-8], [-7], [-6], [-5], [-4], [-3], [-2], [-1], [0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]) / 10
    training_outputs = (np.array([[100], [81], [64], [49], [36], [25], [16], [9], [4], [1], [0], [1], [4], [9], [16], [25], [36], [49], [64], [81], [100]]) / 100)   # Scale to [-1, 1]
    # Train the network
    dnn.train(training_inputs, training_outputs, 1000)

    # Testing x^2
    test_input = np.array([[2.5]]) / 10  # Correct shape (1,1)
    predicted_output = dnn.think(test_input) * 100  # Denormalize output
    print("2.5 squared:", predicted_output[0][0])  # Extract value
