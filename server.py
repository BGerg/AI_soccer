#Coded by Yashraj Singh Chouhan
import socket, threading                                                #Libraries import
import time

host = '127.0.0.1'                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
nicknames = []
teams = {}
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        #time.sleep(1)
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            if client == teams["blue_team"]:
                receiver = teams["yellow_team"]
                receiver.send(message)
            if client == teams["yellow_team"]:
                receiver = teams["blue_team"]
                receiver.send(message)
        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        if nickname == "blue_team":
            teams["blue_team"] = client
        elif nickname == "yellow_team":
            teams["yellow_team"] = client
        print("Nickname is {}".format(nickname))
        if len(clients) == 2:
            #broadcast("{} joined!".format(nickname).encode('ascii'))
            #broadcast('Connected to server!'.encode('ascii'))
            for client in clients:
                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
        elif len(clients) == 1:
            client.send('Waiting for other player to join...'.encode('ascii'))

receive()