a = [1,5,3,7,1]
b = ['a','b','c','d','e']


for i,j in zip(a,b):
    print(j*i, end="\r")