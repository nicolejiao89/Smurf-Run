# This code prints the game Smurf Run
# This code is written by Nicole Jiao

import simplegui
import codeskulptor
import random

# Constants
# Images
BKGD_IMAGE = simplegui.load_image('https://i.imgur.com/Gxwtfup.png')
END = simplegui.load_image('https://i.imgur.com/RpNWPro.png')
ST_BUTTON = simplegui.load_image('https://i.imgur.com/4UVU7Qo.png')
PLAYER1 = simplegui.load_image('http://www.flashpulse.com/moho/smurf_sprite.PNG')
PLAYER2 = simplegui.load_image('https://i.imgur.com/erm8AVQ.png')
ROCK = simplegui.load_image('https://i.imgur.com/uwecPrx.png')
HOLE = simplegui.load_image('https://i.imgur.com/Steb9YT.png')

# Other constants
COLUMNS = 4
ROWS = 4

GROUND = 350

jump_count = 0
alive = True
playing = False
room = 0

room_list = []

# Background sizes
BKGD_WIDTH = 2048
BKGD_HEIGHT = 1024
END_WIDTH = 1024
END_HEIGHT = 1024
WIDTH = 800
HEIGHT = 500

# Button attributes
BUTTON_WIDTH = 1024
BUTTON_HEIGHT = 1024
BUTTON_SIZE_WIDTH = 400
BUTTON_SIZE_HEIGHT = 400
BUTTON_POSITION = [WIDTH/2, HEIGHT/2]

# Player attributes
PLAYER_WIDTH = 512/COLUMNS
PLAYER_HEIGHT = 512/COLUMNS
PLAYER_DRAW_SIZE = (150, 150)
PLAYER_SIZE = [90, 140]
PLAYER_POSITION = [PLAYER_SIZE[0]/2, 350]
PLAYER_VELOCITY = [0, 0]

# Rock attributes
ROCK_WIDTH = 1024
ROCK_HEIGHT = 1024
ROCK_DRAW_SIZE = (180, 275)
ROCK_SIZE = [65, 80]
ROCK_VELOCITY = [0,0]

# Hole attributes
HOLE_WIDTH = 1024
HOLE_HEIGHT = 1024
HOLE_DRAW_SIZE = (450, 504)
HOLE_SIZE = (50, 75)
HOLE_VELOCITY = [0,0]

# Helper funtions
def new_game():
    global player, room_list
    global dist
    global GROUND
    player = Player(PLAYER1, PLAYER2, PLAYER_SIZE, [PLAYER_SIZE[0]/2, 350], PLAYER_VELOCITY)
    room_list = []
    dist = 0
    GROUND = 350
    playing = True
    create_room()

def go_forwards():
    global room
    room += 1
    create_room()
    player.pos[0] = 1
    
def go_backwards():
    global room
    room -= 1
    player.pos[0] = WIDTH - 1
    
def create_room():
    positions = [135, 310, 425, 530, 715]
    random.shuffle(positions)
    rock1 = Rock(ROCK, [positions[0], 405], ROCK_SIZE, ROCK_VELOCITY)
    rock2 = Rock(ROCK, [positions[1], 405], ROCK_SIZE, ROCK_VELOCITY)
    rock3 = Rock(ROCK, [positions[2], 405], ROCK_SIZE, ROCK_VELOCITY)
    hole1 = Hole(HOLE, [positions[3], 469], HOLE_SIZE, HOLE_VELOCITY)    
    hole2 = Hole(HOLE, [positions[4], 469], HOLE_SIZE, HOLE_VELOCITY)
    room = Room(BKGD_IMAGE, [rock1, rock2, rock3], [hole1, hole2])
    room_list.append(room)
    
# Player class
class Player:
    def __init__(self, PLAYER1, PLAYER2, PLAYER_SIZE, PLAYER_POSITION, PLAYER_VELOCITY):
        self.image1 = PLAYER1
        self.image2 = PLAYER2
        self.size = PLAYER_SIZE
        self.pos = PLAYER_POSITION
        self.vel = PLAYER_VELOCITY
        self.time = 0
        
    # Player draw function   
    def draw(self, canvas):
        column = self.time % COLUMNS
        row = self.time // COLUMNS
        tile_center = [PLAYER_WIDTH/2 + column * PLAYER_WIDTH,
                       PLAYER_HEIGHT/2 + row * PLAYER_HEIGHT]

        # Player animation on ground
        if self.pos[1] == GROUND:
            if self.vel[0] < 0:
                canvas.draw_image(self.image2,
                                tile_center,
                                [PLAYER_WIDTH, PLAYER_HEIGHT],
                                self.pos,
                                PLAYER_DRAW_SIZE)                    
            if self.vel[0] > 0:
                canvas.draw_image(self.image1,
                                tile_center,
                                [PLAYER_WIDTH, PLAYER_HEIGHT],
                                self.pos,
                                PLAYER_DRAW_SIZE)                    
            if self.vel[0] == 0:
                canvas.draw_image(self.image1,
                                [PLAYER_WIDTH/2 + PLAYER_WIDTH * 3, PLAYER_HEIGHT/2],
                                [PLAYER_WIDTH, PLAYER_HEIGHT],
                                self.pos,
                                PLAYER_DRAW_SIZE) 
                
        # Player animation above ground       
        if self.pos[1] < GROUND:
            if self.vel[0] < 0:
                canvas.draw_image(self.image2,
                                tile_center,
                                [PLAYER_WIDTH, PLAYER_HEIGHT],
                                self.pos,
                                PLAYER_DRAW_SIZE)
            if self.vel[0] > 0:
                canvas.draw_image(self.image1,
                                tile_center,
                                [PLAYER_WIDTH, PLAYER_HEIGHT],
                                self.pos,
                                PLAYER_DRAW_SIZE)
            if self.vel[0] == 0:
                canvas.draw_image(self.image1,
                                [PLAYER_WIDTH/2 + PLAYER_WIDTH * 3, PLAYER_HEIGHT/2],
                                [PLAYER_WIDTH, PLAYER_HEIGHT],
                                self.pos,
                                PLAYER_DRAW_SIZE)
                
    # Player update function                        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.pos[1] < GROUND:
            self.vel[1] += 1

        self.time += 1
        self.time %= ROWS*COLUMNS
        
        if self.pos[0] > WIDTH:
            go_forwards()

        if self.pos[0] < 0:
            if not room == 0:
                go_backwards()
                
        if room == 0:
            if self.pos[0] < self.size[0]/2:
                player.pos[0] = self.size[0]/2                
    
    # Player jump function           
    def jump(self):
        global jump_count
        if jump_count < 2:
            self.vel[1] -= 12
            jump_count += 1

    # Player fall function
    def has_fallen(self, hole):     
        if (player.pos[0] >= hole.pos[0] - hole.size[0]
                and player.pos[0] <= hole.pos[0] + hole.size[0]
                and player.pos[1] == GROUND):
            return True   

# Rock class
class Rock:
    def __init__ (self, ROCK, position, ROCK_SIZE, ROCK_VELOCITY):
        self.image = ROCK
        self.size = ROCK_SIZE
        self.pos = position
        self.vel = ROCK_VELOCITY
        self.time = 0
        
    # Rock draw function
    def draw(self, canvas):
        canvas.draw_image(self.image,
                         [ROCK_WIDTH/2, ROCK_HEIGHT/2],
                         [ROCK_WIDTH, ROCK_HEIGHT],
                          self.pos,
                          ROCK_DRAW_SIZE)
    # Rock update function            
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    
    # Rock collision
    def has_collided(self, player):
        return (player.size[0]/2 + self.size[0]/2 > abs(self.pos[0] - player.pos[0])
            and player.size[1]/2 + self.size[1]/2 > abs(self.pos[1] - player.pos[1]))

# Hole class
class Hole:
    def __init__ (self, HOLE, position, HOLE_SIZE, HOLE_VELOCITY):
        self.image = HOLE
        self.size = HOLE_SIZE
        self.pos = position
        self.vel = HOLE_VELOCITY
       
    def draw(self, canvas):
        canvas.draw_image(self.image,
                          [HOLE_WIDTH/2, HOLE_HEIGHT/2],
                          [HOLE_WIDTH, HOLE_HEIGHT],
                          self.pos,
                          HOLE_DRAW_SIZE)       
                       
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

# Room class
class Room:
    def __init__ (self, background, rocks, holes):
        self.bg = background
        self.rocks = rocks
        self.holes = holes

# Button class        
class Button:
    def __init__(self, image, location, width, height):
        self.image = image
        self.location = location
        self.width = width
        self.height = height
        
    def draw(self, canvas):
        canvas.draw_image(self.image, 
                          [BUTTON_WIDTH/2, BUTTON_HEIGHT/2], 
                          [BUTTON_WIDTH, BUTTON_HEIGHT],
                          self.location,
                          [self.width, self.height])
    
    def is_selected(self, click_position): #double check pos
        in_x = abs(click_position[0] - self.location[0]) < self.width/4
        in_y = abs(click_position[1] - self.location[1]) < self.height/4   
        return in_x and in_y
            
# Main draw handler
def draw_handler(canvas): 
    global alive, playing
    global GROUND
    global jump_count
    global background
    global hole1, hole2, rock1, rock2, rock3, button1
    global dist
    global room
    
    # Fall
    for hole in room_list[room].holes:        
        if player.has_fallen(hole):        
            GROUND += 1000
            player.vel[0] = 0
            room = 0
            alive = False
            playing = False
            room_list[room].rocks = []
            room_list[room].holes = []
    
    # Not alive
    if alive == False:   
        canvas.draw_image(END,
                      [END_WIDTH/2, END_HEIGHT/2],
                      [END_WIDTH, END_HEIGHT],
                      [WIDTH, HEIGHT/2],
                      [WIDTH*2, HEIGHT]) 
        canvas.draw_text('You died', (325, HEIGHT/2), 40, 'white')        
        canvas.draw_text('Score: ' + str(int(dist)), (350, 275), 25, 'white')
        canvas.draw_text('Press X to restart', (320, 405), 25, 'white')
        
    # Alive    
    if alive == True:
        canvas.draw_image(room_list[room].bg,
                      [BKGD_WIDTH/2, BKGD_HEIGHT/2],
                      [BKGD_WIDTH, BKGD_HEIGHT],
                      [WIDTH/2, HEIGHT/2],
                      [WIDTH, HEIGHT])
        if playing == True:
            dist = (player.pos[0] - PLAYER_SIZE[0]/2 + room*WIDTH)/5
            canvas.draw_text('Distance: '+ str(int(dist)), (595, 35), 30, 'white')
        if playing == False:
            button1.draw(canvas)
            
    for hole in room_list[room].holes:  
        hole.draw(canvas)        
    player.draw(canvas)
    for rock in room_list[room].rocks:
        rock.draw(canvas)
       
    for hole in room_list[room].holes:
        hole.update()   
    player.update()
    for rock in room_list[room].rocks:	
        rock.update()    
    
    # Player ground collisions    
    if player.pos[1] > GROUND:
        player.pos[1] = GROUND
        player.vel[1] = 0
        jump_count = 0
        
    # Rock collisions    
    for rock in room_list[room].rocks:
        if rock.has_collided(player):
            dist0 = ROCK_SIZE[0]/2 + PLAYER_SIZE[0]/2
            dist1 = ROCK_SIZE[1]/2 + PLAYER_SIZE[1]/2
            if player.vel[1] > 0 and player.pos[1] < rock.pos[1] - 90:
                player.pos[1] -= player.pos[1] - rock.pos[1] + dist1
                player.vel[1] = 0
                jump_count = 0
            else:
                if rock.pos[0] > player.pos[0]:
                    player.pos[0] = rock.pos[0] - dist0
                if rock.pos[0] < player.pos[0]:
                    player.pos[0] = rock.pos[0] + dist0
                    
# Mouseclick function                   
def mouse_click(mouse_position):
    global playing
    global button1
    if button1.is_selected(mouse_position):
        playing = True

# buttons in new_game()?
button1 = Button(ST_BUTTON, BUTTON_POSITION, BUTTON_SIZE_WIDTH, BUTTON_SIZE_HEIGHT)

# Key handlers
def key_down(key):
    global playing, alive
   
    if simplegui.KEY_MAP['a'] == key and playing == True:
        player.vel[0] -= 5

    if simplegui.KEY_MAP['d'] == key and playing == True:
        player.vel[0] += 5
       
    if simplegui.KEY_MAP['w'] == key and playing == True:
        player.jump()
       
    if simplegui.KEY_MAP['s'] == key and playing == True:
        player.vel[1] += 10
    
    if simplegui.KEY_MAP['x'] == key and alive == False:     
        alive = True
        playing = True
        new_game()
                       
def key_up(key):
   
    if simplegui.KEY_MAP['a'] == key and playing == True:
        player.vel[0] = 0

    if simplegui.KEY_MAP['d'] == key and playing == True:
        player.vel[0] = 0
                    
frame = simplegui.create_frame('game', WIDTH, HEIGHT)

# Game instructions
instructuions = frame.add_label('Instructions:', 200)
instructuions = frame.add_label('')
instructuions1 = frame.add_label('"a" left', 200)
instructuions2 = frame.add_label('"d" right', 200)
instructuions3 = frame.add_label('"w" jump', 200)
instructuions4 = frame.add_label('"s" down', 200)

frame.set_draw_handler(draw_handler)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_click)

new_game()
frame.start()