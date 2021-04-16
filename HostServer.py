import socketserver
import http.server
import os

def funHostServer(loc='C:',ip='',port=8080):
    os.chdir(loc)
    handler=http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((ip,port),handler) as httpd:
        print("Server is started {0}:{1}".format(ip,port))
        httpd.serve_forever()


    
