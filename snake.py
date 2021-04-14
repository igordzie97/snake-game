import pygame
import time
import random

pygame.init()
pygame.mixer.music.load("features/snake.wav")

BIALY = (255,255,255)
CZARNY = (0,0,0)
CZERWONY = (250,0,0)
ZIELONY = (0,155,0)
NIEBIESKI = (0,0,255)

SZEROKOSC_DISPLAY = 1100
WYSOKOSC_DISPLAY = 800

gameDisplay = pygame.display.set_mode((SZEROKOSC_DISPLAY,WYSOKOSC_DISPLAY))
pygame.display.set_caption('SNAKE')
IKONA = pygame.image.load('features/ikona.png')

pygame.display.set_icon(IKONA)
pygame.display.update()

TLO_START = pygame.image.load('features/tlo.jpg')
TLO_START = pygame.transform.scale(TLO_START,(SZEROKOSC_DISPLAY,WYSOKOSC_DISPLAY))
GLOWA_SNAKE = pygame.image.load('features/head_s.png')
APPLE_IMG = pygame.image.load('features/apple.png')

APPLE_GRUBOSC = 30
WYMIAR_SNAKE = 20
KIERUNEK = "PRAWY"

SMALL_FONT = pygame.font.SysFont("comicsansms",25)
MED_FONT = pygame.font.SysFont("comicsansms", 45)
LARGE_FONT = pygame.font.SysFont("comicsansms",70)

CLOCK = pygame.time.Clock()




def czcionki_obiekty(tekst,kolor,rozmiar):
	if rozmiar == "SMALL":
		textCZCIONKA = SMALL_FONT.render(tekst,True,kolor)
	elif rozmiar == "MEDIUM":
		textCZCIONKA = MED_FONT.render(tekst,True,kolor)
	elif rozmiar == "LARGE":
		textCZCIONKA = LARGE_FONT.render(tekst,True,kolor)
	
	return textCZCIONKA, textCZCIONKA.get_rect()


def wiadomosc_na_ekran(tekst,kolor,H=0,rozmiar="SMALL"):
	textCZCIONKA,textPROSTOKAT = czcionki_obiekty(tekst,kolor,rozmiar)
	
	textPROSTOKAT.center = (SZEROKOSC_DISPLAY/2),(WYSOKOSC_DISPLAY/2) + H
	gameDisplay.blit(textCZCIONKA,textPROSTOKAT)


def wynik(wynik):
	wynik = SMALL_FONT.render("WYNIK: " + str(wynik),True,CZARNY)
	gameDisplay.blit(wynik,[0,0])


def muzyka_gameOver():
	over = pygame.mixer.Sound("features/die.ogg")
	over.play()


def muzyka_jedzenia():
	eat_sound = pygame.mixer.Sound("features/eat.ogg")
	eat_sound.play()


def losowanie_Apple():
	randAppleX = round(random.randrange(0,SZEROKOSC_DISPLAY - APPLE_GRUBOSC))
	randAppleY = round(random.randrange(0,WYSOKOSC_DISPLAY - APPLE_GRUBOSC))
	return randAppleX,randAppleY


def snake(WYMIAR_SNAKE,snakeTable):
	if KIERUNEK == "PRAWY":
		glowa = pygame.transform.rotate(GLOWA_SNAKE,270)
	elif KIERUNEK == "LEWY":
		glowa = pygame.transform.rotate(GLOWA_SNAKE,90)
	elif KIERUNEK == "GORA":
		glowa = GLOWA_SNAKE
	elif KIERUNEK == "DOL":
		glowa = pygame.transform.rotate(GLOWA_SNAKE,180)
	
	gameDisplay.blit(glowa,(snakeTable[-1][0], snakeTable[-1][1])) # tutaj ogarnac jeszcze raz o co chodzi
	
	for XiY in snakeTable[:-1]:
		pygame.draw.rect(gameDisplay,ZIELONY,[XiY[0],XiY[1],WYMIAR_SNAKE,WYMIAR_SNAKE])	#tablica w tablicy 
	


def intro_gry():
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

		gameDisplay.blit(TLO_START,[0,0])
		wiadomosc_na_ekran("Witaj w grze SNAKE!",BIALY,-300,"LARGE")
		wiadomosc_na_ekran("Cel-Zadbaj,zeby Snake nie byl glodny",CZERWONY,-175,"MEDIUM")
		wiadomosc_na_ekran("Im wiecej jablek zjesz - tym Snake bedzie wiekszy!",BIALY,-70,"MEDIUM")
		wiadomosc_na_ekran("Wpadniesz w swoj ogon,albo sciane - Umierasz",CZERWONY,50,"MEDIUM")
		wiadomosc_na_ekran("Wcisnij SPACJA by zaczac,ESC-zeby wyjsc,P-pauza",BIALY,180,"MEDIUM")
		pygame.display.update()
		
		CLOCK.tick(5)

	

def pauza ():
	pygame.mixer.music.pause()
	paused = True
	
	wiadomosc_na_ekran("PAUZA",CZARNY,-100,"LARGE")
	wiadomosc_na_ekran("Wcisnij SPACJA-kontynuuj, ESC-wyjdz",CZARNY,30,"MEDIUM")
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


def gameLoop():
	
	pygame.mixer.music.play(-1)
	global KIERUNEK #to jest chyba zbedne
	FPS=10
	WYNIK = 0
	KIERUNEK = "PRAWY"
	gameExit = False
	gameOver = False
	
	POCZATKOWY_X = SZEROKOSC_DISPLAY/2
	POCZATKOWY_Y = WYSOKOSC_DISPLAY/2
	POCZATKOWY_X_ZMIANA = 10
	POCZATKOWY_Y_ZMIANA = 0
	
	snakeTABLE = []
	snakeDLUGOSC = 1
	
	randAppleX,randAppleY = losowanie_Apple()
	
	while not gameExit:
		if gameOver == True:
			pygame.mixer.music.pause()

			wiadomosc_na_ekran("GAME OVER!",CZERWONY,-180,"LARGE")
			wiadomosc_na_ekran("Twoj wynik wyniosl: " + str(WYNIK),CZARNY,-60,"MEDIUM")
			wiadomosc_na_ekran("SPACJA - jeszcze raz, ESC - wyjdz z gry",CZARNY,50,"MEDIUM")
			pygame.display.update()
	
		while gameOver == True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_SPACE:
						gameLoop()
		

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					KIERUNEK = "LEWY"
					POCZATKOWY_X_ZMIANA -= WYMIAR_SNAKE
					POCZATKOWY_Y_ZMIANA = 0
				elif event.key == pygame.K_RIGHT:
					KIERUNEK = "PRAWY"
					POCZATKOWY_X_ZMIANA += WYMIAR_SNAKE
					POCZATKOWY_Y_ZMIANA = 0
				elif event.key == pygame.K_UP:
					KIERUNEK = "GORA"
					POCZATKOWY_X_ZMIANA = 0
					POCZATKOWY_Y_ZMIANA -= WYMIAR_SNAKE
				elif event.key == pygame.K_DOWN:
					KIERUNEK = "DOL"
					POCZATKOWY_X_ZMIANA = 0
					POCZATKOWY_Y_ZMIANA += WYMIAR_SNAKE
				elif event.key == pygame.K_p:
					pauza()

		if POCZATKOWY_X >= SZEROKOSC_DISPLAY or POCZATKOWY_X <= 0 or POCZATKOWY_Y >= WYSOKOSC_DISPLAY or POCZATKOWY_Y <= 0:
			muzyka_gameOver()
			gameOver = True



		POCZATKOWY_X += POCZATKOWY_X_ZMIANA
		POCZATKOWY_Y += POCZATKOWY_Y_ZMIANA
		
		gameDisplay.fill(BIALY)
		gameDisplay.blit(APPLE_IMG,(randAppleX,randAppleY))
		
		snakeHEAD = []
		snakeHEAD.append(POCZATKOWY_X)
		snakeHEAD.append(POCZATKOWY_Y)
		snakeTABLE.append(snakeHEAD)

		if len(snakeTABLE) > snakeDLUGOSC:
			del snakeTABLE[0]

		for kazdySegment in snakeTABLE[:-1]:
			if kazdySegment == snakeHEAD:
				gameOver = True
				muzyka_gameOver()
		
		snake(WYMIAR_SNAKE,snakeTABLE)
		wynik(WYNIK)
		pygame.display.update()
		
		CLOCK.tick(FPS)

		if POCZATKOWY_X > randAppleX and POCZATKOWY_X < randAppleX + APPLE_GRUBOSC or POCZATKOWY_X + WYMIAR_SNAKE > randAppleX and POCZATKOWY_X + WYMIAR_SNAKE <randAppleX + APPLE_GRUBOSC:
			if POCZATKOWY_Y > randAppleY and POCZATKOWY_Y < randAppleY + APPLE_GRUBOSC or POCZATKOWY_Y + WYMIAR_SNAKE > randAppleY and POCZATKOWY_Y + WYMIAR_SNAKE <randAppleY + APPLE_GRUBOSC:
				
				randAppleX,randAppleY = losowanie_Apple()
				muzyka_jedzenia()
				if FPS < 28:
					FPS += 1
				snakeDLUGOSC += 1
				WYNIK += 1


		
	pygame.quit()
	quit()



intro_gry()
gameLoop()
			


	

