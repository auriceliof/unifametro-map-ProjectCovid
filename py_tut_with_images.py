# IMPORTS ######################################################
import pygame
import random
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

# IMPORTS ######################################################

# VARIABLES ####################################################

PLAYER_IMG = "boneco_covid.png"
ENEMY_IMG = "covid.png"
CLOUD_IMG = "cloud.png"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_SKY = 135, 206, 250
TIME_ENEMY = 500
TIME_CLOUD = 500
MUSIC = "Guns_N_Roses-Sweet_Child_Of_Mine.mp3"
SOUND_MOVE_UP = "Rising_putter.ogg"
VOLUME_MOVE_UP = 1.5
SOUND_MOVE_DOWN = "Falling_putter.ogg"
VOLUME_MOVE_DOWN = 1.5
SOUND_COLLISION = "Collision.ogg"
VOLUME_COLLISION = 1.5
SPEED_HERO = 50
SPEED_COVID_1 = 5
SPEED_COVID_2 = 20

# VARIABLES ####################################################

# STARTUP ######################################################

pygame.init()

# Setup for sounds, defaults are good
pygame.mixer.init()

# Set up the font
pygame.font.init()
font = pygame.font.Font(None, 30)

# STARTUP ######################################################

# PLAYER ###########################################################
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(PLAYER_IMG).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
# PLAYER ###########################################################

# ENEMY ############################################################
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(ENEMY_IMG).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(SPEED_COVID_1, SPEED_COVID_2)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
# ENEMY ############################################################

# CLOUD ############################################################
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(CLOUD_IMG).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
# CLOUD ############################################################

# GAME #############################################################
# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, TIME_ENEMY)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, TIME_CLOUD)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Load all our sound files
move_up_sound = pygame.mixer.Sound(SOUND_MOVE_UP)
move_down_sound = pygame.mixer.Sound(SOUND_MOVE_DOWN)
collision_sound = pygame.mixer.Sound(SOUND_COLLISION)

# Set the base volume for all sounds
move_up_sound.set_volume(VOLUME_MOVE_UP)
move_down_sound.set_volume(VOLUME_MOVE_DOWN)
collision_sound.set_volume(VOLUME_COLLISION)

# Variable to keep our main loop running
running = False

# Our main loop
while not running:
    # Look at every event in the queue
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = True
        elif event.type == QUIT:
            running = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                running = True

    screen.fill(COLOR_SKY)

# FIRST SCREEN #############################################################

    # Draw "MENSAGE"
    pygame.mixer.music.stop()
    screen.fill('black')
    game = font.render("VAMOS INICIAR O COMBATE À COVID", True, ('Red'))
    game_rect = game.get_rect(center=(210, 60))
    screen.blit(game, game_rect.center)

    # Draw "START" button
    start_button_text = font.render("  <  START  >  ", True, (0, 0, 0), ('#218c74'))
    start_button_rect = start_button_text.get_rect(center=(400, 300))
    screen.blit(start_button_text, start_button_rect.topleft)
    pygame.display.flip()


# FIRST SCREEN #############################################################

# Load and play our background music
pygame.mixer.music.load(MUSIC)
pygame.mixer.music.play(loops=-1)

# Restart the clock for the main game loop
clock = pygame.time.Clock()

# Variable to keep our main loop running
running = True

# Our main loop
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            # Create a new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            # Create a new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update enemy and cloud positions
    enemies.update()
    clouds.update()

    # Fill the screen with the background color
    screen.fill(COLOR_SKY)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        pygame.mixer.music.stop()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        #running = False

        game_over = font.render("GAME OVER!!!", True, ('Red'))
        game_rect = game_over.get_rect(center=(210, 100))
        screen.blit(game_over, game_rect.center)

    # Update the display
    pygame.display.flip()

    # Ensure the program maintains a rate of 30 frames per second
    clock.tick(30)

# All done! Stop the music and quit the game
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()

# GAME #############################################################