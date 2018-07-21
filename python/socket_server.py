# -*- encoding:utf-8 -*-
import hashlib
import os
import socket

address = ("localhost", 6666)  # 写明服务端要监听的地址，和端口号
server = socket.socket()        # 生成一个socket对象
server.bind(address)            # 用socket对象绑定要监听的地址和端口
server.listen(5)                 # 开始监听

# 第一种
# conn,addr = server.accept()     #等带新连接接入服务端，返回一个新的socket对象和地址，地址格式同前面格式
# '''
# Wait for an incoming connection.  Return a new socket
# representing the connection, and the address of the client.
# '''
# data = conn.recv(1024)         #接收信息，写明要接收信息的最大容量，单位为字节
# print("server recv:", data)
# conn.send(data.upper())       #对收到的信息处理，返回到客户端

# 第二种
while True:
    # 一条连接关闭后，接入下一条连接
    conn,addr = server.accept()     # 等带新连接接入服务端，返回一个新的socket对象和地址，地址格式同前面格式
    '''
    Wait for an incoming connection.  Return a new socket
    representing the connection, and the address of the client.
    '''
    while True:
        # 使其可以接收多次消息
        data = conn.recv(1024)         # 接收信息，写明要接收信息的最大容量，单位为字节
        # 没收到消息，断开本次连接
        if not data:
            break
        print("server recv:", data)
        conn.send(data.upper())       # 对收到的信息处理，返回到客户端

# 第三种
# while True:
#     # 一条连接关闭后，接入下一条连接
#     conn,addr = server.accept()     # 等带新连接接入服务端，返回一个新的socket对象和地址，地址格式同前面格式
#     '''
#     Wait for an incoming connection.  Return a new socket
#     representing the connection, and the address of the client.
#     '''
#     while True:
#         data = conn.recv(1024)         # 接收信息，写明要接收信息的最大容量，单位为字节
#         # 没收到消息，断开本次连接
#         print data
#         if not data:
#             break
#         cmd_result = os.popen(data.decode(), 'r').read()             # 执行命令，将命令执行结果保存到cmd_result
#         if len(cmd_result) == 0:
#             '''命令执行结果为空，认为接收到错误命令'''
#             cmd_result = "It's a wrong command..."
#
#         while True:
#             conn.send(str(len(cmd_result)).encode('utf-8'))     # 发送命令执行结果的长度
#             confirm = conn.recv(1024).decode()
#             '''客户端确认收到数据长度，发送数据，否则重传；且解决粘包问题'''
#             if confirm == "OK":
#                 conn.send(cmd_result.encode('utf-8'))       # 对收到的信息处理，返回到客户端
#                 break
#             else:
#                 continue

# 第四种
# while True:
#     # 一条连接关闭后，接入下一条连接
#     conn,addr = server.accept()     # 等带新连接接入服务端，返回一个新的socket对象和地址，地址格式同前面格式
#     while True:
#         content = os.popen('ls', 'r').read()
#         conn.send(content.encode('utf-8'))      # 与客户端建立连接后，将服务端有哪些文件发给客户端，供客户端选择
#         filename = conn.recv(1024).decode()      # 接收客户端发来的文件名
#         if os.path.isfile(filename):
#             '''文件存在，开始发送文件'''
#             file_md5 = hashlib.md5()             # 初始化MD5对象，用于传输完成后的校验
#             file_size = os.stat(filename)[6]     # 读取文件大小
#             conn.send(str(file_size).encode('utf-8'))      # 将文件size发给客户端
#             confirm = conn.recv(1024).decode()             # 等待客户端确认接收
#             if confirm == "OK":
#                 '''发送文件数据'''
#                 with open(filename, 'rb') as fp:
#                      for line in fp:
#                          file_md5.update(line)
#                          conn.send(line)
#
#                 client_md5 = conn.recv(1024).decode()        # 传输完成后接收客户端发来的MD5
#                 if file_md5.hexdigest() == client_md5:
#                     conn.send("Success...".encode('utf-8'))
#                 else :
#                     '''文件传输出错，提示客户端删除重传'''
#                     conn.send("This file is changed, please delete it and try again...".encode('utf-8'))
#
#              # 客户端未确认接收，重试
#             else:
#                 conn.send("Error, try again...".encode('utf-8'))
#                 continue
#
#         else :
#             '''文件不存在，让客户端重新发送文件名'''
#             conn.send("The file name is wrong and try again".encode('utf-8'))
server.close()      # 关闭服务端