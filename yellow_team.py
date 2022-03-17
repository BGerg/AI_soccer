import socket, threading

nickname = "yellow_team"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect(('127.0.0.1', 7976))  # connecting client to server


class ClientHandle:
    msg = ""
    already_sent = False

    def receive(self):
        while True:  # making valid connection
            try:
                message = client.recv(1024).decode('ascii')
                self.already_sent = False
                if message == 'NICKNAME':
                    client.send(nickname.encode('ascii'))
                else:
                    self.msg = message
                    print(message)
            except:  # case on wrong ip/port details
                print("An error occured!")
                client.close()
                break

    def write(self):
        while True:  # message layout
            if not self.already_sent:
                message = self.msg+"a"
                client.send(message.encode('ascii'))
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