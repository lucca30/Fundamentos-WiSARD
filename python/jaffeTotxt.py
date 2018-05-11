images_path = "../data/JAFFE/"
from PIL import Image
import numpy as np
images = open('../data/Jaffetxt/images.txt', 'w')
labels = open('../data/Jaffetxt/labels.txt', 'w')
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(images_path) if isfile(join(images_path, f))]


str_ = []
strl_= []
for file in onlyfiles:
    im = Image.open(images_path + file)
    pixels = np.array(im)
    print(file)
    str_.append("")
    strl_.append(file[3:5]+"\n")
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            str_[-1] += str(pixels[i][j]) + " "
    str_[-1] += ("\n")

images.writelines(str_)
labels.writelines(strl_)
images.close()
labels.close()
