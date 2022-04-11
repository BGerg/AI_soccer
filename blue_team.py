import json
import random
import socket
from scipy.spatial import distance

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect(('127.0.0.1', 7976))  # connecting client to server

class ClientHandle:
    msg = b""
    already_sent = False

    def catch_ball_first(self, all_data):
        blue_one = all_data["blue_team"]["blue_one"]
        ball = all_data["ball"]
        n = random.randint(10, 70)
        blue_one["position_x"] = blue_one["position_x"]+(ball["position_x"] - blue_one["position_x"]) / n
        blue_one["position_y"] = blue_one["position_y"]+(ball["position_y"] - blue_one["position_y"]) / n

        return all_data

    def get_closest_player_to_enemy_w_ball(self, all_data):
        player_wb = all_data["player_with_ball"]
        closest_player_name = "blue_one"
        not_goalkeeper = False
        while not_goalkeeper:
            min_distance = distance.euclidean([player_wb["position_x"], player_wb["position_y"]],
                                       [all_data["blue_team"][closest_player_name]["position_x"],
                                        all_data["blue_team"][closest_player_name]["position_y"]])

            for player_name in all_data["blue_team"]:
                player = all_data["blue_team"][player_name]
                tmp_dist = distance.euclidean([player_wb["position_x"], player_wb["position_y"]],
                                   [player["position_x"], player["position_y"]])
                if tmp_dist < min_distance:
                    closest_player_name = player_name

                if all_data["blue_team"][closest_player_name]["role"] == "simple":
                    not_goalkeeper = True
        return closest_player_name

    def follow_ball(self, closest_player, all_data):
        player_wb = all_data["player_with_ball"]
        speed = random.randint(10,30)
        if all_data["blue_team"][closest_player]["role"] == "simple":
            all_data["blue_team"][closest_player]["position_x"] += (player_wb["position_x"] - all_data["blue_team"][closest_player]["position_x"]) / speed
            all_data["blue_team"][closest_player]["position_y"] += (player_wb["position_y"] - all_data["blue_team"][closest_player]["position_y"]) / speed

    def move_players_to_enemy_gate(self, all_data):
        speed = (random.randint(1, 20)/10)
        enemy_gate = all_data["yellow_gate"]
        for player in all_data["blue_team"]:
            if all_data["blue_team"][player]["role"] == "simple":
                dist_x = enemy_gate["position_x"]- all_data["blue_team"][player]["position_x"]
                dist_y = enemy_gate["position_y"]- all_data["blue_team"][player]["position_y"]
                a = int(("1" + (len(str(abs(dist_x)))-1)*"0"))+10
                b = int(("1" + (len(str(abs(dist_x)))-1)*"0"))+10
                all_data["blue_team"][player]["position_x"] += (dist_x / a)*speed
                all_data["blue_team"][player]["position_x"] += (dist_y / b)*speed

    def run(self):
        while True:
            self.msg = client.recv(5000)

            all_data = json.loads(self.msg)
            if all_data["player_with_ball"]["name"] == None:
                all_data = self.catch_ball_first(all_data)
                pass
            else:
                if all_data["player_with_ball"]["color"] == "yellow":
                    closest_player = self.get_closest_player_to_enemy_w_ball(all_data)
                    self.follow_ball(closest_player,all_data)
                else:
                    self.move_players_to_enemy_gate(all_data)
            all_data = json.dumps(all_data)
            all_data = bytes(all_data, 'UTF-8')
            client.send(all_data)
            self.already_sent = True


c_hand = ClientHandle()
c_hand.run()