
import pygame
import win32api
import win32con
import win32gui
import random
import os
import time
from threading import Timer
pygame.init()

# Initialize start loop condition
done = False
# Setup window screen
screen_size = pygame.display.Info()
screen = pygame.display.set_mode((screen_size.current_w,screen_size.current_h), pygame.NOFRAME) # Remove window top border
transparency = (255, 0, 128)  # Transparency color
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency), 0, win32con.LWA_COLORKEY)
# Set window in front of all apps
win32gui.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 1)


# Initialize internal clock
clock = pygame.time.Clock()

#speech bubble
def speech_bubble(screen, text, text_colour, bg_colour, pos, size):

    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, text_colour)
    text_rect = text_surface.get_rect(midbottom=pos)

    # background
    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(20, 20)

    pygame.draw.rect(screen, bg_colour, bg_rect)
    screen.blit(text_surface, text_rect)


screen_bounds = {"MIN":-58,"MAX_B":screen_size.current_h-184,"MAX_R":screen_size.current_w-150}
#Speech Class
'''class speech_bubble(pygame.sprite.Sprite):
    def __init__(self, text, text_colour, bg_colour, pos, size):
        super().__init__()
        self.pos = pos
        self.text = text
        self.size = size
        self.text_colour = text_colour
        self.bg_colour = bg_colour
        self.font = pygame.font.SysFont(None, self.size)
        self.text_surface = self.font.render(self.text, True, self.text_colour)
        self.text_rect = self.text_surface.get_rect(midbottom=self.pos)
        # background
        self.bg_rect = self.text_rect.copy()
        #self.bg_rect.inflate_ip(20, 20)
    def create(self):
        pygame.draw.rect(screen, self.bg_colour, self.bg_rect)
        screen.blit(self.text_surface, self.text_rect)'''

# Pet Class
class Pet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.m_cwd = os.getcwd() # gets the current path to directory HackAlphaX
        self.image_num = 0 # counts which frame of animation it's on
        # loads in a default initial frame to be idle
        self.dir = 0 # 0 is left, 1 is right
        self.image = pygame.image.load(self.m_cwd+"\pet_animations\idle"+str(self.image_num+self.dir*4)+".png")
        self.image = pygame.transform.scale(self.image,(200,200)) # scale image to size
        self.rect = self.image.get_rect() # makes the image an interactable sprite object
        self.rect.x = x # pet sprite coordinates
        self.rect.y = y
        self.speed = 8 # how fast pet moves
        self.status_list = ["idle","walk","sleepb"] # list of behaviours (it's ordered so add new moves
                                                   # at the end of the list)
        self.checkin = ["Did you exercise today?", "Did you drink water?", "API QUOTE"]
        self.motivate = True
        # self.status_list = ["sleepb"]
        self.status = self.status_list[random.randint(0,2)] # idle as default
        self.status_count = 1 # counter for iterating frames after every tick
        #self.motivate = False # The thing used for text box
    
    def update(self):
        self.image_num = (self.image_num+1)%4 # chooses animation (%4 because there are 4 images per animation cycle)
        # label the animations carefully in format [ACTIONNAME][NUMBER FROM 0-3].png
        self.image = pygame.image.load(self.m_cwd+"\pet_animations\\"+self.status+str(self.image_num+self.dir*4)+".png")
        self.image = pygame.transform.scale(self.image,(200,200))
        self.status_count-= 1 # decreases move counter to acknowledge a move is made
        if self.motivate:

            speech_bubble(screen, str(self.checkin[random.randint(0,2)]), (255, 255, 255), (0, 0, 0), self.rect.midtop, 40)
        if (self.status_count < 1): # choose a random new move and the amount of times it does that same action
                                    # given current action is out of moves
            self.dir = 0
            self.status = self.status_list[random.randint(0,2)]
            self.status_count = random.randint(10,70)
            if (self.status == "walk"):
                self.dir = random.randint(0,1) # choose random direction if walking chosen
            print(self.status, self.dir) # just for debugging = shows you what new random move is being selected
        elif (self.status == "walk"):
            if ((self.dir == 0) and ((self.rect.x-self.speed)>screen_bounds["MIN"])):
                self.rect.x = (self.rect.x - self.speed) # move the character given it's current direction
            elif (self.dir ==0):
                self.dir = 1
            elif (self.dir == 1) and ((self.rect.x + self.speed)<screen_bounds["MAX_R"]):                        # stop if out of bounds
                self.rect.x = self.rect.x + self.speed
            elif (self.dir == 1):
                self.dir = 0
    def quote(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.motivate == True:
            speech_bubble(screen, str(self.checkin[random.randint(0,2)]), (255, 255, 255), (0, 0, 0), self.rect.midtop, 40)

# keep track of all the sprites currently existing (i.e. just the pet sprite atm)
all_sprites_list = pygame.sprite.Group()
pet = Pet(random.randint(screen_bounds["MIN"],screen_bounds["MAX_R"]),screen_bounds["MAX_B"])
all_sprites_list.add(pet)

#Sets up timer for quotes
quote = pygame.USEREVENT+1
pygame.time.set_timer(quote, 1000)

# Main game loop
while not done:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit upon click close button
            done = True
        if event.type == quote:
            pet.quote(screen)


    screen.fill(transparency) # Transparent background
    # --- Game logic should go here
    all_sprites_list.update() # runs the update function for all sprites in the list
    #pet.update()
    # --- Drawing code should go here
    all_sprites_list.draw(screen) # draws all the sprites onto the screen (must redraw every cycle of loop like so)
    #pet.draw(screen)
    # Updates screen
    pygame.display.flip()
 
    # Determine FPS
    clock.tick(4)