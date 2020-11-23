import SimpleITK as sitk
import os

folder_path = "E:/Rayplus2021/dicom_basic/T1 dong li/S70"
folder_name = "E:/Rayplus2021/dicom_basic"
file_name = "I10"
file_path = os.path.join(folder_path, file_name)

# 单张读取方法一：直接返回image对象，简单易懂，但是无法读取tag值
img = sitk.ReadImage(file_path)
print(type(img))  # <class 'SimpleITK.SimpleITK.Image'>
sitk.Show(img)

# 单张读取方法二
file_reader = sitk.ImageFileReader()
file_reader.SetFileName(file_path)  # 这里只显示了必需的,还有很多可以设置的参数
data = file_reader.Execute()
for key in file_reader.GetMetaDataKeys():  # 使用这种方法读取Dicom的Tag Value
    print(key, file_reader.GetMetaData(key))

data_np = sitk.GetArrayFromImage(data)
print(data_np.shape)  # (1, 512, 512) = (Slice index, Rows, Columns)

# 序列读取
series_reader = sitk.ImageSeriesReader()
fileNames = series_reader.GetGDCMSeriesFileNames(folder_name)
series_reader.SetFileNames(fileNames)
images = series_reader.Execute()

# 边缘检测
data_32 = sitk.Cast(data, sitk.sitkFloat32)
data_edge_1 = sitk.CannyEdgeDetection(data_32, 5, 30, [5]*3, [0.8]*3)

# 边缘检测2
Canny = sitk.CannyEdgeDetectionImageFilter()
Canny.SetLowerThreshold(5)
Canny.SetUpperThreshold(30)
Canny.SetVariance([5]*3)
Canny.SetMaximumError([0.5]*3)
data_edge_2 = Canny.Execute(data_32)
sitk.Show(data_edge_2)

# 写入一张dicom文件
new_name = "new_MR_2.dcm"
sitk.WriteImage(img, os.path.join(folder_name, new_name))
file_writer = sitk.ImageFileWriter()
file_writer.SetFileName(os.path.join(folder_name, new_name))
file_writer.SetImageIO(imageio="GDCMImageIO")
file_writer.Execute(img)
