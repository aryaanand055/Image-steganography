from nn import NeuralNetwork
import numpy as np
import os
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
import PIL.Image as Image

if __name__ == "__main__":
    modelName = input("Enter the model name to load: ")
    nn = NeuralNetwork(inputLayerSize=784, hiddenLayerSize=16, hiddenLayer2Size=16, outputLayerSize=10)
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    if os.path.exists(f"models/{modelName}.npz"):
        nn.loadModel(modelName)
        print(f"{modelName} model loaded successfully!\nThe model has MSE: {nn.MSE}")
    else:
        print("Model not found. Training the model...")
        X_train = X_train.reshape(X_train.shape[0], 784) / 255.0  # Normalize
        y_train = np.eye(10)[y_train]  # One-hot encoding

        nn.trainNetwork(X_train, y_train, num_iterations=1000, learning_rate=0.001)
        nn.saveModel(modelName)

    # **Load & Preprocess Image**

    continueTrying = True
    while(continueTrying):
        try:
            imageToPredict = input("Enter the image name to predict (e.g., image4.png): ")
            img = Image.open(imageToPredict).convert('L')  # Convert to grayscale
            img = img.resize((28, 28))  # Resize to 28x28
            img_array = np.array(img, dtype=np.float32) / 255.0  # Normalize pixel values

            print("Image shape before flattening:", img_array.shape)

            img_array = img_array.flatten().reshape(1, 784) 
            output = nn.forward(img_array)  
            predicted_class = np.argmax(output)
            confidence = np.max(output) * 100
            print(f"Predicted class: {predicted_class}, Confidence: {confidence:.2f}%")
            if(input("Do you want to predict another image? (y/n): ").lower() != "y"):
                continueTrying = False
            else:
                continueTrying = True
        except FileNotFoundError:
            print("File not found. Please try again.")
   