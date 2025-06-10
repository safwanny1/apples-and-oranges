# Import necessary libraries
from flask import Flask, request, render_template, jsonify
import os
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# Paths for local dataset and trained model
local_path = "./AppleOrange_dataset/"
model_path = "fashion_mnist_model.h5"

# Initialize the Flask application
app = Flask(__name__)

# Load the pre-trained Keras model
model = load_model(model_path)

# Configure the folder to store uploaded images
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to preprocess the image and make a prediction
def predict_image(img_path):
    # Load image and resize to expected input size
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)             # Convert image to array
    img_array = np.expand_dims(img_array, axis=0)   # Add batch dimension
    img_array = img_array / 255.0                   # Normalize pixel values

    # Make prediction using the model
    prediction = model.predict(img_array)

    # Return the label based on prediction score
    label = "Orange" if prediction[0][0] > 0.5 else "Apple"
    return label

# Route for the main page (just renders result.html)
@app.route("/")
def index():
    return render_template("result.html")

# Route to handle image upload from webcam (or frontend)
@app.route("/process-image", methods=["POST"])
def process_image():
    # Check if an image file is part of the POST request
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    # Get the image file and save it to the upload folder
    file = request.files['image']
    filename = 'webcam.jpg'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Predict the class of the image and return the result as JSON
    label = predict_image(file_path)
    return jsonify({'prediction': label})

# Run the app on port 8000 in debug mode
if __name__ == "__main__":
    app.run(debug=True, port=8000)