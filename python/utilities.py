import time
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
        print("Starting Training...")
        start_time = time.time()
        wisard.fit_class( y_train, x_train)
        print("Duration : " + str(time.time()-start_time) )
        print("Average of each image trained: ", str((time.time()-start_time) / len(x_train)))
        total_cases = len(x_test)
        success = 0
        print("Starting Clasify...")
        start_time = time.time()
        answers = wisard.classify(x_test)
        for i in range(len(y_test)):
            if(y_test[i]==answers[i]):
                success+=1
        print("Duration : " + str(time.time()-start_time) )
        print("Average of each image classified: ", str((time.time()-start_time) / len(x_test)))

        result = success/total_cases
        if(result > best_case):
            best_case = result
            #best_config = (wisard.get_mapping(), wisard.get_discriminators())
#    return (best_case, best_config)
    print("best case: " + str(best_case))
    return best_case
