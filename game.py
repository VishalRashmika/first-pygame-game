# game

import pygame
from sys import exit

# initialize pygame
pygame.init()

# screen size
screen = pygame.display.set_mode((576,400))

# title
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()

# sky and ground surfaces
ground_surface = pygame.image.load('assets/background/ground.png').convert_alpha()
sky_surface = pygame.image.load('assets/background/sky.png').convert_alpha()

# "My Game" font
test_font = pygame.font.Font('assets/fonts/font1.ttf', 25)
text_surface = test_font.render('My Runner Game', False, 'Blue')
text_rectangle = text_surface.get_rect(midtop = (288,50))

# enemy
enemy_image = pygame.image.load('assets/characters/enemy/enemy.png').convert_alpha()
enemy_recatngle = enemy_image.get_rect(midbottom = (576,324))

# Player
player_surface = pygame.image.load('assets/characters/player/player.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (100,324))

player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rectangle.bottom >= 324: # check whether the player is in the ground and the space key is pressed
                player_gravity = -20


        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rectangle.collidepoint((event.pos)) and player_rectangle.bottom >= 324: # check whether the mouse touches the player and player is in the ground
                player_gravity = -20

        if event.type == pygame.KEYUP: # triggers when a pressed key is released
            print("key Up")


    # display the sky and the ground
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,76)) # (400-324)

    # display the text
    pygame.draw.rect(screen, 'Pink', text_rectangle)
    pygame.draw.rect(screen, 'Pink', text_rectangle,20)
    screen.blit(text_surface, text_rectangle)

    # animation of enemy
    screen.blit(enemy_image, enemy_recatngle)
    enemy_recatngle.right -= 4
    if enemy_recatngle.right <= 0:
        enemy_recatngle.right = 590


    # player
    player_gravity += 1
    player_rectangle.y += player_gravity

    # Creating the floor
    if player_rectangle.bottom >= 324: player_rectangle.bottom = 324

    # displaying the player
    screen.blit(player_surface, player_rectangle)



    pygame.display.update()
    clock.tick(60)
