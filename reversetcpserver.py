import socket
import select


def reverse_text(text):
    # 文本反转函数
    return text[::-1]


server_ip = '127.0.0.1'  # 服务器监听的IP地址
server_port = 6666       # 服务器监听的端口号
buffer_size = 1024       # 数据接收缓冲区大小

def reversetcpserver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个套接字对象
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)  # 让套接字进入监听状态，最大连接数量是5
    server_socket.setblocking(0)  # 设置为非阻塞模式，使得server能够处理多个client的请求

    inputs = [server_socket]  # 初始化选择输入列表
    outputs = []              # 初始化选择输出列表
    message_queues = {}       # 初始化消息队列字典

    print("服务器启动在 {}:{}".format(server_ip, server_port))

    try:
        while inputs:
            # select函数阻塞程序运行，监听inputs中的套接字
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is server_socket:
                    # 处理新的连接
                    client_socket, client_address = s.accept()
                    print("新的连接来自 {}".format(client_address))
                    client_socket.setblocking(0)
                    inputs.append(client_socket)
                    message_queues[client_socket] = []
                else:
                    # 接收数据
                    data = s.recv(buffer_size)
                    if data:
                        decoded_data = data.decode('utf-8')
                        # 解析数据并根据请求类型进行处理
                        data_parts = decoded_data.split(':')

                        # 如果收到的是initialization报文，回复agree报文
                        if data_parts[0] == 'initialization':
                            print(f"收到来自客户端{client_address}的initialization报文")
                            response_data = f"agree"
                            message_queues[s].append(response_data.encode('utf-8'))
                            if s not in outputs:
                                outputs.append(s)
                            print(f"向客户端{client_address}回复agree报文")

                        # 如果收到的是reverseRequest报文，返回client端reverseAnswer报文
                        elif data_parts[0] == 'reverseRequest':
                            print(f"\n接收到来自客户端{client_address}的数据: {data_parts[2]}")
                            response_data = reverse_text(data_parts[2])
                            message_queues[s].append(response_data.encode('utf-8'))
                            if s not in outputs:
                                outputs.append(s)
                            print(f"发送反转文本: {response_data.encode('utf-8')}")
                    else:
                        # 处理连接断开
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()
                        del message_queues[s]
                        print(f"\n与客户端{client_address}断开连接！\n")

            for s in writable:
                try:
                    next_msg = message_queues[s].pop(0)
                except IndexError:
                    outputs.remove(s)
                else:
                    s.send(next_msg)

            for s in exceptional:
                # 处理异常情况
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del message_queues[s]

    finally:
        server_socket.close()

if __name__ == "__main__":
    reversetcpserver()