import pygame
import math
import NANS_lib as lb
import numpy as np

#VARIABLRS
WIDTH = 1000
HEIGH = 600
BORDER = 10
RADIUS = 20
VELOCITY = 1
FRAMERATE = 400
PADDLEW = 100
PADDLEH = 20
END = False
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
    print(ball1.x, ball2.x,ball1.y,ball2.y)
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
       # ball1.vy = -ball1.vy
        return temp, -ball1.vy
    elif ball1.y == ball2.y:
        #ball1.vx = -ball1.vx
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
                print("Poraz")
        
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
            print("Pobeda")

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
print("Enter number of balls:")
num_balls = input()
num_balls = int(num_balls)

print("Enter number of bricks in the row (1-7)")
bricks_row = int(input())
print("Enter number of bricks in the column (1-8)")
bricks_col = int(input())

#create objects
paddleplay = Paddle(WIDTH//2)

balls = []
for i in range(num_balls):
    ballplay = Ball(WIDTH//2 - i*2*Ball.r, HEIGH - Ball.r - paddleplay.h - 1 - i*2*Ball.r, -VELOCITY, -VELOCITY)
    balls.append(ballplay)

bricks = level(bricks_row, bricks_col)

#Draw scenario
pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGH))

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
    

pygame.quit()
