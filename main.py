import pygame
import random

pygame.init()
win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Cubes game") 

walk_right = [pygame.image.load("Sprites/pygame_right_1.png"), pygame.image.load("Sprites/pygame_right_2.png"), pygame.image.load("Sprites/pygame_right_3.png"), pygame.image.load("Sprites/pygame_right_4.png"), pygame.image.load("Sprites/pygame_right_5.png"), pygame.image.load("Sprites/pygame_right_6.png")]

walk_left = [pygame.image.load("Sprites/pygame_left_1.png"), pygame.image.load("Sprites/pygame_left_2.png"), pygame.image.load("Sprites/pygame_left_3.png"), pygame.image.load("Sprites/pygame_left_4.png"), pygame.image.load("Sprites/pygame_left_5.png"), pygame.image.load("Sprites/pygame_left_6.png")]

bg = pygame.image.load("Sprites/pygame_bg.jpg")
player_stand = pygame.image.load("Sprites/pygame_idle.png")

clock = pygame.time.Clock()

x = 50
y = 425
width = 60
height = 71
speed = 7

is_jump = False
jump_count = 10

left = False
right = False
anim_count = 0
last_move = "right"

cube_count = 0

class Kub():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 10
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        
class Snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing 
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def draw_window():
    global anim_count
    win.blit(bg, (0, 0))  
    win.blit(text, (25, 25))
  
    if anim_count + 1 >=30:
        anim_count = 0

    if left:
        win.blit(walk_left[anim_count // 5], (x, y))
        anim_count += 1
    elif right:
        win.blit(walk_right[anim_count // 5], (x,y))
        anim_count += 1    
    else:
        win.blit(player_stand, (x, y))

    for bullet in bullets:
        bullet.draw(win)
    
    for cube in cubes:
        cube.draw(win)

        
    pygame.display.update()
    
run = True
bullets = []
cubes = []
while run:
    if cube_count < 50:
        clock.tick(30)
    else:
        clock.tick(45)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    for cube in cubes:
        if cube.x < 500 and cube.x > 0 - cube.width:
            cube.x -= cube.vel
        else:
            cube_count += 1
            cubes.pop(cubes.index(cube))
        

    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        if last_move == "right":
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(Snaryad(round(x + width // 2), round(y + height // 2), 6, (255,0,0), facing))

    if len(cubes) < 1:
        cubes.append(Kub(499, random.randrange(340, 490, 75), 100, 50, (0, 0, 0)))
    elif len(cubes) < 2 and cube.x < 250 - cube.width / 2:
        cubes.append(Kub(499, random.randrange(340, 490, 75), 100, 50, (0, 0, 0)))

    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        last_move = "left"
    elif keys[pygame.K_RIGHT] and x < 495 - width:
        x += speed
        left = False
        right = True
        last_move = "right"
    else:
        left = False
        right = False
        anim_count = 0
        
    if not(is_jump):
        if keys[pygame.K_SPACE]:
            is_jump = True
    else:
        if jump_count >= -10:
            if jump_count < 0:
                y += jump_count ** 2 / 2
            else:
                y -= jump_count ** 2 / 2
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10
    
    x_sheape = [z for z in range(x, x + width)]
    y_sheape = [z for z in range(round(y), round(y) + height)]
    
    cube_x_sheape = [z for z in range(cubes[0].x, cubes[0].x + cubes[0].width)] 
    cube_y_sheape = [z for z in range(cubes[0].y, cubes[0].y + cubes[0].height)]
    if len(set(x_sheape) & set(cube_x_sheape)) > 0 and len(set(y_sheape) & set(cube_y_sheape)) > 0:
        run = False

    if len(cubes) == 2:
        cube2_x_sheape = [z for z in range(cubes[1].x, cubes[1].x + cubes[1].width)] 
        cube2_y_sheape = [z for z in range(cubes[1].y, cubes[1].y + cubes[1].height)]
        if len(set(x_sheape) & set(cube2_x_sheape)) > 0 and len(set(y_sheape) & set(cube2_y_sheape)) > 0:
            run = False
            
    font = pygame.font.SysFont('couriernew', 40)
    text = font.render(str(cube_count), True, pygame.color.THECOLORS['green'])  

    draw_window()

pygame.quit()