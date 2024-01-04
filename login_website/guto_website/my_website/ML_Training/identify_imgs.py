from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Flatten, Conv2D, Dense, MaxPooling2D
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
import numpy as np
import glob as gb
import random
import cv2
import os


##Ajustar treinamento para melhorar a qualidade das imagens

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
TRAIN_DIR = "ML_Training/Violence_Datasets/train"
TEST_DIR = "ML_Training/Violence_Datasets/test"
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
    img = view_random_image(target_dir='ML_Training/Violence_Datasets/train/', target_class=class_name)


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


model_path = 'ML_Training/model1.h5'

if os.path.exists(model_path):
    loaded_model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully")
    loaded_model.evaluate(test_set)
else:    
    '''Treinamento'''
    #Treinamento
    history = classifier.fit(training_set,
                            epochs = 10,
                            validation_data = test_set)

    classifier.save('model1.h5')

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
    loaded_model = tf.keras.models.load_model(model_path)



# Diretório onde estão as imagens
directory = 'ML_Training/media/media/'

# Lista para armazenar os caminhos das imagens
image_paths = []

# Percorre o diretório em busca de arquivos de imagem
for filename in os.listdir(directory):
    if filename.endswith('.webp') or filename.endswith('.png') or filename.endswith('.jpg'):
        image_paths.append(os.path.join(directory, filename))

# Loop sobre cada imagem encontrada
for image_path in image_paths:
    image = cv2.imread(image_path)

    if image is not None:
        # Converta a imagem do OpenCV para uma imagem PIL
        image_pil = Image.fromarray(image, 'RGB')

        # Redimensione a imagem
        resized_image = image_pil.resize((128, 128))

        # Expanda as dimensões e normalize os dados de entrada
        expanded_input = np.expand_dims(resized_image, axis=0)
        input_data = expanded_input / 255.0  # Normalize os valores de pixel entre 0 e 1

        # Carregue o modelo treinado
        model_path = 'ML_Training/model1.h5'
        loaded_model = tf.keras.models.load_model(model_path)

        # Faça previsões
        predictions = loaded_model.predict(input_data)
        result = np.argmax(predictions)

        print(f"A classe prevista para {image_path} é: {result}")
    else:
        print(f"Não foi possível ler a imagem {image_path} ou a imagem não existe.")