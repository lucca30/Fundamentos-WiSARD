import random

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

    def fit_class(self, name_class,retinas):
        tuple_ = [[0 for x in range(self.tuple_size)] for y in range(self.M)]
        if(name_class not in self.discriminators):
            self.discriminators[name_class] = {}
            for i in range(0, len(tuple_)):
                self.discriminators[name_class][i] = {}

        for retina in retinas:
            for i in range(0, len(tuple_)):
                for j in range(0, len(tuple_[i])):
                    pixel = self.mapping[i][j]
                    tuple_[i][j] = retina[pixel[0]][pixel[1]]

                pos_ram = convert_toBinary(tuple_[i])

                if(pos_ram not in self.discriminators[name_class][i]):
                    self.discriminators[name_class][i][pos_ram] = 0

                self.discriminators[name_class][i][pos_ram] += 1
                self.max_bleaching = max(self.max_bleaching, self.discriminators[name_class][i][pos_ram])

    # necessário pelo menos duas classes para que possa classificar
    def classify(self, retina):
        tuple_ = [[0 for x in range(self.tuple_size)] for y in range(self.M)]

        for bleaching in range(1, self.max_bleaching+1):
            results = []
            for classes in self.discriminators:
                R = 0
                for i in range(0, len(tuple_)):
                    for j in range(0, len(tuple_[i])):
                        pixel = self.mapping[i][j]
                        tuple_[i][j] = retina[pixel[0]][pixel[1]]

                    pos_ram = convert_toBinary(tuple_[i])

                    if( (pos_ram in self.discriminators[classes][i]) and (self.discriminators[classes][i][pos_ram] >= bleaching) ):
                        R+=1
                results.append((R, classes))
            results.sort()
            if( (results[-1][0] > results[-2][0]) or (bleaching == self.max_bleaching) ):
                confidence = (results[-1][0] - results[-2][0])/results[-1][0]
                return (results[-1][1], confidence)
