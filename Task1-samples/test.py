from scipy import integrate
def f(x):
    return x**2
e = integrate.quad(f,1,2)
print(e[0])  # quad方法会返回精确的值和误差
input()