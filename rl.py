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
NUM_CARS = 15

LIGHT_POS = ROAD_LENGTH / 2 # the traffic light is halfway down the road

LIGHT_CYCLE_LENGTH = 60

LIGHT_TIME = 0

road = [] # lanes 0, 1 go in one way and 2, 3 go in the other
cars = []

class LightState(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2

LIGHT_STATE = LightState.RED

class Car:
    def __init__(self):
        self.lane = random.randint(0, 3) # the lane also determines the direction
        self.speed = random.randint(1, 5)
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
        return ("Lane: " + str(self.lane) + ", Speed: " + str(self.speed) + ", Position: " + str(self.pos))

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
        if not printed:
            print(c)
            c.update_state()
            # printed = True

def update_sim():
    update_light()
    update_cars()
    return 0


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
        pygame.display.flip()
        time.sleep(UPDATE_TIME)
    pygame.quit()

main()
