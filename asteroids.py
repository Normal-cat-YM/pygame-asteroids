import pygame
from random import randint as rand
import os
pygame.init()
pygame.display.set_caption('Asteroids')
class player:
    global screen, SCREEN_HEIGHT, SCREEN_WIDTH
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed  = speed


    def move(self, key_left, key_right, speed = 0):
        if not speed == 0:
            self.speed = speed
        if key_left:
            self.x -= self.speed
            

            if self.x < 0:
                self.x = 0
        if key_right:
            self.x += self.speed

            if self.x > SCREEN_WIDTH - 35:
                self.x = SCREEN_WIDTH - 35


    def draw(self):
        self.player_obj = pygame.draw.rect(screen, (0,200,0), (self.x, self.y, 35, 35))

class asteroid:
    global screen, SCREEN_HEIGHT, SCREEN_WIDTH
    score = 0
    def __init__(self, asteroid_speed, y):
        self.speed = asteroid_speed
        self.x = rand(0, SCREEN_WIDTH)
        self.height = SCREEN_HEIGHT
        self.y = y

    def move(self, speed = 0):
        if not speed == 0:
            self.speed = speed
        self.y += self.speed
        if self.y - 20 > self.height:
            self.y = 0
            self.x = rand(0, SCREEN_WIDTH - 20)
            asteroid.score += 1
        return asteroid.score

    def draw(self):
        self.asteroid_obj = pygame.draw.ellipse(screen, (255, 0, 0), (self.x, self.y, 20, 20)) 
        return self.asteroid_obj

class button:
    global screen

    def __init__(self, button_x, button_y, width, height, button_color, text="", text_color=(0,0,0), text_size=100, text_x=0, text_y=0):
        self.button_x = button_x
        self.button_y = button_y
        self.text_x = text_x + button_x
        self.text_y = text_y + button_y
        self.width = width
        self.height = height
        self.text = text
        self.button_RGB = button_color
        self.text_RGB = text_color
        self.text_size = text_size
    
    def draw(self):
        self.button_obj = pygame.draw.rect(screen, self.button_RGB, (self.button_x, self.button_y, self.width, self.height))
        if self.text != "":
            font = pygame.font.SysFont(None, self.text_size)
            self.text_obj = font.render(self.text, True, self.text_RGB)
            screen.blit(self.text_obj, (self.text_x, self.text_y))
    
    def pressed(self, mouse_pos, mouse_clicked):
        if self.button_obj.collidepoint(mouse_pos) and mouse_clicked:
            return True
        else:
            return False

class text:
    global screen

    def __init__(self, text:str, x=0, y=0, color=(255,255,255), size=50):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def draw(self, text=""):
        if text != "":
            self.text = text
        font = pygame.font.SysFont(None, self.size)
        self.text_obj = font.render(self.text, True, self.color)
        screen.blit(self.text_obj, (self.x, self.y))


#====================
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
FPS = 100
#====================

time_to_delay = int(1000/FPS)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
done = False
mouse_clicked = False
mouse_pos = (0, 0)





def menu():
    global screen
    file = "score.txt"
    lines = []
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("0\n0")
        f.close()
    f = open(file, "r+")
    data = f.read()
    lines = data.split('\n')
    f.close()
    max_score = lines[0]
    last_score = lines[1]
    if not max_score.isdigit() or not last_score.isdigit():
        max_score = 0
        last_score = "[NO DATA]"

    else:
        max_score = int(lines[0])
        last_score = int(lines[1])
    mouse_clicked = False
    mouse_pos = (0, 0)
    done = False
    while not done:
        pygame.time.delay(time_to_delay)
        screen.fill((50,50,50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
        start_button = button(200, 50, 200, 50, (0,255,0), "Start", (255, 255, 255), 50, 60, 10)
        start_button.draw()
        if not max_score == 0:
            max_score_text = text("Max score: " + str(max_score), 190, 150)
        else:
            max_score_text = text("Max score: [NO DATA]", 190, 150)
        max_score_text.draw()
        last_score_text = text("Last score: " + str(last_score), 190, 200)
        last_score_text.draw()
        if start_button.pressed(mouse_pos, mouse_clicked):
            game_for_one_person(max_score, last_score)
        pygame.display.flip()
    pygame.quit()
    exit()

def game_for_one_person(max_score, last_score):
    global screen, time_to_delay

    #==========================
    speed = 2
    p = player(300, 700, speed)
    next_score = 50
    sec_before_start = 5
    #==========================

    done = False
    key_right_pressed = False
    key_left_pressed = False
    asteroids = []
    asteroids.append(asteroid(speed*3, -200))
    asteroids.append(asteroid(speed*3, -400))
    asteroids.append(asteroid(speed*3, 0))
    asteroid.score = 0
    score = 0
    last_score = 0
    sec = 1001
    sec_before_start += 1
    counting_text = text(str(sec_before_start), 250, 250, (0, 200, 0), 200)
    while not done:
        if sec > 1000 and sec_before_start != 0:
            screen.fill((50,50,50))
            sec_before_start -= 1
            counting_text.draw(str(sec_before_start))
            sec = 0
        pygame.time.delay(time_to_delay)
        sec += time_to_delay
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    key_right_pressed = False
                    key_left_pressed = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    key_left_pressed = False
                    key_right_pressed = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    key_left_pressed = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    key_right_pressed = False
        if sec_before_start == 0:
            screen.fill((50,50,50))
            p.move(key_left_pressed, key_right_pressed, speed)
            p.draw()
        
            for object in asteroids[:]:
                score = asteroid.move(object, speed*3)
                if p.player_obj.colliderect(asteroid.draw(object)):
                   done = True
            if max_score < score:
                max_score = score
            if next_score < score:
                next_score += 10
                speed += 0.2
            last_score = score
            t = text("Score: " + str(score), 230, 10, (255, 0, 0), 50)
            t.draw()
        pygame.display.flip()
    file = "score.txt"
    f = open(file, "w")
    f.write(str(max_score) + '\n' + str(last_score))
    f.close()
    menu()

menu()
