import random
import bisect

def convert_toBinary(x):
    temp = 1
    sum_ = 0
    for i in x:
        sum_ += i*temp
        temp *= 2
    return sum_

class WiSARD:
    # Mapping associa uma posição da matriz de tuplas com o pixel que ele representa

    def __init__(self, retina_x, retina_y, tuple_size):
        self.retina_x = retina_x
        self.retina_y = retina_y
        self.tuple_size = tuple_size
        if( (retina_x*retina_y)%tuple_size !=0 ):
            print("Invalid tuple size")
        self.M = (retina_x*retina_y)//tuple_size
        self.tuples = []
        self.mapping = []
        self.discriminators = {}
        self.max_bleaching = 0

    def random_mapping(self):
        self.mapping = []
        temp = []
        for i in range(0, self.retina_x):
            for j in range(0, self.retina_y):
                temp.append((i, j))

        for i in range(0, self.M):
            temp_array = []
            for j in range(0, self.tuple_size):
                element = random.choice(temp)
                temp.remove(element)
                temp_array.append(element)
            self.mapping.append(temp_array)

    def set_mapping(self, mapping):
        self.mapping = mapping

    def get_mapping(self):
        return self.mapping

    def set_discriminators(self, ds):
        self.discriminators = ds

    def get_discriminators(self):
        return self.discriminators

    def fit_class(self, labels,retinas):
        if(len(retinas) != len(labels) ):
            print("Size error")
            return 0
        for i in range(len(labels)):
            if(labels[i] not in self.discriminators):
                self.discriminators[labels[i]] = [{} for x in range(self.M)]

            for j in range(self.M):
                pos_ram = 0
                for k in range(self.tuple_size):
                    pixel = self.mapping[j][k]
                    pos_ram += retinas[i][pixel[0]][pixel[1]]* (2**k)

                if(pos_ram not in self.discriminators[labels[i]][j]):
                    self.discriminators[labels[i]][j][pos_ram] = 0

                self.discriminators[labels[i]][j][pos_ram] += 1
                self.max_bleaching = max(self.max_bleaching, self.discriminators[labels[i]][j][pos_ram])

    # necessário pelo menos duas classes para que possa classificar
    def classify(self, retinas):
        ret = []
        for retina in retinas:
            ram_count = {}
            for classes in self.discriminators:
                ram_count[classes] = []
                for i in range(self.M):
                    pos_ram=0
                    for j in range(self.tuple_size):
                        pixel = self.mapping[i][j]
                        pos_ram += retina[pixel[0]][pixel[1]] * (2**j)
                    if(pos_ram in self.discriminators[classes][i]):
                        ram_count[classes].append(self.discriminators[classes][i][pos_ram])
                ram_count[classes].sort()
            for bleaching in range(1, self.max_bleaching+1):
                results = []
                for classes in self.discriminators:
                    R = len(ram_count[classes]) -  bisect.bisect_right(ram_count[classes], bleaching)
                    results.append((R, classes))
                results.sort()
                if( (results[-1][0] > results[-2][0]) or (bleaching == self.max_bleaching) ):
                #    confidence = (results[-1][0] - results[-2][0])/results[-1][0]
                #    print(bleaching)
                    ret.append(results[-1][1])
                    break
        return ret
