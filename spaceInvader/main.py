"""
Main function for the space pygame
"""
import random
import math
import pygame
from pygame import mixer

# Initialise the pygame
pygame.init()

# create the screen with the width and height
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load('background.png')

# Background Music
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 means play in loop (continuously)

# Title and Icon
pygame.display.set_caption("space Invaders")

# player details
space_invader = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480

playerX_change = 0
playerY_change = 0

# Monster
monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
num_of_monster = 6

# Multiple number of the monsters
for i in range(num_of_monster):
    monsterImg.append(pygame.image.load('monster.png'))
    monsterX.append(random.randint(0, 800))
    monsterY.append(random.randint(50, 200))

    monsterX_change.append(3)
    monsterY_change.append(40)

# Bullet
# ready state of the bullet is that we can't see that
# fire state we can see the bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# score value and font details
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# game over font
over_font = pygame.font.Font('freesansbold.ttf', 64)

textX = 10
textY = 10


def game_over_text():
    """
    rendering the screen for the GAME OVER TEXT and displaying on the screen
    """
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x, y):
    """
    Rendering the screen for score and displaying on the screen
    :param x:  X Coordinate for the score
    :param y: Y coordinate for the score
    """
    score = font.render("Score:   " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    """
    Player appearance in the window
    :return:
    """
    screen.blit(space_invader, (x, y))


def monster(x, y, i):
    """
    monster appearance in the window
    :return:
    """
    screen.blit(monsterImg[i], (x, y))


def fire_bullet(x, y):
    """

    :param x: X coordinate for the bullet
    :param y:  Y coordinate for the bullet
    """
    global bullet_state
    bullet_state = "fire"
    # appear from the center of the spaceship
    screen.blit(bulletImg, (x + 2, y + 5))


def isCollision(monsterX, monsterY, bulletX, bulletY):
    distance = math.sqrt((math.pow(monsterX - bulletX, 2)) + (math.pow(monsterY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Exit window pygame
running = True
# Main loop for the game execution to run the game
while running:

    # RGB colour
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            print("pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Incrementing the player value according to the choice
    playerX += playerX_change
    # Draw the player

    if playerX <= 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768

    player(playerX, playerY)

    # Monster render

    # monster Movement
    for i in range(num_of_monster):

        # Game Over
        if monsterY[i] > 440:
            for j in range(num_of_monster):
                monsterY[j] = 2000
            game_over_text()
            mixer.music.stop()
            break
        monsterX[i] += monsterX_change[i]

        # Monster boundary
        if monsterX[i] <= 0:
            monsterX_change[i] = 3
            monsterY[i] += monsterY_change[i]
        elif monsterX[i] >= 768:
            monsterX_change[i] = -3
            monsterY[i] += monsterY_change[i]

        # Collision
        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            # Repositioning the enemy
            monsterX[i] = random.randint(0, 800)
            monsterY[i] = random.randint(50, 200)

        monster(monsterX[i], monsterY[i], i)

    show_score(textX, textY)
    # Render the display
    pygame.display.update()
