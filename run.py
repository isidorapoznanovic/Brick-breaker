import pygame
import math
import NANS_lib as lb
import numpy as np
import argparse
import time
import random

#VARIABLRS
WIDTH = 1000
HEIGH = 600
BORDER = 10
RADIUS = 20
VELOCITY_X = 1
VELOCITY_Y = 1
FRAMERATE = 400
PADDLEW = 100
PADDLEH = 20
END = False
WIN = False
FINAL_END = False
BRICKH = 50
BRICKW = 120

#define functions
def collision_ball_brick(ball, brick):
    '''
    If a collision between ball and brick occurs this function returns true and position of ball center, otherwise returns false and 0
      3 | 1 | 4
    ------------
      2 |   | 2
    ------------
      5 | 1 | 6
    '''
    
    p = 0

    if ball.x < brick.x: # 2 or 3 or 5
        tempX = brick.x
        p = 10
    elif ball.x > brick.x + brick.w:  # 4 or 2 or 6
        tempX = brick.x + brick.w
        p = 12
    else:
        tempX = ball.x
        p = 1
    
    if p != 1:
        if ball.y < brick.y: # 3 or 1 or 4
            tempY = brick.y
            if p == 10:
                p = 3
            elif p == 12:
                p = 4
        elif ball.y >= brick.y + brick.h: # 5 or 1 or 6
            tempY = brick.y + brick.h
            if p == 10:
                p = 5
            elif p == 12:
                p = 6
        else:
            tempY = ball.y
            p = 2
    elif ball.y < brick.y:
        tempY = brick.y
    else:
        tempY = brick.y + brick.h


    if math.sqrt((tempX - ball.x)**2 + (tempY - ball.y)**2) <= ball.r:
        return True, p
    else:
        return False, 0
    
def collision_ball_paddle(ball, paddle):
    '''
    If a collision between ball and paddle occurs this function returns true and position of ball center, otherwise returns false and 0
      3 | 1 | 4
    -------------
      2 |   | 2
    '''
    p = 0

    tempY = paddle.y

    if ball.x < paddle.x - paddle.w//2:
        tempX = paddle.x - paddle.w//2
        p = 5
    elif ball.x > paddle.x + paddle.w//2:
        tempX = paddle.x + paddle.w//2
        p = 6
    else:
        tempX = ball.x
        p = 1

    if ball.y < paddle.y:
        tempY = ball.y
        if p == 5:
            p = 3
        elif p == 6:
            p = 4

    if math.sqrt((tempX - ball.x)**2 + (tempY - ball.y)**2) <= ball.r:
        return True, p
    else:
        return False, 0

def collision_ball_ball(ball1, ball2):
    if np.sqrt((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2 ) < ball1.r + ball2.r:
        return True
    else:
        return False

def calculate_velocity(x1, y1, x2, y2, vx, vy, p, w, h):  #x1, y1 je krug
    if p == 1:
        return vx, -vy
    elif p == 2:
        return -vx, vy
    elif p == 3:
        fx1 = np.array([x1, x2])
        fy1 = np.array([y1, y2])
        p = lb.lagrange_interpolation(fx1, fy1)
        interscCR = np.polyval(p, 0)
        koef = math.sqrt(2) / math.sqrt((0 - x2)**2 + (interscCR - y2)**2)
        vx = abs(0 - x2) * koef
        vy = abs(interscCR - y2) * koef
        return -vy, -vx
    elif p == 4:
        x2 = x2 + w
        fx1 = np.array([x1,x2])
        fy1 = np.array([y1,y2])
        p = lb.lagrange_interpolation(fx1, fy1)
        interscCR = np.polyval(p, WIDTH)
        koef = math.sqrt(2) / math.sqrt((WIDTH - x2)**2 + (interscCR - y2)**2)
        vx = (WIDTH - x2) * koef
        vy = (interscCR - y2) * koef
        return -vy, -vx
    elif p == 5:
        y2 = y2 + h
        fx1 = np.array([x1, x2])
        fy1 = np.array([y1, y2])
        p = lb.lagrange_interpolation(fx1, fy1)
        interscCR = np.polyval(p, 0)
        koef = math.sqrt(2) / math.sqrt((0 - x2)**2 + (interscCR - y2)**2)
        vx = (0 - x2) * koef
        vy = (interscCR - y2) * koef
        return -vy, -vx
    elif p == 6:
        x2 = x2 + w
        y2 = y2 + h
        fx1 = np.array([x1,x2])
        fy1 = np.array([y1,y2])
        p = lb.lagrange_interpolation(fx1, fy1)
        interscCR = np.polyval(p, WIDTH)
        koef = math.sqrt(2) / math.sqrt((WIDTH - x2)**2 + (interscCR - y2)**2)
        vx  = -(WIDTH - x2) * koef
        vy = -(interscCR - y2) * koef
        return -vy, -vx

    return vx, vy
#TODO spoji ifove
def calculate_velocity_ball_ball(ball1, ball2):
    temp = ball1.vx
    if ball1.x < ball2.x and ball1.y < ball2.y:
        if ball1.vx*ball1.vy < 0:
            ball1.vx = np.sign(ball1.vx)*abs(ball1.vy)
            ball1.vy = np.sign(ball1.vy)*abs(temp)
            return ball1.vx, ball1.vy
        else:
            ball1.vx = -np.sign(ball1.vx)*abs(ball1.vy)
            ball1.vy = -np.sign(ball1.vy)*abs(temp)
            return ball1.vx, ball1.vy
    elif ball1.x < ball2.x and ball1.y > ball2.y:
        if ball1.vx*ball1.vy > 0:
            ball1.vx = ball1.vy
            ball1.vy = temp
            return ball1.vx, ball1.vy
        else:
            ball1.vx = -np.sign(ball1.vx)*abs(ball1.vy)
            ball1.vy = -np.sign(ball1.vy)*abs(temp)
            return ball1.vx, ball1.vy
    elif ball1.x > ball2.x and ball1.y < ball2.y:
        if ball1.vx*ball1.vy > 0:
            ball1.vx = ball1.vy
            ball1.vy = temp
            return ball1.vx, ball1.vy
        else:
            ball1.vx = -np.sign(ball1.vx)*abs(ball1.vy)
            ball1.vy = -np.sign(ball1.vy)*abs(temp)
            return ball1.vx, ball1.vy
    elif ball1.x > ball2.x and ball1.y > ball2.y:
        if ball1.vx*ball1.vy < 0:
            ball1.vx = np.sign(ball1.vx)*abs(ball1.vy)
            ball1.vy = np.sign(ball1.vy)*abs(temp)
            return ball1.vx, ball1.vy
        else:
            ball1.vx = -np.sign(ball1.vx)*abs(ball1.vy)
            ball1.vy = -np.sign(ball1.vy)*abs(temp)
            return ball1.vx, ball1.vy
    elif ball1.x == ball2.x:
        return temp, -ball1.vy
    elif ball1.y == ball2.y:
        return -ball1.vx, ball1.vy
    else:
        print('kako')
        return ball1.vx, ball1.vy

def level(a, b):
    list = []
    x = np.linspace(50, WIDTH - BORDER - BRICKW - 50, a)
    for j in range(b):
        for i in range(len(x)):
            brick = Brick(x[i], 50 + 60*j)
            list.append(brick)
    return list

def spaceBricks(bricks):
    maxx = 0
    maxy = 0
    minx = WIDTH
    miny = HEIGH

    for i in range(len(bricks)):
        if(bricks[i].x + bricks[i].w > maxx):
            maxx = bricks[i].x + bricks[i].w
        if(bricks[i].x < minx):
            minx = bricks[i].x
        if(bricks[i].y + bricks[i].h > maxy):
            maxy = bricks[i].y + bricks[i].h
        if(bricks[i].y < miny):
            miny = bricks[i].y

    return minx, maxx, miny, maxy

#functions for graphics

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGH))
clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 48)
font1 = pygame.font.SysFont('arial', 32)

color_active = pygame.Color('white')
color_passive = pygame.Color('gray30')
color = color_passive

three_pl_rect = pygame.Rect(200, 200, 140, 64)
four_pl_rect = pygame.Rect(350, 200, 140, 64)
five_pl_rect = pygame.Rect(500, 200, 140, 64)
six_pl_rect = pygame.Rect(650, 200, 140, 64)
color1 = [color_passive, color_passive, color_passive, color_passive]


def welcome():
	welcome_text1 = font.render("     Welcome to", True, (255, 255, 255))
	display.blit(welcome_text1, (300, 130))
	welcome_text2 = font.render("brick breaker", True, (255, 255, 255))
	display.blit(welcome_text2, (350, 180))
	welcome_text3 = font1.render("      Press enter to play!", True, (255, 255, 255))
	display.blit(welcome_text3, (300, 400))

def num_of_balls():
	num_of_balls_text = font.render("Select number of balls", True, (255, 255, 255))
	display.blit(num_of_balls_text, (270, 130))

def pl_choice():
	three_pl_text = font.render("    1", True, (255, 255, 255))
	display.blit(three_pl_text, (205, 205))
	pygame.draw.rect(display, color1[0], three_pl_rect, 2)
	four_pl_text = font.render("    2", True, (255, 255, 255))
	display.blit(four_pl_text, (355, 205))
	pygame.draw.rect(display, color1[1], four_pl_rect, 2)
	five_pl_text = font.render("    3", True, (255, 255, 255))
	display.blit(five_pl_text, (505, 205))
	pygame.draw.rect(display, color1[2], five_pl_rect, 2)
	six_pl_text = font.render("    4", True, (255, 255, 255))
	display.blit(six_pl_text, (655, 205))
	pygame.draw.rect(display, color1[3], six_pl_rect, 2)

def goodbye(b):
    if b == True:
	    welcome_text1 = font.render(" You won!", True, (255, 255, 255))
	    display.blit(welcome_text1, (370, 180))
    else:
	    welcome_text2 = font.render("   You lose...", True, (255, 255, 255))
	    display.blit(welcome_text2, (350, 180))
    welcome_text3 = font1.render("    Press enter to play again or q to quit!", True, (255, 255, 255))
    display.blit(welcome_text3, (220, 400))

#define classes
class Ball:

    r = RADIUS
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self, color):
        global display
        pygame.draw.circle(display, color, (self.x, self.y), self.r)

    def update(self, paddle, bricks, balls):
        global bg_color, fg_color

        tempx = self.x + self.vx
        tempy = self.y + self.vy

        #collision with borders
        if tempx < BORDER + self.r or tempx > WIDTH - BORDER - self.r:  #left and right border
            self.vx = - self.vx
        elif tempy < BORDER + self.r:   #top border
            self.vy = - self.vy

        #collision with paddle
        if tempy > HEIGH - paddle.h - self.r - 1:
            
            is_coll, poss_coll = collision_ball_paddle(self, paddle)

            if is_coll:
                self.vx, self.vy = calculate_velocity(tempx, tempy, paddle.x - paddle.w, paddle.y, self.vx, self.vy, poss_coll, paddle.w, paddle.h)

            if tempy > HEIGH:
                global END
                END = True
        
        #collision with bricks
        if(len(bricks) != 0):
            minx, maxx, miny, maxy = spaceBricks(bricks)
            if tempx > minx - self.r - 1 and tempx < maxx + self.r + 1 and tempy > miny - self.r - 1 and tempy < maxy + self.r + 1:
                for i in range(len(bricks)):
                    is_coll, poss_coll = collision_ball_brick(self, bricks[i])
                    if is_coll:
                        self.vx, self.vy = calculate_velocity(tempx, tempy, bricks[i].x, bricks[i].y, self.vx, self.vy, poss_coll, bricks[i].w, bricks[i].h)
                        bricks[i].show_and_update(bg_color)
                        bricks.remove(bricks[i])
                        break
        else:
            END = True
            global WIN
            WIN = True

        #collision with balls
        for i in range(num_balls):
            if (self != balls[i] and collision_ball_ball(self, balls[i]) == True):
                self.vx, self.vy = calculate_velocity_ball_ball(self, balls[i])

    def repaint(self):
        self.show(bg_color)
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.show(fg_color)


class Paddle:

    w = PADDLEW
    h = PADDLEH
    y = HEIGH - h

    def __init__(self, x):  #center of the paddle
        self.x = x

    def show(self, color):
        global display
        pygame.draw.rect(display, color, pygame.Rect((self.x - self.w//2, HEIGH - self.h), (self.w, self.h)))

    def update(self):
        global bg_color, fg_color
        self.show(bg_color)
        self.x = pygame.mouse.get_pos()[0]
        self.show(fg_color)

class Brick:
    
    h = BRICKH
    w = BRICKW

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show_and_update(self, color):
        global display
        pygame.draw.rect(display, color, pygame.Rect((self.x, self.y), (self.w, self.h)))

#parameters

parser = argparse.ArgumentParser(prog='PROG')

group = parser.add_mutually_exclusive_group()
arg = group.add_argument('-g', action='store_true', help='Graphic environment')
group.add_argument('-balls', type=int, default=1, help='Number of balls')

group1 = parser.add_mutually_exclusive_group()
group1._group_actions.append(arg)
group1.add_argument('-rows', type=int, default=4, help="Number of rows")

group2 = parser.add_mutually_exclusive_group()
group2._group_actions.append(arg)
group2.add_argument('-cols', type=int, default=5, help="Number of collumns")

parser.add_argument('-r', action='store_true', help='Random velocities')

args = parser.parse_args()

#create objects

scene1 = True
scene2 = True
while not FINAL_END:
    END = False
    WIN = False
    if args.r:
        random.seed(time.time())
        VELOCITY_Y = random.uniform(0, math.sqrt(2))
        VELOCITY_X = random.choice((-1,1))*math.sqrt(2 - VELOCITY_Y**2)
    paddleplay = Paddle(WIDTH//2)

    balls = []
    if not args.g:
        num_balls = args.balls
        bricks_row = args.rows
        bricks_col = args.cols

        for i in range(num_balls):
            ballplay = Ball(WIDTH//2 - i*2*Ball.r, HEIGH - Ball.r - paddleplay.h - 1 - i*2*Ball.r, -VELOCITY_X, -VELOCITY_Y)
            balls.append(ballplay)

        bricks = level(bricks_row, bricks_col)

#Draw scenario

    pygame.init()

    if args.g:
        while scene1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scene1 = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        scene1 = False

            display.fill((0, 100, 200))
            welcome()
            clock.tick(30)
            pygame.display.update()

        nop = 0
        k = -1

        while scene2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scene2 = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        color1[0] = color_active
                        k = 0
                    if k in [1, 2]:
                        if event.key == pygame.K_RETURN:
                            scene2 = False
                            nop = k + 1
                        if event.key == pygame.K_LEFT:
                            color1[k] = color_passive
                            k -= 1
                            color1[k] = color_active
                        if event.key == pygame.K_RIGHT:
                            color1[k] = color_passive
                            k += 1
                            color1[k] = color_active				
                    elif k == 0:
                        if event.key == pygame.K_RETURN:
                            scene2 = False
                            nop = k + 1
                        if event.key == pygame.K_RIGHT:
                            color1[k] = color_passive
                            k += 1
                            color1[k] = color_active
                    elif k == 3:
                        if event.key == pygame.K_RETURN:
                            scene2 = False
                            nop = k + 1
                        if event.key == pygame.K_LEFT:
                            color1[k] = color_passive
                            k -= 1
                            color1[k] = color_active			

                if event.type == pygame.MOUSEBUTTONDOWN:	
                        
                    if three_pl_rect.collidepoint(event.pos):
                        color1[0] = color_active
                        color1[1] = color_passive
                        color1[2] = color_passive
                        color1[3] = color_passive
                        scene2 = False
                        nop = 1

                    if four_pl_rect.collidepoint(event.pos):
                        color1[1] = color_active
                        color1[0] = color_passive
                        color1[2] = color_passive
                        color1[3] = color_passive
                        scene2 = False
                        nop = 2

                    if five_pl_rect.collidepoint(event.pos):
                        color1[2] = color_active
                        color1[0] = color_passive
                        color1[1] = color_passive
                        color1[3] = color_passive
                        scene2 = False
                        nop = 3

                    if six_pl_rect.collidepoint(event.pos):
                        color1[3] = color_active
                        color1[0] = color_passive
                        color1[1] = color_passive
                        color1[2] = color_passive
                        scene2 = False
                        nop = 4

            display.fill((0, 100, 200))
            num_of_balls()
            pl_choice()
            clock.tick(30)
            pygame.display.update()
            if nop != 0:
                time.sleep(0.3)
                num_balls = nop
                
        for i in range(num_balls):
            ballplay = Ball(WIDTH//2 - i*2*Ball.r, HEIGH - Ball.r - paddleplay.h - 1 - i*2*Ball.r, -VELOCITY_X, -VELOCITY_Y)
            balls.append(ballplay)
        
        bricks = level(3, 5)
    else:
        num_balls = args.balls
        bricks_row = args.rows
        bricks_col = args.cols

    display.fill((0,0,0))
    pygame.display.update()

    fg_color = pygame.Color("white")
    bg_color = pygame.Color("black")

    pygame.draw.rect(display, fg_color, pygame.Rect((0,0), (WIDTH, BORDER)))
    pygame.draw.rect(display, fg_color, pygame.Rect((0,0), (BORDER, HEIGH - PADDLEH)))
    pygame.draw.rect(display, fg_color, pygame.Rect((WIDTH - BORDER, 0), (BORDER, HEIGH - PADDLEH)))

    for i in range(num_balls):
        balls[i].show(fg_color)

    paddleplay.show(fg_color)

    for i in range(len(bricks)):
        bricks[i].show_and_update(fg_color)

    clock = pygame.time.Clock()

    scene3 = True
    while not END:
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break

        clock.tick(FRAMERATE)

        pygame.display.flip()
        for i in range(num_balls):
            balls[i].update(paddleplay, bricks, balls)
        for i in range(num_balls):
            balls[i].repaint()   
        paddleplay.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END = True
                FINAL_END = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    if(len(bricks) > 1):
                        bricks[len(bricks)-1].show_and_update(bg_color)
                        bricks.pop()
    if WIN == True:
        print("You won!")
    else:
        print("You lose...")
    if args.g:
        while scene3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    scene3 = False
                    FINAL_END = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        scene3 = False
                    if event.key == pygame.K_q:
                        scene3 = False
                        FINAL_END = True

            display.fill((0, 100, 200))
            goodbye(WIN)
            clock.tick(30)
            pygame.display.update()
    else:
        FINAL_END = True

pygame.quit()
