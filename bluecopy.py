
import socket, threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('127.0.0.1', 7976))                             #connecting client to server
HEADERSIZE_ONE = 10

class ClientHandle:
    msg = b""
    already_sent = False
    msglen = 0
    result = ""
    def receive(self):
        full_msg = b''
        new_msg = True
        while True:                                                 #making valid connection
            msg = client.recv(16)
            if new_msg and msg != b'':
                self.msglen = int(msg[:HEADERSIZE_ONE])
                new_msg = False
            full_msg += msg

            if len(full_msg) - HEADERSIZE_ONE == self.msglen:
                self.result = pickle.loads(full_msg[HEADERSIZE_ONE:])
                print(self.result)
                new_msg = True
                full_msg = b""
                msglen = 0
                self.already_sent = False

    def write(self):
        while True:                                                   #message layout
            if not self.already_sent:
                msg = pickle.dumps(self.result)
                msg = bytes(f"{len(msg):<{HEADERSIZE_ONE}}", 'utf-8') + msg
                client.send(msg)
                self.already_sent = True
            else:
                pass

    def run(self):
        receive_thread = threading.Thread(target=self.receive)               #receiving multiple messages
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)                   #sending messages
        write_thread.start()

c_hand = ClientHandle()
c_hand.run()