#recebe o arquivo images.txt e o labels.txt
#dado o tamanho do conjunto de dados, ele quebrará em 10 pedaços iguais, podendo ter que descartar alguns casos
#9 grupos vão para um arquivo de teste, 1 vai para o de treino
#serão criados os seguintes arquivos:
# images_train_x.txt , labels_train_x.txt , images_test_x.txt , labels_test_x.txt
# onde x varia de 0 a 9, e representa qual dos conjuntos virou o grupo de teste
mapeamento = {
 "HA":"0",
 "SU":"1",
 "FE":"2",
 "NE":"3",
 "AN":"4",
 "DI":"5",
 "SA":"6"
}
import random
n_parts = 10
def chunkify(lst,n):
    return [lst[i::n] for i in range(n)]

path_images = "../data/Jaffetxt_limiar_simples/images.txt"
path_labels = "../data/Jaffetxt_limiar_simples/labels.txt"
path_output = "../data/Jaffetxt_limiar_simples/val_cruz/"

file_images = open(path_images, 'r')
list_images = file_images.readlines()
file_images.close()

file_labels = open(path_labels, 'r')
list_labels = file_labels.readlines()
file_labels.close()

list_both = []
for i in range(len(list_images)):
    list_both.append((list_images[i], list_labels[i]))

size = len(list_images)
to_remove = (size%n_parts)
list_both = list_both[:-to_remove]

random.shuffle(list_both)
parts = chunkify(list_both, n_parts)


for i in range(n_parts):
    path_test_images = "images_test_" + str(i)+ ".txt"
    path_test_labels = "labels_test_" + str(i)+ ".txt"
    path_train_images = "images_train_" + str(i)+ ".txt"
    path_train_labels = "labels_train_" + str(i)+ ".txt"

    test_images = [x[0] for x in parts[i]]
    test_labels = [mapeamento[x[1][:2]]+'\n' for x in parts[i]]

    train_images = []
    train_labels = []
    for j in range(n_parts):
        if(j==i):
            continue
        train_images += [x[0] for x in parts[j]]
        train_labels += [mapeamento[x[1][:2]]+'\n' for x in parts[j]]

    f = open(path_output+path_test_images, 'w')
    f.writelines(test_images)
    f.close()

    f = open(path_output+path_test_labels, 'w')
    f.writelines(test_labels)
    f.close()

    f = open(path_output+path_train_images, 'w')
    f.writelines(train_images)
    f.close()

    f = open(path_output+path_train_labels, 'w')
    f.writelines(train_labels)
    f.close()
