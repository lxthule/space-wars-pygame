import pygame
import os
pygame.font.init() # initianalize pygame font
# is a 2D surface platform for creating games in python

WIDTH, HEIGHT = 900, 500

#set window sizing for pygame
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# caption application
pygame.display.set_caption('My First Pygame! : Space WARS')
# setting color background
WHITE = (255,255,255)
#setting game border rect for players and divide window in half
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

#health text 
HEALTH_FONT = pygame.font.SysFont('comicsans', 40) #(font family, font size)

#BORDER COLOR
BLACK = (0, 0, 0)
# uno bullet color = RED
UNO_BUL_COLOR = (225, 225, 0)
# dos bullet color = YELLOW
DOS_BUL_COLOR = (255, 0, 0)

# set bullet variable FOR VELOCITY
BULLET_VEL = 7
# infinite number of bullets
MAX_BULLETS = 3
#frames per second
FPS = 60
# player width and height
PLAYER_WIDTH, PLAYER_HEIGHT = 55, 40

# uno and dos hit events
UNO_HIT = pygame.USEREVENT + 1
DOS_HIT = pygame.USEREVENT + 2

# winner text font
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# 1:30:27 for sound effects
# pygame.mixer.load(os.path.join('Assets', 'filepath.mp3'))

# velocity for how much the keys to move
VEL = 5
# init image for player one
READY_PLAYER_ONE = pygame.image.load(os.path.join('Assets', 'space_one.png'))
# resize player one to fit in window
PLAYER_ONE = pygame.transform.scale(READY_PLAYER_ONE, (PLAYER_WIDTH, PLAYER_HEIGHT))
# ROTATE PLAYER ONE 90deg
PLAYER_ONE_TRANS = pygame.transform.rotate(PLAYER_ONE, 270)
# init image for player two
READY_PLAYER_TWO = pygame.image.load(os.path.join('Assets', 'space_two.png'))
# resize player two to fit in window
PLAYER_TWO = pygame.transform.scale(READY_PLAYER_TWO, (PLAYER_WIDTH, PLAYER_HEIGHT))
# ROTATE PLAYER TWO 90deg
PLAYER_TWO_TRANS = pygame.transform.rotate(PLAYER_TWO, 90)

# game background image
SPACE = pygame.image.load(os.path.join('Assets', 'space_bg.webp'))
SPACE_IMG = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))

def draw_window(uno, dos, uno_bullets, dos_bullets, uno_health, dos_health): # parameter for x and y position on one and two
    # fill color
    # WIN.fill(WHITE)
    WIN.blit(SPACE_IMG, (0, 0)) # SET BACKGROUND IMAGE
    # DRAWING BLACK BORDER DIVING SCREEN IN HALF
    pygame.draw.rect(WIN, BLACK, BORDER)

    #set player health to render on pygame window
    uno_health_text = HEALTH_FONT.render('Health: ' + str(dos_health), 1, WHITE)
    dos_health_text = HEALTH_FONT.render('Health: '  + str(uno_health), 1, WHITE)

    # render health text on screen
    WIN.blit(uno_health_text, (WIDTH - uno_health_text.get_width() - 10, 10))
    WIN.blit(dos_health_text, (10, 10))

    # draw player one and two to the window
    WIN.blit(PLAYER_ONE_TRANS, (uno.x, uno.y))
    WIN.blit(PLAYER_TWO_TRANS, (dos.x, dos.y))

    # uno and dos bullets to draw bullets... pass params
    for bullet in uno_bullets:
        pygame.draw.rect(WIN, UNO_BUL_COLOR, bullet)

    for bullet in dos_bullets:
        pygame.draw.rect(WIN, DOS_BUL_COLOR, bullet)

    pygame.display.update()  # call update function after change

# set function for player one movement
def uno_movement(keys_pressed, uno):
    if keys_pressed[pygame.K_a] and uno.x - VEL > 0:   
        uno.x -= VEL           # a means LEFT
    if keys_pressed[pygame.K_d] and uno.x + VEL + uno.width < BORDER.x:   
        uno.x += VEL           # d means RIGHT
    if keys_pressed[pygame.K_w] and uno.y - VEL > 0:   
        uno.y -= VEL           # w means UP
    if keys_pressed[pygame.K_s] and uno.y + VEL + uno.height < HEIGHT - 15:   
        uno.y += VEL           # s means DOWN 

def dos_movement(keys_pressed, dos):
    if keys_pressed[pygame.K_LEFT] and dos.x - VEL > BORDER.x + BORDER.width:   
        dos.x -= VEL           # a means LEFT
    if keys_pressed[pygame.K_RIGHT] and dos.x + VEL + dos.width < WIDTH:   
        dos.x += VEL           # d means RIGHT
    if keys_pressed[pygame.K_UP] and dos.y - VEL > 0:   
        dos.y -= VEL           # w means UP
    if keys_pressed[pygame.K_DOWN] and dos.y + VEL + dos.height < HEIGHT - 15:   
        dos.y += VEL           # s means DOWN 

def handle_bullets(uno_bullets, dos_bullets, uno, dos):
    for bullet in uno_bullets:
        bullet.x += BULLET_VEL
        # check of bullet collieded with dos
        if dos.colliderect(bullet):
            pygame.event.post(pygame.event.Event(DOS_HIT))
            uno_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            uno_bullets.remove(bullet)

    for bullet in dos_bullets:
        bullet.x -= BULLET_VEL
        # check of bullet collieded with uno
        if uno.colliderect(bullet):
            pygame.event.post(pygame.event.Event(UNO_HIT))
            dos_bullets.remove(bullet)
        elif bullet.x < 0:
            dos_bullets.remove(bullet)

def draw_winner(text):
    # drawing winner text on pygame window screen
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    # show winner then delay 5 secs then restart game
    pygame.time.delay(5000)

def main():
    # player position
    uno = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    dos = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    # player one bullets 
    uno_bullets = []
    #player two bullets
    dos_bullets = []

    #player health
    uno_health = 10
    dos_health = 10

    clock = pygame.time.Clock()
    # function for game loop
    run = True
    while run:
        clock.tick(FPS) #ensure game speed is controlled to FPS and not any faster
        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # eg if user quits window, close game
                run = False
                pygame.quit()

            # bullets for players function
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(uno_bullets) < MAX_BULLETS:
                    # bullet Rect(bullet dimensions, width and height pf bullet)
                    bullet = pygame.Rect(uno.x + uno.width, uno.y + uno.height//2 - 2, 10, 5)
                    uno_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(dos_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(dos.x, dos.y + dos.height//2 - 2, 10, 5)
                    dos_bullets.append(bullet)

            # events for uno and dos hit
            if event.type == UNO_HIT:
                uno_health -= 1
            if event.type == DOS_HIT:   
                dos_health -= 1
        winner_text = ''
        if uno_health <= 0:
            winner_text = 'Player Two Wins!'
        if dos_health <= 0:
            winner_text = 'Player One Wins!'
        if winner_text != '':
            draw_winner(winner_text)
            break

        # uno.x += 1   # move position updating position by 1 per fps
        # using keyboard keys to move players 
        # while while loop is looping store keys being pressed currently
        # print(uno_bullets, dos_bullets)   # console logging bullets
        keys_pressed = pygame.key.get_pressed()
        
        uno_movement(keys_pressed, uno)     # call uno function
        dos_movement(keys_pressed, dos)     #call dos function

        # function to handle bullets
        handle_bullets(uno_bullets, dos_bullets, uno, dos)


        # pass in uno and dos as arguements to function draw_window
        draw_window(uno, dos, uno_bullets, dos_bullets, uno_health, dos_health)

    # instead of quitting game, game restarts after winner displayed text
    main()  

if __name__ == '__main__':
    main() # run game function