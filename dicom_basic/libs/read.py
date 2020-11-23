from skimage import exposure, img_as_float
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2
import numpy as np
import pydicom
import SimpleITK
import SimpleITK as sitk
import os
import time

folder_path = "E:/Rayplus2021/dicom_basic/T1 dong li/S70"
folder_name = "E:/Rayplus2021/dicom_basic"
file_name = "I10"
file = os.path.join(folder_path, file_name)


def show(file):

    img = sitk.ReadImage(file)
    # print(type(img))  # <class 'SimpleITK.SimpleITK.Image'>
    sitk.Show(img)


def is_dicom_file(filename):

    # 判断某文件是否是dicom格式的文件
    file_stream = open(filename, 'rb')
    file_stream.seek(128)
    data = file_stream.read(4)
    file_stream.close()
    if data == b'DICM':
        return True
    return False


def load_patient(src_dir):
    '''
        读取某文件夹内的所有dicom文件
    :param src_dir: dicom文件夹路径
    :return: dicom list
    '''
    files = os.listdir(src_dir)
    slices = []
    for s in files:
        if is_dicom_file(src_dir + '/' + s):
            instance = pydicom.read_file(src_dir + '/' + s)
            slices.append(instance)

    try:
        slice_thickness = np.abs(
            slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(
            slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness
    return slices


def get_pixels_hu_by_simpleitk(dicom_dir):
    '''
        读取某文件夹内的所有dicom文件
    :param src_dir: dicom文件夹路径
    :return: image array
    '''
    reader = SimpleITK.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    img_array = SimpleITK.GetArrayFromImage(image)
    img_array[img_array == -2000] = 0
    return img_array


def dcm2png(file,filename):
    '''
    arg file: str, file with path
    return: cv2.img
    '''

    dcm = pydicom.dcmread(file,force=True)
    imageX = dcm.pixel_array
    temp = imageX.copy()
    print("imageX shape (for debug):", imageX.shape)
    picMax = imageX.max()
    vmin = imageX.min()
    vmax = temp[temp < picMax].max()
    # print("vmin (for debug) : ", vmin)
    # print("vmax (for debug) : ", vmax)
    imageX[imageX > vmax] = 0
    imageX[imageX < vmin] = 0
    # result = exposure.is_low_contrast(imageX)
    # # print(result)
    dst = file.replace(filename,'')
    pngname = dst + 'show.png'
    image = img_as_float(imageX)
    plt.cla()
    plt.figure('adjust_gamma', figsize=(10.24, 10.24))
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.imshow(image, 'gray')
    plt.axis('off')
    plt.savefig(pngname)
    time.sleep(1)
    
    # cv2.imwrite('static/uploads/show.png')
    # return png


# dcm2png(file)
