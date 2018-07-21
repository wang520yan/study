# -*- encoding:utf-8 -*-
# 客户端
import hashlib
import socket

address = ('localhost', 6666)    # 写明要发送消息的服务端的地址和端口号
client = socket.socket()
client.connect(address)           # 连接服务端

# 第一种
# client.send(b"hell world")      # 发送信息，注意在python3中socket的发送只支持bytes类型
# data = client.recv(1024)         # 等待接收服务端返回的信息
# print("client recv:", data)

# 第二种
while True:
    # 使其可以向服务端多次发送消息
    msg = raw_input(">>>:").strip()
    # 如果发送的消息为空，则不再发送
    if len(msg) == 0:
        break
    msg = msg.encode('utf-8')   # 将要发送的消息转为bytes类型
    client.send(msg)      # 发送信息，注意在python3中socket的发送只支持bytes类型
    data = client.recv(1024)         # 等待接收服务端返回的信息
    print("client recv:", data.decode())
#

# 第三种
# while True:
#     cmd = raw_input("(command)>>>:").strip()
#     if len(cmd) == 0:
#         '''发送空命令时，结束本次循环'''
#         continue
#     if cmd == "#exit":
#         '''当检测到#exit，客户端与服务端断开连接'''
#         break
#     client.send(cmd.encode())        #向服务端发送命令
#     cmd_result = ''      #目前已接收的数据
#     size_data = 0        #目前已接收数据的长度
#     size_cmd_result = int(client.recv(1024).decode())  #接收命令执行结果的长度
#     client.send("OK".encode("utf-8"))  #向服务端确认收到数据长度
#     while size_data < size_cmd_result:
#         '''命令的执行结果可能大于设置的接收buffersize，多次接收'''
#         data = client.recv(1024).decode()           #每次接收的数据
#         size_data += len(data)
#         cmd_result += data
#     print(cmd_result)

# 第四种 实现一个简单的ftp的服务端和客户端
# while True:
#     content = client.recv(4096)             # 接收并打印服务端有哪些文件
#     print("Files List".center(75, '-'))
#     print(content.decode())
#
#     # 向服务端发送想要接收的文件名
#     filename = raw_input("(You want to get)>>>:").strip()
#     if filename == '#exit':
#         break
#     client.send(filename.encode('utf-8'))
#     file_size = client.recv(1024).decode()
#     if file_size.isdigit():
#         '''文件大小是不小于0的数字，则文件存在，准备接收'''
#         file_size = int(file_size)
#         if file_size >= 0:
#             data_size = 0
#             data_md5 = hashlib.md5()         #初始化MD5对象，用以向服务端校验
#             client.send("OK".encode('utf-8'))         #向服务端确认接收数据
#             with open(filename, 'wb') as fp:
#                 while data_size < file_size:
#                     data = client.recv(1024)
#                     data_md5.update(data)
#                     data_size += len(data)
#                     fp.write(data)
#             client.send(data_md5.hexdigest().encode('utf-8'))    #发送服务端发送数据的MD5码
#             message = client.recv(1024).decode()           #接收并打印服务端的校验信息
#             print(message)
#             print('\n\n\n')
#     else:
#          '''文件大小不是数字，则出错，打印服务端的提示信息'''
#          print(file_size)
#          continue



client.close()                   # 关闭客户端