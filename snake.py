import pygame
import time
import random

pygame.init()
pygame.mixer.music.load("features/snake.wav")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (250,0,0)
GREEN = (0,155,0)
BLUE = (0,0,255)

WIDTH_DISPLAY = 1100
HEIGHT_DISPLAY = 800

game_display = pygame.display.set_mode((WIDTH_DISPLAY,HEIGHT_DISPLAY))
pygame.display.set_caption('SNAKE')
ICON = pygame.image.load('features/ikona.png')

pygame.display.set_icon(ICON)
pygame.display.update()

BACKGROUND_START = pygame.image.load('features/tlo.jpg')
BACKGROUND_START = pygame.transform.scale(BACKGROUND_START,(WIDTH_DISPLAY,HEIGHT_DISPLAY))
HEAD_SNAKE = pygame.image.load('features/head_s.png')
APPLE_IMG = pygame.image.load('features/apple.png')

APPLE_WIDTH = 30
SIZE_SNAKE = 20
DIRECTION = "RIGHT"

SMALL_FONT = pygame.font.SysFont("comicsansms",25)
MED_FONT = pygame.font.SysFont("comicsansms", 45)
LARGE_FONT = pygame.font.SysFont("comicsansms",70)

CLOCK = pygame.time.Clock()

def fonts_objects(text,colour,size):
	if size == "SMALL":
		text_font = SMALL_FONT.render(text,True,colour)
	elif size == "MEDIUM":
		text_font = MED_FONT.render(text,True,colour)
	elif size == "LARGE":
		text_font = LARGE_FONT.render(text,True,colour)
	
	return text_font, text_font.get_rect()

def display_message(text,colour,H=0,size="SMALL"):
	text_font,text_rectangle = fonts_objects(text,colour,size)
	
	text_rectangle.center = (WIDTH_DISPLAY/2),(HEIGHT_DISPLAY/2) + H
	game_display.blit(text_font,text_rectangle)

def results(result):
	result = SMALL_FONT.render("RESULT: " + str(result),True,BLACK)
	game_display.blit(result,[0,0])

def music_game_over():
	over = pygame.mixer.Sound("features/die.ogg")
	over.play()

def music_food():
	eat_sound = pygame.mixer.Sound("features/eat.ogg")
	eat_sound.play()

def random_apple():
	rand_appple_x = round(random.randrange(0,WIDTH_DISPLAY - APPLE_WIDTH))
	rand_appple_y = round(random.randrange(0,HEIGHT_DISPLAY - APPLE_WIDTH))
	return rand_appple_x,rand_appple_y

def snake(snake_size,snake_table):
	if DIRECTION == "RIGHT":
		head = pygame.transform.rotate(HEAD_SNAKE,270)
	elif DIRECTION == "LEFT":
		head = pygame.transform.rotate(HEAD_SNAKE,90)
	elif DIRECTION == "UP":
		head = HEAD_SNAKE
	elif DIRECTION == "DOWN":
		head = pygame.transform.rotate(HEAD_SNAKE,180)
	
	game_display.blit(head,(snake_table[-1][0], snake_table[-1][1]))
	
	for xy in snake_table[:-1]:
		pygame.draw.rect(game_display,GREEN,[xy[0],xy[1],snake_size,snake_size])

def game_intro():
	intro = True
	
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					intro = False
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()

		game_display.blit(BACKGROUND_START,[0,0])
		display_message("WLECOME TO SNAKE GAME!",WHITE,-300,"LARGE")
		display_message("YOUR GOAL - Don't let snake to be hungry",RED,-175,"MEDIUM")
		display_message("The more apple you eat, the bigger you will be!",WHITE,-70,"MEDIUM")
		display_message("Don't die - avoid your tail",RED,50,"MEDIUM")
		display_message("SPACE - begin, ESC - exit, P - pause",WHITE,180,"MEDIUM")
		pygame.display.update()
		
		CLOCK.tick(5)

def pause ():
	pygame.mixer.music.pause()
	paused = True
	
	display_message("PAUSE",BLACK,-100,"LARGE")
	display_message("SPACE - continue, ESC - exit",BLACK,30,"MEDIUM")
	pygame.display.update()
	
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					paused = False
					pygame.mixer.music.unpause()
				elif event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()

		CLOCK.tick(5)

def game_loop():
	pygame.mixer.music.play(-1)
	global DIRECTION 
	FPS = 10
	RESULT = 0
	DIRECTION = "RIGHT"
	game_exit = False
	game_over = False
	
	BEGIN_X = WIDTH_DISPLAY/2
	BEGIN_Y = HEIGHT_DISPLAY/2
	BEGIN_X_CHANGE = 10
	BEGIN_Y_CHANGE = 0
	
	snake_table = []
	snake_size = 1
	
	rand_apple_x,rand_apple_y = random_apple()
	
	while not game_exit:
		if game_over == True:
			pygame.mixer.music.pause()

			display_message("GAME OVER!",RED,-180,"LARGE")
			display_message("Your result: " + str(RESULT),BLACK,-60,"MEDIUM")
			display_message("SPACE - play again, ESC - exit the game",RED,50,"MEDIUM")
			pygame.display.update()
	
		while game_over == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					game_exit = True
					game_over = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						game_exit = True
						game_over = False
					if event.key == pygame.K_SPACE:
						game_loop()
		

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				game_exit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					DIRECTION = "LEFT"
					BEGIN_X_CHANGE -= SIZE_SNAKE
					BEGIN_Y_CHANGE = 0
				elif event.key == pygame.K_RIGHT:
					DIRECTION = "RIGHT"
					BEGIN_X_CHANGE += SIZE_SNAKE
					BEGIN_Y_CHANGE = 0
				elif event.key == pygame.K_UP:
					DIRECTION = "UP"
					BEGIN_X_CHANGE = 0
					BEGIN_Y_CHANGE -= SIZE_SNAKE
				elif event.key == pygame.K_DOWN:
					DIRECTION = "DOWN"
					BEGIN_X_CHANGE = 0
					BEGIN_Y_CHANGE += SIZE_SNAKE
				elif event.key == pygame.K_p:
					pause()

		if BEGIN_X >= WIDTH_DISPLAY or BEGIN_X <= 0 or BEGIN_Y >= HEIGHT_DISPLAY or BEGIN_Y <= 0:
			music_game_over()
			game_over = True

		BEGIN_X += BEGIN_X_CHANGE
		BEGIN_Y += BEGIN_Y_CHANGE
		
		game_display.fill(WHITE)
		game_display.blit(APPLE_IMG,(rand_apple_x,rand_apple_y))
		
		snake_head = []
		snake_head.append(BEGIN_X)
		snake_head.append(BEGIN_Y)
		snake_table.append(snake_head)

		if len(snake_table) > snake_size:
			del snake_table[0]

		for element in snake_table[:-1]:
			if element == snake_head:
				game_over = True
				music_game_over()
		
		snake(SIZE_SNAKE,snake_table)
		results(RESULT)
		pygame.display.update()
		
		CLOCK.tick(FPS)

		if BEGIN_X > rand_apple_x and BEGIN_X < rand_apple_x + APPLE_WIDTH or BEGIN_X + SIZE_SNAKE > rand_apple_x and BEGIN_X + SIZE_SNAKE < rand_apple_x + APPLE_WIDTH:
			if BEGIN_X > rand_apple_y and BEGIN_Y < rand_apple_y + APPLE_WIDTH or BEGIN_Y + SIZE_SNAKE > rand_apple_y and BEGIN_Y + SIZE_SNAKE < rand_apple_y + APPLE_WIDTH:
				
				rand_apple_x, rand_apple_y = random_apple()
				music_food()
				if FPS < 28:
					FPS += 1
				snake_size += 1
				RESULT += 1

	pygame.quit()
	quit()

game_intro()
game_loop()