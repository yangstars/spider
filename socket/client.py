#-*- coding:utf-8 -*-
import socket


#定义服务器访问地址或者ip地址
target_host="192.168.0.2"
#定义访问的端口号
target_port =8081

#建立一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 参数：ipv4   tcp

#连接客户端
client.connect((target_host,target_port))

client.send("ceshi")

response = client.recv("4096")