import pygame
from pygame import mixer
import time
import random

pygame.init()
pygame.display.set_caption('SNAKE GAME')
height, width = 800, 900
screen = pygame.display.set_mode((width, height))
myfont = pygame.font.SysFont("arial", 72, True)
score = pygame.font.SysFont("arial", 30, True)
background = pygame.image.load("SBG.jpg")

menu = True
game = False
game_pause = False
game_music = True

# Initialize Sounds
mixer.init()
snake_bite = mixer.Sound("SNAKE_BITE.ogg")
snake_move = mixer.Sound("SNAKE_MOVE.ogg")
snake_crash = mixer.Sound("SNAKE_COLLISION.ogg")
game_over = mixer.Sound("GAME_OVER.ogg")
level_up = mixer.Sound("LEVEL_UP.ogg")
game_intro = mixer.Sound("GAME_INTRO.ogg")

# INITIALIZE FRUIT POSITION
f_x = 80
f_y = 60
# SET INITIAL DIRECTION
new_dir = None
curr_dir = None
# INITIALIZE SNAKE'S POSITION
cur_x = 300
cur_y = 300
# SET THE GRID AND BLOCK SIZE
bsize = 20
# SNAKE TAIL AND PREVIOUS POSITIONS AND BODY COLOR
body_color = (255,255,255)
snake_body_color = (0,255,0)
snake_body = []
prev_2x = 0
prev_2y = 0
prev_x = 0
prev_y = 0
fruit_hit = False
# INITIALIZE COIN ADDER
coin = 10
# INITIALIZE PLAYGROUND HEIGHT WIDTH
pg_h = 660
pg_w = 500
origin_pg_x = 40
origin_pg_y = 40

# INITIALIZE SCORE
playerscore = 0
# INITIALIZE ACHIEVEMENTS
ach = [50, 100, 1000, 5000, 10000, 50000, 100000, 300000]




def snake_collision():
    global fruit_hit, game_music
    if [cur_x, cur_y] in snake_body and fruit_hit is not True:
        if game_music:
            snake_crash.play()
        return True
    else:
        fruit_hit = False
    return False


def draw_grid():
    global width, height, screen, bsize
    for x_axis in range(width):
        for y_axis in range(height):
            rect = pygame.Rect(x_axis * bsize, y_axis * bsize, bsize, bsize)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)


def fruit_randomize_and_collision():
    global cur_x, cur_y, f_x, f_y, snake_body, playerscore, game_music, coin
    if cur_x == f_x and cur_y == f_y:
        if game_music:
            snake_bite.play()
        playerscore += coin
        f_x = random.randrange(origin_pg_x, pg_w, bsize)
        f_y = random.randrange(origin_pg_y, pg_h, bsize)
        snake_body.append([cur_x, cur_y])
        return True
    return False


def movements(new_dir):
    global curr_dir, cur_x, cur_y, game_music
    # To Disregard opposite direction changes
    if curr_dir == 'u' and new_dir == 'd':
        pass
    elif curr_dir == 'd' and new_dir == 'u':
        pass
    elif curr_dir == 'r' and new_dir == 'l':
        pass
    elif curr_dir == 'l' and new_dir == 'r':
        pass
    else:
        if new_dir != curr_dir:
            if game_music:
                snake_move.play()

        curr_dir = new_dir

    # TO UPDATE DIRECTION
    if curr_dir == 'd':
        cur_y = cur_y + bsize

    elif curr_dir == 'u':
        cur_y = cur_y - bsize

    elif curr_dir == 'l':
        cur_x = cur_x - bsize

    elif curr_dir == 'r':
        cur_x = cur_x + bsize


def check_boundaries():
    global cur_x, cur_y
    # TO CHECK BOUNDARIES

    if cur_x >= pg_w + 20:
        cur_x = origin_pg_x
        return True
    elif cur_x <= origin_pg_x - 20:
        cur_x = pg_w
        return True
    if cur_y >= pg_h + 40:
        cur_y = origin_pg_y
        return True
    elif cur_y <= origin_pg_y - 20:
        cur_y = pg_h
        return True

    return False


def instructions():
    global game_pause,game_music,body_color

    instruct = pygame.font.SysFont("arial", 25, True)
    display = "INSTRUCTIONS:"
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (560, 200))

    instruct = pygame.font.SysFont("arial", 13, True)
    display = "1.USE DIRECTION KEYS TO CONTROL SNAKE "
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (560, 240))

    display = "2.PRESS 'P' TO PAUSE OR PLAY "
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (560, 280))

    display = "3.PRESS 'M' TO STOP OR START BACKGROUND "
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (560, 320))
    display = "AND GAME MUSIC"
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (570, 340))

    rect = pygame.Rect(560, 400, 300, 120)
    pygame.draw.rect(screen, body_color, rect, 3)

    if not game_music:
        switch = "OFF"
    else:
        switch = "ON"
    instruct = pygame.font.SysFont("arial",25,True)
    display = "BGM : "+switch
    text = instruct.render(display, True, (255, 255, 255))
    screen.blit(text, (565, 420))

    instruct = pygame.font.SysFont("arial", 17, True)
    display = "DEVELOPED BY AADITYA PRABU K"
    text = instruct.render(display, True, snake_body_color)
    screen.blit(text, (565, 690))









def show_score():
    global body_color
    rect = pygame.Rect(560, 70, 300, 100)
    pygame.draw.rect(screen, body_color, rect, 3)
    global playerscore
    display = "SCORE:" + str(playerscore)
    text = score.render(display, True, (255, 255, 255))
    screen.blit(text, (565, 105))


def level():
    global coin, ach, game,body_color
    if playerscore in ach:
        ach.pop(0)
        if game_music:
            level_up.play()
        if coin == 10:
            coin = 50
            body_color = (255, 0, 0)
        elif coin == 50:
            coin = 100
            body_color = (255, 111, 0)
        elif coin == 100:
            coin = 500
            body_color = (255, 234, 0)
        elif coin == 500:
            coin = 1000
            body_color = (0, 255, 26)
        elif coin == 2000:
            coin = 5000
            body_color = (0, 255, 238)
        elif coin == 5000:
            coin == 10000
            body_color = (68, 0, 255)
        elif coin == 10000:
            coin = 50000
            body_color = (136, 0, 255)

    if len(snake_body) >= 329999:
        if game_music:
            game_over.play()
        game = False



def update_game():

    global screen, cur_x, cur_y, snake_body, prev_x, prev_y, prev_2x, prev_2y,body_color,snake_body_color
    color_changer = 0
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, body_color, (origin_pg_x - 10, origin_pg_y - 10, pg_w, pg_h + 20), 5)
    show_score()
    level()
    instructions()
    # updates snake's head position
    rect = pygame.Rect(cur_x, cur_y, bsize, bsize)
    pygame.draw.rect(screen,snake_body_color, rect)

    # update snake's body position
    if snake_body:
        prev_x = cur_x
        prev_y = cur_y
        for i in range(len(snake_body)):
            rect = pygame.Rect(snake_body[i][0], snake_body[i][1], bsize, bsize)
            pygame.draw.rect(screen, snake_body_color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            # Update all positions of the body
            prev_2x, prev_2y = snake_body[i]
            snake_body[i] = [prev_x, prev_y]
            prev_x, prev_y = prev_2x, prev_2y
            if color_changer == 0:
                color_changer = 1
                snake_body_color = (255, 0, 0)
            elif color_changer == 1:
                color_changer = 2
                snake_body_color = (255, 111, 0)
            elif color_changer == 2:
                color_changer = 3
                snake_body_color = (255, 234, 0)
            elif color_changer == 3:
                color_changer = 4
                snake_body_color = (0, 255, 26)
            elif color_changer == 4:
                color_changer = 5
                snake_body_color = (0, 255, 238)
            elif color_changer == 5:
                color_changer = 6
                snake_body_color = (68, 0, 255)
            elif color_changer == 6:
                color_changer =0
                snake_body_color = (136, 0, 255)



    # Plot Fruit
    pygame.draw.rect(screen, snake_body_color, (f_x, f_y, bsize, bsize))
    pygame.display.update()


def game_status():

    instruct = pygame.font.SysFont("ARIAL",24,True)
    gamestatus = "GAME  STATUS : PAUSE"
    text = instruct.render(gamestatus, True, (255, 255, 255))
    screen.blit(text, (565, 460))

def game_menu():

    global  menu,game,background
    pygame.display.update()
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    instruct = pygame.font.SysFont("ARIAL", 50, True)
    menumessage = " WELCOME TO SNAKE AND FRUIT"
    game_intro.play()
    text = instruct.render(menumessage, True, (0,0,0))
    screen.blit(text, (23, 20))
    menumessage = " PRESS 'S' TO START "
    text = instruct.render(menumessage, True, (0,0,0))
    screen.blit(text, (23, 300))
    menumessage = " PRESS 'E' TO EXIT "
    text = instruct.render(menumessage, True, (0,0,0))
    screen.blit(text, (23, 600))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game = True
                game_intro.stop()
                update_game()

            if event.key == pygame.K_e:
                menu = False
while menu:
        game_menu()
        while game:
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        new_dir = 'd'
                    elif event.key == pygame.K_UP:
                        new_dir = 'u'
                    elif event.key == pygame.K_LEFT:
                        new_dir = 'l'
                    elif event.key == pygame.K_RIGHT:
                        new_dir = 'r'
                    elif event.key == pygame.K_e:
                        game = False
                    elif event.key == pygame.K_p:
                        if game_pause == False:
                            game_pause = True
                            game_status()
                            pygame.display.update()
                            while game_pause:
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_p:
                                            game_pause = False
                                    if event.type == pygame.QUIT:
                                        game_pause = False
                                        game = False

                    elif event.key == pygame.K_m:
                        if game_music:
                            game_music = False
                        else:
                            game_music = True

            movements(new_dir)

            fruit_hit = fruit_randomize_and_collision()

            if snake_collision():
                if game_music:
                    game_over.play()
                text = myfont.render("GAME OVER", True, (255, 255, 255))
                screen.blit(text, (60, 300))
                pygame.display.flip()
                time.sleep(4)
                game = False

            check_boundaries()
            update_game()
pygame.quit()
