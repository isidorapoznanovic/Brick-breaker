import pygame
import pymunk
import math
import NANS_lib as lb
import numpy as np

#VARIABLRS
WIDTH = 1000
HEIGH = 600
BORDER = 10
RADIUS = 10
VELOCITY = 1
FRAMERATE = 400
PADDLEW = 100
PADDLEH = 20
END = False
BRICKH = 50
BRICKW = 120
IMMUNITY = PADDLEH//2 + 1
#define functions
def collision_ball_rect(ball, rect):
    '''
    If collision happen this function returns true and position of ball center, otherwise returns false and 0
      3 | 1 | 4
    -------------
      2 |   | 2
    -------------
      5 | 1 | 6
    '''
    
    p = 0
    tempX = ball.x
    tempY = ball.y

    if ball.x < rect.x: # 2 or 3 or 5
        tempX = rect.x
        p = 10
    elif ball.x > rect.x + rect.w:  # 4 or 2 or 6
        tempX = rect.x + rect.w
        p = 12
    else:
        p = 1

    if ball.y < rect.y: # 3 or 1 or 4
        tempY = rect.y
        if p == 10:
            p = 3
        elif p == 12:
            p = 4
    elif ball.y > rect.y + rect.h: # 5 or 1 or 6
        tempY = rect.y + rect.h
        if p == 10:
            p = 5
        elif p == 12:
            p = 6
    else:
        p = 2

    if math.sqrt((tempX - ball.x)**2 + (tempY - ball.y)**2) <= 0:
        return True, p
    else:
        return False, 0
    
def collision_ball_paddle(ball, paddle):
    '''
    If collision happen this function returns true and position of ball center, otherwise returns false and 0
      3 | 1 | 4
    -------------
      2 |   | 2
    '''
    p = 0

    tempX = ball.x
    tempY = ball.y

    if ball.x < paddle.x - paddle.w//2:
        tempX = paddle.x - paddle.w//2
        p = 5
    elif ball.x > paddle.x + paddle.w//2:
        tempX = paddle.x + paddle.w//2
        p = 6
    else:
        p = 1

    if ball.y < paddle.y:
        tempY = paddle.y
        if p == 5:
            p = 3
        elif p == 6:
            p = 4

    if math.sqrt((tempX - ball.x)**2 + (tempY - ball.y)**2) <= ball.r:
        return True, p
    else:
        return False, 0

#NECE RADITI LEPO JER NE GLEDAMO U ODNOSU NA KOJE TACNO TEME  
def calculate_velocity(x1, y1, x2, y2, vx, vy, p, w=0, h=0):  #x1, y1 je krug

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
        #koef = math.sqrt((x1 - x2)**2 + (y1 - y2)**2) / math.sqrt((0 - x2)**2 + (interscCR - y2)**2) #radijus nije koren iz dva budalo
        # print(koef)
        # print(x1, y1, x2, y2)
        vx = math.sqrt((0 - x2)**2) * koef
        vy = math.sqrt((interscCR - y2)**2) * koef
        return -vy, -vx
    elif p == 4:
        fx1 = np.array([x1,x2+w])
        fy1 = np.array([y1,y2])
        p = lb.lagrange_interpolation(fx1, fy1)
        interscCR = np.polyval(p, w)
        koef = math.sqrt(2) / math.sqrt((w - x2)**2 + ( interscCR - y2)**2)
        vx = d = math.sqrt((w - x2)**2) * koef
        vy = math.sqrt((np.polyval(p, w) - y2)**2) * koef
        return -vx, -vy
    elif p == 5:        #NEISPITANO
        fx1 = np.array([x1, x2])
        fy1 = np.array([y1, y2 + h])
        p = lb.lagrange_interpolation(fx1, fy1)
        interscCR = np.polyval(p, 0)
        koef = math.sqrt(2) / math.sqrt((0 - x2)**2 + (interscCR - y2)**2)
        print(koef)
        print(x1, y1, x2, y2)
        vx = math.sqrt((0 - x2)**2) * koef
        vy = math.sqrt((interscCR - y2)**2) * koef
        return -vy, -vx
    elif p == 6:
        fx1 = np.array([x1,x2+w])
        fy1 = np.array([y1,y2+h])
        p = lb.lagrange_interpolation(fx1, fy1)
        interscCR = np.polyval(p, w)
        koef = math.sqrt(2) / math.sqrt((w - x2)**2 + ( interscCR - y2)**2)
        vx = d = math.sqrt((w - x2)**2) * koef
        vy = math.sqrt((np.polyval(p, w) - y2)**2) * koef
        return -vx, -vy

    return vx, vy

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

    def update(self, paddle):
        global bg_color, fg_color

        imm = 0

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
                self.vx, self.vy = calculate_velocity(tempx, tempy, paddle.x - paddle.w, paddle.y, self.vx, self.vy, poss_coll, paddle.w)
                print(self.vx, self.vy)
                # if poss_coll == 1:
                #     self.vy = - self.vy
                # elif poss_coll == 3 or poss_coll == 4:
                #     self.vx = - self.vx
                #     self.vy = - self.vy

            if tempy > HEIGH:
                global END
                END = True

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
    
    w = BRICKW
    h = BRICKH

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show_and_update(self, color):
        global display
        pygame.draw.rect(display, color, pygame.Rect((self.x, self.y), (self.w, self.h)))

#create objects
paddleplay = Paddle(WIDTH//2)
ballplay = Ball(WIDTH//2, HEIGH - Ball.r - paddleplay.h - 1, -VELOCITY, -VELOCITY)

#Draw scenario
pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGH))

fg_color = pygame.Color("white")
bg_color = pygame.Color("black")

pygame.draw.rect(display, fg_color, pygame.Rect((0,0), (WIDTH, BORDER)))
pygame.draw.rect(display, fg_color, pygame.Rect((0,0), (BORDER, HEIGH - PADDLEH)))
pygame.draw.rect(display, fg_color, pygame.Rect((WIDTH - BORDER, 0), (BORDER, HEIGH - PADDLEH)))

ballplay.show(fg_color)
paddleplay.show(fg_color)

clock = pygame.time.Clock()

while not END:
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    clock.tick(FRAMERATE)

    pygame.display.flip()
    ballplay.update(paddleplay)
    paddleplay.update()
    

pygame.quit()
