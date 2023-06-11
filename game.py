#game

import pygame
from sys import exit
import random

# initialize pygame
pygame.init()

# screen size
screen = pygame.display.set_mode((576,400))

game_active = False

# title
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()

# sky and ground surfaces
ground_surface = pygame.image.load('assets/background/ground.png').convert_alpha()
sky_surface = pygame.image.load('assets/background/sky.png').convert_alpha()

# "My Game" font
test_font = pygame.font.Font('assets/fonts/font1.ttf', 25)

# text for the Intro Screen
text_surface = test_font.render('My Runner Game', False, 'Black')
text_rectangle = text_surface.get_rect(midtop = (288,50))
text_surface_2 = test_font.render('press space to start', False, 'Black')
text_rectangle_2 = text_surface_2.get_rect(midtop = (288, 300))

# displaying score
start_time = 0
def display_score(x, y):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'SCORE : {current_time}', False, 'Blue')
    score_rectangle = score_surface.get_rect(midtop = (x,y))
    screen.blit(score_surface,score_rectangle)
    return current_time

# obstacles
## Enemy
enemy_image = pygame.image.load('assets/characters/enemy/enemy.png').convert_alpha()
enemy_recatngle = enemy_image.get_rect(midbottom = (576,324))

enemy_surface_2 = pygame.image.load('assets/characters/enemy/enemy2.png')
#enemy_rectangle_2 = enemy_surface_2.get_rect(midbottom = (576))

# obstacle rectangle list
obstacles_rect_list = []


# Player
player_surface = pygame.image.load('assets/characters/player/player.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (100,324))

# Intro Screen
player_stand = pygame.image.load('assets/characters/player/player.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand.get_rect(midtop = (288, 110))

# Other Variables
player_gravity = 0
score = 0

# Timers
## Creating Custom User Events
obstacle_timer = pygame.USEREVENT + 1
## Trigger The Created Event In Certain Intervals
pygame.time.set_timer(obstacle_timer, 1500)

def obstacle_movement(obstacle_list):
    if obstacle_list: # returns False if the list is empty
        for obstacle_rectangle in obstacle_list:
            obstacle_rectangle.x -= 5

            # logic for displaying different types of obstacles
            if obstacle_rectangle.bottom == 324:
                screen.blit(enemy_image, obstacle_rectangle)
            else:
                screen.blit(enemy_surface_2,obstacle_rectangle)

        # copy the list only if the x value is greater than -100
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collissions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

while True:
    for event in pygame.event.get():
        # code to exit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 324: # check whether the player is in the ground and the space key is pressed
                    player_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint((event.pos)) and player_rectangle.bottom >= 324: # check whether the mouse touches the player and player is in the ground
                    player_gravity = -20

            if event.type == pygame.KEYUP: # triggers when a pressed key is released
                print("key Up")

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    enemy_recatngle.right = 590
                    start_time = int(pygame.time.get_ticks() / 1000) # resets the time when space is pressed to restart the game

        # Timer Event
        if event.type == obstacle_timer and game_active:
            if random.randint(0,2): # if 1 --> TRUE
                obstacles_rect_list.append(enemy_image.get_rect(midbottom = (random.randint(576,1075),324)))
            else:
                obstacles_rect_list.append(enemy_surface_2.get_rect(midbottom = (random.randint(576,1075),250)))

    if game_active:
        # display the sky and the ground
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,76)) # (400-324)

        # display the score
        score = display_score(288,50)

        # player
        player_gravity += 1
        player_rectangle.y += player_gravity

        #obstacle movement
        obstacles_rect_list = obstacle_movement(obstacles_rect_list)

        # Creating the floor
        if player_rectangle.bottom >= 324: player_rectangle.bottom = 324

        # displaying the player
        screen.blit(player_surface, player_rectangle)

        # player collission
        game_active = collissions(player_rectangle,obstacles_rect_list)

    else:
        # Load Screen Part
        screen.fill((93,129,162))
        screen.blit(player_stand, player_stand_rectangle)
        screen.blit(text_surface, text_rectangle)

        score_message = test_font.render(f'Score : {score}', False, 'Black')
        score_message_rectangle = score_message.get_rect(midtop = (288, 300))

        # Intro Screen Logic
        if score == 0:
            screen.blit(text_surface_2,text_rectangle_2)
        else:
            screen.blit(score_message,score_message_rectangle)
            text_rectangle_2.midtop = (288,350)
            screen.blit(text_surface_2, text_rectangle_2)

        # emptying the obstacles_rect_list after the game is ended
        obstacles_rect_list.clear()

        # put the player on the ground after the game is ended
        player_rectangle.midbottom = (100,324)
        player_gravity = 0 # doesnt fall any further

    pygame.display.update()

    # frames per second (FPS)
    clock.tick(60)
