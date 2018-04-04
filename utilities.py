def filter_image(image, k):
    temp = []
    for i in range(0, len(image)):
        temp.append([])
        for j in range(0,len(image[i])):
            if(image[i][j]>=k):
                temp[i].append(1)
            else:
                temp[i].append(0)
    return temp

# n_trains is the number of images that will be used in train
# iterations is the number of times that will repeat a eval
def eval(wisard, train_set, n_trains , test_set, k, iterations=1):
    import random
    best_case = 0.0
    for i in range(iterations):
        random.shuffle(train_set)
        wisard.random_mapping()
        for j in range(n_trains):
             wisard.fit_class( train_set[j][0], [filter_image(train_set[j][1], k)] )
        total_cases = len(test_set)
        success = 0
        for test in test_set:
            if(wisard.classify(filter_image(test[1], k)) == test[0] ):
                success+=1
        result = success/total_cases
        if(result > best_case):
            best_case = result
            best_config = (wisard.get_mapping(), wisard.get_discriminators())
#    return (best_case, best_config)
    return best_case
