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
def eval(wisard, x_train , y_train , x_test, y_test, iterations=1):
    import random
    best_case = 0.0
    for i in range(iterations):
        wisard.random_mapping()
        wisard.fit_class( y_train, x_train)
        total_cases = len(x_test)
        success = 0
        for j in range(total_cases):
            if(wisard.classify(x_test[j]) == y_test[j] ):
                success+=1
        result = success/total_cases
        if(result > best_case):
            best_case = result
            #best_config = (wisard.get_mapping(), wisard.get_discriminators())
#    return (best_case, best_config)
    print("best case: " + str(best_case))
    return best_case
