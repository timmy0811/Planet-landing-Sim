import pygame, random

pygame.init()
pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

#classes and functions
def draw_bg(bg_y, bg_x):
    screen.fill((0,0,0))
    tileset = 0
    for row in range(height + 1):
        tileset += 1

        for tile in range(width):
            if(tileset < int(height/4)):
                temp_surface = bg_tile[0] #exo
            elif(tileset == int(height/4)):
                temp_surface = bg_tile[1] #exomeso
            elif(tileset > int(height/4) and tileset < int(height/2)):
                temp_surface = bg_tile[2] #meso
            elif(tileset == int(height/2)):
                temp_surface = bg_tile[3] #mesotopo
            elif(tileset > int(height/2) and tileset < int(height/4 * 3)):
                temp_surface = bg_tile[4] #topo
            elif(tileset == int(height/4 * 3)):
                temp_surface = bg_tile[5] #topothermo
            else: 
                temp_surface = bg_tile[6]
            screen.blit(temp_surface, (((-(width/2) * win_x) + (tile *win_x)) - bg_y, ((-3 * win_y) + (row * win_y)) - bg_x)) 

def draw_fg(bg_y, bg_x):
    tileset = 0
    for row in range(height + 1):
        tileset += 1
        #WOP draw different foregrounds at different levels
        for tile in range(width):
            if(tileset < int(height/4)):
                temp_surface = fg1 #exo
            elif(tileset == int(height/4)):
                temp_surface = fg1 #exomeso
            elif(tileset > int(height/4) and tileset < int(height/2)):
                temp_surface = fg1 #meso
            elif(tileset == int(height/2)):
                temp_surface = fg2 #mesotopo
            elif(tileset > int(height/2) and tileset < int(height/4 * 3)):
                temp_surface = fg1 #topo
            elif(tileset == int(height/4 * 3)):
                temp_surface = fg2 #topothermo
            else: 
                temp_surface = fg1
            screen.blit(temp_surface, (((-(width/2) * win_x) + (tile *win_x)) - bg_y, ((-3 * win_y) + (row * win_y)) - bg_x)) 

def gen_ground():
    for tile in range(width):
        ground_rect.centerx = (-(width/2) * win_x) + (tile * win_x) + (win_x/2) - bg_x
        screen.blit(ground_surface, ground_rect)

def draw_lander():
    if(thr_left and fuel > 0):
        animated_surface = lander_left[animation_index]
    elif(thr_right and fuel > 0):
        animated_surface = lander_right[animation_index]
    else: 
        animated_surface = lander_surface

    rot_lander_surface = pygame.transform.rotozoom(animated_surface, angle, 1)
    rot_lander_rect = rot_lander_surface.get_rect(center = ((win_x/2, win_x/2 + 40)))
    
    if(thr_up and fuel > 0):
        rot_flame_surface = pygame.transform.rotozoom(flame[animation_index], angle, 1)
        rot_flame_rect = rot_flame_surface.get_rect(center = rot_lander_rect.center)

        screen.blit(rot_flame_surface, rot_flame_rect)

    screen.blit(rot_lander_surface, rot_lander_rect)

    return rot_lander_rect
        
def calc_thrust(y_movement, x_movement, angle, angle_left_exp, angle_right_exp):

    if(fuel > 0):
        if(thr_up):
            y_movement -= thrust_upward

            if(angle > 0 and angle < 180 or angle > -360 and angle < -180):
                x_movement -= angle * angle_thrust_factor

            if(angle < 0 and angle > -180 or angle > 360 and angle > 180):
                x_movement -= angle * angle_thrust_factor
                
        if(thr_left):
            angle_left_exp += angle_factor
        if(thr_right):
            angle_right_exp += angle_factor

        if(angle_left_exp >0 and thr_left == False):
            angle_left_exp -= angle_drag
        if(angle_right_exp >0 and thr_right == False):
            angle_right_exp -= angle_drag
        
        angle += angle_left_exp
        angle -= angle_right_exp

    if(angle >= 360 or angle <= -360): angle = 0

    return y_movement, x_movement, angle, angle_left_exp, angle_right_exp

def draw_score(altitude):
    
    data_alt_surface = font_data_m.render('Altitude: ' + str(int(altitude * 10) ) + ' m', True, (255, 255, 255))
    data_alt_rect = data_alt_surface.get_rect(topleft = (10, 10))

    data_fuel_surface = font_data_m.render('Fuel: ' + str(int(fuel)), True, (255, 255, 255))
    data_fuel_rect = data_fuel_surface.get_rect(topleft = (10, 45))

    data_angle_surface = font_data_m.render('Angle: ' + str(int(angle)) + '°', True, (255, 255, 255))
    data_angle_rect = data_fuel_surface.get_rect(topleft = (10, 115))

    data_xpos_surface = font_data_s.render('Pos: ' + str(x_pos) + 'm', True, (249, 135, 255))
    data_xpos_rect = data_xpos_surface.get_rect(center = (win_x/2, win_y/2 - 70))

    data_site_surface = font_data_s.render('Site: ' + str(site) + 'm', True, (249, 135, 255))
    data_site_rect = data_site_surface.get_rect(center = (win_x/2, win_y/2 - 45))

    speedy = y_movement
    speedx = x_movement
    data_speed_surface = font_data_m.render('Speed: ' + str(int(amount(speedy * 10))) + ' m/s', True, (255, 255, 255))
    data_speed_rect = data_speed_surface.get_rect(topleft = (10, 80))

    screen.blit(data_site_surface, data_site_rect)
    screen.blit(data_alt_surface, data_alt_rect)
    screen.blit(data_fuel_surface, data_fuel_rect)
    screen.blit(data_speed_surface, data_speed_rect)
    screen.blit(data_angle_surface, data_angle_rect)
    screen.blit(data_xpos_surface, data_xpos_rect)

def draw_instr():
    if(show_allert and altitude <= 30 and not landed):
        screen.blit(alt_warning_surface, alt_warning_rect) 

    if(landed and not crashed):
        landed_surface = font_instr_m.render('You landed!', True, (0, 196, 26))
        landed_rect = landed_surface.get_rect(center = (win_x/2, win_y/2 + 7))
        screen.blit(landed_surface, landed_rect)
    elif(crashed):
        landed_surface = font_instr_m.render('You crashed', True, (130, 0, 2))
        landed_rect = landed_surface.get_rect(center = (win_x/2, win_y/2 + 7))
        screen.blit(landed_surface, landed_rect)
    
    if(amount(site) - amount(x_pos) <= 10 and amount(site) - amount(x_pos) >= -10 ):
        range_surface = font_instr_s.render("on landing site", True, (16, 87, 0))
    else: range_surface = font_instr_s.render("out of landing site", True, (115, 11, 0))

    screen.blit(range_surface, range_surface.get_rect(center = (win_x/2, win_y/ 2 + 240)))

def amount(number):
    if(number < 0): 
        return number * -1
    else: return number

def calc_volume():
    volume_wind = (amount(y_movement) * 0.0666) * 0.5

    if(thr_up and fuel > 0):
        volume_main_thrust = 0.3
    else: volume_main_thrust = 0

    if(thr_left or thr_right and fuel > 0):
        volume_side_thrust = 0.2
    else: volume_side_thrust = 0

    sound_wind.set_volume(volume_wind)
    sound_main_thrust.set_volume(volume_main_thrust)
    sound_side_thrust.set_volume(volume_side_thrust)

def check_landing(x_movement, y_movement, angle, landed, crashed, altitude):
    if(rot_lander_rect.colliderect(ground_check_rect)):
        if(angle < 5 and y_movement < 2 and x_movement < 1.5 and landed == False and x_pos > site - 10 and x_pos < site + 10):
            print("landed")
            landed = True
            sound_landed.play()
        elif(landed == False):
                print("chrashed")
                landed = True
                crashed = True
                sound_crash.play()
                sound_ping.set_volume(0)
    
    if(landed):
        y_movement = 0
        x_movement = 0
        angle = 0
        altitude = 0

    return x_movement, y_movement, angle, landed, crashed, altitude

def manage_fuel(fuel):
    if(thr_up or thr_left or thr_right and fuel > 0):
        fuel -= 0.2
    return fuel

def compass(x_pos):
    x_pos = int(x_pos / 30)

    screen.blit(compass_bg_surface, (150, win_y/2 + 200))
    screen.blit(compass_node_surface, (100 + site - x_pos, win_y/2 + 200))

    screen.blit(alt_surface, (win_x - 50, 95))
    pygame.draw.rect(screen, (194, 0, 0), (win_x - 51, (win_y - 95) - (altitude / compass_height_seg), 15, 15), True)

    return x_pos
    
#variables
win_x = 700
win_y = 650
animation_index = 0
game_status = 'fall'

site = random.randrange(-200, 200, 1)
x_pos = 0
y_movement = 3
x_movement = 0
gravity = 0.048
angle = 0

height = 20 + 5 #minimum 10 tiles
width = 30

altitude = ((height - 3) * win_y ) / 60
speedy = 0
speedx = 0
fuel = amount(site) * 2 + 300

angle_factor = 0.005
angle_thrust_factor = 0.001 
angle_left_exp = 0
angle_right_exp = 0
angle_drag = 0.002
bg_x = 0
bg_y = 0
landed = False
crashed = False
temp_surface = None
show_allert = False
compass_height_seg = altitude / 400

thr_up = False
thrust_upward = 0.07

thr_left = False
thrust_left = 0.5

thr_right = False
thrust_right = 0.5

#window setup
screen = pygame.display.set_mode((win_x, win_y))
clock = pygame.time.Clock()

programIcon = pygame.image.load('Space landing Simulator/assets/lander.png').convert_alpha()
pygame.display.set_icon(programIcon)
pygame.display.set_caption('Planet landing Simulator')

#import sprites
lander_surface = pygame.image.load('Space landing Simulator/assets/lander.png').convert_alpha()
lander_rect = lander_surface.get_rect(center = (win_x/2, win_y/2))

ground_surface = pygame.image.load('Space landing Simulator/assets/ground_tile.png').convert_alpha()
ground_rect = ground_surface.get_rect(center = (win_x/2, win_y/2))

compass_bg_surface = pygame.image.load('Space landing Simulator/assets/compass_bg.png').convert_alpha()
compass_node_surface = pygame.image.load('Space landing Simulator/assets/compass_node.png').convert_alpha()
alt_surface = pygame.image.load('Space landing Simulator/assets/sidescroll.png').convert_alpha()

lander_left1 = pygame.image.load('Space landing Simulator/assets/lander_left1.png').convert_alpha()
lander_left2 = pygame.image.load('Space landing Simulator/assets/lander_left2.png').convert_alpha()
lander_left3 = pygame.image.load('Space landing Simulator/assets/lander_left3.png').convert_alpha()

lander_right1 = pygame.image.load('Space landing Simulator/assets/lander_right1.png').convert_alpha()
lander_right2 = pygame.image.load('Space landing Simulator/assets/lander_right2.png').convert_alpha()
lander_right3 = pygame.image.load('Space landing Simulator/assets/lander_right3.png').convert_alpha()

flame1 = pygame.image.load('Space landing Simulator/assets/thrust1.png').convert_alpha()
flame2 = pygame.image.load('Space landing Simulator/assets/thrust2.png').convert_alpha()
flame3 = pygame.image.load('Space landing Simulator/assets/thrust3.png').convert_alpha()

bg_exo = pygame.image.load('Space landing Simulator/assets/Bg1.png').convert_alpha()
bg_exo_meso = pygame.image.load('Space landing Simulator/assets/Bg2.png').convert_alpha()
bg_meso = pygame.image.load('Space landing Simulator/assets/Bg3.png').convert_alpha()
bg_meso_topo = pygame.image.load('Space landing Simulator/assets/Bg4.png').convert_alpha()
bg_topo = pygame.image.load('Space landing Simulator/assets/Bg5.png').convert_alpha()
bg_topo_thermo = pygame.image.load('Space landing Simulator/assets/Bg6.png').convert_alpha()
bg_thermo = pygame.image.load('Space landing Simulator/assets/Bg7.png').convert_alpha()

fg1 = pygame.image.load('Space landing Simulator/assets/fg1.png').convert_alpha()
fg2 = pygame.image.load('Space landing Simulator/assets/fg2.png').convert_alpha()

bg_tile = [bg_exo, bg_exo_meso, bg_meso, bg_meso_topo, bg_topo, bg_topo_thermo, bg_thermo]

lander_left = [lander_left1, lander_left2, lander_left3]
lander_right = [lander_right1, lander_right2, lander_right3]
flame = [flame1, flame2, flame3]

ground_check_surface = pygame.image.load('Space landing Simulator/assets/ground_check.png').convert_alpha()
ground_check_rect = ground_check_surface.get_rect(center = (win_x/2, 1000))

#sounds
sound_wind = pygame.mixer.Sound('Space landing Simulator/assets/wind.wav')
sound_main_thrust = pygame.mixer.Sound('Space landing Simulator/assets/main_thrust.wav')
sound_side_thrust = pygame.mixer.Sound('Space landing Simulator/assets/side_thrust.wav')
sound_ambient_music = pygame.mixer.Sound('Space landing Simulator/assets/ambient.wav')
sound_beep = pygame.mixer.Sound('Space landing Simulator/assets/beep.wav')
sound_crash = pygame.mixer.Sound('Space landing Simulator/assets/crash.wav')
sound_ping = pygame.mixer.Sound('Space landing Simulator/assets/ping.wav')
sound_landed = pygame.mixer.Sound('Space landing Simulator/assets/landed.wav')

volume_main_thrust = 0
volume_side_thrust = 0
volume_wind = 0

sound_wind.set_volume(0)
sound_main_thrust.set_volume(0)
sound_side_thrust.set_volume(0)
sound_beep.set_volume(0.1)
sound_ambient_music.set_volume(0.2)
sound_crash.set_volume(0.3)
sound_ping.set_volume(0.1)
sound_landed.set_volume(0.15)

sound_wind.play()
sound_main_thrust.play()
sound_side_thrust.play()
sound_ambient_music.play()
sound_ping.play()

#fonts
font_data_m = pygame.font.Font('Space landing Simulator/droid.ttf', 45)
font_data_s = pygame.font.Font('Space landing Simulator/droid.ttf', 35)
font_instr_m = pygame.font.Font('Space landing Simulator/ka1.ttf', 21)
font_instr_s = pygame.font.Font('Space landing Simulator/ka1.ttf', 15)

alt_warning_surface = font_instr_m.render('ALTITUDE WARNING!', True, (245, 227, 66))
alt_warning_rect =  alt_warning_surface.get_rect(center = (win_x/2, win_y/2 - 100))

#events
ANIMATION = pygame.USEREVENT
pygame.time.set_timer(ANIMATION, 100)

WIND = pygame.USEREVENT + 1
pygame.time.set_timer(WIND, 75000)

MAINTHRUST = pygame.USEREVENT + 2
pygame.time.set_timer(MAINTHRUST, 2815)

SIDETHRUST = pygame.USEREVENT + 3
pygame.time.set_timer(SIDETHRUST, 2043)

ALTALLERT = pygame.USEREVENT + 4
pygame.time.set_timer(ALTALLERT, 300)

PING = pygame.USEREVENT + 5
pygame.time.set_timer(PING, 25519)

running = True
while (running):
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE):
                thr_up = True
            if(event.key == pygame.K_LEFT):
                thr_left = True
            if(event.key == pygame.K_RIGHT):
                thr_right = True
        if (event.type == pygame.KEYUP):
            if(event.key == pygame.K_SPACE):
                thr_up = False
            if(event.key == pygame.K_LEFT):
                thr_left = False
            if(event.key == pygame.K_RIGHT):
                thr_right = False
        if (event.type == ANIMATION):
            animation_index += 1
            if(animation_index > 2): animation_index = 0
        if (event.type == WIND):
            sound_wind.play()
        if (event.type == MAINTHRUST):
            sound_main_thrust.play()
        if (event.type == SIDETHRUST):
            sound_side_thrust.play()
        if (event.type == PING and not landed):
            sound_ping.play()
        if (event.type == ALTALLERT):
            if(altitude <= 30 and not landed):
                sound_beep.play()
            if(show_allert):
                show_allert = False
            else: show_allert = True
           
#draw
    #GAME-MODE FALLING
    if(game_status == 'fall'):
        #background offset
        if(not landed):
            bg_x += x_movement
            bg_y += y_movement

        draw_bg(bg_x, bg_y)
        
        #generate ground
        ground_rect.top = (height - 3) * win_y - bg_y 
        ground_rect.centerx = win_x/2 - bg_x 

        gen_ground()

        #draw lander
        rot_lander_rect = draw_lander()

        #draw foreground WORK IN PROGRESS
        #draw_fg(bg_x, bg_y)

        #apply gravity and calculate thrust
        y_movement += gravity
        y_movement, x_movement, angle, angle_left_exp, angle_right_exp = calc_thrust(y_movement, x_movement, angle, angle_left_exp, angle_right_exp)
        if(y_movement > 15): y_movement = 15
        
        #draw data to screen
        altitude -= y_movement / 60 
        draw_score(altitude)

        draw_instr()
        fuel = manage_fuel(fuel)
        x_pos = compass(bg_x)
        
        #check if craft has landed
        x_movement, y_movement, angle, landed, crashed, altitude = check_landing(x_movement, y_movement, angle, landed, crashed, altitude)
        ground_check_rect.top = ground_rect.top

        #calculate sound volume
        calc_volume()
    
#refresh times
    pygame.display.flip()
    clock.tick(60)

pygame.quit()