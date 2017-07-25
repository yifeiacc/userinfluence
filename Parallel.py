
def split(l,n):#helper function for data partition
    L =[]
    gap = int(len(l)/n)
    begin = 0
    for i in range(0,n):
        if i == n-1:
            L.append(l[begin:])
        else:
            L.append(l[begin:begin + gap])
        begin = begin+gap
    return L

