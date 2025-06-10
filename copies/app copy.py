from flask import Flask, request, render_template, jsonify
import os
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

local_path = "./AppleOrange_dataset/"
model_path = "fashion_mnist_model.h5"

app = Flask(__name__)
model = load_model("fashion_mnist_model.h5")
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = load_model(model_path)


def predict_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize
    prediction = model.predict(img_array)
    label = "Orange" if prediction[0][0] > 0.5 else "Apple"

    return label

@app.route("/")
def index():
    return render_template("result.html")

@app.route("/process-image", methods=["POST"])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    filename = 'webcam.jpg'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    label = predict_image(file_path)
    return jsonify({'prediction': label})

if __name__ == "__main__":
    app.run(debug=True, port=8000)