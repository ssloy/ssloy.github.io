import pygame
from PIL import Image, ImageSequence
import numpy as np
import random

def make_transparent(target):
    arr = pygame.surfarray.pixels3d(target)
    alpha = pygame.surfarray.pixels_alpha(target)
    mask = (arr[:, :, 0] > 240) & (arr[:, :, 1] > 240) & (arr[:, :, 2] > 240)
    alpha[mask] = 0


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, gif_path, scale=None, loop=True):
        super().__init__()

        self.frames = []
        self.durations = []
        self.loop = loop
        self.playing = False

        # Charger le GIF
        gif = Image.open(gif_path)

        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")

            if scale:
                frame = frame.resize(scale, Image.NEAREST)

            surf = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode
            )
            make_transparent(surf)
     

            self.frames.append(surf)
            self.durations.append(.1)

        self.frame_index = 0
        self.time_acc = 0
        self.image = self.frames[0]

    def update(self, dt):
        if not self.playing:
            return
        self.time_acc += dt
        if self.time_acc >= self.durations[self.frame_index]:
            self.time_acc = 0
            self.frame_index += 1
            
            if self.frame_index >= len(self.frames):
                if self.loop:
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.frames) - 1
                    self.playing = False

            self.image = self.frames[self.frame_index]

    def reset(self):
        self.frame_index = 0
        self.time_acc = 0
        self.image = self.frames[0]

    def draw(self, surface,pos):
        surface.blit(self.image, self.image.get_rect(topleft=pos))




#####################################################################################################

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
FPS = 60


hand_pos = (230,  570)
pixel_per_meter = 40


monkey = AnimatedSprite(
    "monkey.gif",
    scale=(256, 256),
    loop=False
)

banana = AnimatedSprite(
    "banana.gif",
    scale=(60, 30),
    loop=True
)
splash = AnimatedSprite(
    "splash.gif",
    scale=(128, 64),
    loop=True
)


background = pygame.image.load("background.png") 
target = pygame.image.load("target.png")
make_transparent(target)


button = pygame.image.load("targeth.png")


def add_target(world_coordinates):
    screen.blit(target,(hand_pos[0]+pixel_per_meter*world_coordinates[0]-64,hand_pos[1]-pixel_per_meter*world_coordinates[1]-64))

v0=(5,20)
g = -9.81

t =  np.arange(0, 20, 0.1)
x = v0[0]*t
y = v0[1]*t + g*t*t 


def reset_trajectory():
    global x
    global y
    v0 = (random.uniform(2,15),random.uniform(2,30))
    x = v0[0]*t
    y = v0[1]*t + g*t*t 


state = "wait"
running = True
fly_time = 0
while running:
    dt = clock.tick(FPS) / 1000  # Returns milliseconds between each call to 'tick'. The convert time to seconds.
    screen.fill((255,255,255))  # Fill the screen with background color.
    screen.blit(background,(0,0))
    screen.blit(button,(10,10))
    
    add_target((20,1))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect((10,10,144,79)).collidepoint(event.pos):
                reset_trajectory()
            state = "warmup"
            monkey.reset()
            monkey.playing = True
    
    if state != "wait":
        monkey.update(dt)
        if monkey.frame_index>5 and state == "warmup":
            state = "fly"
            fly_time = 0

    monkey.draw(screen,pos=(0, 470))

    if state == "fly":
        banana.pos = (hand_pos[0] + pixel_per_meter*x[int(10*fly_time)],hand_pos[1] - pixel_per_meter*y[int(10*fly_time)])
        if y[int(10*fly_time)]<0:
            state = "splash"
            splash.reset()
        else: 
            banana.update(dt)
            rotated = pygame.transform.rotate(banana.image, -150.*fly_time)
            screen.blit(rotated, rotated.get_rect(center=(banana.pos[0]+14,+banana.pos[1]+6)))
            fly_time += dt

    if state == "splash":
            splash.draw(screen,pos=(banana.pos[0]-64,hand_pos[1]-32))
            splash.update(dt)
            if splash.frame_index==0 and dt>1:
                state = "wait"
        
    pygame.display.update() 

print("Exited the game loop. Game will quit...")
quit()  # Not actually necessary since the script will exit anyway.