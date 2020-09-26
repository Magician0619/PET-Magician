import os
from numpy import array
import numpy as np
import pylab as pl
import re


oriPath = "Task1-samples\\energy.csv"
global max_value,nomrmal
max_value = 40000
normal = 511
# 创建一个函数用来读取数据
def get_data(lines):
    sizeArry = []
    for line in lines:
        # line = line.replace(bytes("\n",'utf-8'),"")
        # str = '\n'
        # str = str.encode()
        # line = line.replace(str,"")
        line = line.replace('\n',"")
        line = int(float(line))
        sizeArry.append(line)
    return array(sizeArry)

# 首先打开文件从文件中读取数据
f = open(oriPath,encoding="utf-8")
Lenths = get_data(f.readlines())

def draw_hist(lenths):
    data = lenths/max_value*normal
    bins = np.linspace(min(data),600,200)

    pl.hist(data,bins)
    pl.xlabel('Energy')
    pl.ylabel('Counts')
    pl.title('The energy spectra and coincidence-time histograms')
    pl.show()

draw_hist(Lenths)


