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
    
