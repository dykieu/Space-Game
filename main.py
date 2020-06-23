import pygame
import os
import random
import math
from os import path
from pygame.locals import *
from pygame import mixer

# Inits pygame module
pygame.init()

# Folder Paths
mainPath = os.path.dirname(__file__)
resourcePath = os.path.join(mainPath, 'resources')
iconPath = os.path.join(resourcePath, 'icon')
shipPath = os.path.join(resourcePath, 'spaceship')
monsterPath = os.path.join(resourcePath, 'monster')
backgroundPath = os.path.join(resourcePath, 'background')
fontPath = os.path.join(resourcePath, 'font')
soundPath = os.path.join(resourcePath,'sound')

# File Names
shipFile = 'ship.png'
iconFile = 'icon.png'
laserFile = 'laser.png'
alienFile = 'alien3.png'
fontFile = 'airstrike.ttf'
explosionSound = 'explosion.wav'
shootingSound = 'laser.wav'
bgmSound = 'bgm.wav'

# Game variables
totalScore = 0
gOver = 'Game Over'
textStyle = pygame.font.Font(os.path.join(fontPath, fontFile), 32)
gOverStyle = pygame.font.Font(os.path.join(fontPath, fontFile), 72)
textPosX = 10
textPosY = 10 
numAliens = 5

# Game Object Speeds
playerLeft = -3
playerRight = 3
playerUP = -5
playerDown = -5
alienLeft = -3
alienRight = 3
alienDown = 60
laserSpeed = 4

# Background music
mixer.music.load(os.path.join(soundPath, bgmSound))
mixer.music.set_volume(.1)
mixer.music.play(-1)

# Inits a game screen (x, y) axis
screen = pygame.display.set_mode((800, 600))

# Game state
gameRunning = True

# Game Window Title
pygame.display.set_caption('Space Invader')

# Game Window Icon
gameIcon = pygame.image.load(os.path.join(iconPath, iconFile))
pygame.display.set_icon(gameIcon)

# Spaceshape Icon (Player)
shipIcon = pygame.image.load(os.path.join(shipPath, shipFile))
shipPosX = 370
shipPosY = 480
playerXChange = 0
playerYChange = 0

# Laser Icon (Loaded = no display, fire = moving)
laserIcon = pygame.image.load(os.path.join(shipPath, laserFile))
laserPosX = 0
laserPosY = 480
laserXChange = 0
laserYchange = laserSpeed
laserState = 'loaded'

# Monster Icon
alienIcon = []
alienPosX = []
alienPosY = []
alienXChange = []
alienYChange = []

for i in range(numAliens):
	alienIcon.append(pygame.image.load(os.path.join(monsterPath, alienFile)))
	alienPosX.append(random.randint(0, 735))
	alienPosY.append(random.randint(0, 50))

	if (random.randint(0, 1) == 1):
		alienXChange.append(alienLeft)
	else:
		alienXChange.append(alienRight)
	alienYChange.append(alienDown)

# Background Image
backgroundImg = pygame.image.load(os.path.join(backgroundPath, 'stars.png'))

# Draw image to screen (receives player movement)
def player(x, y):
	screen.blit(shipIcon, (round(x), round(y)))

# Draw alien to screen
def alien(x, y, i):
	screen.blit(alienIcon[i], (round(x), round(y)))

# Draw lasers to screen
def shootLaser(x, y):
	global laserState
	laserState = 'fire'
	screen.blit(laserIcon, (x + 16, y + 10))

# Alien and bullet collision
def killMob(alienPosX, alienPosY, laserPosX, laserPosY):
	dist = math.sqrt((math.pow(alienPosX - laserPosX, 2)) + (math.pow(alienPosY - laserPosY, 2)))
	if dist < 45:
		return True

	return False

# Displays score
def showScore(x, y):
	score = textStyle.render('Score: ' + str(totalScore), True, (255, 255, 255))
	screen.blit(score, (x, y))

# Game over
def gameOver():
	gOverDisplay = gOverStyle.render(gOver, True, (255, 255, 255))
	screen.blit(gOverDisplay, (190, 250))

# Game Loop (keeps game window open)
while gameRunning:
	# Game Background (rgb)
	screen.fill((0, 0, 0))

	# Draws Background Img (x, y)
	screen.blit(backgroundImg, (0,0))

	# Goes through events that happen inside the game window
	for event in pygame.event.get():
		# Checks for close button (If so, close window)
		if event.type == pygame.QUIT:
			gameRunning = False

		# Check for keystroke down
		if event.type == pygame.KEYDOWN:
			# If [LEFT]
			if event.key == pygame.K_LEFT:
				playerXChange = playerLeft
			# If [Right]
			if event.key == pygame.K_RIGHT:
				playerXChange = playerRight

			if event.key == pygame.K_SPACE:
				if laserState == 'loaded':
					laserPosX = shipPosX
					shootLaser(laserPosX, shipPosY)
					playLaser = mixer.Sound(os.path.join(soundPath, shootingSound))
					playLaser.set_volume(.04)
					playLaser.play()
		# Check for keystroke UP
		if event.type == pygame.KEYUP:
			# If either key is released
			if event.key == pygame.K_LEFT or pygame.K_RIGHT:
				playerXChange = 0

	# Player Movement
	shipPosX += playerXChange
	shipPosY += playerYChange


	# Player boundaries
	if shipPosX < 0:
		shipPosX = 0
	elif shipPosX >= 736:
		shipPosX = 736

	# Monster Movement
	for i in range(numAliens):
		alienPosX[i] += alienXChange[i]

		# Game over state
		if alienPosY[i] > 420:
			# Remove monsters
			for j in range(numAliens):
				alienPosY[j] = 1000
			gameOver()
			break

		# Monster boundaries
		if alienPosX[i] <= 0:
			alienXChange[i] = alienRight
			alienPosY[i] += alienYChange[i]
		elif alienPosX[i] >= 736:
			alienXChange[i] = alienLeft
			alienPosY[i] += alienYChange[i]

		# Laser and Alien Collision
		collision = killMob(alienPosX[i], alienPosY[i], laserPosX, laserPosY)
		if collision == True:
			#collision sound
			playExplosion = mixer.Sound(os.path.join(soundPath, explosionSound))
			playExplosion.play()
			laserPosY = 480
			laserState = 'loaded'
			totalScore += 1

			# Respawn
			alienPosX[i] = random.randint(100, 635)
			alienPosY[i] = random.randint(0, 50)

		# Draws alien into the game
		alien(alienPosX[i], alienPosY[i], i)

	# Laser movement
	if laserPosY <= 0 :
		laserPosY = 480
		laserState = 'loaded'

	if laserState == 'fire':
		shootLaser(laserPosX, laserPosY)
		laserPosY -= laserYchange

	# Draws player into the game
	player(shipPosX, shipPosY)

	# Display Score
	showScore(textPosX, textPosY)

	# Updates game display each loop
	pygame.display.update()