
from inspect import Parameter
import matplotlib.mlab as mlab
from re import error
from matplotlib import patches
# from matplotlib.pyplot import plt
import pylab as plt
from numpy import array
import numpy as np
import pylab as pl
from scipy.optimize import curve_fit
from scipy.stats import norm


oriPath = "Task1-samples\\Task1-ReleaseV1.0\\energy_2020-09-30.csv"
global max_value,nomrmal
max_value = 40000
normal = 511
global gx_rate,gy_rate
# gx_rate = 1
# gy_rate = 1
gx_rate = 100
gy_rate = 1600


def get_data(lines):
    '''
    读取数据
    '''
    sizeArry = []
    for line in lines:
        line = line.replace('\n',"")
        line = line.replace(',','')
        line = int(float(line))
        sizeArry.append(line)
    return array(sizeArry)

def gaussian(data):

    x = np.array(data) 
    mu =np.mean(x) #计算均值 
    sigma =np.std(x) 
    num_bins = 30 #直方图柱子的数量 
    n, bins, patches = plt.hist(x, num_bins,density=1, alpha=0.75) 
    #直方图函数，x为x轴的值，normed=1表示为概率密度，即和为一，绿色方块，色深参数0.5.返回n个概率，直方块左边线的x值，及各个方块对象 
    y = norm.pdf(bins, mu, sigma)#拟合一条最佳正态分布曲线y 

    plt.grid(True)
    plt.plot(bins, y, 'r--') #绘制y的曲线 
    plt.xlabel('values') #绘制x轴 
    plt.ylabel('Probability') #绘制y轴 
    plt.title('Histogram : $\mu$=' + str(round(mu,2)) + ' $\sigma=$'+str(round(sigma,2)))  #中文标题 u'xxx' 
    #plt.subplots_adjust(left=0.15)#左边距 

def gaussian_singletrue(x,*param):
    '''
    真实事件的高斯峰
    '''
    return param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def gaussian_1(x,*param):
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))

def gaussian_2(x,*param):
    '''二元高斯函数拟合过程

    '''
    return param[0]*np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.)))+\
           param[1]*np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def gaussian_3(x,a1,a2,a3,m1,m2,m3,s1,s2,s3):   # 三元高斯拟合函数 
     
    return a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)

def draw_hist(lenths):

    # 绘制直方图
    bins1 = np.linspace(min(lenths),max(lenths),200)
    pl.figure("能谱直方图")
    n1, bins1, patches1 = pl.hist(lenths,bins1)
    pl.xlabel('Energy')
    pl.ylabel('Counts')
    pl.title('Energy spectrum histogram')


    # 能谱归一化
    n12 = n1.tolist()
    frequent_index = n12.index(max(n12)) 
    data = lenths*511/(0.5*(bins1[frequent_index]+bins1[frequent_index+1]))
    bins2 = np.linspace(min(data),max(data),200)
    pl.figure("归一化能谱直方图")
    n2, bins2, patches2 = pl.hist(data,bins2)
    pl.xlabel('Energy')
    pl.ylabel('Counts')
    pl.title('Normalized energy spectrum histogram')




    # 绘制高斯拟合图
    # bins比n多一个数
    # bins = np.delete(bins,-1) # 方法一：去除列表最后面的一个数
    guass_x = []
    guass_x = np.array(guass_x)
    guass_y = n2
    for i in range(len(bins2)-1):    #方法二：bins需要取矩形两端端点的均值
        temp = 0.5*(bins2[i]+bins2[i+1])
        guass_x = np.append(guass_x,temp)
    popt,pcov = curve_fit(gaussian_2,guass_x/gx_rate,guass_y/gy_rate,p0=[3,4,3,6,1,1],maxfev = 140000)

    plt.figure("高斯拟合图")
    plt.plot(guass_x,guass_y,'b*:',label='data')
    plt.plot(guass_x,gaussian_2(guass_x/gx_rate,*popt)*gy_rate,'r',label='fit')
    plt.legend()
    plt.show()
    print("高斯拟合的参数：",*popt)

    # 计算能量分辨率
    
    

    # 循环计算列表横坐标中的拟合值是否等于半高度
    '''
    global half_h_w1, half_h_w2,E_max
    half_h_w1, half_h_w2 = 0,0
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
    '''双峰融合版
    global half_h_w_list
    half_h_w_list = []
    high = max(gaussian_2(guass_x/gx_rate,*popt)*gy_rate)
    for x in guass_x:       
        if(int(gaussian_2(x/gx_rate,*popt)*gy_rate)>int(0.5*high)):
            half_h_w_list = np.append(half_h_w_list,x)
    E_max = 511
    
    half_h_w = max(half_h_w_list)-min(half_h_w_list)
    eta = half_h_w/E_max
    print("能量分辨率为：",eta)
    '''
    global half_h_w_list
    half_h_w_list = []
    high = max(gaussian_singletrue(guass_x/gx_rate,*popt)*gy_rate)
    for x in guass_x:       
        if(int(gaussian_singletrue(x/gx_rate,*popt)*gy_rate)>int(0.5*high)):
            half_h_w_list = np.append(half_h_w_list,x)
    E_max = 511
    
    half_h_w = max(half_h_w_list)-min(half_h_w_list)
    eta = half_h_w/E_max
    print("能量分辨率为：",eta)
    
    '''    
    high = max(gaussian_2(guass_x,*popt))
    
    for x in x_point:
    '''     
    

           
# 首先打开文件从文件中读取数据
f = open(oriPath,encoding="utf-8")
Lenths = get_data(f.readlines())  
draw_hist(Lenths)


