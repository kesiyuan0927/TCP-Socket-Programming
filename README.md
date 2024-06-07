# TCP Socket Programming

## 1. 简介

此系统允许客户端从一个ASCII文本文件中读取数据块，发送给服务器，服务器将文本块反转后返回给客户端。客户端和服务器均为基于TCP的命令行程序。此系统设计支持多客户端同时操作，并且能够非阻塞方式处理客户端请求。

## 2. 环境要求

*   操作系统：任何支持Python和TCP/IP套接字的操作系统，如Windows, Linux, macOS。
*   Python版本：Python 3.6 或更高版本。

## 3. 文件说明

*   `reversetcpclient.py`：客户端程序，用于发送数据块和接收反转后的数据块。
*   `reversetcpserver.py`：服务器程序，用于接收数据块、处理数据（文本反转）并返回结果。
*   `text.txt`：示例的ASCII文本文件，应由用户根据需要创建。
*   `reversed_text.txt`：运行客户端程序后，自动生成在text.txt文本文件的相同目录下，用于记录反转结果，无需用户创建。

## 4. 配置和运行指导

### 客户端配置选项

客户端启动时需要指定以下参数：

*   `server_ip`：服务器的IP地址。
*   `server_port`：服务器监听的端口号。
*   `file_path`：要发送的ASCII文本文件的路径。
*   `lmin`：发送的最小数据块大小（字节）。
*   `lmax`：发送的最大数据块大小（字节）。

### 运行客户端

打开命令行窗口，使用以下命令运行客户端：

```bash
python reversetcpclient.py <server_ip> <server_port> <file_path> <lmin> <lmax>
```

示例：

```bash
python reversetcpclient.py 127.0.0.1 6666 text.txt 1 5
```

### 服务器配置选项

服务器端需要手动配置监听的IP地址和端口，在reversetcpserver.py文件中修改server\_ip和server\_port的值。

### 运行服务器

打开命令行窗口，运行以下命令启动服务器：

```bash
python reversetcpserver.py
```

服务器将开始监听配置的端口，并等待客户端连接和数据。

## 5. 注意事项

*   确保客户端和服务器使用相同的端口号和符合网络配置的IP地址。
*   文件路径应正确指向一个存在的ASCII文本文件。
*   控制块大小`lmin`和`lmax`参数确保在指定范围内。

