import numpy as np
a = [1,2,3,4]
a = np.array(a)
b = []
b = np.array(b)
a = a.astype(float)
for i in range(len(a)-1):
    c = 0.5*(a[i]+a[i+1])
    b = np.append(b,c)
print(b)
print(a)
c = [4,5,6,7]
print(np.mean(a)) 
