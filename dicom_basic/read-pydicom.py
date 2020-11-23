from matplotlib import pyplot
from PIL import Image
import numpy as np
import os
import pydicom

# 调用本地的 dicom file
folder_path = "E:/Rayplus2021/dicom_basic/T1 dong li/S70"
file_name = "I10"
file_path = os.path.join(folder_path, file_name)
ds = pydicom.dcmread(file_path)
# ds = pydicom.dcmread(file_path,force=True)	# 缺少原文件信息头情况下强制读取
print("PatientID:%s, StudyDate:%s, Modality:%s" %
      (ds.PatientID, ds.StudyDate, ds.Modality))

data = np.array(ds.pixel_array)
data_img = Image.fromarray(ds.pixel_array)
data_img_rotated = data_img.rotate(
    angle=45, resample=Image.BICUBIC, fillcolor=data_img.getpixel((0, 0)))
data_rotated = np.array(data_img_rotated, dtype=np.int16)

print(data.dtype)  # int16
print(data_img)   # int32

pyplot.imshow(ds.pixel_array, cmap=pyplot.cm.bone)
pyplot.show()

data_img.show()
# data_img.save("test.png")

'''
ds.PixelData = data_rotated.tobytes()
ds.Rows, ds.Columns = data_rotated.shape
new_name = "dicom_rotated.dcm"
# ds.save_as(os.path.join(folder_path, new_name))
ds.save_as(new_name)
'''