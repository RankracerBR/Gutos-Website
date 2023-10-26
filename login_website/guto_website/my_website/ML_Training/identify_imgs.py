from sklearn.model_selection import train_test_split
from tensorflow.keras import layers
from tensorflow import keras
import tensorflow as tf
import numpy as np
import cv2
import os

data = []
labels = []

folder_path = 'login_website/guto_website/my_website/media/media'

for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        image = cv2.imread(os.path.join(folder_path, filename))
        image = cv2.resize(image, (128,128))
        data.append(image)
        labels.append(0)

data = np.array(data)
labels = np.array(labels)

train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.2, random_state=42)
train_data, val_data, train_labels, val_labels = train_test_split(train_data, train_labels, test_size=0.2, random_state=42)

model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_data, train_labels, epochs=10, validation_data=(val_data, val_labels))

test_loss, test_acc = model.evaluate(test_data, test_labels)
print(f"Acurácia no conjunto de teste: {test_acc}")