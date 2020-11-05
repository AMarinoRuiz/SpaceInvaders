import pygame
import random
import math
import sys
import os

global laserX
#test para git
#initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((800,600))

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo_icon.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('background.jpg')

#Player 
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerX_vel = 3

#laser 
laserImg_start = pygame.image.load('laser.png')
laserImg_beam = pygame.image.load('laser2.png')
laserX = playerX
laserY = 480
laserY_change = 0
laserY_vel = 8
laser_state = 'ready'

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyX_vel = []
enemyY_change = []
enemyX_start = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('enemy.png'))
	enemyX.append(random.randint(15,721))
	enemyY.append(random.randint(0,100))
	enemyX_vel.append(2)
	enemyY_change.append(0)
	enemyX_start.append(random.randint(1,10))
	if enemyX_start[i]>5:
		enemyX_change.append(enemyX_vel[i])
	else:
		enemyX_change.append(-enemyX_vel[i])

#score
score = 0
font = pygame.font.Font('freesansbold.ttf',32)

#game over font
over_font = pygame.font.Font('freesansbold.ttf',64)


textX = 10
textY = 10

def gameOver():
	over_text = over_font.render('GAME OVER',True,(255,60,50))
	screen.blit(over_text,(200,200))

def showScore(x,y):
	score_value = font.render("Score: {}".format(score),True,(50,255,50))
	screen.blit(score_value,(x,y))

def player(x,y):
	screen.blit(playerImg,(x,y))

def enemy(x,y,i):
	screen.blit(enemyImg[i],(x,y))

def fireLaser(x,y):
	global laser_state
	
	laserX = x
	laser_state = 'fire'
	if y==480:
		screen.blit(laserImg_start,(x+16,480-10))
	elif y>=460 and y<=480:
		screen.blit(laserImg_start,(x+16,480-10))
		screen.blit(laserImg_beam,(x+32,y+10))
	else:
		screen.blit(laserImg_beam,(x+32,y+10))

def isCollision(laserX,laserY,enemyX,enemyY):
	distance = math.sqrt((enemyX-laserX)**2 + (enemyY-laserY)**2)
	return distance < 27

#game loop
running = True
while running:
	screen.fill((0,0,0))
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False  #closes when pressing X on the window
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change -= playerX_vel
			if event.key == pygame.K_RIGHT:
				playerX_change += playerX_vel
			if event.key == pygame.K_SPACE and laser_state == 'ready':
				laserX = playerX
				fireLaser(laserX,laserY)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0

	#laser movement
	if laser_state == 'fire':
		laserY -= laserY_vel
		fireLaser(laserX,laserY)
	if laserY <= 0:
		laserY = 480
		laser_state = 'ready'
		
	playerX += playerX_change
	if playerX <= 15:
		playerX = 15
	if playerX >= 721:
		playerX = 721

	for i in range(num_of_enemies):
		enemyX[i] += enemyX_change[i]
		enemyY[i] += enemyY_change[i]
		if enemyX[i] <= 15:
			enemyX_change[i] = enemyX_vel[i]
			enemyY[i] += 30
		if enemyX[i] >= 721:
			enemyX_change[i] = -enemyX_vel[i]
			enemyY[i] += 30
		#Colision
		collision = isCollision(laserX,laserY,enemyX[i],enemyY[i])

		if enemyY[i] > 440:
			enemyY = [2000] * num_of_enemies #los saco de la pantalla
			playerX = 2000
			playerY = 2000
			gameOver()
			break

		if collision:
			laserY = 480
			laser_state = 'ready'
			score +=1
			enemyX[i] = random.randint(15,721)
			enemyY[i] = random.randint(0,100)
			enemyX_vel[i] = 2 * (1+7/100*score)
			enemyX_start[i] = random.randint(1,10)
			if enemyX_start[i]>5:
				enemyX_change[i] = (enemyX_vel[i])
			else:
				enemyX_change[i] = (-enemyX_vel[i])			

		enemy(enemyX[i],enemyY[i],i)

	player(playerX,playerY)
	showScore(textX,textY)

	pygame.display.update()
