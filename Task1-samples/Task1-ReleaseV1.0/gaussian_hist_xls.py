
import matplotlib.mlab as mlab
from re import error
from matplotlib import patches
# from matplotlib.pyplot import plt
import pylab as plt
from numpy import array
import numpy as np
import pylab as pl
from scipy.optimize import curve_fit


oriPath = "Task1-samples\\Task1-ReleaseV1.0\\energy_2020-09-29.xls"
global max_value,nomrmal
max_value = 40000
normal = 511
global gx_rate,gy_rate
gx_rate = 10
gy_rate = 200


def get_data(lines):
    '''
    读取数据
    '''
    sizeArry = []
    for line in lines:
        line = line.replace('\n',"")
        line = int(float(line))
        sizeArry.append(line)
    return array(sizeArry)

# 首先打开文件从文件中读取数据
f = open(oriPath,encoding="utf-8")
Lenths = get_data(f.readlines())

def gaussian_1(x):
    num_bins = 30 #直方图柱子的数量 
    n, bins, patches = plt.hist(x, num_bins,normed=1, facecolor='blue', alpha=0.5) 
    #直方图函数，x为x轴的值，normed=1表示为概率密度，即和为一，绿色方块，色深参数0.5.返回n个概率，直方块左边线的x值，及各个方块对象 
    y = mlab.normpdf(bins, mu, sigma)#拟合一条最佳正态分布曲线y 
    plt.plot(bins, y, 'r--') #绘制y的曲线 
    plt.xlabel('Energy') #绘制x轴 
    plt.ylabel('Probability') #绘制y轴 
    plt.title(r'Histogram : $\mu=5.8433$,$\sigma=0.8253$')#中文标题 u'xxx' 
    plt.subplots_adjust(left=0.15)#左边距 
    plt.show()

def gaussian_2(x,*param):
    '''二元高斯函数拟合过程

    '''
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+\
           param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def gaussian_3(x,a1,a2,a3,m1,m2,m3,s1,s2,s3):   # 三元高斯拟合函数 
     
    return a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)

def draw_hist(lenths):
    data = lenths/max_value*normal  # 对数据归一化
    bins = np.linspace(min(data),600,200)


    n, bins, patches = pl.hist(data,bins)
    
    # 绘制直方图
    pl.xlabel('Energy')
    pl.ylabel('Counts')
    pl.title('The energy spectra and coincidence-time histograms')
    pl.show()

    # 绘制高斯拟合图
    # bins比n多一个数
    # bins = np.delete(bins,-1) # 方法一：去除列表最后面的一个数
    x_point = []
    x_point = np.array(x_point)
    guass_y = n
    for i in range(len(bins)-1):    #方法二：bins需要取矩形两端端点的均值
        temp = 0.5*(bins[i]+bins[i+1])
        x_point = np.append(x_point,temp)
    popt,pcov = curve_fit(gaussian_2,x_point,guass_y,p0=[70,80,60,120,10,20],maxfev = 140000)
    plt.plot(x_point,guass_y,'b+:',label='data')
    plt.plot(x_point,gaussian_2(x_point,*popt),'ro:',label='fit')
    plt.legend()
    plt.show()

    # 计算能量分辨率
    
    global half_h_w1, half_h_w2,E_max
    half_h_w1, half_h_w2 = 0,0

    # 循环计算列表横坐标中的拟合值是否等于半高度
    '''
    for x in x_point:       
        if(x<256&int(gaussian_2(x,*popt))==int(0.5*high)):
            half_h_w1 = x
        if(x>256&int(gaussian_2(x,*popt))==int(0.5*high)):
            half_h_w2 = x
        E_max = 0
        if(int(gaussian_2(x,*popt)>E_max)):
            E_max = x
    half_h_w = half_h_w2-half_h_w1
    '''

    # 将大于半高度的横坐标保存下来，并追加列表，计算列表中首尾两项的差值
    global half_h_w_list
    half_h_w_list = []
    x_point = np.linspace(min(data),max(data),500000)
    high = max(gaussian_2(x_point,*popt))
    for x in x_point:       
        if(int(gaussian_2(x,*popt))>int(0.5*high)):
            half_h_w_list = np.append(half_h_w_list,x)
    E_max = 511
    
    half_h_w = max(half_h_w_list)-min(half_h_w_list)
    eta = half_h_w/E_max
    print("能量分辨率为：",eta)
    
    
    '''    
    high = max(gaussian_2(guass_x,*popt))
    
    for x in x_point:
    '''     
    

           
    
draw_hist(Lenths)


