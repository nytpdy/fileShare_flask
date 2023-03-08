import ctypes
import json
import os
import platform
import socket
import time
import uuid
from urllib.parse import urljoin
import subprocess

import pandas as pd
from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS  # 跨域
from flask_login import LoginManager, login_user, logout_user, login_required
from gevent import pywsgi

from models import User, query_user
from pds import deletefile, writefile, collection

storage_path = str(os.getcwd()) + '\storage'
storage_datapath = str(os.getcwd()) + '\data'

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = '1234567'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '请登录'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id
        return curr_user


@app.route('/getfiles', methods=['POST'])
# @login_required
def getfiles():
    res = request.get_json()
    uname = res['username']
    print(uname)
    pat = storage_path
    files = list(os.walk(pat))[0][2]
    # 读取目录文件的名字信息
    data = {}
    for fil in files:
        with open(storage_datapath + '\\' + fil + '.json', 'r') as load_f:
            j = json.load(load_f)
        info = {
            'fileName': fil,
            'fileSuffix': fil.split(".")[1],
            'userName': j['username'],
            'dateTime': j['datetime'],
            'size': str(j['size'] / 1000) + 'kb',
            'checked': j['checked'],
            'fileType': 'file',
            'fileCollect': collection(uname, fil)
        }
        data[fil] = info

    files = list(os.walk(pat))[0][1]
    # 读取目录文件夹的名字信息

    res_json = json.dumps(data)
    # return 响应体, 状态码, 响应头
    return res_json, 200, {"Content-Type": "application/json"}


@app.route('/getpicture', methods=['POST'])
# @login_required
def getpicture():
    res = request.get_json()
    uname = res['username']
    # print('进入getpic')
    pat = storage_path
    files = list(os.walk(pat))[0][2]
    # 读取目录文件的名字信息
    data = {}
    pic = ['jpg', 'png', 'jpeg', 'gif', 'bmp', 'JPG', 'PNG', 'JPEG', 'GIF', 'BMP']
    for fil in files:
        # print(fil.split(".")[1])
        if fil.split(".")[1] not in pic:
            continue
        with open(storage_datapath + '\\' + fil + '.json', 'r') as load_f:
            j = json.load(load_f)
        info = {
            'fileName': fil,
            'fileSuffix': fil.split(".")[1],
            'userName': j['username'],
            'dateTime': j['datetime'],
            'size': str(j['size'] / 1000) + 'kb',
            'checked': j['checked'],
            'fileType': 'file',
            'fileCollect': collection(uname, fil)
        }
        data[fil] = info

    files = list(os.walk(pat))[0][1]
    # 读取目录文件夹的名字信息

    res_json = json.dumps(data)
    # return 响应体, 状态码, 响应头
    return res_json, 200, {"Content-Type": "application/json"}


@app.route('/getCollection', methods=['POST'])
def getCollection():
    res = request.get_json()
    uname = res['username']
    # print('进入getpic')
    pat = storage_path
    files = list(os.walk(pat))[0][2]
    # 读取目录文件的名字信息
    data = {}
    for fil in files:
        # print(fil.split(".")[1])
        if collection(uname, fil) != 1:
            continue
        with open(storage_datapath + '\\' + fil + '.json', 'r') as load_f:
            j = json.load(load_f)
        info = {
            'fileName': fil,
            'fileSuffix': fil.split(".")[1],
            'userName': j['username'],
            'dateTime': j['datetime'],
            'size': str(j['size'] / 1000) + 'kb',
            'checked': j['checked'],
            'fileType': 'file',
            'fileCollect': collection(uname, fil)
        }
        data[fil] = info

    files = list(os.walk(pat))[0][1]
    # 读取目录文件夹的名字信息

    res_json = json.dumps(data)
    # return 响应体, 状态码, 响应头
    return res_json, 200, {"Content-Type": "application/json"}


# 登录验证
@app.route('/login', methods=['GET', 'POST'])
# @login_required
def login():
    data = request.get_json()
    print(data)
    user_id = data['userName']
    user_pw = data['passWord']
    print(user_id, user_pw)
    if request.method == 'POST' and user_id and user_pw:
        # user_id = request.get_data('username')
        # print("user_id = ", user_id)
        # user_pw = request.get_data('password')
        # user = get_user(user_id)
        user = query_user(user_id)
        print(user)
        if user is None:
            print("-1")
            data = {
                'status': '-1',
                'msg': "用户不存在"
            }
            res_json = json.dumps(data)
            return res_json, 200, {"Content-Type": "application/json"}
        elif user_pw != user['password']:
            print("0")
            data = {
                'status': '0',
                'msg': "密码错误"
            }
            res_json = json.dumps(data)
            return res_json, 200, {"Content-Type": "application/json"}
        elif user_pw == user['password']:
            curr_user = User()
            curr_user.id = user_id
            login_user(curr_user)
            data = {
                'username': user['username'],
                'userid': user['id'],
                'fileMax': get_free_space_mb(storage_path),
                'filesize': getFileSize(storage_path)
            }
            res_json = json.dumps(data)
            print("登陆成功")
            return res_json, 200, {"Content-Type": "application/json"}
            # return "user_id"
        else:
            res_json = json.dumps({'1': 1})
            return res_json, 200, {"Content-Type": "application/json"}
    else:
        return "error"


# ----------------------------------------------------------------------------------------------------------------------


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


def getIp():
    """
    获取本机ip地址
    :return: str: 本机ip
    """
    ip = '127.0.0.1'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(str(e)[0:0] + '获取本机ip失败 默认设置为：127.0.0.1')
    return ip


# 上传文件
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     f = request.files.get('file')
#     username = request.args.get('name')
#     if f is None:
#         return "获取文件为空"
#     print("yes2")
#     # f.save(os.path.join(os.getcwd(), f.filename))
#     f.save(os.path.join(storage_path, f.filename))
#     insert_file_info(f.filename, username)
#     return json.loads('{}')


def insert_file_info(filename, username):
    '''
    file_basename: 文件名
    username: 用户名
    保存用户上传文件的信息，每次谁谁什么时候上传...
    '''
    filepath = os.path.join(storage_path, filename)  # 文件的全路径
    infopath = os.path.join(storage_datapath, filename + '.json')  # 文件信息的全路径
    info = {
        'username': username,
        'datetime': time.strftime(r'%F %T'),
        'size': os.path.getsize(filepath),
        "checked": "false"
    }
    with open(infopath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(info))


# 下载 yes
@app.route('/download')
def download():
    # print(os.path.pardir)
    # return send_from_directory(os.path.pardir, filename, as_attachment=True)
    # return send_from_directory(os.getcwd(), filename, as_attachment=True)
    # fileName = request.form.get('fileName')
    fileName = request.args.get('fileName')
    # 生成二维码
    # img = qrcode.make(data=send_from_directory(storage_path, fileName, as_attachment=True))
    # # 将二维码保存为图片
    # with open('test.png', 'wb') as f:
    #     img.save(f)
    print("下载完成", fileName)
    return send_from_directory(storage_path, fileName, as_attachment=True)


# 重命名 yes
@app.route('/rename', methods=['POST'])
def rename():
    data = request.get_json()
    # print(data)
    os.rename(storage_datapath + '\\' + data['fileName'] + '.json', storage_datapath + '\\' + data['newName'] + '.json')
    os.rename(storage_path + '\\' + data['fileName'], storage_path + '\\' + data['newName'])
    return 'yes'


# 收藏 yes
@app.route('/setcollect', methods=['POST'])
def setcollect():
    res = request.get_json()
    # print(res)
    # collection(res['username'], res['fileName'])
    writefile(res['username'], res['fileName'])
    return 'yes'


# 取消收藏 yes
@app.route('/cancelcollect', methods=['POST'])
def cancelcollect():
    res = request.get_json()
    # print(res)
    # collection(res['username'], res['fileName'])
    deletefile(res['username'], res['fileName'])
    return 'yes'


# 文件删除
@app.route('/deletefile', methods=['POST'])
def delete():
    data = request.get_json()
    print(data)
    username = data['userName']
    res = {}
    filedata = str(data['fileData']).split("+++")
    for fl in filedata:
        print("删除file" + fl)
        os.remove(storage_path + '\\' + fl)
        os.remove(storage_datapath + '\\' + fl + '.json')
    res_json = json.dumps({'code': 200})
    return res_json, 200, {"Content-Type": "application/json"}


@app.route('/index', methods=['POST'])
def loginindex():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    # path = os.getcwd()
    path = storage_path
    print('===========================' + path)
    files = list(os.walk(path))[0][2]
    # files.remove('运行.bat')
    return render_template('index.html', files=files, ip=ip)


def get_free_space_mb(folder):
    """
    获取磁盘剩余空间
    :param folder: 磁盘路径 例如 D:\\
    :return: 剩余空间 单位 G
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024 // 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 // 1024


def getFileSize(filePath, size=0):
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    size = size / float(1024 * 1024)
    return round(size, 2)


# @app.route('/uploadFile', methods=['POST'])
# def uploadFile():
#     file0 = request.form.get(
#         'fileToUpload')  # request.form outputs ImmutableMultiDict([]); request.form.get('fileToUpload') outputs None
#     file = request.files.getlist('fileToUpload')[0]  # the type of file is FileStorage
#     upload_dataset = pd.read_csv(file)
#     username = request.args.get('name')
#     if upload_dataset is None:
#         return "获取文件为空"
#     print("yes2")
#     # f.save(os.path.join(os.getcwd(), f.filename))
#     upload_dataset.save(os.path.join(storage_path, upload_dataset.filename))
#     insert_file_info(upload_dataset.filename, username)
#     return json.loads('{}')


##################################################################################################
# 配置文件
##################################################################################################
UPLOAD_FOLDER = 'storage'
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 允许的扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'avi'}

# 20g
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024 * 20


# 检查后缀名是否为允许的文件
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 获取文件名
def random_filename(filename):
    ext = os.path.splitext(filename)[-1]
    return uuid.uuid4().hex + ext


# 上传文件
@app.route("/upload", methods=['POST'])
def upload():
    file = request.files.get('file')
    username = request.files.get('useaName')

    if file and allowed_file(file.filename):
        print(file.filename)

        filename = random_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(os.path.join(app.root_path, filepath))

        file_url = urljoin(request.host_url, filepath)

        insert_file_info(filename, username)

        return file_url
    return "not allow ext"


# 获取文件
@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/test')
def test():
    ls = []
    sizeMax = get_free_space_mb(storage_path)
    ls.append(sizeMax)
    fsize = getFileSize(storage_path)
    ls.append(fsize)
    ls.append("hello")
    return ls


@app.route('/hello')
def hello():
    return "hello"


if __name__ == '__main__':
    print('#' * 40)
    print(storage_path)
    print(' ' * 3 + f'访问地址：http://{getIp()}:5000')
    print('#' * 40)
    print('服务启动------------------------------------------>')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    # print('复制' + ip + ':5000' + '到浏览器打开')
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
