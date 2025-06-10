import kagglehub
import shutil
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential

# Download latest version
path = kagglehub.dataset_download("balraj98/apple2orange-dataset")

print("Path to dataset files:", path)

# Define local save path
local_path = "./AppleOrange_dataset/"
model_path = "fashion_mnist_model.h5"

# Ensure the local directory exists
os.makedirs(local_path, exist_ok=True)

# Define the path for the new training_set directory
training_set_path = os.path.join(local_path, "training_set")
testing_set_path = os.path.join(local_path, "testing_set")

# Ensure the training_set directory exists
os.makedirs(training_set_path, exist_ok=True)
os.makedirs(testing_set_path, exist_ok=True)


# Copy the dataset to the local directory
for item in os.listdir(path):
    print(item)
    s = os.path.join(path, item)
    d = None

    if item in ["trainA", "trainB"]:
        d = os.path.join(training_set_path, item)
    elif item in ["testA", "testB"]:
        d = os.path.join(testing_set_path, item)


    # Only attempt to copy if a valid destination was found
    if d is not None:
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

print(f"Dataset saved at: {local_path}")

print(f"Dataset saved at: {local_path}")

# Correcting paths
train_dir = "./AppleOrange_dataset/training_set/"
test_dir = "./AppleOrange_dataset/testing_set/"

# Define ImageDataGenerator for augmentation and rescaling
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

# Load training dataset
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
)

# Load testing dataset
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
)

model = Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # Binary classification (Cat vs Dog)
])

# Compile the model
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    epochs=5,
    validation_data=test_generator
)

model.save(model_path)

test_loss, test_acc = model.evaluate(test_generator)
print(f"Test Accuracy: {test_acc:.2f}")

