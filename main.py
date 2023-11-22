import math
from random import choice
from random import randint
import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
g=1
background = pygame.transform.scale(pygame.image.load("images/background.jpg"), (800, 600))
snitchim = pygame.image.load("images/output.png")
tank = pygame.transform.scale(pygame.image.load("images/tank.png"), (100,100))
exit_button = pygame.image.load("images/exit.png")



class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        if((self.x+self.r)<800) or(self.vx<0) :
            self.x += self.vx
        else:
            self.vx=-0.6*self.vx

        if((self.y+self.r)<600) or(self.vy>0):
            self.y -= self.vy
        else:
            self.vy = -0.7*self.vy
        self.vy -= g
        # self.x += self.vx
        # self.y -= self.vy
        # self

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if(((self.x-obj.x)**2+(self.y-obj.y)**2)<(self.r+obj.r)**2):
            return True
        else:
            return False

class manyBall():
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.num=5
        self.balls=[]
    def give_balls(self):
        for i in range(self.num):
            new_ball=Ball(self.screen)
            new_ball.x = self.x
            new_ball.y=self.y
            new_ball.vx = self.vx
            new_ball.vy=self.vy+5-2*i
            self.balls.append(new_ball)
        return self.balls





class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y=450
        self.img = tank

    def move_left(self):
        if(self.x>=45):
            self.x= self.x-25

    def move_right(self):
        if(self.x<=755):
            self.x= self.x+25

    def move_up(self):
        if(self.y>=300):
            self.y-=5

    def move_down(self):
        if (self.y<=500):
            self.y+=5

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event, Kspace):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet

        # bullet += 1
        # new_ball = Ball(self.screen)
        # new_ball.r += 5
        #self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        # new_ball.vx = self.f2_power * math.cos(self.an)
        # new_ball.vy = -self.f2_power * math.sin(self.an)
        vx = self.f2_power * math.cos(self.an)
        vy = -self.f2_power * math.sin(self.an)
        if (Kspace):
            newmanyball = manyBall(self.screen)
            newmanyball.x=self.x
            newmanyball.y=self.y
            newmanyball.vx = vx
            newmanyball.vy=vy
            new_balls = newmanyball.give_balls()
            balls += new_balls
            bullet+=len(new_balls)
        else:
            new_ball = Ball(self.screen)
            new_ball.x=self.x
            new_ball.y=self.y
            new_ball.vx=vx
            new_ball.vy=vy
            bullet += 1
            balls.append(new_ball)


        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    # def draw(self):
    #     width = int(100 + self.f2_power * 0.1)
    #     height = 4
    #     self.rectsurface = pygame.Surface((width, height))
    #     self.rectsurface.fill((255, 0, 0))  # Use RGB tuple for RED
    #
    #     self.rect = self.rectsurface.get_rect()
    #     self.rect.center = (100, 100)
    #
    #     # Draw rectangle on the surface
    #     pygame.draw.rect(self.rectsurface, (0, 255, 0), (0, 0, width, height))  # Use RGB tuple for GREEN
    #
    #     self.rotsurf = pygame.transform.rotate(self.rectsurface, 30)  # Adjust the rotation angle
    #     self.rotrect = self.rotsurf.get_rect()
    #     self.rotrect.center = (40, 450)
    #     screen.blit(self.rotsurf, self.rotrect)
    def draw(self):
        tank_rect = self.img.get_rect(center=(self.x, self.y))
        tank_rect[0]=tank_rect[0]-5
        tank_rect[1] = tank_rect[1] +15
        screen.blit(self.img, tank_rect)
        pygame.draw.line(
            self.screen,
            self.color,
            (self.x, self.y),
            (self.x + math.cos(self.an) * (15 + self.f2_power / 2), self.y + math.sin(self.an)
             * (15 + self.f2_power / 2)),
            width=7
        )


        # width = int(100+self.f2_power*0.1)
        # height = 50
        # self.rectsurface = pygame.Surface((width, height))
        # self.rectsurface.fill(RED)
        #
        # self.rect = self.rectsurface.get_rect()
        # self.rect.center =(100, 100)
        # pygame.draw.rect(self.rectsurface, self.color, (20,430,50,30))
        #
        #
        # self.rotsurf = pygame.transform.rotate(self.rectsurface, 1)
        # self.rotrect = self.rotsurf.get_rect()
        # self.rotrect.center = (40, 450)
        # screen.blit(self.rotsurf, self.rotrect)
        # pygame.draw.rect(screen, self.color, (20, 450, width, height))
        # rotrect = rotsurf.get_rect()
        # rotrect.center=(width/2, height/2)
        #rect1 = rotrect.get_rect(center=rect.center)

        #FIXIT don't know how to do it

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.new_target()
        self.points =0
        # self.live=1

        # self.color = RED
        # x = self.x = randint(600, 780)
        # y = self.y = randint(300, 550)
        # r = self.r = randint(2, 50)


    def new_target(self):
        """ Инициализация новой цели. """
        # x = self.x = randint(600, 780)
        # y = self.y = randint(300, 550)
        # r = self.r = randint(2, 50)
        # color = self.color = RED
        self.live = 1
        self.color = RED
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(25, 50)
        self.vx = 15
        self.vy = 15

    def hit(self):
        """Попадание шарика в цель."""
        self.points += 1

    def move(self):
        if ((self.x + self.r) >= 800) and (self.vx>0):
            self.vx= -self.vx
        elif ((self.x + self.r) <= 200) and (self.vx<0):
            self.vx = -self.vx
        else:
            self.x+=self.vx
        # if (((self.y + self.r)>590) and (self.vy<0)):
        #     self.vy = -self.vy
        # elif (((self.y + self.r)<10) and (self.vy>0)):
        #     self.vy = -self.vy
        # else:
        #     self.y-=self.vy


        # if ((self.x + self.r) < 800) or (self.vx < 0):
        #     self.x += self.vx
        # else:
        #     self.vx =  -self.vx
        #
        # if ((((self.y + self.r) < 600)) and (self.vy > 0)) or (((self.y+self.r)>200) and (self.vy<0)):
        #     self.y -= self.vy
        # else:
        #     self.vy = -0.7 * self.vy


    def draw(self):
        pygame.draw.circle(self.screen, self.color,(self.x, self.y), self.r)


class Snitch(Target):
    def move(self):
        self.vx=randint(-40,40)
        self.vy = randint(-40, 40)
        if ((self.x + self.r) >= 800) and (self.vx>0):
            self.vx= -self.vx
        elif ((self.x + self.r) <= 200) and (self.vx<0):
            self.vx = -self.vx
        self.x+=self.vx
        if (((self.y + self.r)>590) and (self.vy<0)):
            self.vy = -self.vy
        elif (((self.y + self.r)<10) and (self.vy>0)):
            self.vy = -self.vy
        self.y-=self.vy

    def draw(self):
        sn_now=pygame.transform.scale(snitchim,(2*self.r,2*self.r))
        screen.blit(sn_now, (self.x - self.r, self.y - self.r))


class Exit_Button():
    def __init__(self, screen):
        self.width = 100
        self.height = 100
        self.screen=screen
        self.img = pygame.transform.scale(exit_button, (100, 100))
        self.rect = self.img.get_rect(center=(740, 60))

    def draw(self):
        self.screen.blit(self.img, self.rect)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
score = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target(screen)
target2 = Snitch(screen)
targets = [target1, target2]
finished = False
exit_b = Exit_Button(screen)
Kspace=0
Akey = 0
Wkey=0
Skey=0
Dkey=0
score = 0
textfont = pygame.font.SysFont('monospace', 40)
while not finished:
    #screen.fill(WHITE)

    screen.blit(background, (0,0))
    exit_b.draw()
    text = textfont.render("Points in game: " + str(score), 1, YELLOW)
    screen.blit(text, (30, 20))
    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if((event.pos[0]>exit_b.rect.left) and (event.pos[0]<exit_b.rect.right) and (event.pos[1]<exit_b.rect.bottom) and (event.pos[1]>exit_b.rect.top)):
                finished = True
            else:
                gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event, Kspace)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE):
                if(Kspace):
                    Kspace=0
                else:
                    Kspace=1
            if event.key == pygame.K_a:
                Akey = 1
            if event.key == pygame.K_s:
                Skey = 1
            if event.key == pygame.K_d:
                Dkey = 1
            if event.key == pygame.K_w:
                Wkey = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Akey = 0
            if event.key == pygame.K_s:
                Skey = 0
            if event.key == pygame.K_d:
                Dkey = 0
            if event.key == pygame.K_w:
                Wkey = 0
 #Движение танка





    if Akey:
        gun.move_left()
    if Skey:
        gun.move_down()
    if Dkey:
        gun.move_right()
    if Wkey:
        gun.move_up()
    for t in targets:
        t.move()

    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                t.live = 0
                t.hit()
                t.new_target()
    score = 0
    for t in targets:
        score+=t.points

    #score = target1.points+target2.points

    gun.power_up()
    if(len(balls) > 50):
        balls=balls[len(balls)-30:]


pygame.quit()
