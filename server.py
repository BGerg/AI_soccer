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


blue_one = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
blue_two = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
blue_three = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
blue_four = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
blue_five = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
blue_goalkeeper = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}

yellow_one = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
yellow_two = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
yellow_three = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
yellow_four = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
yellow_five = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}
yellow_goalkeeper = {"id": 1, "color": "blue", "position_x": 123,"position_y": 123, "ball": "False"}

blue_team = {"blue_one": blue_one, "blue_two": blue_two, "blue_three": blue_three, "blue_four": blue_four, "blue_five": blue_five, "blue_goalkeeper":blue_goalkeeper }

yellow_team = {"yellow_one": yellow_one, "yellow_two": yellow_two, "yellow_three": yellow_three, "yellow_four": yellow_four, "yellow_five": yellow_five, "yellow_goalkeeper":yellow_goalkeeper}


ball = {"position_x": 123, "position_y": 123}

blue_gate = {"position_x": 123, "position_y": 123, "ball": False}
yellow_gate = {"position_x": 123, "position_y": 123, "ball": False}
goal_area_yellow = {"position_x": 123, "position_y": 123, "ball": False}
goal_area_blue = {"position_x": 123, "position_y": 123, "ball": False}

data = {"yellow_team":yellow_team, "blue_team": blue_team, "blue_gate":blue_gate, "yellow_gate":yellow_gate, "goal_area_yellow": goal_area_yellow,"goal_area_blue":goal_area_blue }

def handle(client):
    seresr = 0
    first = True
    while True:
        #time.sleep(1)
        if first:
            a = data
            a = json.dumps(a)
            a = bytes(a, 'UTF-8')
            client[0].send(a)
            first = False

        message = client[0].recv(5000)

        decoded = json.loads(message)
        print(f"{decoded}\n")
        a = json.dumps(decoded)
        a = bytes(a, 'UTF-8')
        client[1].send(a)

        message = client[1].recv(5000)
        decoded = json.loads(message)
        print(f"{decoded}\n")
        a = json.dumps(decoded)
        a = bytes(a, 'UTF-8')
        client[0].send(a)

def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)
        if len(clients) == 2:
            handle(clients)

receive()