from __future__ import annotations
import json
import random
import socket
from scipy.spatial import distance
from abc import ABC, abstractmethod
from typing import Any, Optional


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
client.connect(('127.0.0.1', 7976))  # connecting client to server

class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None


    def set_next(self, handler: Handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any):
        if self._next_handler:
            return self._next_handler.handle(request)

        return None

class Player:
    def __init__(self, name, role, color, ball, pos_x, pos_y):
        self.name = name
        self.role = role
        self.color = color
        self.ball = ball
        self.pos_x = pos_x
        self.pos_y = pos_y

class ClientTeam:
    def __init__(self):
        self.players = []

class EnemyWithBall:
    def __init__(self):
        self.enemy_w_ball = ""

class EnemyGate:
    def __init__(self):
        self.ball = ""
        self.pos_x = ""
        self.pos_y = ""

class Ball:
    def __init__(self):
        self.pos_x = ""
        self.pos_y = ""

class GameElements:
    def __init__(self):
        self.client_team: ClientTeam = None
        self.enemy: EnemyWithBall = None
        self.enemy_gate: EnemyGate = None
        self.ball: Ball = None

class FirstCatchHandler(AbstractHandler):
    def handle(self, elem: Any):
        if not elem.enemy.enemy_w_ball.name:
            self.catch_ball_first(elem)
        else:
            return super().handle(elem)

    def catch_ball_first(self, elem):
        player_one = ""
        for player in elem.client_team.players:
            if player.name == "yellow_one":
                player_one = player

        n = random.randint(10, 70)
        pos_x = player_one.pos_x
        pos_y = player_one.pos_y
        player_one.pos_x = pos_x + (elem.ball.pos_x - pos_x) / n
        player_one.pos_y = pos_y + (elem.ball.pos_y - pos_y) / n

class EnemyAttackHandler(AbstractHandler):
    def handle(self, elem: Any):
        if elem.enemy.enemy_w_ball.color != elem.client_team.players[0].color:
            closest_player = self.get_closest_player_to_enemy_w_ball(elem)
            self.follow_ball(closest_player, elem.enemy.enemy_w_ball)
        else:
            return super().handle(elem)

    def get_closest_player_to_enemy_w_ball(self, elem):
        closest_player = elem.client_team.players[0]
        min_distance = distance.euclidean([elem.enemy.enemy_w_ball.pos_x, elem.enemy.enemy_w_ball.pos_y],
                                          [closest_player.pos_x, closest_player.pos_y])

        for player in elem.client_team.players:
            dist = distance.euclidean([elem.enemy.enemy_w_ball.pos_x, elem.enemy.enemy_w_ball.pos_y],
                                      [player.pos_x, player.pos_y])
            if dist < min_distance and player.role == "simple":
                closest_player = player

        return closest_player

    def follow_ball(self, closest_player, enemy_w_ball):
        speed = random.randint(10,30)
        if closest_player.role == "simple":
            closest_player.pos_x += (enemy_w_ball.pos_x - closest_player.pos_x) / speed
            closest_player.pos_y += (enemy_w_ball.pos_y - closest_player.pos_y) / speed

class ClientAttackHandler(AbstractHandler):
    def handle(self, elem: Any):
        if elem.enemy.enemy_w_ball.color == elem.client_team.players[0].color:
            self.move_players_to_enemy_gate(elem.client_team, elem.enemy_gate)
        else:
            return super().handle(elem)

    def move_players_to_enemy_gate(self, client_team, enemy_gate):
        for player in client_team.players:
            if player.role == "simple":
                speed = (random.randint(1, 20) / 10)
                dist_x = enemy_gate.pos_x - player.pos_x
                dist_y = enemy_gate.pos_y - player.pos_y
                a = int(("1" + (len(str(abs(dist_x))) - 1) * "0")) + 10
                b = int(("1" + (len(str(abs(dist_x))) - 1) * "0")) + 10
                player.pos_x += (dist_x / a) * speed
                player.pos_y += (dist_y / b) * speed


class ClientHandle:
    msg = b""
    already_sent = False

    def create_object_from_dict(self, all_data, client_team_name):
        elements = GameElements()
        client_team = elements.client_team = ClientTeam
        enemy = elements.enemy = EnemyWithBall
        enemy_gate = elements.enemy_gate = EnemyGate
        ball = elements.ball = Ball

        team_players = []
        for player in all_data[client_team_name]:
            player_data = all_data[client_team_name][player]
            team_players.append(Player(**player_data))
        client_team.players = team_players

        enemy_w_ball_data = all_data["player_with_ball"]
        enemy.enemy_w_ball = Player(**enemy_w_ball_data)

        enemy_gate.ball = all_data["blue_gate"]["ball"]
        enemy_gate.pos_x = all_data["blue_gate"]["pos_x"]
        enemy_gate.pos_y = all_data["blue_gate"]["pos_y"]

        ball.pos_x = all_data["ball"]["pos_x"]
        ball.pos_y = all_data["ball"]["pos_y"]
        return elements

    def create_dict_from_objects(self, all_data, client_team, client_team_name, enemy_gate):
        for player in client_team:
            all_data[client_team_name][player.name]["role"] = player.role
            all_data[client_team_name][player.name]["color"] = player.color
            all_data[client_team_name][player.name]["ball"] = player.ball
            all_data[client_team_name][player.name]["pos_x"] = player.pos_x
            all_data[client_team_name][player.name]["pos_y"] = player.pos_y

        all_data["blue_gate"]["ball"] = enemy_gate.ball

        return all_data

    def run(self):
        while True:
            self.msg = client.recv(5000)
            all_data = json.loads(self.msg)
            client_team_name = "yellow_team"
            client_team_color = "yellow"
            game_elements = self.create_object_from_dict(all_data, client_team_name)

            first_catch = FirstCatchHandler()
            enemy_attack = EnemyAttackHandler()
            client_attack = ClientAttackHandler()

            first_catch.set_next(enemy_attack).set_next(client_attack)
            first_catch.handle(game_elements)

            all_data = self.create_dict_from_objects(all_data,
                                                     game_elements.client_team.players,
                                                     client_team_name,
                                                     game_elements.enemy_gate)
            all_data = json.dumps(all_data)
            all_data = bytes(all_data, 'UTF-8')
            client.send(all_data)

c_hand = ClientHandle()
c_hand.run()