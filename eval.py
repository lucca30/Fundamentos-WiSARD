import WiSARD as Wi
import keras
import utilities

from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()


print(utilities.eval(Wi.WiSARD(28, 28, 28),x_train, y_train, 1000, x_test[:1000], y_test[:1000], 40, 1 ))
