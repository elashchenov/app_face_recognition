import ast
import base64
import os
import shutil
import sys
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import requests
import configs.config as config

id_user = -1
epochs = 100


class CustomCallback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 5 == 0:
            _ = requests.post(config.api_set_percent + str(100 * (epoch + 1) / epochs) + "/" + str(id_user))


def train(user_id):
    global id_user
    id_user = user_id
    main_dir = "/Users/lashchenov/university/ТРКПО Маслаков/app_access_with_Face_Recognition/neural_network"
    train_data_dir = os.path.join(main_dir, "images", f'{user_id}',  "train")
    validation_data_dir = os.path.join(main_dir, "images", f'{user_id}', "test")
    nb_train_samples = 160
    nb_validation_samples = 40
    img_width, img_height = 128, 128

    batch_size = 160
    num_classes = 1  # username and not_username

    if K.image_data_format() == "channels_first":
        input_shape = (1, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 1)

    model = Sequential()

    model.add(Conv2D(32, (3, 3), activation='relu', padding='same',
                     input_shape=input_shape))
    model.add(BatchNormalization(axis=-1))
    model.add(MaxPooling2D(pool_size=(4, 4)))
    model.add(Dropout(0.5))

    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization(axis=-1))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization(axis=-1))
    model.add(MaxPooling2D(pool_size=(4, 4)))
    model.add(Dropout(0.5))

    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization(axis=-1))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization(axis=-1))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='sigmoid'))

    history = model.compile(loss="mse",
                            optimizer="adam",
                            metrics=["acc"])

    model.summary()

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False)

    # this is the augmentation configuration we will use for testing:
    # Rescale
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size, color_mode='grayscale',
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size, color_mode='grayscale',
        class_mode='categorical')

    history = model.fit_generator(
        train_generator,
        steps_per_epoch=nb_train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=nb_train_samples // batch_size,
        callbacks=[CustomCallback()])

    model.save(os.path.join(main_dir, "models", user_id, "model_face.h5"))
