# coding:utf-8

from libs.read import dcm2png
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
import redis
import pickle
import re

from datetime import timedelta

from libs import *

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'dcm', ''])


def allowed_file(filename):

    fileTF = '.' in filename and filename.rsplit(
        '.', 1)[1] in ALLOWED_EXTENSIONS or not('.' in filename)
    # 判断.dcm文件或者无后缀名的文件
    try:
        filetype = filename.rsplit('.', 1)[1]
    except IndexError as error:
        print(error, '该文件没有后缀名，并请注意检查该文件是否是DICOM文件！！！')
        filetype = '.dcm'
    print("文件名：", filename)
    print("文件类型：", filetype)
    return filename, fileTF, filetype


class CACHE:
    def __init__(self, host='127.0.0.1', password='123456'):
        pool = redis.ConnectionPool(host=host, password=password)
        self.conn = redis.Redis(connection_pool=pool)

    def insert_image(self, frame_id, frame):
        # 将图片序列化存入redis中
        b = pickle.dumps(frame)  # frame is numpy.ndarray
        self.conn.set(frame_id, b)

    def get_image(self, frame_id):
        # 从redis中取出序列化的图片并进行反序列化
        return pickle.loads(self.conn.get(frame_id))


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

# 配置Redis
app.config['REDIS_HOST'] = "127.0.0.1"
app.config['REDIS_PORT'] = 6379
redis_store = redis.StrictRedis(host="127.0.0.1", port=6379)


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload')
@app.route('/', methods=['POST', 'GET'])  # 添加路由
def upload():

    if request.method == 'POST':

        # 传输文件操作
        f = request.files['file']
        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        # 判断文件是否符合类型
        filename, fileTF, filetype = allowed_file(f.filename)

        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        try:
            upload_path = os.path.join(
                basepath, 'static/uploads', secure_filename(f.filename))
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')
        except FileNotFoundError as error:
            upload_path = os.path.join(
                basepath, 'static/uploads', secure_filename(f.filename))
            print(error, '注意：没有的文件夹一定要先创建，不然会提示没有该路径')
        f.save(upload_path)

        print(type(f))
        # redis_store.set(f.filename, f.CACHE.insert_img)
        # redis_store.set(f.filename, f)


        # 根据文件类型做出对应的操作
        if fileTF and filetype =='.dcm':
            dcm2png(file=upload_path,filename=filename)
            

        elif fileTF and filetype!='dcm':
            # 使用Opencv转换一下图片格式和名称
            png = cv2.imread(upload_path)
            cv2.imwrite(os.path.join(basepath, 'static/uploads', 'show.png'), png)
            # img = redis_store.get(f.filename)
        else:
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp、dcm"})

        
        # img_redis = imgCACHE.insert_img
        # img_redis = redis_store.get('test.jpg')

        return render_template('upload_ok.html', userinput=user_input, val1=time.time())

    return render_template('upload.html')


if __name__ == '__main__':
    # app.debug = True
    # app.run(host='0.0.0.0', port=8987, debug=True)
    app.run(debug=True)
