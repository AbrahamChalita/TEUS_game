import pygame
import sys
import time
import random
import smtplib
pygame.init()

email = input("Escribe to correo para enviar tu puntaje!\n")

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('pruebasdepy@gmail.com','Temporal1@')

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 30
BLACK = (0, 0, 0)
ADD_NEW_EXAMS_RATE = 40
ADD_NEW_GEXAMS_RATE = 100
sky_img = pygame.transform.scale(pygame.image.load('sky.png'), (1920,50))
sky_img_rect = sky_img.get_rect() 
sky_img_rect.left = 0
floor_img = pygame.transform.scale(pygame.image.load('floor.png'), (1920,50))
floor_img_rect = floor_img.get_rect()
floor_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.Font('font/PIXELITE.FON', 600)

canvas = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Teus')

music = pygame.mixer.Sound('intro.wav')
music.play()

class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()

class Pencil:
    pencil_velocity = 10

    def __init__(self):
        self.pencil_img = pygame.transform.scale(pygame.image.load('pencil.png'), (130,200))
        self.pencil_img_rect = self.pencil_img.get_rect()
        self.pencil_img_rect.width -= 10
        self.pencil_img_rect.height -= 10
        self.pencil_img_rect.top = WINDOW_HEIGHT/2
        self.pencil_img_rect.right = 12*WINDOW_WIDTH/13
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.pencil_img, self.pencil_img_rect)
        if self.pencil_img_rect.top <= sky_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.pencil_img_rect.bottom >= floor_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.pencil_img_rect.top -= self.pencil_velocity
        elif self.down:
            self.pencil_img_rect.top += self.pencil_velocity

class Exams:
    exams_velocity = 20

    def __init__(self):
        self.exams_img = pygame.transform.scale((pygame.image.load('exam.png')), (130,130))
        self.exams_img_rect = self.exams_img.get_rect()
        self.exams_img_rect.right = pencil.pencil_img_rect.left
        self.exams_img_rect.top = pencil.pencil_img_rect.top

    def update(self):
        canvas.blit(self.exams_img, self.exams_img_rect)

        if self.exams_img_rect.left > 0:
            self.exams_img_rect.left -= self.exams_velocity * LEVEL

class Gexams:
    gexams_velocity = 20

    def __init__(self):
        self.gexams_img = pygame.transform.scale((pygame.image.load('gexam.png')), (130,130))
        self.gexams_img_rect = self.gexams_img.get_rect()
        self.gexams_img_rect.right = random.randint(10,1910)
        self.gexams_img_rect.top = 0
    def update(self):
        canvas.blit(self.gexams_img, self.gexams_img_rect)

        if self.gexams_img_rect.bottom > 0:
            self.gexams_img_rect.bottom += self.gexams_velocity

class Teus:
    velocity = 10

    def __init__(self):
        self.teus_img = pygame.transform.scale(pygame.image.load('teus.png'), (130,200))
        self.teus_img_rect = self.teus_img.get_rect()
        self.teus_img_rect.left = 20
        self.teus_img_rect.top = 8 * WINDOW_HEIGHT/10
        self.down = False
        self.up = False
        self.right = False
        self.left = False

    def update(self):
        canvas.blit(self.teus_img, self.teus_img_rect)
        if self.teus_img_rect.top <= sky_img_rect.bottom:
            self.up = False
        if self.teus_img_rect.bottom >= floor_img_rect.top:
            self.down = False
        if self.up:
            self.teus_img_rect.top -= 30 
        if self.down:
            self.teus_img_rect.bottom += 30 
        if self.right:
            self.teus_img_rect.right += 30
        if self.left:
            self.teus_img_rect.left -= 30

def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('death_sound.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.transform.scale((pygame.image.load('end.png')),(960,540))
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sc = str(topscore.high_score)
                    server.sendmail('preubasdepy@gmail.com',email, "Hola! En breve te enviaremos tu puntaje mas alto del Juego de Teus!")
                    server.sendmail('preubasdepy@gmail.com',email, sc)
                    server.quit()
                    print("Tu puntaje se ha enviado exitosamente!")
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()

def start_game():
    canvas.fill(BLACK)
    #canvas.blit(pygame.image.load('background.png'))
    start_img = pygame.transform.scale(pygame.image.load('start.png'),(1920, 1080))
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

def check_level(LSCORE):
    global LEVEL
    if LSCORE in range(0, 10):
        sky_img_rect.bottom = 50
        floor_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif LSCORE in range(10, 20):
        LEVEL = 2
    elif LSCORE in range(20, 30):
        LEVEL = 3
    elif LSCORE in range(30, 40):
        LEVEL = 4
    elif LSCORE in range(40, 50):
        LEVEL = 5
    elif LSCORE > 50:
        LEVEL = 6




def game_loop():
    while True:
        global pencil
        pencil = Pencil()
        exams = Exams()
        gexams = Gexams()
        teus = Teus()
        add_new_exams_counter = 0
        add_new_gexams_counter = 0
        global SCORE
        SCORE = 0
        LSCORE = 0
        global  HIGH_SCORE
        exams_list = []
        gexams_list = []
        while True:
            canvas.blit(pygame.transform.scale((pygame.image.load("background.png")),(1920,1080)),(0,0))
            check_level(SCORE)
            pencil.update()
            add_new_exams_counter += 1
            add_new_gexams_counter += 1

            if add_new_exams_counter * LEVEL/3 >= ADD_NEW_EXAMS_RATE:
                add_new_exams_counter = 0
                new_exams = Exams()
                exams_list.append(new_exams)
            for f in exams_list:
                if f.exams_img_rect.left <= 0:
                    exams_list.remove(f)
                    SCORE += 1
                f.update()

            if add_new_gexams_counter >= ADD_NEW_GEXAMS_RATE:
                add_new_gexams_counter = 0
                new_gexams = Gexams()
                gexams_list.append(new_gexams)
            for f in gexams_list:
                if f.gexams_img_rect.bottom <= 0:
                    gexams_list.remove(f)
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        teus.up = True
                        teus.down = False
                    elif event.key == pygame.K_DOWN:
                        teus.down = True
                        teus.up = False
                    elif event.key == pygame.K_LEFT:
                        teus.left = True
                        teus.right = False
                    elif event.key == pygame.K_RIGHT:
                        teus.right = True
                        teus.left = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        teus.up = False
                        teus.down = True
                    elif event.key == pygame.K_DOWN:
                        teus.down = True
                        teus.up = False
                    elif event.key == pygame.K_LEFT:
                        teus.left = False
                    elif event.key == pygame.K_RIGHT:
                        teus.right = False

            LSCORE += 1

            score_font = font.render('Puntaje:'+str(SCORE), True, BLACK)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (100, sky_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Nivel:'+str(LEVEL), True, BLACK)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (960, sky_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Puntaje mas alto:'+str(topscore.high_score),True,BLACK)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (1800, sky_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(sky_img, sky_img_rect)
            canvas.blit(floor_img, floor_img_rect)
            teus.update()
            for f in gexams_list:
                if f.gexams_img_rect.colliderect(teus.teus_img_rect):
                    SCORE += 5
                    gexams_list.remove(f)
            for f in exams_list:
                if f.exams_img_rect.colliderect(teus.teus_img_rect):
                    game_over()
                    if SCORE > teus.teus_score:
                        teus.teus_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)
start_game()