import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
from land import Land

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Load and preprocess data

def predictor(data): # a list of Lands:
    ds = numpy.array(data)
    number_of_possible_outcomes = ... # whatever the number of possible outputs (building types) we have
    
    split_ratio = 0.8
    split_index = int(len(ds) * split_ratio)
    (x_train, y_train) = ds[split_index:]
    (x_test, y_test) = ds[:split_index]

    # Define the neural network model
    model = keras.Sequential([
        keras.layers.Input(shape=(4,)),  # Flatten 2D image into 1D array
        keras.layers.Dense(128, activation='relu'),  # Hidden layer with 128 neurons
        keras.layers.Dense(number_of_possible_outcomes, activation='softmax')  # Output layer with 10 neurons (for 10 classes)
    ])

    # Compile the model
    model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train, epochs=5)

    # Evaluate the model
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print("\nTest accuracy:", test_acc)


    # Load and preprocess your custom image
    def preprocess_image(image_path):
        img = Image.open(image_path).convert("L")  # Convert to grayscale
        img = img.resize((28, 28))  # Resize to 28x28 pixels
        img = np.array(img)  # Convert to numpy array
        img = 255 - img  # Invert the colors (since MNIST has white background, black text)
        img = img / 255.0  # Normalize pixel values to [0, 1]
        img = img.reshape(1, 28, 28)  # Reshape for model input (batch size of 1)

        # Debug: Visualize the preprocessed image
        plt.imshow(img[0], cmap='gray')
        plt.title("Preprocessed Custom Image")
        plt.show()

        return img


    for i in range(15):
        # index = random.randint(0, len(x_test) - 1)
        # image = x_test
        
        image = preprocess_image(f"matejs_testing_shit/{i}.png")
        index = 0

        # Predict the digit
        prediction = model.predict(image)
        predicted_digit = np.argmax(prediction[index])

        # Get the confidence value (probability of the predicted class)
        confidence = prediction[index][predicted_digit]

        # Display the image and predicted number
        plt.imshow(image[index], cmap='gray')
        plt.title(f"Predicted: {predicted_digit}\nConfidence: {confidence:.4f}")
        plt.show()

