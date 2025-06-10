# Core Libraries
import shutil
import os

# TensorFlow and Keras
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential

# KaggleHub for dataset download
import kagglehub

# Define datasert details
kaggle_dataset_id = "balraj98/apple2orange-dataset"
local_dataset_name = "./AppleOrange_dataset/" # Keeps consistent with block 2
model_path = "fashion_mnist_model.h5"

path = None

try:
  # Download latest version
  print(f"Attempting to download the latest dataset: {kaggle_dataset_id}")
  path = kagglehub.dataset_download(kaggle_dataset_id)
  print(f"Dataset successfully downloaded to: {path}")
except Exception as e:
  print(f"Error downloading dataset: {e}")
  # Handles the error as appropriate, e.g., exit the script
  exit()

# Use the local_path variable from block 1
local_path = f"./{local_dataset_name}/"

# Ensure the local directory exists
os.makedirs(local_path, exist_ok=True)

# Define the path for the new training_set and testing_set directories
training_set_dir_name = "training_set"
testing_set_dir_name = "testing_set"

training_set_path = os.path.join(local_path, "training_set")
testing_set_path = os.path.join(local_path, "testing_set")

# Ensure the training_set directory exists
os.makedirs(training_set_path, exist_ok=True)
os.makedirs(testing_set_path, exist_ok=True)

# Mapping the source directory names to destination directory names
dataset_structure_map = {
    "trainA" : training_set_path,
    "trainB" : training_set_path,
    "testA" : testing_set_path,
    "testB" : testing_set_path,
  }

# Copy the dataset to the local directory
print(f"Organizing dataset from {path} to {local_path}")
for item in os.listdir(path):
  s = os.path.join(path, item)
  d = dataset_structure_map.get(item) # Use .get() for safe access

  # Only attempt to copy if the item is in our mapping
  if d is not None:
    try:
      if os.path.isdir(s):
        # Create the subdirectory within the destination path
        dest_subdir = os.path.join(d, item)
        print(f"Copying directory {s} to {dest_subdir}")
        shutil.copytree(s, dest_subdir, dirs_exist_ok = True)
      else:
        # For files directly in the downloaded root we want to copy
        print(f"Copying file {s} to {d}")
        shutil.copy2(s, d)
    except Exception as e:
      print(f"Error copying {item}: {e}")

print(f"Dataset organization complete. Saved at: {local_path}")

# Define the base path using the variable from Block 1
base_path = f"./{local_dataset_name}/"

# Correcting paths using os.path.join
train_dir = os.path.join(base_path, training_set_dir_name)
test_dir = os.path.join(base_path, testing_set_dir_name)

# Define ImageDataGenerator for augmentation and rescaling
# Rescale the pixel values to be between 0 and 1
# Apply data augemtation to the training set to improve robustness
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20, # Rotate images by up to 20 degrees
    width_shift_range=0.2, # Shift image horizontally by up to 20% of the width
    height_shift_range=0.2, # Shift image vertically by up to 20% of the height
    shear_range=0.2, # Apply shearing transformation
    zoom_range=0.2, # Apply zoom transformation
    horizontal_flip=True, # Flip images horizontally
    fill_mode='nearest' # Fill newly created pixels after transformations
    # You can experiment with adding other augmentation within this section
    # e.g brigntess_range, channel_shift_range
)

# Only rescale the test set
test_datagen = ImageDataGenerator(rescale=1./255)

# Load training dataset
# Target size of 150x150 pixels
# Batch size of 32 used for training
# class_mode = 'binary' is use for binary classification
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode = 'binary'
    # You may adjust batch_size depending on memory
)

# Load testing dataset
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
)

# Define the Sequential model
model = tf.keras.models.Sequential([
    # First convolutional layer with 32 filters, 3x3 kernel, ReLU activation, and input shape
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150, 150, 3)),
    # First max pooling layer
    tf.keras.layers.MaxPooling2D(2,2),

    # Second convolutional layer with 64 filters, 3x3 kernel, ReLU activation
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    # Second max pooling layer
    tf.keras.layers.MaxPooling2D(2,2),

    # Third convolutional layer with 128 filters, 3x3 kernel, ReLU activation
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    # Third max pooling layer
    tf.keras.layers.MaxPooling2D(2,2),

    # Flatten the output from the convolutional layers
    tf.keras.layers.Flatten(),
    # First dense layer with 512 units and ReLU activation
    tf.keras.layers.Dense(512, activation='relu'),
    # Output dense layer with 1 unit and sigmoid activation for binary classification
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
# Use binary crossentropy as the loss function for binary classification
# Use the Adam optimizer (consider experimenting with other optimizers and learning rates)
# Evaluate the model based on accuracy
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train the model using the data generators
# Train for a specified number of epochs (consider increasing this for better results)
# Validate the model during training using the testing data
print ("Starting model training...")
history = model.fit(
    train_generator,
    epochs=5,
    validation_data=test_generator
)
print ("Model training has finished")

# saves model
model.save(model_path)

# Model evaulation
print ("Evaluating model on test set...")
test_loss, test_acc = model.evaluate(test_generator)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_acc:.2f}")

