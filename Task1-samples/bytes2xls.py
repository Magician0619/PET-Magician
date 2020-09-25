import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import math
import random
import csv
import xlwt


f = xlwt.Workbook()
sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True)


'''
binFile=open('cy.samples','rb')
a=binFile.read()

print(len(a))
cycle=int(len(a)/67)+1

print(cycle-1)

cycle=8  #前七组数据 

squares=[]        
for i in range(1,cycle,1):
    b=a[(i-1)*67:i*67]
    c=struct.unpack('<Bhdddddddd', b)
    # print(c)
    for j in range(2,10): 
        squares.append(c[j]-c[2])
        print("时间：",c[j]-c[2])
print(squares)
'''

def convert(filename):
    """
    # Date:
    # Function:
    # Paramters:
    # Attentions:
    """

    binfile = open(filename, "rb")
    binf = binfile.read()   # 读取得到的字节
    binf_lenfth = len(binf) # 字节长度
    binf_num = int(binf_lenfth/67)+1

    squares = []
    for i in range (100):
        binf_single = binf[i*68 : (i+1)*68]
        content = struct.unpack('<hhdddddddd', binf_single)
        for k in range(2):
            sheet1.write(i,k,content[k])       
        for j in range(2,10): 
            squares.append(content[j]-content[2])
            sheet1.write(i,j,content[j]-content[2])

convert('E:\\PET\\数据集\\6BDM.samples')
f.save("save.xls") #保存文件