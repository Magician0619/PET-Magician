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
    for i in range (binf_num):
        binf_single = binf[i*67 : (i+1)*67]
        content = struct.unpack('<Bhdddddddd', binf_single)       
        for j in range(2,10): 
            squares.append(content[j]-content[2])
            sheet1.write(i,j,content[j])

convert('cy.samples')
f.save("save.xlsx") #保存文件