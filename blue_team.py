import json
import socket, threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('127.0.0.1', 7976))                             #connecting client to server
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

data = {"yellow_team":yellow_team}
class ClientHandle:
    msg = b""
    already_sent = False
    def receive(self):
        while True:                                                 #making valid connection
            try:
                self.msg = client.recv(1024)
                self.already_sent = False
                print(json.loads(self.msg))
            except Exception as e:  # case on wrong ip/port details
                print(f"An error occured! {e}")
                client.close()
                break
    def write(self):
        while True:                                                   #message layout
            if not self.already_sent:
                a = data
                a = json.dumps(a)
                a = bytes(a, 'UTF-8')
                client.send(a)
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