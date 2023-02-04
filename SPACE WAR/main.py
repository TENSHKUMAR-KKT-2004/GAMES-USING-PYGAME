import pygame
import os
# init font
pygame.font.init()
# init sound effect
pygame.mixer.init()

# setting up the window to show the game as display object
WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SPACE WAR")

# load a assets
# load the ships
SPACESHIP_1_PNG = pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
SPACESHIP_2_PNG = pygame.image.load(os.path.join("Assets","spaceship_red.png"))
# load the background image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(WIDTH,HEIGHT))
# load the sound effects
BULLET_HIT = pygame.mixer.Sound(os.path.join("Assets","Grenade_Sound.mp3"))
BULLET_FIRED = pygame.mixer.Sound(os.path.join("Assets","Gun_Silencer.mp3"))

# background color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,1)
YELLOW = (255,255,0)

# border b/w two ships
BORDER = pygame.Rect(WIDTH//2 -5,0,10,HEIGHT) # Rect arguments (x-axis position on the screen,y-axis on the screen,width of the rectangle,height of the rectangle)

# set the frame rate value
FPS = 60
# key movements
VELOCITY = 3 # velocity of the box movement as pixel
# bullets velocity and MAX bullets
B_VEL = 6
MAX_B = 3

# create a own events for check the ships was attacked or not
YELLOW_HIT = pygame.USEREVENT + 1 # +1 and +2 for make the event as unique
RED_HIT = pygame.USEREVENT + 2

# transform into small scale size
S_WIDTH = 40
S_HEIGHT = 35
SPACESHIP_1_RESIZE = pygame.transform.scale(SPACESHIP_1_PNG , (S_WIDTH,S_HEIGHT))
SPACESHIP_2_RESIZE = pygame.transform.scale(SPACESHIP_2_PNG , (S_WIDTH,S_HEIGHT))

# transform the image rotation 
SPACESHIP_1 = pygame.transform.rotate(SPACESHIP_1_RESIZE,90)
SPACESHIP_2 = pygame.transform.rotate(SPACESHIP_2_RESIZE,270)

# health font init adding style and size
HEALTH_FONT = pygame.font.SysFont("comicsans",40)
# winner font init adding style and size
WINNER_FONT = pygame.font.SysFont("comicsans",80)

# draw the window
def draw_window(yellow,red,yellow_bullets,red_bullets,red_health,yellow_health):
    # background picture setup
    WIN.blit(SPACE,(0,0))
    # all updates will be added after the fill the background and the order is must because this is 2d representation
    pygame.draw.rect(WIN,BLACK,BORDER)
    # draw the health
    # set the text object
    red_health_text = HEALTH_FONT.render("Health:"+str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:"+str(yellow_health),1,WHITE)
    # draw the text on the screen
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))
    # display the ships
    WIN.blit(SPACESHIP_1,(yellow.x,yellow.y)) # arguments as (loader_image , position of the image on the screen)
    WIN.blit(SPACESHIP_2,(red.x,red.y))# blit is used to show something on the screen
    # shoot the bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    # display all updates on the predefined window which is made by us (WIN) 
    pygame.display.update() # all of the previous modification will update

# yellow ship movement
def yellow_handle_movement(keys_pressed,yellow):
    # here we need to check the movement of the ship based on the key pressed and the ship don't go aut of the screen
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0 : #LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x : #RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0 : #UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT-5 : #DOWN
        yellow.y += VELOCITY
# red ship movement
def red_handle_movement(keys_pressed,red):
    # here we need to check the movement of the ship based on the key pressed and the ship don't go aut of the screen
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + 15 : #LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x +VELOCITY + red.width < WIDTH: #RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0 : #UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT-5 : #DOWN
        red.y += VELOCITY

# handle the bullet movement, collision of the bullet 
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += B_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT)) # trigger our own event to tell the collision was occured 
            yellow_bullets.remove(bullet) # remove the bullet from the array as well as from screen
        elif bullet.x > WIDTH : # we need to remove after the bullet pass over the edge of the screen. if doesn't remove means it will not fire another set of 3 bullets.
             yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= B_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT)) # trigger our own event to tell the collision was occured 
            red_bullets.remove(bullet) # remove the bullet from the array as well as from screen
        elif bullet.x < 0: # we need to remove after the bullet pass over the edge of the screen. if doesn't remove means it will not fire another set of 3 bullets.
           red_bullets.remove(bullet)

# draw the winner text on the screen 
def draw_winner(text):
    # set the text object
    draw_text = WINNER_FONT.render(text,1,WHITE)
    # draw the text on the screen
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2 , HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    # for move the image we need to consider images as Rectangle box
    yellow = pygame.Rect(300,100,S_WIDTH,S_HEIGHT) # arguments as (image positions on the screen x,y & image size WIDTH,HEIGHT)
    red = pygame.Rect(700,100,S_WIDTH,S_HEIGHT)
    
    # health of the ships
    yellow_health = 10
    red_health = 10
    
    # create clock object to set a frame rate
    clock = pygame.time.Clock()
    
    # bullets of the ships
    yellow_bullets = []
    red_bullets = []

    run = True

    while run:     
        # setting up the fps rate
        clock.tick(FPS)
        
        # event handling
        for event in pygame.event.get():
            # event handling for close the game  
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # when the shoot button was triggerd we need to create the bullets and make sure the MAX no of bullets is 3 when they passed on the screen  
            if event.type == pygame.KEYDOWN:
                # for yellow ship
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_B:
                    bullet = pygame.Rect(yellow.x + yellow.width , yellow.y + yellow.height//2 -2 ,8,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRED.play()
                # for red ship  
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_B:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 -2 ,8,5)
                    red_bullets.append(bullet)
                    BULLET_FIRED.play()                

            # if the bullet collide with ship means our own event get triggered. so we need to play a hit sound and subtract the health of the ship
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1  
                BULLET_HIT.play()

        # check the winner and show the winner on the screen
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW SHIP WIN!"
        if yellow_health <= 0:
            winner_text = "RED SHIP WIN!" 
        if winner_text != "":
            draw_winner(winner_text) 
            break

        # getting the pressed keys and move the ship based on the key pressed
        keys_pressed = pygame.key.get_pressed()
        # send the key pressed as dict and ship boxes (rectangle)
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        # handle the bullets
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        
        # draw the game on the screen
        draw_window(yellow,red,yellow_bullets,red_bullets,red_health,yellow_health)

    main()
    
# make sure this file will run directly or not and call the main function   
if __name__ == "__main__":
    main()