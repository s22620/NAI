"""
ROZPOZNAWANIE UBRAŃ ZA POMOCĄ SIECI NEURONOWYCH

Autorzy: Jakub Marcinkowski s21021, Dagmara Gibas s22620

Opis problemu:
1. Budowa i porównanie dwóch modeli sieci neuronowych do klasyfikacji ubrań z wykorzystaniem zbioru Fashion MNIST.
2. Analiza skuteczności modeli poprzez porównanie dokładności testowej.

Instrukcja użycia:
1. Upewnij się, że masz zainstalowany Python 3+ oraz pip.
2. Zainstaluj wymagane biblioteki:
   pip install tensorflow
   pip install silence-tensorflow
3. Uruchom skrypt:
   python <Zadanie_3>.py

Framework: TensorFlow
Zbiór danych: Fashion MNIST
"""

from silence_tensorflow import silence_tensorflow

import tensorflow as tf

silence_tensorflow()

fashion_mnist = tf.keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images / 255.0

test_images = test_images / 255.0

def recognize_clothes(model):


    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(train_images, train_labels, epochs=10)

    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

    return test_acc

if __name__ == '__main__':
   

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    test_acc1 = recognize_clothes(model)

    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10)
    ])
    test_acc2 = recognize_clothes(model)
    print('\nTest accuracy for small neuron network:', test_acc1)
    print('\nTest accuracy for bigger neuron network:', test_acc2)