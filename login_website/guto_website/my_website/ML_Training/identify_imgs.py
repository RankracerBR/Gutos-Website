from keras.preprocessing.image import ImageDataGenerator
from tensorflow import keras
from keras.layers import MaxPooling2D
from keras.models import Sequential
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import Dense
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np
import glob as gb
import random
import cv2
import os

#Função de analisar a imagem
def view_random_image(target_dir, target_class):
    #Analisar as imagens aqui
    target_folder = target_dir + target_class
    
    #Pega uma imagem aleatória
    random_image = random.sample(os.listdir(target_folder),1)
    
    #Lê a imagem e plota
    img = mpimg.imread(target_folder+'/'+random_image[0])
    plt.imshow(img)
    plt.title(target_class)
    plt.axis('off')
    print(f'-Image Shape: {img.shape}')
    
    return img

#Referência as pastas
TRAIN_DIR = "Violence_Datasets/train"
TEST_DIR = "Violence_Datasets/train"
BATCH_SIZE = 64

#Conta a quantidade de imagens
for folder in os.listdir(TRAIN_DIR):
    files = gb.glob(pathname=str(TRAIN_DIR + "/"+ folder + "/*.jpg"))
    print(f"For training data, found {len(files)} in folder {folder}")

for folder in os.listdir(TEST_DIR):
    files = gb.glob(pathname=str(TRAIN_DIR + "/"+ folder + "/*.jpg"))
    print(f"For training data, found {len(files)} in folder {folder}")

#Classificação (obs: esses nomes no parâmetro da lista abaixo vãos referênciar os nomes das pastas em: "target_class=class_name" portanto cuidado ao renomear)
class_names = ['violence','non_violence']

plt.figure(figsize=(10, 10))
for i in range(18):
    plt.subplot(3, 6, i+1)
    class_name = random.choice(class_names)
    img = view_random_image(target_dir='Violence_Datasets/train/', target_class=class_name)
plt.show()

#Preparando para o Treinamento
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory(TRAIN_DIR,
                                                 target_size = (128, 128),
                                                 batch_size = BATCH_SIZE,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(TEST_DIR,
                                            target_size = (128,128),
                                            batch_size = BATCH_SIZE,
                                            class_mode = 'categorical')

#Modelo Base para classificação
classifier = Sequential()

#Convolução 1-
classifier.add(Conv2D(16, (3, 3), input_shape=(128 , 128, 3), activation='relu'))

#Agrupamento 2-
classifier.add(MaxPooling2D(pool_size = (2,2)))

#Adicionando uma segunda camada
classifier.add(Conv2D(32, (3,3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2,2)))

#Achatamento
classifier.add(Flatten())

#Conexão
classifier.add(Dense(units = 128, activation = 'relu'))

classifier.add(Dense(units = 2, activation = 'softmax'))

#Compila
classifier.compile(optimizer = 'adam', loss="categorical_crossentropy", metrics = ['accuracy'])

#Sumário do classificatório
classifier.summary()


'''Treinamento em manutenção'''
#Treinamento
history = classifier.fit(training_set,
                         epochs = 10,
                         validation_data = test_set)

classifier.save('model1.h5') #Cria um arquivo do tipo HDF5 para salvar o treinamento

classifier.evaluate(test_set) 

pd.DataFrame(history.history)[['loss','val_loss']].plot()
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')

pd.DataFrame(history.history)[['accuracy','val_accuracy']].plot()
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
model_path = 'model1.h5'
loaded_model = keras.models.load_model(model_path)

image = cv2.imread() #Colocar imagem para ler aqui

image_fromarray - Image.fromarray(image, 'RGB')
resize_image = image_fromarray.resize((128, 128))
expand_input = np.expand_dims(resize_image, axis=0)
input_data = np.array(expand_input)
input_data = input_data/255

pred = loaded_model.predict(input_data)
result = pred.argmax()
result

training_set.class_indices