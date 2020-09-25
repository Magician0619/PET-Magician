
'''
##########################################
# 双指数曲线拟合
##########################################
def double_exp(x,a,b,c,d,e,f):
    '''
    双指数函数曲线
    '''
    # return  a*np.exp(b*x)+c*np.exp(d*x)+e
    return  a*np.exp(b*x)+c*np.exp(d*x)
    # return  a*np.exp(b*x)+c*np.exp(d*x)+e*x+f

rate = 1000
x_dexp = x/rate
y_dexp = y/rate 
popt, pcov = curve_fit(double_exp, x_dexp, y_dexp)
# bounds=(-20,[0.01,0.01,0.01,0.01,0.01,0.01])
# ,bounds=(0,[1000,1000,1000,1000,1000,1000])
'''
# 曲线拟合，并得到拟合曲线相关系数
# popt：阵列参数的最佳值，以使（扩展数据，*popt）-ydata平方残差之和最小
# pcov：二维阵列popt的估计协方差，对角线提供参数估计的方差。
# perr = np.sqrt(np.diag(pcov))，使用perr计算参数的一个标准偏差误差。
'''
print("所得双指数函数形式为：%fexp(%fx)+%fexp(%fx)+%f"%(popt[0],popt[1],popt[2],popt[3],popt[4]))

# 对数据进行插值，使得双指数曲线更加光滑

x_inter = np.linspace(0,x_dexp[7],1000)
y_inter = double_exp(x_inter,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5]) #拟合y值

plt.figure("双指数插值曲线")
# plt.plot(x, y, 's',label='original values')
plt.plot(x_inter, y_inter, 'r',label='polyfit values')
plt.title('Double exponential interpolation curve')
plt.xlabel('Time(ns)')
plt.ylabel('Voltage(mv)')
plt.legend()

'''
