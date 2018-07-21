# # -*- coding: utf-8 -*-
# """
# 应用程序通常通过"套接字"向网络发出请求或者应答网络请求。
# 套接字的作用之一就是用来区分不同应用进程，当某个进程绑定了本机ip的某个端口，
# 那么所有传送至这个ip地址上的这个端口的所有数据都会被内核送至该进程进行处理。
# Python 提供了两个基本的 socket 模块。
#    第一个是 Socket，它提供了标准的 BSD Sockets API。
#    第二个是 SocketServer， 它提供了服务器中心类，可以简化网络服务器的开发。
# ----socket
#    先来说第一个。
# 我们知道，现在的应用程序大多为C/S架构，也就是分为客户端/服务器端。
# 　　服务器端：服务器端进程需要申请套接字，然后自己绑定在这个套接字上，并对这个套接字进行监听。
# 当有客户端发送数据了，则接受数据进行处理，处理完成后对客户端进行响应。
# 　　客户端：客户端则相对简单些，客户端只需要申请一个套接字，然后通过这个套接字连接服务器端的套接字，
# 连接建立后就可以进行后续操作了。
# """
# # python编写服务器端的步骤：
# # 1  创建套接字
# import socket
#
# import family as family
#
# s1 = socket.socket(family,type)
# # family参数代表地址家族，可为AF_INET或AF_UNIX。AF_INET家族包括Internet地址，AF_UNIX家族用于同一台机器上的进程间通信。
# # type参数代表套接字类型，可为SOCK_STREAM(流套接字，就是TCP套接字)和SOCK_DGRAM(数据报套接字，就是UDP套接字)。
# # 默认为family=AF_INET  type=SOCK_STREM
# # 返回一个整数描述符，用这个描述符来标识这个套接字
#
# # 2  绑定套接字
# s1.bind('159.226.95.66',8006)
# # 由AF_INET所创建的套接字，address地址必须是一个双元素元组，格式是(host,port)。host代表主机，port代表端口号。
# # 如果端口号正在使用、主机名不正确或端口已被保留，bind方法将引发socket.error异常。
# # 例: ('192.168.1.1',9999)
#
# # 3  监听套接字
# s1.listen(10)
# # backlog指定最多允许多少个客户连接到服务器。它的值至少为1。收到连接请求后，这些请求需要排队，
# # 如果队列满，就拒绝请求。
#
# # 4  等待接受连接
# connection, address = s1.accept()
# # 调用accept方法时，socket会时入“waiting”状态，也就是处于阻塞状态。客户请求连接时，
# # 方法建立连接并返回服务器。
# # accept方法返回一个含有两个元素的元组(connection,address)。
# # 第一个元素connection是所连接的客户端的socket对象（实际上是该对象的内存地址），
# # 服务器必须通过它与客户端通信；
# # 第二个元素 address是客户的Internet地址。
#
# # 5  处理阶段
# connection.recv(bufsize[,flag])
# #注意此处为connection
# #接受套接字的数据。数据以字符串形式返回，bufsize指定最多可以接收的数量。flag提供有关消息的其他信息，通常可以忽略
#
# connection.send(string[,flag])
# #将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。即：可能未将指定内容全部发送。
#
# # 6  传输结束，关闭连接
# s1.close()
# #关闭套接字
#
# # python编写客户端
#
# # 1  创建socket对象
# import socket
# s2=socket.socket()
#
# # 2  连接至服务器端
# # 2.connect(address)
# #连接到address处的套接字。一般，address的格式为元组（hostname,port）,如果连接出错，返回socket.error错误。
#
# # 3  处理阶段
# s2.recv(bufsize[,flag])
# #接受套接字的数据。数据以字符串形式返回，bufsize指定最多可以接收的数量。flag提供有关消息的其他信息，通常可以忽略
#
# s2.send(string[,flag])
# #将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。即：可能未将指定内容全部发送。
#
# # 4  连接结束，关闭套接字
# s2.close()
#
# """socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0) #获取要连接的对端主机地址
#
# sk.bind(address)
#   将套接字绑定到地址。address地址的格式取决于地址族。在AF_INET下，以元组（host,port）的形式表示地址。
#
# sk.listen(backlog)
#   开始监听传入连接。backlog指定在拒绝连接之前，可以挂起的最大连接数量。
#   backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5，这个值不能无限大，因为要在内核中维护连接队列
#
# sk.setblocking(bool)
#   是否阻塞（默认True），如果设置False，那么accept和recv时一旦无数据，则报错。
#
# sk.accept()
#   接受连接并返回（conn,address）,其中conn是新的套接字对象，可以用来接收和发送数据。address是连接客户端的地址。接收TCP 客户的连接（阻塞式）等待连接的到来
#
# sk.connect(address)
#   连接到address处的套接字。一般，address的格式为元组（hostname,port）,如果连接出错，返回socket.error错误。
#
# sk.connect_ex(address)
#   同上，只不过会有返回值，连接成功时返回 0 ，连接失败时候返回编码，例如：10061
#
# sk.close()
#   关闭套接字
#
# sk.recv(bufsize[,flag])
#   接受套接字的数据。数据以字符串形式返回，bufsize指定最多可以接收的数量。flag提供有关消息的其他信息，通常可以忽略。
#
# sk.recvfrom(bufsize[.flag])
#   与recv()类似，但返回值是（data,address）。其中data是包含接收数据的字符串，address是发送数据的套接字地址。
#
# sk.send(string[,flag])
#   将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。即：可能未将指定内容全部发送。
#
# sk.sendall(string[,flag])
#   将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。内部通过递归调用send，将所有内容发送出去。
#
# sk.sendto(string[,flag],address)
#   将数据发送到套接字，address是形式为（ipaddr，port）的元组，指定远程地址。返回值是发送的字节数。该函数主要用于UDP协议。
#
# sk.settimeout(timeout)
#   设置套接字操作的超时期，timeout是一个浮点数，单位是秒。值为None表示没有超时期。一般，超时期应该在刚创建套接字时设置，
#   因为它们可能用于连接的操作（如 client 连接最多等待5s ）
#
# sk.getpeername()
#   返回连接套接字的远程地址。返回值通常是元组（ipaddr,port）。
#
# sk.getsockname()
#   返回套接字自己的地址。通常是一个元组(ipaddr,port)
#
# sk.fileno()
#   套接字的文件描述符
#
# socket.sendfile(file, offset=0, count=None)
#   发送文件
# """
#
#
# """
# ----socketserver
# 　　虽说用Python编写简单的网络程序很方便，但复杂一点的网络程序还是用现成的框架比较
# 好。这样就可以专心事务逻辑，而不是套接字的各种细节。SocketServer模块简化了编写网络服务程序的任务。同时SocketServer模块也
# 是Python标准库中很多服务器框架的基础。
# socketserver在python2中为SocketServer, 在python3种取消了首字母大写，改名为socketserver。
# socketserver中包含了两种类，一种为服务类（server
#
#
# class ），一种为请求处理类（request handle class ）。前者提供了许多方法：像绑定，监听，运行…… （也就是建立连接的过程） 后者则专注于如何处理用户所发送的数据（也就是事务逻辑）。
#
# 　　一般情况下，所有的服务，都是先建立连接，也就是建立一个服务类的实例，然后开始处理用户请求，也就是建立一个请求处理类的实例。
#
# 我们分析一下源码，来看一看服务类是如何与请求处理类建立联系的。
# 复制代码
#
#
# class BaseServer:
#     # 我们创建服务类时，需要指定（地址，端口）,服务处理类。
#     def __init__(self, server_address, RequestHandlerClass):
#         """Constructor.  May be extended, do not override."""
#         self.server_address = server_address
#         self.RequestHandlerClass = RequestHandlerClass
#         self.__is_shut_down = threading.Event()
#         self.__shutdown_request = False
#
#     # …………此处省略n多代码，当我们执行server_forever方法时，里面就会调用很多服务类中的其他方法，但最终会调用finish_request方法。
#
#     def finish_request(self, request, client_address):
#         """Finish one request by instantiating RequestHandlerClass."""
#         self.RequestHandlerClass(request, client_address, self)
#
#
# # finish_request方法中执行了self.RequestHandlerClass(request, client_address, self)。self.RequestHandlerClass是什么呢？
# # self.RequestHandlerClass = RequestHandlerClass（就在__init__方法中）。所以finish_request方法本质上就是创建了一个服务处理实例。
#
#
# class BaseRequestHandler:
#     def __init__(self, request, client_address, server):
#         self.request = request
#         self.client_address = client_address
#         self.server = server
#         self.setup()
#         try:
#             self.handle()
#         finally:
#             self.finish()
#
# # 当我们创建服务处理类实例时，就会运行handle()方法，而handle()方法则一般是我们处理事务逻辑的代码块。
# # …………此处省略n多代码
# 复制代码
#
# 我们接下来介绍一下这两个类
# 先来看服务类：
# 5
# 种类型：BaseServer，TCPServer，UnixStreamServer，UDPServer，UnixDatagramServer。
# BaseServer不直接对外服务。
# TCPServer针对TCP套接字流
# UDPServer针对UDP数据报套接字
# UnixStreamServer和UnixDatagramServer针对UNIX域套接字，不常用。
# """