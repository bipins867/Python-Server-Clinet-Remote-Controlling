import WiFi as wf
import os
import myStringLib as ms
import socket


def check_int_conn():
    try:
        socket.gethostbyname("www.google.com")
        return True
    except:
        return False

def get_current_ip():
    if(check_int_conn()):
        data=os.popen('ipconfig').read()
        d=ms.find_get_text(data,'IPv4',55)
        d=ms.find_get_text(d,': ',20)
        index=d.index('\n')
        d=d[:index]
        d=ms.trimString(d,' ')

        return d
    else:

        print("System is not connected to <Internet>")


def client_connect(ip='192.168.1.100',port=44):
    s=socket.socket()
    try:
        s.connect((ip,port))

        return s

    except:
        print("Can't Connect To The Server")


def create_server(ip='192.168.1.100',port=44,no_of_client=5):
    s=socket.socket()
    
    try:
        s.bind((ip,port))
        s.listen(no_of_client)
        return s
    except:
        print("Can't Create Server")
