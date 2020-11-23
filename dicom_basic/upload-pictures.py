# coding:utf-8
 
from flask import Flask,render_template,request,redirect,url_for,make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
 
from datetime import timedelta
 
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
 
@app.route('/', methods=['POST', 'GET'])  # 添加路由
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        image_data = open(upload_path, "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
 
    return render_template('upload.html')
 
if __name__ == '__main__':
    # app.debug = True
    # app.run(host = '0.0.0.0',port = 8987,debug= True)
	app.run(debug=True)