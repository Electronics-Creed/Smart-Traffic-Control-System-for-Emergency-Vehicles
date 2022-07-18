# import packages
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizer_v2.adam import Adam
import matplotlib.pyplot as plt

# path to dataset
PATH = os.getcwd()

train_dir = os.path.join(PATH, '\\training_dataset\\train')
validation_dir = os.path.join(PATH, '\\training_dataset\\validate')

# create the sequential model
model = tf.keras.models.Sequential(
    [tf.keras.layers.Conv2D(8, (3, 3), activation='relu', input_shape=(128, 384, 1), padding='valid'),  # Check shape
     tf.keras.layers.Conv2D(16, (3, 3), activation='relu', padding='valid'),
     tf.keras.layers.MaxPooling2D(3, 3),
     tf.keras.layers.Conv2D(16, (3, 3), activation='relu', padding='valid'),
     tf.keras.layers.MaxPooling2D(3, 3),
     tf.keras.layers.Conv2D(8, (3, 3), activation='relu', padding='valid'),
     tf.keras.layers.MaxPooling2D(3, 3),
     tf.keras.layers.Flatten(),
     tf.keras.layers.Dense(8, activation=tf.nn.relu),
     tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)])

model.summary()  # print the model summary

# compile the model
model.compile(
    optimizer=Adam(learning_rate=0.5e-4 * 0.8, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, name="Adam"),
    loss='binary_crossentropy', metrics=['accuracy'])

# get the images
train_datagen = ImageDataGenerator()
test_datagen = ImageDataGenerator()
train_generator = train_datagen.flow_from_directory(train_dir, target_size=(128, 384), color_mode="grayscale",
                                                    batch_size=32,
                                                    class_mode="binary",
                                                    shuffle=True)
validation_generator = test_datagen.flow_from_directory(validation_dir, target_size=(128, 384), color_mode="grayscale",
                                                        batch_size=32,
                                                        class_mode="binary",
                                                        shuffle=True)

# train the neural network model
history = model.fit_generator(train_generator, validation_data=validation_generator, epochs=300, verbose=1)
print(history.history)

# save the model and weights
model.save_weights('model_weights.h5')
model.save('model.h5')

# plot the graphs of accuracy and loss
acc = history.history['accuracy']  # loss: 0.0717 - accuracy: 0.9826 - val_loss: 0.0966 - val_accuracy: 0.9667
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'r-', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.show()

plt.plot(epochs, loss, 'r-', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()
