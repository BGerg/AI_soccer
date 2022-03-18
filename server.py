#Coded by Yashraj Singh Chouhan
import json
import socket, threading                                                #Libraries import
import time

host = '127.0.0.1'                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
teams = {}

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    seresr = 0
    while True:
        #time.sleep(1)


        message = client.recv(5000)
        if message != b'':


            print(f"{json.loads(message)}\n")
        #if client == teams["blue_team"]:
         #   receiver = teams["yellow_team"]
         #   receiver.send(message)
        #if client == teams["yellow_team"]:
         #   receiver = teams["blue_team"]
         #   receiver.send(message)


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)
        if "blue_team" in teams:
            teams["yellow_team"] = client
        else:
            teams["blue_team"] = client
        #if len(clients) == 2:
            #broadcast("{} joined!".format(nickname).encode('ascii'))
            #broadcast('Connected to server!'.encode('ascii'))
            #for client in clients:
             #   thread = threading.Thread(target=handle, args=(client,))
            #    thread.start()
        handle(clients[0])
            #handle(clients[1])

receive()