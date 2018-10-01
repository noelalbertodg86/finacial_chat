import sys
import socket
import threading
import traceback
import json

from utilities import Utilities
from Model.chatMessageModel import chatMessageModel
from config import getconfigValue

class Server:
    #create socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        #inicialize socket listen by de 10000 port in localhost
        self.connections = []
        self.server_address = getconfigValue('SERVER', 'ip')
        self.server_port = int(getconfigValue('SERVER', 'port'))
        self.sock.bind((self.server_address, self.server_port))
        self.sock.listen()
        self.chatMessage_ = chatMessageModel()

    def handler(self, c, a):
        while True:
            try:
                data = c.recv(1024)
                print('Server recive: => %s' % str(data))
                jsonData = json.loads(data.decode())

                ## the bot is call
                if jsonData['message'].find('APPL') > -1:
                    util_ = Utilities(self.connections)
                    util_.invokeBot(body=str(data,'utf-8'))
                else:
                    #save message in db except bot call
                    iThread = threading.Thread(target=self.saveMessage(jsonData))
                    iThread.start()

                #the receive message is send to all the conected client except by the one who send the message
                for connection in self.connections:
                    if connection.fileno() != c.fileno():
                        connection.send(bytes(jsonData['user']+':: '+jsonData['message'],'utf-8'))

                #validations
                if not data:
                    self.connections.remove(c)
                    c.close()
                    print(str(a[0]) + ':' + str(a[1]) + ' disconnected')
                    break
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
                print(str(a[0]) + ':' + str(a[1]) + ' disconnected. Error: ' + str(error))
                break

    def saveMessage(self, params):
        self.chatMessage_.saveMessage(params)

    def run(self):
        count = 0
        while True:
            count += 1
            #trace print
            print('Server is listen (%s:%s)...' % (self.server_address, self.server_port))
            # wait for a connections to accept and start the process
            c, a = self.sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            # initialize daemon
            cThread.daemon = True
            cThread.start()
            #add all connections at the list for forward every message to all connections
            self.connections.append(c)
            # trace print
            print(str(a[0]) + ':' + str(a[1]) + ' is connected')


server = Server()
server.run()


