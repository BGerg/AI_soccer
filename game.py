# Import the pygame module
import time

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

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self,player_color, player_posx, player_posy):
        super(Player, self).__init__()
        self.player_color = player_color
        if self.player_color == "blue":
            self.surf = pygame.image.load("player_blue.png").convert()
        elif self.player_color == "yellow":
            self.surf = pygame.image.load("player_yellow.png").convert()
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

    def move_to(self, ball_pos):
        self.rect.move_ip(ball_pos)

    def has_ball(self):
        if self.player_color == "yellow" and self.ball == False:
            self.surf = pygame.image.load("player_yellow.png").convert()
        elif self.player_color == "blue" and self.ball == False:
            self.surf = pygame.image.load("player_blue.png").convert()
        elif self.player_color == "yellow" and self.ball:
            self.surf = pygame.image.load("player_yellow_w_ball.png").convert()
        elif self.player_color == "blue" and self.ball:
            self.surf = pygame.image.load("player_blue_w_ball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)



# Define the ball object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'ball'
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.image.load("ball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=((SCREEN_WIDTH/2),SCREEN_HEIGHT/2))


    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, positions):
        self.rect.move_ip(positions)

    def hide_ball(self):
        self.surf = pygame.image.load("hideball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

    def unhide_ball(self):
        self.surf = pygame.image.load("ball.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

class SoccerGate(pygame.sprite.Sprite):
    def __init__(self, position_x, position_y):
        super(SoccerGate, self).__init__()
        self.surf = pygame.image.load("soccergate.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(position_x, position_y, 50, 150)
        self.ball = False

    def has_ball(self, has):
        if has:
            self.surf = pygame.image.load("goalgate.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if not has:
            self.surf = pygame.image.load("soccergate.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)


class GoalAreaBlue(pygame.sprite.Sprite):
    def __init__(self):
        super(GoalAreaBlue, self).__init__()
        self.surf = pygame.image.load("goalfiled.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(SCREEN_WIDTH-(160+50), SCREEN_HEIGHT/2-325/2, 162, 325)

class GoalAreaYellow(pygame.sprite.Sprite):
    def __init__(self):
        super(GoalAreaYellow, self).__init__()
        self.surf = pygame.image.load("goalfiled.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = pygame.Rect(50, SCREEN_HEIGHT/2-325/2, 162, 325)

def get_closest_player(team, player_w_ball):
    closest_player = ""
    tmp_distance = 0
    distance = 999999999999999999999999999
    for player in team:
        if player != player_w_ball:
            tmp_distance = abs(player_w_ball.rect[0]-player.rect[0])\
                           +abs(player_w_ball.rect[1]-player.rect[1])
        else:
            continue
        if tmp_distance < distance:
            distance = tmp_distance
            closest_player = player

    return closest_player


def handle_players_collision(player_w_ball, team_wo_ball, team_w_ball):
    action_number = random.randint(0, 2)
    for player_wo_ball in team_wo_ball:
        if pygame.sprite.collide_rect(player_w_ball, player_wo_ball):
            #if action_number == 0:
             #   pass
            if action_number == 1:
                closest_player = get_closest_player(team_w_ball, player_w_ball)
                player_w_ball.ball = False
                closest_player.ball = True
                closest_player.has_ball()
                player_w_ball.has_ball()
            elif action_number == 2:
                player_w_ball.ball = False
                player_wo_ball.ball = True
                player_wo_ball.has_ball()
                player_w_ball.has_ball()
            break

def who_has_ball(all_players, yellow_team, blue_team, gates):
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

def move_players_to_enemy_gate(b_team, y_team, b_gate, y_gate, team_ball):
    for player in y_team:
        if player in team_ball:
            a = "1" + (len(str(abs(player.rect[0] - b_gate.rect[0])))-1)*"0"
            b = "1" + (len(str(abs(player.rect[1] - b_gate.rect[1])))-1)*"0"
            pos_x = (b_gate.rect[0]- player.rect[0]) / (int(a)+10)
            pos_y = (b_gate.rect[1]- player.rect[1]) / (int(b)+10)
            player.move_to((pos_x, pos_y))
    for player in b_team:
        if player in team_ball:
            a = "1" + (len(str(abs(player.rect[0] - y_gate.rect[0])))-1)*"0"
            b = "1" + (len(str(abs(player.rect[1] - y_gate.rect[1])))-1)*"0"
            pos_x = (y_gate.rect[0]- player.rect[0]) / (int(a)+10)
            pos_y = (y_gate.rect[1]- player.rect[1]) / (int(b)+10)
            player.move_to((pos_x, pos_y))



# Setup for sounds. Defaults are good.
#pygame.mixer.init()

# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("soccer_field.jpeg").convert()
# Create a custom event for adding a new ball
ADDBALL = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBALL, 250)



# Instantiate player. Right now, this is just a rectangle.
yellow_one = Player("yellow", 440, 240)
yellow_two = Player("yellow", 390, 375)
yellow_three = Player("yellow", 390, 95)
yellow_four = Player("yellow", 255, 130)
yellow_five = Player("yellow", 255, 330)
yellow_goalkeeper = Player("yellow", 55, 240)

blue_one = Player("blue", 615, 240)
blue_two = Player("blue", 670, 100)
blue_three = Player("blue", 670, 375)
blue_four = Player("blue", 805, 130)
blue_five = Player("blue", 805, 330)
blue_goalkeeper = Player("blue", 1005, 240)

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
    yellow_goalkeeper.rect[0] = 55
    yellow_goalkeeper.rect[1] = 240

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
    blue_goalkeeper.rect[0] = 1005
    blue_goalkeeper.rect[1] = 240

    yellow_goalkeeper.ball = False
    yellow_goalkeeper.has_ball()
    blue_goalkeeper.ball = False
    blue_goalkeeper.has_ball()

    yellow_gate.has_ball(False)
    blue_gate.has_ball(False)

    new_ball.add(ball)
    new_ball.unhide_ball()
# Variable to keep the main loop running
running = True


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

    # Get the set of keys pressed and check for user input
    #pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    #yellow_one.update(pressed_keys)
    # Update ball position


    screen.blit(background_image, [0, 0])
    # Draw the player on the screen
    screen.blit(yellow_one.surf, yellow_one.rect)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)


    screen.blit(new_ball.surf, new_ball.rect)

    for entity in goal_areas:
        screen.blit(entity.surf, entity.rect)

    player_w_ball, team_wo_ball, team_w_ball = who_has_ball(all_players,yellow_team, blue_team, blue_gate)
    if not player_w_ball:
        n = random.randint(10,70)
        pos_x_to_blue = (new_ball.rect[0] - blue_one.rect[0])/n
        pos_y_to_blue = (new_ball.rect[1] - blue_one.rect[1])/n
        pos_x_to_yellow = (new_ball.rect[0] - yellow_one.rect[0])/n
        pos_y_to_yellow = (new_ball.rect[1] - yellow_one.rect[1])/n
        blue_one.move_to((pos_x_to_blue, pos_y_to_blue ))
        yellow_one.move_to((pos_x_to_yellow, pos_y_to_yellow ))

    for player in team_w_ball:
        if pygame.sprite.collide_rect(player, goal_area_blue)  and player.ball:
            n = random.randint(0, 1)
            player.ball = False
            player.has_ball()

            if n == 0 and blue_gate.ball != True:
                blue_goalkeeper.ball = True
                blue_goalkeeper.has_ball()
            elif n == 1 and blue_goalkeeper.ball != True:
                blue_gate.has_ball(True)

            reset()

    for player in team_w_ball:
        if pygame.sprite.collide_rect(player, goal_area_yellow)  and player.ball:
            n = random.randint(0, 1)
            player.ball = False
            player.has_ball()

            if n == 0 and blue_gate.ball != True:
                yellow_goalkeeper.ball = True
                yellow_goalkeeper.has_ball()
            elif n == 1 and yellow_goalkeeper.ball != True:
                yellow_gate.has_ball(True)

            reset()


    if player_w_ball:
        handle_players_collision(player_w_ball, team_wo_ball, team_w_ball)
        closest_player = get_closest_player(team_wo_ball, player_w_ball)
        n = random.randint(10,30)
        pos_x = (player_w_ball.rect[0] - closest_player.rect[0])/n
        pos_y = (player_w_ball.rect[1] - closest_player.rect[1])/n
        closest_player.move_to((pos_x,pos_y))
        move_players_to_enemy_gate(blue_team, yellow_team, blue_gate, yellow_gate, team_w_ball)



    if pygame.sprite.spritecollideany(yellow_one, ball):
        # If so, then remove the player and stop the loop
        yellow_one.ball = True
        yellow_one.has_ball()
        new_ball.hide_ball()
        new_ball.remove(ball)

    # Check if any ball have collided with the player
    if pygame.sprite.spritecollideany(blue_one, ball):
        # If so, then remove the player and stop the loop
        yellow_one.ball = True
        yellow_one.has_ball()
        new_ball.hide_ball()
        new_ball.remove(ball)

    # Update the display
    pygame.display.flip()
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
