import json
import socket, threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect(('127.0.0.1', 7976))  # connecting client to server


class ClientHandle:
    msg = b""
    already_sent = False

    def receive(self):
        while True:  # making valid connection
            try:
                self.msg = client.recv(1024)
                self.already_sent = False
                print(f"jon: {json.loads(self.msg)}\n")
            except Exception as e:  # case on wrong ip/port details
                print(f"An error occured! {e}")
                client.close()
                break

    def write(self):
        while True:  # message layout
            if not self.already_sent:
                a = {"dsf": "erz"}
                a = json.dumps(a)
                a = bytes(a, 'UTF-8')
                client.send(a)
                self.already_sent = True
            else:
                pass

    def run(self):
        receive_thread = threading.Thread(target=self.receive)  # receiving multiple messages
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)  # sending messages
        write_thread.start()


c_hand = ClientHandle()
c_hand.run()