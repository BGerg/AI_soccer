# Import the pygame module
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
SCREEN_HEIGHT   = 600
SCREEN_WIDTH  = int(1.869*SCREEN_HEIGHT)

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self,player_color):
        super(Player, self).__init__()
        self.player_color = player_color
        if self.player_color == "blue":
            self.surf = pygame.image.load("player_blue.png").convert()
        elif self.player_color == "yellow":
            self.surf = pygame.image.load("player_yellow.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
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


    def has_ball(self):
        if self.player_color == "yellow" and self.ball == False:
            self.surf = pygame.image.load("player_yellow.png").convert()
        elif self.player_color == "blue" and self.ball == False:
            self.surf = pygame.image.load("player_blue.png").convert()
            print("dsfdsf")
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
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self, positions):
        self.rect.move_ip(positions)


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
player_yellow = Player("yellow")
player_blue = Player("blue")
new_ball = Ball()

# Create groups to hold enemy sprites and all sprites
# - ball is used for collision detection and position updates
# - all_sprites is used for rendering
ball = pygame.sprite.Group()
yellow_team = pygame.sprite.Group()
blue_team =  pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

yellow_team.add(player_yellow)
blue_team.add(player_blue)
ball.add(new_ball)

blocks_hit_list = [blue_team]

all_sprites.add(new_ball)
all_sprites.add(player_yellow)
all_sprites.add(player_blue)
# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Load and play background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
# pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
# pygame.mixer.music.play(loops=-1)

# Load all sound files
# Sound sources: Jon Fincher
# move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
# move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
# collision_sound = pygame.mixer.Sound("Collision.ogg")

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
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player_yellow.update(pressed_keys)
    # Update ball position
    new_ball.update((0,0))

    screen.blit(background_image, [0, 0])
    # Draw the player on the screen
    screen.blit(player_yellow.surf, player_yellow.rect)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.collide_rect(player_yellow, player_blue):
        if player_blue.ball:
            player_yellow.ball = True
            player_blue.ball = False
            player_yellow.has_ball()
            player_blue.has_ball()
        elif player_yellow.ball:
            player_blue.ball = True
            player_yellow.ball = False
            player_blue.has_ball()
            player_yellow.has_ball()


    # Check if any ball have collided with the player
    if pygame.sprite.spritecollideany(player_yellow, ball):
        # If so, then remove the player and stop the loop
        player_yellow.ball = True
        player_yellow.has_ball()
        # # Stop any moving sounds and play the collision sound
        # move_up_sound.stop()
        # move_down_sound.stop()
        # collision_sound.play()

    # Check if any ball have collided with the player
    if pygame.sprite.spritecollideany(player_blue, ball):
        # If so, then remove the player and stop the loop
        player_yellow.ball = True
        player_yellow.has_ball()
        # # Stop any moving sounds and play the collision sound
        # move_up_sound.stop()
        # move_down_sound.stop()
        # collision_sound.play()








    # Update the display
    pygame.display.flip()
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

# # At this point, we're done, so we can stop and quit the mixer
# pygame.mixer.music.stop()
# pygame.mixer.quit()