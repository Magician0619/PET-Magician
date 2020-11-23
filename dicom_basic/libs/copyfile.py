import shutil
import os
#第一部分，准备工作，拼接出要存放的文件夹的路径
file = 'E:/测试/1.jpg'
#current_foder是‘模拟’文件夹下所有子文件名组成的一个列表
current_folder = os.listdir('E:/测试/模拟')#current_foder是‘模拟’文件夹下所有子文件名组成的一个列表

# 第二部分，将名称为file的文件复制到名为file_dir的文件夹中
for x in current_folder:
    #拼接出要存放的文件夹的路径
    file_dir = 'E:/测试/模拟'+'/'+x
    #将指定的文件file复制到file_dir的文件夹里面
    shutil.copy(file,file_dir)
def copy(filesrc,filedst):
    file
print(file.path)