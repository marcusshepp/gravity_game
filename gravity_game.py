from pygame import *
# import pygame._view
from random import *
from math import *
import time as t
# #################################################### #
# ##                                                ## #
# ##  This game was made by Jeremy Gagnier in 2010  ## #
# ##                                                ## #
# #################################################### #
from GA import evolve # mjs

init()

size = width,height = 800,600

screen = display.set_mode(size)

density_font = font.Font('fonts/BOOKOS.ttf',20)
font1 = font.Font('fonts/BOOKOS.ttf',24)

# PLANET = [X,Y,RADIUS,DENSITY]

class solar_system:
    def __init__(self):
        """This class is for handling all of the major game components."""
        self.planets = []
        self.home_planet = []
        self.goal_planet = []
        self.player = []

    def new_game(self,planets,difficulty):
        """Create a randomized game map."""
        home_rad = randint(40,60)
        self.home_planet = [randint(home_rad,width-home_rad),\
        randint(home_rad,height-home_rad), home_rad,round(home_rad/2),round(home_rad/2)/home_rad]
        goal_rad = randint(40-difficulty,60-difficulty)
        rand_x = randint(goal_rad,width-goal_rad)
        rand_y = randint(goal_rad,height-goal_rad)
        while sqrt((rand_x-self.home_planet[0])**2+(rand_y-self.home_planet[1])**2) < home_rad+goal_rad+200:
            rand_x = randint(goal_rad,width-goal_rad)
            rand_y = randint(goal_rad,height-goal_rad)
        gravity = round(goal_rad*randint(10,15)/10)
        self.goal_planet = [rand_x,rand_y,goal_rad,gravity,gravity/goal_rad]
        self.planets = []
        for i in range(planets-1):
            planet_rad = randint(40+difficulty,60+difficulty)
            rand_x = randint(planet_rad,width-planet_rad)
            rand_y = randint(planet_rad,height-planet_rad)
            while 1:
                touching = False
                if sqrt((rand_x-self.home_planet[0])**2+(rand_y-self.home_planet[1])**2) < home_rad+planet_rad:
                    touching = True
                if sqrt((rand_x-self.goal_planet[0])**2+(rand_y-self.goal_planet[1])**2) < goal_rad+planet_rad:
                    touching = True
                if len(self.planets) > 0:
                    for b in self.planets:
                        if sqrt((rand_x-b[0])**2+(rand_y-b[1])**2) < b[2]+planet_rad:
                            touching = True
                if not touching: break
                else:
                    rand_x = randint(planet_rad,width-planet_rad)
                    rand_y = randint(planet_rad,height-planet_rad)
            gravity = round(goal_rad*randint(8,round(12+difficulty/10))/10)
            self.planets.append([rand_x,rand_y,planet_rad,gravity,gravity/planet_rad])
        # print(self.planets)
        # with open("current_board.txt", "w") as my_file:
        #     my_file.write(str(self.planets))

    def draw(self):
        """Draw the planets and the player."""
        global launch_start,power,max_power
        # home planet
        draw.circle(screen,(0,0,255),self.home_planet[0:2],self.home_planet[2])
        message = density_font.render(str(round(self.home_planet[4],2)),1,(255,255,255))
        w,h = density_font.size(str(round(self.home_planet[4],2)))
        screen.blit(message,(self.home_planet[0]-w/2,self.home_planet[1]-h/2))
        # target planet
        draw.circle(screen,(0,255,0),self.goal_planet[0:2],self.goal_planet[2])
        message = density_font.render(str(round(self.goal_planet[4],2)),1,(255,255,255))
        w,h = density_font.size(str(round(self.goal_planet[4],2)))
        screen.blit(message,(self.goal_planet[0]-w/2,self.goal_planet[1]-h/2))
        # enemy planets
        for i in self.planets:
            draw.circle(screen,(255,0,0),i[0:2],i[2])
            message = density_font.render(str(round(i[4],2)),1,(255,255,255))
            w,h = density_font.size(str(round(i[4],2)))
            screen.blit(message,(i[0]-w/2,i[1]-h/2))
        # player
        if self.player != []:
            x2 = self.player[0]-self.player[2]/6
            y2 = self.player[1]-self.player[3]/6
            draw.line(screen,(125,0,125),(self.player[0],self.player[1]),(x2,y2),2)
        # launch scaler
        draw.rect(screen,(0,0,0),(740,10,50,100),5)
        draw.rect(screen,(0,255,0),(740,10+100-power*(100/max_power),50,power*(100/max_power)))

    def launch(self,x,y,click,angle):
        """Launch the player towards the mouse."""
        global launch_start,power,power_direction,max_power,min_power
        if self.player == []:
            if not launch_start and click:
                launch_start = 1
                power = 10
            elif launch_start and click:
                power += power_direction
                if power >= max_power: power_direction = -sqrt(power_direction**2)
                if power <= min_power: power_direction = sqrt(power_direction**2)
            elif launch_start and not click:
                self.player = [x,y,cos(angle)*power,sin(angle)*power]
                launch_start = 0

    def update(self):
        """Update the players' position."""
        if self.player != []:
            for i in self.planets:
                distance = sqrt((i[0]-self.player[0])**2+(i[1]-self.player[1])**2)-i[3]
                angle = atan((i[1]-self.player[1])/(i[0]-self.player[0]+0.0000001))
                if i[0] < self.player[0]: angle += radians(180)
                grav_effect = i[3]*(i[2]/(i[2]+distance))**2
                self.player[2] += cos(angle)*grav_effect/10
                self.player[3] += sin(angle)*grav_effect/10
            for i in (self.home_planet,self.goal_planet):
                distance = sqrt((i[0]-self.player[0])**2+(i[1]-self.player[1])**2)-i[3]
                angle = atan((i[1]-self.player[1])/(i[0]-self.player[0]+0.0000001))
                if i[0] < self.player[0]: angle += radians(180)
                grav_effect = i[3]*(i[2]/(i[2]+distance))**2
                self.player[2] += cos(angle)*grav_effect/10
                self.player[3] += sin(angle)*grav_effect/10
            self.player[0] += self.player[2]/10
            self.player[1] += self.player[3]/10
            for i in self.planets:
                if sqrt((i[0]-self.player[0])**2+(i[1]-self.player[1])**2) < i[2]:
                    return -1
            if sqrt((self.home_planet[0]-self.player[0])**2+\
            (self.home_planet[1]-self.player[1])**2) < self.home_planet[2]:
                return -1
            if sqrt((self.goal_planet[0]-self.player[0])**2+\
            (self.goal_planet[1]-self.player[1])**2) < self.goal_planet[2]:
                return 1
            if self.player[0] < 0 or self.player[0] > 800 or self.player[1] < 0 or self.player[1] > 600:
                return -1
        return 0

    def load_map(self,filename):
        """Change global variables to predefined paramaters in the file."""
        global max_power,min_power
        exec(open(filename,'r').read())


# Draw the opening screen
screen.fill((255,255,255))
screen.blit(font1.render("Welcome to the Gravity Game",1,(0,0,0)),(10,10))
screen.blit(font1.render("Controls:",1,(0,0,0)),(10,80))
screen.blit(font1.render("Left Click : Charges your flier's power. Release to launch.",1,(0,0,0)),(50,120))
screen.blit(font1.render("R : Resets your flier.",1,(0,0,0)),(50,160))
screen.blit(font1.render("N : Creates a new map.",1,(0,0,0)),(50,200))
screen.blit(font1.render("Instructions:",1,(0,0,0)),(10,270))
screen.blit(font1.render("Launch your flier from the blue planet to the green planet.",1,(0,0,0)),(50,310))
screen.blit(font1.render("Use the red planets to curve your flier's path, but don't crash!",1,(0,0,0)),(50,350))
screen.blit(font1.render("Press anything to continue...",1,(0,0,0)),(10,540))

display.flip()

cont = 1
while cont:             # Wait for left click
    for evnt in event.get():
        if evnt.type == QUIT:   # Closes the game
            cont = 0
        elif evnt.type == KEYDOWN:
            cont = 0
        elif evnt.type == MOUSEBUTTONUP:
            cont = 0

    time.wait(30)

game = solar_system()   # Initialise the game

held_kn = 0
launch_start = 0

max_power = 60
min_power = 10
power = 10
power_direction = 2

level = 0
maps = ['maps/map'+str(i+1)+'.md' for i in range(10)]

game.load_map(maps[level])  # Load the first level
mx, my = evolve(1, "maps/map1.md")
lc = 1
cont = 1
while cont:
    for evnt in event.get():
        if evnt.type == QUIT:   # Closes the game
            cont = 0
        if evnt.type == KEYDOWN:
            if evnt.key == K_ESCAPE: # Closes the game
                cont = 0
            if evnt.key == K_r:      # Resets the player
                game.player = []
                power = min_power
            if evnt.key == K_n:      # Makes a new map
                game.new_game(1,0)
                game.player = []
                power = min_power

    # mx,my = mouse.get_pos()
    # lc = mouse.get_pressed()[0]



    # print(lc)

    f_angle = atan((my-game.home_planet[1])/(mx-game.home_planet[0]+0.00000001))
    if mx < game.home_planet[0]: f_angle += radians(180)
    x = cos(f_angle)*game.home_planet[2]+game.home_planet[0]
    y = sin(f_angle)*game.home_planet[2]+game.home_planet[1]

    # limit space
    power = max_power

    game.launch(x,y,lc,f_angle)
    lc = 0
    action = game.update()  # Will return -1 if the player crashed and 1 if he succeeded
    if action < 0:
        game.player = []
        # power = min_power
    elif action > 0:
        level += 1
        try: game.load_map(maps[level]) # Tries to load the next map
        except: game.new_game(4,0)
        game.player = []
        # power = min_power
        lc = 1

    # Update screen
    screen.fill((255,255,255))
    screen.blit(font1.render(str(mx) + " " + str(my),1,(0,0,0)),(10,540)) # mjs
    game.draw()
    if game.player == []: draw.circle(screen,(255,0,0),(round(x),round(y)),5)

    display.flip()
    time.delay(30)

quit()
