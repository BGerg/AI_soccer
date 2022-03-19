import json
import socket, threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect(('127.0.0.1', 7976))  # connecting client to server

class ClientHandle:
    msg = b""
    already_sent = False


    def valami(self, dict_):
        a = json.dumps(dict_)
        a = bytes(a, 'UTF-8')
        return a

    def run(self):
        while True:
            self.msg = client.recv(5000)

            a = json.loads(self.msg)
            print(a)
            a = json.dumps(a)
            a = bytes(a, 'UTF-8')
            client.send(a)
            self.already_sent = True


c_hand = ClientHandle()
c_hand.run()