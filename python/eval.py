import WiSARD as Wi
import keras
import utilities
from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
n_trains = 5000 #of each label
n_tests = 10000
k=125
x_train_filtered = []
y_train_filtered = []
count = [0 for x in range(10)]
cnt = 0
for i in range(len(y_train)):
    if(count[y_train[i]]<n_trains):
        cnt+=1
        count[y_train[i]]+=1
        x_train_filtered.append(utilities.filter_image(x_train[i], k  ) )
        y_train_filtered.append(y_train[i])
    if(cnt==(n_trains*10)):
        break
for i in range(n_tests):
    x_test[i] = utilities.filter_image(x_test[i], k)


print(utilities.eval(Wi.WiSARD(28, 28, 28),x_train_filtered ,y_train_filtered, x_test[:n_tests],y_test[:n_tests], 1 ) )
