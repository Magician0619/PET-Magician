import numpy as np
from scipy import ndimage
from scipy.signal import convolve
import matplotlib.pyplot as plt
import imageio
from cv2 import cv2

#两种滤波器的实现
def RLFilter(N, d):
    filterRL = np.zeros((N,))
    for i in range(N):
        filterRL[i] = - 1.0 / np.power((i - N / 2) * np.pi * d, 2.0)
        if np.mod(i - N / 2, 2) == 0:
            filterRL[i] = 0
    filterRL[int(N/2)] = 1 / (4 * np.power(d, 2.0))
    return filterRL

def SLFilter(N, d):
    filterSL = np.zeros((N,))
    for i in range(N):
        #filterSL[i] = - 2 / (np.power(np.pi, 2.0) * np.power(d, 2.0) * (np.power((4 * (i - N / 2)), 2.0) - 1))
        filterSL[i] = - 2 / (np.pi**2.0 * d**2.0 * (4 * (i - N / 2)**2.0 - 1))
    return filterSL

def IRandonTransform(image, steps):
    #定义用于存储重建后的图像的数组
    channels = len(image[0])
    origin = np.zeros((steps, channels, channels))
    #filter = RLFilter(channels, 1)
    filter = SLFilter(channels, 1)
    for i in range(steps):
        projectionValue = image[:, i]
        projectionValueFiltered = convolve(filter, projectionValue, "same")
        projectionValueExpandDim = np.expand_dims(projectionValueFiltered, axis=0)
        projectionValueRepeat = projectionValueExpandDim.repeat(channels, axis=0)
        origin[i] = ndimage.rotate(projectionValueRepeat, i*180/steps, reshape=False).astype(np.float64)
    iradon = np.sum(origin, axis=0)
    return iradon

#读取图片
#image = cv2.imread('straightLine.png', cv2.IMREAD_GRAYSCALE)
image = cv2.imread("v.png", cv2.IMREAD_GRAYSCALE)

iradon = IRandonTransform(image, len(image[0]))
#绘制原始图像和对应的sinogram图
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.subplot(1, 2, 2)
plt.imshow(iradon, cmap='gray')
plt.show()
