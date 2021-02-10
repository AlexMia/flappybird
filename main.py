import pygame, sys, json
from pygame.locals import *
from random import randint as rnd

pygame.init()
pygame.font.init()
pygame.display.set_caption("Flappy Bird")


# Constants

WIN_SIZE = (600, 400)
FPS = 60
G = .25
PIPE_SPACING = 250
PIPE_MIN_HEIGHT = 70
PIPE_MAX_HEIGHT = WIN_SIZE[1] - PIPE_MIN_HEIGHT


# Pygame variables

screen = pygame.display.set_mode(WIN_SIZE, 0)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)


# Classes

class Bird:
	def __init__(self, x, y, size):
		self.initialY = y
		self.x = x
		self.y = y
		self.yvel = 0
		self.jumpVel = 5
		self.birdSize = size
		self.image = pygame.image.load("bird.png")
		self.score = 0
		self.scoreText = font.render(f"SCORE: {self.score}", False, (255, 255, 255))

	def getRect(self):
		rect = pygame.Rect((self.x-self.birdSize/2, self.y-self.birdSize/2), (self.birdSize, self.birdSize))
		return rect

	def show(self):
		screen.blit(self.image, (self.x-self.birdSize/2, self.y-self.birdSize/2))
		screen.blit(self.scoreText, (10,10))

	def jump(self):
		self.yvel = -self.jumpVel
		return True

	def update(self, G, pipes, started):
		# Player death handling
		if self.y >= WIN_SIZE[1] or self.y <= 0 or self.getRect().collidelist([j for sub in [pipe.getRect() for pipe in pipes] for j in sub]) >= 0:
			save(self.score)
			return False
		if pipes[0].x < self.x and not pipes[0].checked:
			self.score += 1
			self.scoreText = font.render(f"SCORE: {self.score}", False, (255, 255, 255))
			pipes[0].checked = True
		if started:
			self.y += self.yvel
			self.yvel += G
			return True

	def reset(self):
		self.y = self.initialY
		self.yvel = 0
		self.score = 0
		self.scoreText = font.render(f"SCORE: {self.score}", False, (255, 255, 255))

class Pipe:
	def __init__(self, x, holeY, holeSize, size, xvel):
		self.initialX = x
		self.x = x
		self.holeY = holeY
		self.holeSize = holeSize
		self.size = size
		self.xvel = xvel
		self.color = (4, 204, 0)
		self.checked = False
		self.image = pygame.image.load("pipe.png")

	def getRect(self):
		rect1 = pygame.Rect((self.x, 0), (self.size, self.holeY-self.holeSize/2))
		rect2 = pygame.Rect((self.x, self.holeY+self.holeSize/2), (self.size, WIN_SIZE[1]-(self.holeY+self.holeSize/2)))
		return([rect1, rect2])

	def show(self):
		screen.blit(self.image, (self.x, -WIN_SIZE[1]+self.holeY-self.holeSize/2))
		screen.blit(pygame.transform.flip(self.image, True, True), (self.x, self.holeY+self.holeSize/2))

	def update(self, lastX, started):
		if started:
			self.x -= self.xvel
			if self.x <= -10:
				return Pipe(lastX + PIPE_SPACING, rnd(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT), 80, 30, 3.5)
			return None


# Variables

started = False
bird = Bird(50, WIN_SIZE[1]/2, 20)
pipes = []
for i in range(4):
	pipes.append(Pipe(WIN_SIZE[0] + i*PIPE_SPACING, rnd(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT), 80, 32, 3.5))


# Functions

def redrawWindow(screen, bird, pipes):
	screen.fill((0, 0, 0))
	for pipe in pipes: pipe.show()
	bird.show()
	pygame.display.update()

def reset():
	global started
	global pipes
	started = False
	bird.reset()
	pipes = []
	for i in range(4):
		pipes.append(Pipe(WIN_SIZE[0] + i*PIPE_SPACING, rnd(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT), 80, 30, 3.5))

def save(score):
	try:
		with open('scores.txt', 'r') as f:
			data = json.loads(f.read())
		if data['hs'] < score:
			with open('scores.txt', 'w') as f:
				f.write(json.dumps({'hs': score}))
	except:
		with open('scores.txt', 'w') as f:
				f.write(json.dumps({'hs': score}))

def exit():
	save(bird.score)
	pygame.quit()
	sys.exit()


# Main loop

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				if not started:
					reset()
					started = True
				if started:
					started = bird.jump()
			if event.key == K_ESCAPE:
				exit()

	redrawWindow(screen, bird, pipes)
	started = bird.update(G, pipes, started)
	for pipe in pipes:
		if r:=pipe.update(pipes[-1].x, started) :
			pipes.pop(0)
			pipes.append(r)
	clock.tick(FPS)
