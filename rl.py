import pygame
import time
import random
from enum import Enum

# needs python 3

WORLD_WIDTH = 500
WORLD_HEIGHT = 500

UPDATE_TIME = 0.1

ROAD_LENGTH = 50
MAX_SPEED = 5
NUM_CARS = 2

LIGHT_POS = ROAD_LENGTH / 2 # the traffic light is halfway down the road

LIGHT_CYCLE_LENGTH = 60

LIGHT_TIME = 0

road = [] # lanes 0, 1 go in one way and 2, 3 go in the other
cars = [] 

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
dark_blue = (0,0,128)
white = (255,255,255)
gray = (120, 120, 120)
black = (0,0,0)
pink = (255,200,200)
yellow = (255, 239, 0)
orange = (255, 128, 0)

class LightState(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2

LIGHT_STATE = LightState.RED

class Car:
    def __init__(self):
        self.lane = random.randint(0, 3) # the lane also determines the direction
        # self.speed = random.randint(1, 5)
        self.speed = 2
        self.pos = random.randint(0, ROAD_LENGTH - 1)

    def get_position(self):
        return self.pos

    def get_lane(self):
       return self.lane

    def update_state(self, new_lane = -1, new_speed = -1):
        if new_speed != -1:
            self.speed = new_speed
        if new_lane != -1:
            self.lane = new_lane
        if self.lane == 0 or self.lane == 1:
            self.pos += self.speed
            self.pos %= ROAD_LENGTH
        else:
            self.pos += ROAD_LENGTH
            self.pos -= self.speed
            self.pos %= ROAD_LENGTH

    def __repr__(self):
        return ("CAR: Lane: " + str(self.lane) + ", Speed: " + str(self.speed) + ", Position: " + str(self.pos))

class Person:
    def __init__(self, _pos):
        self.pos = _pos
        self.lane = 0

    def get_position(self):
        return self.pos


# initialize the simulation
def init_sim():
    # construct the road
    for i in range(4):
        road.append([])
        for j in range(ROAD_LENGTH):
            road[i].append(None)
    for i in range(NUM_CARS):
        c = Car()
        road[c.get_lane()][c.get_position()] = c
        cars.append(c)
  
def update_light():
    global LIGHT_TIME
    global LIGHT_STATE
    global LIGHT_CYCLE_LENGTH
    factor = 20
    LIGHT_TIME += 1
    LIGHT_TIME %= LIGHT_CYCLE_LENGTH
    if LIGHT_TIME > LIGHT_CYCLE_LENGTH - LIGHT_CYCLE_LENGTH / factor:
        LIGHT_STATE = LightState.YELLOW
    elif LIGHT_TIME > LIGHT_CYCLE_LENGTH / 2 + LIGHT_CYCLE_LENGTH / factor:
        LIGHT_STATE = LightState.GREEN
    elif LIGHT_TIME > LIGHT_CYCLE_LENGTH / 2 - LIGHT_CYCLE_LENGTH / factor:
        LIGHT_STATE = LightState.YELLOW
    elif LIGHT_TIME > LIGHT_CYCLE_LENGTH / factor:
        LIGHT_STATE = LightState.RED
    else:
        LIGHT_STATE = LightState.YELLOW

def update_cars():
    printed = False
    for c in cars:
        i = c.get_lane()
        j = c.get_position()
        road[i][j] = None
    for c in cars:
        if not printed:
            print(c)
        c.update_state()
    for c in cars:
        i = c.get_lane()
        j = c.get_position()
        road[i][j] = c
            # printed = True

def update_pedestrians():
    # advance the pedestrians who are currently on the road
    for i in range(ROAD_LENGTH):
        for k in range(4):
            j = 3 - k
            if isinstance(road[j][i], Person):
                p_ref = road[j][i]
                if j != 3:
                    road[j + 1][i] = p_ref
                road[j][i] = None
    # generate new pedestrians
    recip_ped_prob = 5
    rand_max = recip_ped_prob * ROAD_LENGTH
    for i in range(ROAD_LENGTH):
        if road[0][i] is not None:
            continue
        r = random.randint(1, rand_max)
        if r == 1:
            road[0][i] = Person(i)
    return 0

def update_sim():
    update_light()
    update_cars()
    update_pedestrians()
    return 0

def draw_everything(screen):
    SQUARE_SIZE = 10
    for i in range(4):
        for j in range(ROAD_LENGTH):
            my_color = gray
            if isinstance(road[i][j], Person):
                my_color = pink
            if isinstance(road[i][j], Car):
                my_color = blue
            pygame.draw.rect(screen, my_color, (i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)
    if LIGHT_STATE == LightState.GREEN:
        pygame.draw.rect(screen, green, (4 * SQUARE_SIZE, LIGHT_POS * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)
    elif LIGHT_STATE == LightState.RED:
        pygame.draw.rect(screen, red, (4 * SQUARE_SIZE, LIGHT_POS * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)
    else:
        pygame.draw.rect(screen, yellow, (4 * SQUARE_SIZE, LIGHT_POS * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 0)

def main():
    pygame.init()
    # some basic initialization stuff
    main_surface = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
    init_sim()
    
    while True:
        # main loop
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
        update_sim()
        print("updating")
        print(LIGHT_STATE)
        draw_everything(main_surface)
        pygame.display.flip()
        time.sleep(UPDATE_TIME)
    pygame.quit()

main()
