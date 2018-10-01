import sys
import socket
import json

from config import getconfigValue

server_address = getconfigValue('CLIENT', 'ip')
server_port = int(getconfigValue('CLIENT', 'port'))

class Client:
    #create socket object
    sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user_name = ''

    def __init__(self, user_, userId_):
        self.user_name = user_
        self.userId = userId_
        self.sock_client.connect((server_address, server_port))
        print('...Client start successfully')


    def sendMessage_to_chatroom(self, message_, chatRoom = 'DEFAULT'):
        try:
            sendMessage = json.dumps({'userId': self.userId, 'user':self.user_name, 'message': message_, 'chatRoom': chatRoom})
            print('client.sendMessage_to_chatroom input: %s' % sendMessage)
            self.sock_client.send(bytes(sendMessage, 'utf-8'))
        except Exception as w:
            print('ERROR CLIENT SEND MESSAGE TO SHOWROOM: %s' % w.args[0])

    def reciveMessage_from_chatroom(self):
        while True:
            data = self.sock_client.recv(1024)
            print('client.reciveMessage_from_chatroom: ' + str(data, 'utf-8'))
            return (str(data, 'utf-8'))


    def sendMessage(self):
        while True:
            self.sock_client.send(bytes(self.user_name+': ' +input(""), 'utf-8'))

    def reciveMessage(self):
        while True:
            data = self.sock_client.recv(1024)
            print(str(data, 'utf-8'))
            if not data:
                break

# if len(sys.argv) > 1:
#     client = Client(sys.argv[1])
# else:
#     print('ERROR you must initialize the client with de user')
