# apples-and-oranges

# # 🍎🍊 Apples vs. Oranges Image Classifier
A deep learning CNN that classifies apples and oranges using TensorFlow/Keras. Trained in Colab, deployable in VS Code.

## 🧠 Project Overview
This project is a deep learning image classification model built with TensorFlow/Keras that distinguishes between images of apples and oranges. It utilizes a convolutional neural network (CNN) architecture trained on a labeled dataset sourced via Kagglehub. The model is developed and trained in Google Colab and is exportable to VS Code for further testing or deployment.

## 📂 Dataset
- Source: [Kaggle – Apple2Orange](https://www.kaggle.com/datasets/balraj98/apple2orange-dataset)
- Organized into `train/` and `test/` folders

## ⚙️ Installation
1. Clone the repository
2. Upload `kaggle.json` to authenticate with Kaggle
3. Install dependencies:
   ```bash
   pip install kagglehub pandas numpy tensorflow

## 🧪 Inference
Use `predict.py` to run predictions on new images. Example:
```bash
python predict.py --image test_image.jpg

