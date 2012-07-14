import argparse
import socketserver
import socket
import server_handler
import sys


class ChatRequestHandler(socketserver.BaseRequestHandler):

    def handle(self): 
        addr = self.client_address[0] 
        print("[%s] Verbindung hergestellt" % addr )
        while True: 
            s = self.request.recv(1024) 
            if s: 
                print("[%s] %s" % (addr, s) )
            else: 
                print("[%s] Verbindung geschlossen" % addr) 
                break

class Client:
    host = "localhost"
    port = 9999
    def __init__(self, host = "localhost", port = 9999):
        self.host = host
        self.port = port

    def connect(self):

        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server and send data
        self.sock.connect((self.host, self.port))


    def close(self):
        self.sock.close()

    def send(self, message):
        if message is None and self.sock is None:    
            return None 
        self.sock.sendall(bytes(data + "\n", "utf-8"))
        
        # Receive data from the server and return it
        return str(self.sock.recv(1024), "utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Little script to simplify the communication between different machines.')
    parser.add_argument("mode", choices=["server", "client"], help="specify whether the script will act as the server or the client")
    parser.add_argument("-p", "--port", type=int, default=9999, help="specify the port to use")
    args = parser.parse_args()
    if not args.mode in ["client","server"]:
        print("PyCom: mode '" + args.mode + "' unknown, must be one of the following: client, server")
    elif args.mode == "server":
        print(args.mode)

        # Create the server, binding to localhost on port 9999
        server = socketserver.TCPServer(("localhost", args.port), server_handler.ServerHandler)

        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    else:#client
        host = input("host: ")
        client = Client(host,args.port)
        try:
            client.connect()

            data = input("<<< ")
            while data != "!close":
                answer = client.send(data)

                print(">>> {}".format(answer))
                
                data = input("<<< ")

        finally:
            client.close()