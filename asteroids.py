from ast import If
from pickle import TRUE
import pygame
from random import randint as rand
import os
pygame.init()
pygame.display.set_caption('Asteroids')


file = "settings."
lines = []
if not os.path.exists(file):
    open(file, "x")
    f = open(file, "w")
    f.write("SCREEN_HEIGHT: 750\nSCREEN_WIDTH: 600\nFPS: 100\nStart speed: 3\nNext score: 50\nSeconds before start: 5")
    f.close()
f = open(file, "r+")
data = f.read()
lines = data.split('\n')
for line_num in range(0, len(lines)):
    lines[line_num] = lines[line_num].split(": ")[1]
f.close()
SCREEN_HEIGHT = int(lines[0])
SCREEN_WIDTH = int(lines[1])
FPS = int(lines[2])
speed = float(lines[3])
next_score = int(lines[4])
sec_before_start = int(lines[5])


class player:
    global screen, SCREEN_HEIGHT, SCREEN_WIDTH

    def __init__(self, x, y, speed, color=(0,255,0)):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color

    def move(self, key_left, key_right, speed=0):
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

    def draw(self, color=""):
        if color == "":
            color = self.color
        self.color = color
        self.player_obj = pygame.draw.rect(
            screen, self.color, (self.x, self.y, 35, 35))


class asteroid:
    global screen, SCREEN_HEIGHT, SCREEN_WIDTH
    score = 0

    def __init__(self, asteroid_speed, y):
        self.speed = asteroid_speed
        self.x = rand(0, SCREEN_WIDTH)
        self.height = SCREEN_HEIGHT
        self.y = y

    def move(self, speed=0):
        if not speed == 0:
            self.speed = speed
        self.y += self.speed
        if self.y - 50 > self.height:
            self.y = 0
            self.x = rand(0, SCREEN_WIDTH - 50)
            asteroid.score += 1
        return asteroid.score

    def draw(self):
        self.asteroid_obj = pygame.draw.ellipse(
            screen, (100, 100, 100), (self.x, self.y, 50, 50))
        return self.asteroid_obj


class button:
    global screen

    def __init__(self, button_x, button_y, width, height, button_color, text="", text_color=(0, 0, 0), text_size=100, text_x=0, text_y=0):
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
        self.button_obj = pygame.draw.rect(
            screen, self.button_RGB, (self.button_x, self.button_y, self.width, self.height))
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

    def __init__(self, text: str, x=0, y=0, color=(255, 255, 255), size=50):
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


time_to_delay = int(1000/FPS)
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
done = False
mouse_clicked = False
mouse_pos = (0, 0)


fullscreen = False


def menu():
    global screen, fullscreen, SCREEN_WIDTH, SCREEN_HEIGHT, FPS

    time_to_delay = int(1000/FPS)

    file = "score."
    lines = []
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("Max score: 0")
        f.close()
    f = open(file, "r+")
    data = f.read()
    lines = data.split('\n')
    lines[0] = lines[0].split(": ")[1]
    f.close()
    
    max_score = lines[0]
    
    file = "statistic."
    lines = []
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("0")
        f.close()
    f = open(file, "r+")
    data = f.read()
    lines = data.split('\n')
    f.close()
    last_score = lines[-1]
    if not max_score.isdigit() or not last_score.isdigit():
        max_score = 0
        last_score = "[NO DATA]"

    else:
        max_score = int(max_score)
        last_score = int(last_score)
    mouse_clicked = False
    mouse_pos = (0, 0)
    done = False
    if fullscreen:
        screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
    else:
        screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
    while not done:
        pygame.time.delay(time_to_delay)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                    game_for_one_person(max_score, last_score)
                if event.key == pygame.K_F11 and not fullscreen:
                    fullscreen = True
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                elif event.key == pygame.K_F11 and fullscreen:
                    fullscreen = False
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

        start_button = button(200, 50, 200, 50, (0, 255, 0),
                              "Start for one", (255, 255, 255), 40, 16, 15)
        start_button_2 = button(200, 150, 200, 50, (0, 255, 255),
                              "Start for two", (255, 255, 255), 40, 16, 15)
        start_button_3 = button(200, 250, 200, 50, (255, 0, 255),
                              "Start for four", (255, 255, 255), 40, 16, 15)
        start_button.draw()
        start_button_2.draw()
        start_button_3.draw()
        statistic_button = button(
            200, 350, 200, 50, (0, 0, 255), "Statistic", (255, 255, 255), 50, 40, 10)
        statistic_button.draw()
        if not max_score == 0:
            max_score_text = text("Max score: " + str(max_score), 190, 450)
        else:
            max_score_text = text("Max score: [NO DATA]", 190, 450)
        max_score_text.draw()
        last_score_text = text("Last score: " + str(last_score), 190, 500)
        last_score_text.draw()
        if start_button.pressed(mouse_pos, mouse_clicked):
            game_for_one_person(max_score, last_score)
        if statistic_button.pressed(mouse_pos, mouse_clicked):
            statistic_graph()
        if start_button_2.pressed(mouse_pos, mouse_clicked):
            game_for_two_persons(max_score, last_score)
        if start_button_3.pressed(mouse_pos, mouse_clicked):
            game_for_four_persons(max_score, last_score)
        pygame.display.flip()
    pygame.quit()
    quit()


def game_for_one_person(max_score, last_score):
    global screen, time_to_delay, fullscreen, SCREEN_WIDTH, SCREEN_HEIGHT, speed, next_score, sec_before_start
    done = False
    key_right_pressed = False
    key_left_pressed = False
    file = "settings."
    lines = []
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("SCREEN_HEIGHT: 750\nSCREEN_WIDTH: 600\nFPS: 100\nStart speed: 3\nNext score: 50\nSeconds before start: 5")
        f.close()
    f = open(file, "r+")
    data = f.read()
    lines = data.split('\n')
    for line_num in range(0, len(lines)):
        lines[line_num] = lines[line_num].split(": ")[1]
    f.close()
    speed = float(lines[3])
    next_score = int(lines[4])
    sec_before_start = int(lines[5])
    #=================================================
    p = player(300, 700, speed)
    asteroids = []
    asteroids.append(asteroid(speed*3, -SCREEN_HEIGHT//3))
    asteroids.append(asteroid(speed*3, -SCREEN_HEIGHT//3*2))
    asteroids.append(asteroid(speed*3, 0))
    #=================================================

    asteroid.score = 0
    score = 0
    sec = 1001
    count_left = sec_before_start 
    count_left += 1
    counting_text = text(str(sec_before_start), 250, 250, (0, 200, 0), 300)
    while not done:
        if sec > 1000 and count_left != 0:
            screen.fill((0, 0, 0))
            count_left -= 1
            counting_text.draw(str(count_left))
            sec = 0
        pygame.time.delay(time_to_delay)
        sec += time_to_delay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    key_right_pressed = False
                    key_left_pressed = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    key_left_pressed = False
                    key_right_pressed = True
                if event.key == pygame.K_F11  and not fullscreen:
                    fullscreen = True
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                elif event.key == pygame.K_F11  and fullscreen:
                    fullscreen = False
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        key_right_pressed = True
                    key_left_pressed = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        key_left_pressed = True

                    key_right_pressed = False
        if count_left == 0:
            screen.fill((0, 0, 0))
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
            t = text("Score: " + str(score), 230, 10, (255, 255, 255), 50)
            t.draw()
        pygame.display.flip()
    file = "score."
    f = open(file, "w")
    f.write("Max score: " + str(max_score))
    f.close()
    file = "statistic."
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("0")
        f.close()
    f = open(file, "a+")
    if score > 20:
        f.write('\n' + str(score))
    f.close()
    menu()

def game_for_two_persons(max_score, last_score):
    global screen, time_to_delay, fullscreen, SCREEN_WIDTH, SCREEN_HEIGHT, speed, next_score, sec_before_start
    done = False
    key_left_pressed_p1 = False
    key_right_pressed_p1 = False
    key_left_pressed_p2 = False
    key_right_pressed_p2 = False
    file = "settings."
    lines = []
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("SCREEN_HEIGHT: 750\nSCREEN_WIDTH: 600\nFPS: 100\nStart speed: 3\nNext score: 50\nSeconds before start: 5")
        f.close()
    f = open(file, "r+")
    data = f.read()
    lines = data.split('\n')
    for line_num in range(0, len(lines)):
        lines[line_num] = lines[line_num].split(": ")[1]
    f.close()
    speed = float(lines[3])
    next_score = int(lines[4])
    sec_before_start = int(lines[5])
    #=================================================
    p1 = player(300, 700, speed, (0,255,0))
    p2 = player(300, 700, speed, (255,0,0))
    asteroids = []
    asteroids.append(asteroid(speed*3, -SCREEN_HEIGHT//3))
    asteroids.append(asteroid(speed*3, -SCREEN_HEIGHT//3*2))
    asteroids.append(asteroid(speed*3, 0))
    #=================================================
    done_p1 = False
    done_p2 = False
    asteroid.score = 0
    score = 0
    sec = 1001
    count_left = sec_before_start 
    count_left += 1
    counting_text = text(str(sec_before_start), 250, 250, (0, 200, 0), 300)
    while not done:
        if sec > 1000 and count_left != 0:
            screen.fill((0, 0, 0))
            count_left -= 1
            counting_text.draw(str(count_left))
            sec = 0
        pygame.time.delay(time_to_delay)
        sec += time_to_delay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                if event.key == pygame.K_a:
                    key_right_pressed_p1 = False
                    key_left_pressed_p1 = True
                if event.key == pygame.K_LEFT:
                    key_right_pressed_p2 = False
                    key_left_pressed_p2 = True
                if event.key == pygame.K_d:
                    key_left_pressed_p1 = False
                    key_right_pressed_p1 = True
                if event.key == pygame.K_RIGHT:
                    key_left_pressed_p2 = False
                    key_right_pressed_p2 = True
                if event.key == pygame.K_F11 and not fullscreen:
                    fullscreen = True
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                elif event.key == pygame.K_F11 and fullscreen:
                    fullscreen = False
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_d]:
                        key_right_pressed_p1 = True
                    key_left_pressed_p1 = False
                if event.key == pygame.K_RIGHT:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        key_right_pressed_p2 = True
                    key_right_pressed_p2 = False
                if event.key == pygame.K_d:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a]:
                        key_left_pressed_p1 = True
                    key_right_pressed_p1 = False
                if event.key == pygame.K_LEFT:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RIGHT]:
                        key_right_pressed_p2 = True
                    key_left_pressed_p2 = False
        if count_left == 0:
            screen.fill((0, 0, 0))
            if done_p2:
                p2.move(key_left_pressed_p2, key_right_pressed_p2, speed)
                p2.draw((70,0,0))
            if done_p1:
                p1.move(key_left_pressed_p1, key_right_pressed_p1, speed)
                p1.draw((0,70,0))
            
            if done_p2 == False:
                p2.move(key_left_pressed_p2, key_right_pressed_p2, speed)
                p2.draw()
            if done_p1 == False:
                p1.move(key_left_pressed_p1, key_right_pressed_p1, speed)
                p1.draw()

            
            if done_p1 and done_p2:
                done = True

            for object in asteroids[:]:
                score = asteroid.move(object, speed*3)
                if p1.player_obj.colliderect(asteroid.draw(object)):
                    done_p1 = True
                if p2.player_obj.colliderect(asteroid.draw(object)):
                    done_p2 = True
            if max_score < score:
                max_score = score
            if next_score < score:
                next_score += 10
                speed += 0.2
            t = text("Score: " + str(score), 230, 10, (255, 255, 255), 50)
            t.draw()
        pygame.display.flip()
    file = "score."
    f = open(file, "w")
    f.write("Max score: " + str(max_score))
    f.close()
    file = "statistic."
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("0")
        f.close()
    f = open(file, "a+")
    if score > 20:
        f.write('\n' + str(score))
    f.close()
    menu()


def game_for_four_persons(max_score, last_score):
    global screen, time_to_delay, fullscreen, SCREEN_WIDTH, SCREEN_HEIGHT, speed, next_score, sec_before_start
    done = False
    key_left_pressed_p1 = False
    key_right_pressed_p1 = False
    key_left_pressed_p2 = False
    key_right_pressed_p2 = False
    key_left_pressed_p3 = False
    key_right_pressed_p3 = False
    file = "settings."
    lines = []
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("SCREEN_HEIGHT: 750\nSCREEN_WIDTH: 600\nFPS: 100\nStart speed: 3\nNext score: 50\nSeconds before start: 5")
        f.close()
    f = open(file, "r+")
    data = f.read()
    lines = data.split('\n')
    for line_num in range(0, len(lines)):
        lines[line_num] = lines[line_num].split(": ")[1]
    f.close()
    speed = float(lines[3])
    next_score = int(lines[4])
    sec_before_start = int(lines[5])
    #=================================================
    p1 = player(200, 700, speed, (0,255,0))
    p2 = player(300, 700, speed, (255,0,0))
    p3 = player(400, 700, speed, (0,0,255))
    p4 = player(500, 700, speed, (0,255,255))
    asteroids = []
    asteroids.append(asteroid(speed*3, -SCREEN_HEIGHT//3))
    asteroids.append(asteroid(speed*3, -SCREEN_HEIGHT//3*2))
    asteroids.append(asteroid(speed*3, 0))
    #=================================================
    done_p1 = False
    done_p2 = False
    done_p3 = False
    done_p4 = False
    asteroid.score = 0
    score = 0
    sec = 1001
    count_left = sec_before_start 
    count_left += 1
    counting_text = text(str(sec_before_start), 250, 250, (0, 200, 0), 300)
    while not done:
        if sec > 1000 and count_left != 0:
            screen.fill((0, 0, 0))
            count_left -= 1
            counting_text.draw(str(count_left))
            sec = 0
        pygame.time.delay(time_to_delay)
        sec += time_to_delay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                if event.key == pygame.K_a:
                    key_right_pressed_p1 = False
                    key_left_pressed_p1 = True
                if event.key == pygame.K_LEFT:
                    key_right_pressed_p2 = False
                    key_left_pressed_p2 = True
                if event.key == pygame.K_KP_3:
                    key_right_pressed_p3 = False
                    key_left_pressed_p3 = True

                if event.key == pygame.K_d:
                    key_left_pressed_p1 = False
                    key_right_pressed_p1 = True
                if event.key == pygame.K_RIGHT:
                    key_left_pressed_p2 = False
                    key_right_pressed_p2 = True
                if event.key == pygame.K_KP_9:
                    key_left_pressed_p3 = False
                    key_right_pressed_p3 = True
                if event.key == pygame.K_F11 and not fullscreen:
                    fullscreen = True
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                elif event.key == pygame.K_F11 and fullscreen:
                    fullscreen = False
                    screen = pygame.display.set_mode(
                        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_d]:
                        key_right_pressed_p1 = True
                    key_left_pressed_p1 = False
                if event.key == pygame.K_RIGHT:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]:
                        key_right_pressed_p2 = True
                    key_right_pressed_p2 = False
                if event.key == pygame.K_KP_9:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_KP_3]:
                        key_right_pressed_p3 = True
                    key_right_pressed_p3 = False
                if event.key == pygame.K_d:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a]:
                        key_left_pressed_p1 = True
                    key_right_pressed_p1 = False
                if event.key == pygame.K_LEFT:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RIGHT]:
                        key_right_pressed_p2 = True
                    key_left_pressed_p2 = False
                if event.key == pygame.K_KP_3:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_KP_9]:
                        key_right_pressed_p3 = True
                    key_left_pressed_p3 = False
        if count_left == 0:
            screen.fill((0, 0, 0))
            if not done_p4:
                p4.move(pygame.mouse.get_pressed()[0], pygame.mouse.get_pressed()[2], speed)
                p4.draw()
            if not done_p3:
                p3.move(key_left_pressed_p3, key_right_pressed_p3, speed)
                p3.draw()
            if not done_p2:
                p2.move(key_left_pressed_p2, key_right_pressed_p2, speed)
                p2.draw()
            if not done_p1:
                p1.move(key_left_pressed_p1, key_right_pressed_p1, speed)
                p1.draw()
            

            
            if done_p1 and done_p2 and done_p3 and done_p4:
                done = True

            for object in asteroids[:]:
                score = asteroid.move(object, speed*3)
                if p1.player_obj.colliderect(asteroid.draw(object)):
                    done_p1 = True
                if p2.player_obj.colliderect(asteroid.draw(object)):
                    done_p2 = True
                if p3.player_obj.colliderect(asteroid.draw(object)):
                    done_p3 = True
                if p4.player_obj.colliderect(asteroid.draw(object)):
                    done_p4 = True
            if max_score < score:
                max_score = score
            if next_score < score:
                next_score += 10
                speed += 0.2
            t = text("Score: " + str(score), 230, 10, (255, 255, 255), 50)
            t.draw()
        pygame.display.flip()
    file = "score."
    f = open(file, "w")
    f.write("Max score: " + str(max_score))
    f.close()
    file = "statistic."
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("0")
        f.close()
    f = open(file, "a+")
    if score > 20:
        f.write('\n' + str(score))
    f.close()
    menu()


def statistic_graph():
    global fullscreen, screen
    file = "statistic."
    lines = []
    if not os.path.exists(file):
        open(file, "x")
        f = open(file, "w")
        f.write("0")
        f.close()
    f = open(file, "r+")
    data = f.read()
    lines = data.split('\n')
    f.close()
    move_left = 0
    show_lines = lines
    if len(lines) > 50:
        show_lines = lines[len(lines)-50:]

    # ====================
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 500
    FPS = 30
    # ====================
    max_num = 0
    for check_num in lines:
        check_num = int(check_num)
        if max_num < check_num:
            max_num = check_num
    if not max_num == 0:
        proportion = SCREEN_HEIGHT/5*4/max_num
    else:
        proportion = 0
    time_to_delay = int(1000/FPS)
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
    coficent_x = SCREEN_WIDTH / len(show_lines)
    line_number = 0
    for line in show_lines:
        num = int(line)

        if not line_number >= len(show_lines)-1:
            next_num = int(show_lines[line_number + 1])
            pygame.draw.line(screen, (0, 255, 0),  ((line_number+1)*coficent_x, SCREEN_HEIGHT -
                             proportion*next_num), (line_number * coficent_x, SCREEN_HEIGHT - proportion * num))
        line_number += 1

    pygame.display.flip()
    closed = False
    while not closed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    closed = True
                if event.key == pygame.K_LEFT:
                    move_left += 1
                    if move_left > len(lines) - 50:
                        move_left = len(lines) - 50
                    if len(lines) > 50:
                        show_lines = lines[len(lines)-50-move_left:-move_left]
                if event.key == pygame.K_RIGHT:
                    move_left -= 1
                    if move_left <= 1:
                        move_left = 0
                    if len(lines) > 50:
                        show_lines = lines[len(lines) - 50 - move_left : -1 * move_left]
                        if move_left == 0:
                            show_lines = lines[len(lines) - 50 - move_left :]
        if fullscreen:
            screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        else:
            screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE | pygame.SCALED)

        screen.fill((0, 0, 0))
        line_number = 0
        for line in show_lines:
            num = int(line)

            if not line_number >= len(show_lines)-1:
                next_num = int(show_lines[line_number + 1])
                if next_num > num:
                    pygame.draw.line(screen, (0, 255, 0),  ((line_number+1)*coficent_x, SCREEN_HEIGHT -
                                     proportion*next_num), (line_number * coficent_x, SCREEN_HEIGHT - proportion * num), 3)
                elif next_num < num:
                    pygame.draw.line(screen, (255, 0, 0),  ((line_number+1)*coficent_x, SCREEN_HEIGHT -
                                     proportion*next_num), (line_number * coficent_x, SCREEN_HEIGHT - proportion * num), 3)
                else:
                    pygame.draw.line(screen, (255, 255, 0),  ((line_number+1)*coficent_x, SCREEN_HEIGHT -
                                     proportion*next_num), (line_number * coficent_x, SCREEN_HEIGHT - proportion * num), 3)
            if int(coficent_x) > 60:
                text_size = 60
            else:
                text_size = int(coficent_x)
            text.draw(text(line, line_number * coficent_x, SCREEN_HEIGHT -
                      proportion * num - 25, (255, 255, 255), text_size))
            line_number += 1
        pygame.display.flip()
        pygame.time.delay(time_to_delay)
    menu()


menu()
