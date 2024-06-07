import socket
import sys
import os
import random

message_queues = []  # 初始化待发送消息队列


def read_file_in_chunks(file_path, chunk_sizes):
    # 以指定大小读取文件的生成器
    with open(file_path, 'r') as file:  # 读入二进制文件
        while True:
            try:
                size = next(chunk_sizes)
            except StopIteration:
                return  # 当没有更多的 chunk size 时，结束生成器
            data = file.read(size)
            if not data:
                break
            yield data


# 生成随机大小的文件块生成器
def chunk_size_generator(lmin, lmax, total_size):
    # 考虑程序的健壮性，需要先检验输入参数是否合法
    if lmin < 1:
        print("输入的lmin参数小于1，请重新输入！")
        sys.exit(0)
    if lmax < 1:
        print("输入的lmax参数小于1，请重新输入！")
        sys.exit(0)
    if lmin > lmax:
        print("输入的lmin大于lmax，请重新输入！")
        sys.exit(0)
    if lmin > total_size:
        print("输入的lmin大于文本文件的最大长度，请重新输入！")
        sys.exit(0)
    remaining = total_size
    while remaining > 0:
        # 因为randint()函数是左闭右开，所以上界需要加1
        size = random.randint(min(lmin, remaining), min(lmax, remaining) + 1)
        yield size
        remaining -= size

def reversetcpclient():
    # 考虑程序健壮性，对命令行参数进行检查
    if len(sys.argv) != 6:
        print("您输入的参数个数有误，请重新输入！\n格式为：python reversetcpclient.py <server_ip> <server_port> <file_path> <lmin> <lmax>")
        sys.exit(1)
    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        file_path = sys.argv[3]
        lmin = int(sys.argv[4])
        lmax = int(sys.argv[5])
    except Exception:
        print("您输入的参数格式有误，请检查后重新输入！\n格式为：python reversetcpclient.py <server_ip> <server_port> <file_path> <lmin> <lmax>")
        sys.exit(1)

    total_size = os.path.getsize(file_path)
    chunk_sizes = chunk_size_generator(lmin, lmax, total_size)

    # 在开始发送数据块前，随机确定待发送File中的各块的长度，再计算块数N
    for i, chunk in enumerate(read_file_in_chunks(file_path, chunk_sizes), start=1):
        # 向服务器发送数据块请求，并接收反转后的数据块
        request = f"reverseRequest:{len(chunk)}:{chunk}".encode('utf-8')
        message_queues.append(request)

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        # 向服务器发送initialization报文。
        client_socket.send(f"initialization:{len(message_queues)}".encode('utf-8'))
        ack = client_socket.recv(1024)

        # 如果收到服务器回复的agree报文，继续发送reverseRequest报文
        if ack.decode('utf-8') == "agree":
            filepath = os.path.dirname(os.path.abspath(file_path)) + '\\reversed_text.txt'
            f = open(filepath, 'w')
            Answer = ''
            for i, message in enumerate(message_queues, start=1):
                client_socket.send(message)
                response = client_socket.recv(1024).decode('utf-8')
                Answer += response
                # time.sleep(2)  # 通过设置延迟2秒可以测试多个client端和server端的连接
                reverseAnswer = f"第{i}块反转的文本: {response}"
                # 每次 client收到来自server 的 reverseAnswer 报文，都在命令行下打印出来
                print(reverseAnswer)
                # 将结果保存在文本文件里，该文件是原始文件的全部反转
                f.write(reverseAnswer + '\n')
            f.write("\n原始文件的全部反转是：" + Answer)
            f.close()
        else:
            print(f"未收到服务器({server_ip, server_port})的agree报文！")
    except Exception:
        print(f"与服务器({server_ip, server_port})连接建立失败！\n请检查与服务器IP地址和端口是否输入正确，客户端与服务器之间的通信是否正常！")
    finally:
        client_socket.close()


if __name__ == "__main__":
    reversetcpclient()
