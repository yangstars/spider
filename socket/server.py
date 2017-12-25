#-*- coding:utf-8 -*-
import socket
import threading


#定义服务器访问地址或者ip地址
bing_ip="127.0.0.1"
#定义访问的端口号
bing_port =8082

#创建socket 对象
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((bing_ip,bing_port))
server.listen(5)

#创建一个客户处理线程

def handle_client(client_socket):
    #打印出客户端发送得到的消息
    request = client_socket.recv(1024)
    print "request %s"%(str(request))

    #返回一个数据包
    client_socket.send("ACK!")
    client_socket.close()

while True:
    client,addr = server.accept()

    #挂起而客户端线程，进行数据处理
    client_handle = threading.Thread(target=handle_client,args=(client,))
    client_handle.start()


