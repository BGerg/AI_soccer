# Import the pygame module
import json
import socket
import time
from scipy.spatial import distance
import pygame
import random
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_HEIGHT = 587
SCREEN_WIDTH = int(1.869*SCREEN_HEIGHT)
all_data = {}
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, name, color, player_posx, player_posy):
        super(Player, self).__init__()
        self.color = color
        self.name = name
        if self.color == "blue":
            self.surf = pygame.image.load("images/player_blue.png").convert()
        elif self.color == "yellow":
            self.surf = pygame.image.load("images/player_yellow.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(player_posx, player_posy, 44, 77)
        self.ball = False


    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        direction = ()
        if pressed_keys[K_UP]:
            direction = (0, -5)
            self.rect.move_ip(direction)
            #move_up_sound.play()
        if pressed_keys[K_DOWN]:
            direction = (0, 5)
            self.rect.move_ip(direction)
            #move_down_sound.play()
        if pressed_keys[K_LEFT]:
            direction = (-5, 0)
            self.rect.move_ip(direction)
        if pressed_keys[K_RIGHT]:
            direction = (5, 0)
            self.rect.move_ip(direction)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def move_to(self, position):
        self.rect.move_ip(position)

    def has_ball(self):
        if self.color == "yellow" and self.ball == False:
            self.surf = pygame.image.load("images/player_yellow.png").convert()
        elif self.color == "blue" and self.ball == False:
            self.surf = pygame.image.load("images/player_blue.png").convert()
        elif self.color == "yellow" and self.ball:
            self.surf = pygame.image.load("images/player_yellow_w_ball.png").convert()
        elif self.color == "blue" and self.ball:
            self.surf = pygame.image.load("images/player_blue_w_ball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

class PlayerGoalKeeper(pygame.sprite.Sprite):
    def __init__(self,color, player_posx, player_posy):
        super(PlayerGoalKeeper, self).__init__()
        self.color = color
        if self.color == "blue":
            self.surf = pygame.image.load("images/goolkeeper_1.png").convert()
        elif self.color == "yellow":
            self.surf = pygame.image.load("images/goolkeeper_2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(player_posx, player_posy, 44, 77)
        self.ball = False

    def has_ball(self):
        if self.color == "yellow" and self.ball == False:
            self.surf = pygame.image.load("images/goolkeeper_2.png").convert()
        elif self.color == "blue" and self.ball == False:
            self.surf = pygame.image.load("images/goolkeeper_1.png").convert()
        elif self.color == "yellow" and self.ball:
            self.surf = pygame.image.load("images/goolkeeper_goal_1.png").convert()
        elif self.color == "blue" and self.ball:
            self.surf = pygame.image.load("images/goolkeeper_goal_2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)


# Define the ball object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'ball'
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.image.load("images/ball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=((SCREEN_WIDTH/2),SCREEN_HEIGHT/2))


    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, positions):
        self.rect.move_ip(positions)

    def hide_ball(self):
        self.surf = pygame.image.load("images/hideball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

    def unhide_ball(self):
        self.surf = pygame.image.load("images/ball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

class SoccerGate(pygame.sprite.Sprite):
    def __init__(self,position_x, position_y):
        super(SoccerGate, self).__init__()
        self.surf = pygame.image.load("images/soccergate.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(position_x, position_y, 50, 150)
        self.ball = False

    def has_ball(self, has):
        if has:
            self.surf = pygame.image.load("images/goalgate.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if not has:
            self.surf = pygame.image.load("images/soccergate.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)


class GoalAreaBlue(pygame.sprite.Sprite):
    def __init__(self):
        super(GoalAreaBlue, self).__init__()
        self.surf = pygame.image.load("images/goalfiled.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(SCREEN_WIDTH-(160+50), SCREEN_HEIGHT/2-325/2, 162, 325)

class GoalAreaYellow(pygame.sprite.Sprite):
    def __init__(self):
        super(GoalAreaYellow, self).__init__()
        self.surf = pygame.image.load("images/goalfiled.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(50, SCREEN_HEIGHT/2-325/2, 162, 325)


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("images/soccer_field.jpeg").convert()
# Create a custom event for adding a new ball
ADDBALL = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBALL, 250)



# Instantiate player. Right now, this is just a rectangle.
yellow_one = Player("yellow_one", "yellow", 440, 240)
yellow_two = Player("yellow_two","yellow", 390, 375)
yellow_three = Player("yellow_three","yellow", 390, 95)
yellow_four = Player("yellow_four","yellow", 255, 130)
yellow_five = Player("yellow_five","yellow", 255, 330)
yellow_goalkeeper = PlayerGoalKeeper("yellow",50, 240)

blue_one = Player("blue_one","blue", 615, 240)
blue_two = Player("blue_two","blue", 670, 100)
blue_three = Player("blue_three","blue", 670, 375)
blue_four = Player("blue_four","blue", 805, 130)
blue_five = Player("blue_five","blue", 805, 330)
blue_goalkeeper = PlayerGoalKeeper("blue", 1005, 240)

new_ball = Ball()
blue_gate = SoccerGate(SCREEN_WIDTH-50, SCREEN_HEIGHT/2-150/2)
yellow_gate = SoccerGate(0, SCREEN_HEIGHT/2-150/2)
goal_area_yellow = GoalAreaYellow()
goal_area_blue = GoalAreaBlue()

# Create groups to hold enemy sprites and all sprites
# - ball is used for collision detection and position updates
# - all_sprites is used for rendering
ball = pygame.sprite.Group()
yellow_team = pygame.sprite.Group()
blue_team = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_players = pygame.sprite.Group()
soccer_gates = pygame.sprite.Group()
goal_areas = pygame.sprite.Group()

yellow_team.add(yellow_one)
yellow_team.add(yellow_two)
yellow_team.add(yellow_three)
yellow_team.add(yellow_four)
yellow_team.add(yellow_five)


blue_team.add(blue_one)
blue_team.add(blue_two)
blue_team.add(blue_three)
blue_team.add(blue_four)
blue_team.add(blue_five)


ball.add(new_ball)

soccer_gates.add(blue_gate)
soccer_gates.add(yellow_gate)

goal_areas.add(goal_area_yellow)
goal_areas.add(goal_area_blue)

all_players.add(blue_team)
all_players.add(yellow_team)
all_sprites.add(yellow_one)
all_sprites.add(yellow_two)
all_sprites.add(yellow_three)
all_sprites.add(yellow_four)
all_sprites.add(yellow_five)
all_sprites.add(yellow_goalkeeper)

all_sprites.add(blue_one)
all_sprites.add(blue_two)
all_sprites.add(blue_three)
all_sprites.add(blue_four)
all_sprites.add(blue_five)
all_sprites.add(blue_goalkeeper)

all_sprites.add(blue_gate)
all_sprites.add(yellow_gate)


# Setup the clock for a decent framerate
clock = pygame.time.Clock()

def reset():

    yellow_one.rect[0] = 440
    yellow_one.rect[1] = 240
    yellow_two.rect[0] = 390
    yellow_two.rect[1] = 375
    yellow_three.rect[0] = 390
    yellow_three.rect[1] = 95
    yellow_four.rect[0] = 255
    yellow_four.rect[1] = 130
    yellow_five.rect[0] = 255
    yellow_five.rect[1] = 330

    blue_one.rect[0] = 615
    blue_one.rect[1] = 240
    blue_two.rect[0] = 670
    blue_two.rect[1] = 100
    blue_three.rect[0] = 670
    blue_three.rect[1] = 375
    blue_four.rect[0] = 805
    blue_four.rect[1] = 130
    blue_five.rect[0] = 805
    blue_five.rect[1] = 330


    yellow_goalkeeper.ball = False
    yellow_goalkeeper.has_ball()
    blue_goalkeeper.ball = False
    blue_goalkeeper.has_ball()

    yellow_gate.has_ball(False)
    blue_gate.has_ball(False)

    new_ball.add(ball)
    new_ball.unhide_ball()

# def get_closest_player(team, player_w_ball):
#     closest_player = ""
#     tmp_distance = 0
#     dist = 999999999999999999999999999
#     for player in team:
#         if player != player_w_ball:
#             tmp_distance = distance.euclidean([player_w_ball.rect[0],player_w_ball.rect[1]],
#                                               [player.rect[0],player.rect[1]])
#         else:
#             continue
#         if tmp_distance < dist:
#             dist = tmp_distance
#             closest_player = player
#
#     return closest_player

def get_random_other_player_his_team(team):
    return random.choice(list(team))


def handle_players_collision(player_w_ball, team_wo_ball, team_w_ball):
    action_number = random.randint(0, 2)
    for player_wo_ball in team_wo_ball:
        if pygame.sprite.collide_rect(player_w_ball, player_wo_ball):
            fg = all_data
            if action_number == 1:
                teammate = get_random_other_player_his_team(team_w_ball)
                #closest_player = get_closest_player(team_w_ball, player_w_ball)
                player_w_ball.ball = False
                teammate.ball = True
                teammate.has_ball()
                player_w_ball.has_ball()
            elif action_number == 2:
                player_w_ball.ball = False
                player_wo_ball.ball = True
                player_wo_ball.has_ball()
                player_w_ball.has_ball()
            break

def who_has_ball(all_players, yellow_team, blue_team):
    team_wo_ball = ""
    team_w_ball = ""
    player_w_ball = ""
    for player in all_players:
        if player.ball:
            player_w_ball = player

    if player_w_ball in yellow_team:
        team_wo_ball = blue_team
        team_w_ball = yellow_team
    else:
        team_wo_ball = yellow_team
        team_w_ball = blue_team

    return player_w_ball, team_wo_ball, team_w_ball

# def move_players_to_enemy_gate(b_team, y_team, b_gate, y_gate, team_ball):
#     for player in y_team:
#         if player in team_ball:
#             a = "1" + (len(str(abs(player.rect[0] - b_gate.rect[0])))-1)*"0"
#             b = "1" + (len(str(abs(player.rect[1] - b_gate.rect[1])))-1)*"0"
#             pos_x = (b_gate.rect[0]- player.rect[0]) / (int(a)+10)
#             pos_y = (b_gate.rect[1]- player.rect[1]) / (int(b)+10)
#             player.move_to((pos_x, pos_y))
#     for player in b_team:
#         if player in team_ball:
#             a = "1" + (len(str(abs(player.rect[0] - y_gate.rect[0])))-1)*"0"
#             b = "1" + (len(str(abs(player.rect[1] - y_gate.rect[1])))-1)*"0"
#             pos_x = (y_gate.rect[0]- player.rect[0]) / (int(a)+10)
#             pos_y = (y_gate.rect[1]- player.rect[1]) / (int(b)+10)
#             player.move_to((pos_x, pos_y))


def check_goal(team_w_ball):
    for player in team_w_ball:
        if player.color == "yellow":
            goal_area = goal_area_blue
            goal_keeper = blue_goalkeeper
            gate = blue_gate
        elif player.color == "blue":
            goal_area = goal_area_yellow
            goal_keeper = yellow_goalkeeper
            gate = yellow_gate
        if pygame.sprite.collide_rect(player, goal_area) and player.ball:
            n = random.randint(0, 1)
            player.ball = False
            player.has_ball()

            if n == 0 and blue_gate.ball != True:
                goal_keeper.ball = True
                goal_keeper.has_ball()
            elif n == 1 and goal_keeper.ball != True:
                gate.has_ball(True)

            reset()

# def catch_ball_first(player_w_ball):
#     if not player_w_ball:
#         n = random.randint(10,70)
#         pos_x_to_blue = (new_ball.rect[0] - blue_one.rect[0])/n
#         pos_y_to_blue = (new_ball.rect[1] - blue_one.rect[1])/n
#         pos_x_to_yellow = (new_ball.rect[0] - yellow_one.rect[0])/n
#         pos_y_to_yellow = (new_ball.rect[1] - yellow_one.rect[1])/n
#         blue_one.move_to((pos_x_to_blue, pos_y_to_blue ))
#         yellow_one.move_to((pos_x_to_yellow, pos_y_to_yellow ))

def conversion_data_to_dict(blue_team, yellow_team, ball, yellow_goalarea,
                            blue_goalarea, blue_gate, yellow_gate,
                            player_w_ball):
    global all_data

    player_with_ball = get_player_with_ball_to_dict(player_w_ball)
    ball_dict = {"position_x": ball.rect[0],
                         "position_y": ball.rect[1]}
    blue_goalarea_dict = {"position_x": blue_goalarea.rect[0],
                          "position_y": blue_goalarea.rect[1]}
    yellow_goalarea_dict = {"position_x": yellow_goalarea.rect[0],
                          "position_y": yellow_goalarea.rect[1]}
    blue_gate_dict = {"position_x": blue_gate.rect[0],
                       "position_y": blue_gate.rect[1],
                       "ball": blue_gate.ball}
    yellow_gate_dict = {"position_x": yellow_gate.rect[0],
                       "position_y": yellow_gate.rect[1],
                       "ball": yellow_gate.ball}

    yellow_team_dict = create_dict_from_team_sprite(yellow_team)
    blue_team_dict = create_dict_from_team_sprite(blue_team)

    all_data={"yellow_team": yellow_team_dict, "blue_team": blue_team_dict,
            "ball": ball_dict, "blue_goalarea":blue_goalarea_dict,
            "yellow_goalarea":yellow_goalarea_dict, "blue_gate": blue_gate_dict,
            "yellow_gate": yellow_gate_dict, "player_with_ball": player_with_ball}

def get_player_with_ball_to_dict(player_w_ball):
    player_with_ball = {}
    if player_w_ball:
        player_with_ball["name"] = player_w_ball.name
        player_with_ball["color"] = player_w_ball.color
        player_with_ball["ball"] = player_w_ball.ball
        player_with_ball["position_x"] = player_w_ball.rect[0]
        player_with_ball["position_y"] = player_w_ball.rect[1]
    else:
        player_with_ball["name"] = None
        player_with_ball["color"] = None
        player_with_ball["ball"] = None
        player_with_ball["position_x"] = None
        player_with_ball["position_y"] = None

    return player_with_ball

def create_dict_from_team_sprite(team):
    team_dict = {}
    for player in team:
        player_dict = {}
        id = player.name
        player_dict["color"] = player.color
        player_dict["ball"] = player.ball
        player_dict["position_x"] = player.rect[0]
        player_dict["position_y"] = player.rect[1]
        team_dict[id] = player_dict

    return team_dict



def update_team_states(team, team_color):
    for player, player_dict in zip(team, all_data[team_color]):
        player.rect[0] = all_data[team_color][player_dict]["position_x"]
        player.rect[1] = all_data[team_color][player_dict]["position_y"]
        player.ball = all_data[team_color][player_dict]["ball"]

# Variable to keep the main loop running
running = True

host = '127.0.0.1'                                                      #LocalHost
port = 7976                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

def handle(client):

    global all_data
    a = all_data
    a = json.dumps(a)
    a = bytes(a, 'UTF-8')
    client[0].send(a)

    x = all_data
    message = client[0].recv(5000)
    all_data = json.loads(message)
    to_send = json.dumps(all_data)
    to_send = bytes(to_send, 'UTF-8')
    client[1].send(to_send)

    message = client[1].recv(5000)
    all_data = json.loads(message)


clients = []


def main():
    ez = False
    running = True
    first_run = True
    # Main loop
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        screen.blit(background_image, [0, 0])
        screen.blit(new_ball.surf, new_ball.rect)

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        for entity in goal_areas:
            screen.blit(entity.surf, entity.rect)

        player_w_ball, team_wo_ball, team_w_ball = who_has_ball(all_players, yellow_team, blue_team)


        conversion_data_to_dict(blue_team, yellow_team, new_ball,
                                goal_area_yellow, goal_area_blue,
                                blue_gate, yellow_gate, player_w_ball)
        handle(clients)
        update_team_states(yellow_team, "yellow_team")
        update_team_states(blue_team, "blue_team")

        if first_run:
            conversion_data_to_dict(blue_team, yellow_team, new_ball,
                                    goal_area_yellow, goal_area_blue,
                                    blue_gate, yellow_gate, player_w_ball)
            first_run = False

        #catch_ball_first(player_w_ball)
        check_goal(team_w_ball)
        if player_w_ball:
            handle_players_collision(player_w_ball, team_wo_ball, team_w_ball)
            # closest_player = get_closest_player(team_wo_ball, player_w_ball)
            # n = random.randint(10,30)
            # pos_x = (player_w_ball.rect[0] - closest_player.rect[0])/n
            # pos_y = (player_w_ball.rect[1] - closest_player.rect[1])/n
            # closest_player.move_to((pos_x,pos_y))
            # move_players_to_enemy_gate(blue_team, yellow_team, blue_gate, yellow_gate, team_w_ball)

        if pygame.sprite.spritecollideany(yellow_one, ball):
            # If so, then remove the player and stop the loop
            yellow_one.ball = True
            yellow_one.has_ball()
            new_ball.hide_ball()
            new_ball.remove(ball)



        # Check if any ball have collided with the player
        if pygame.sprite.spritecollideany(blue_one, ball):
            # If so, then remove the player and stop the loop
            blue_one.ball = True
            blue_one.has_ball()
            new_ball.hide_ball()
            new_ball.remove(ball)

            # Update the display
        pygame.display.flip()
        # Ensure program maintains a rate of 30 frames per second
        clock.tick(25)

while True:
    client, address = server.accept()
    print("Connected with {}".format(str(address)))
    clients.append(client)
    if len(clients) == 2:
        main()

