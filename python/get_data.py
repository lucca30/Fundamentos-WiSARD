import keras
from keras.datasets import mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()


train_images = open('../data/mnist/train_images.txt', 'w')
train_labels = open('../data/mnist/train_labels.txt', 'w' )
test_images = open('../data/mnist/test_images.txt', 'w')
test_labels = open('../data/mnist/test_labels.txt', 'w')

str_ = []
for i in range(len(x_train)):
    str_.append("")
    for j in range(28):
        for k in range(28):
            str_[i] += str(x_train[i][j][k]) + " "
    str_[i] += ("\n")
train_images.writelines(str_)
train_images.close()
print("Train images done")

str_ = []
for i in range(len(x_test)):
    str_.append("")
    for j in range(28):
        for k in range(28):
            str_[i] += str(x_test[i][j][k]) + " "
    str_[i] += ("\n")
test_images.writelines(str_)
test_images.close()
print("Test images done")

str_ = []
for i in range(len(y_train)):
    str_.append(str(y_train[i]) + "\n")

train_labels.writelines(str_)
train_labels.close()
print("Train Labels done")

str_ = []
for i in range(len(y_test)):
    str_.append(str(y_test[i]) + "\n")
test_labels.writelines(str_)
test_labels.close()
print("Test labels done")
