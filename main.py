import pygame
import random
import math
from pygame import mixer

# initialise the game
pygame.init()

# create the screen (width and height)
screen = pygame.display.set_mode((800, 600))
running = True
# background
background = pygame.image.load('RE.png')
# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)  # plays on loop because of -1 value
# caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("player.png")
playerX = 370  # x-coordinate
playerY = 480  # y -coordinate
playerX_Change = 0
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("Invader (2).png"))
    enemyX.append(random.randint(0, 735))  # x-coordinate
    enemyY.append(random.randint(50, 150))  # y -coordinate
    enemyX_Change.append(4)
    enemyY_Change.append(40)
# Bullet
# Ready - Cant see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("003-bullet.png")
bulletX = 0  # x-coordinate
bulletY = 480  # y -coordinate
bulletX_Change = 0  # no movement in x direction
bulletY_Change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 72)


def player(x, y):
    # blit used to draw the image on the screen
    screen.blit(playerImg, (x, y))  # drawing the image


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # appears on the center of the spaceship


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def iscollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow((enemy_x - bullet_x), 2) + math.pow((enemy_y - bullet_y), 2))
    if distance < 27:
        return True
    else:
        return False


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# events in the window
while running:
    # rgb values 0-255
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0
    # checking boundaries of the players
    playerX += playerX_Change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # checking boundary of the enemy

    for i in range(num_of_enemies):
        # GAME OVER
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = 4
            enemyY[i] += enemyY_Change[i]
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -4
            enemyX[i] = 736
            enemyY[i] += enemyY_Change[i]

            # Collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # enemy will reset to a random position after being hit
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    show_score(textX, textY)
    # display needs to be updated
    pygame.display.update()