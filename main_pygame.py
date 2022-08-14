
import pygame
import win32api
import win32con
import win32gui
import random
import os
import time
import json
import requests
from threading import Timer
pygame.init()

url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"

querystring = {"lon":"-118","lat":"34"}

headers = {
	"X-RapidAPI-Key": "ee7bf798a6msh35a2e659e32f426p1dea94jsnc8ef175b5a09",
	"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
response_dict = json.loads(response.text)
#print(response.text)
print("For Today's weather in,",response_dict["data"][0]["timezone"]+", there are",response_dict["data"][0]["weather"]["description"],"with temperatures of",str(response_dict["data"][0]["temp"])+"C.")

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

quote_length_time = 4000
quote_frequency = 5000


#speech bubble
def speech_bubble(screen, text, text_colour, bg_colour, pos, size):

    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, text_colour)
    text_rect = text_surface.get_rect(midbottom=pos)

    # background
    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(20, 20)

    #frame
    frame_rect = bg_rect.copy()
    frame_rect.inflate_ip(4,4)

    # pygame.draw.rect(screen, bg_colour, bg_rect)
    pygame.draw.rect(screen, text_colour, frame_rect)
    pygame.draw.rect(screen, bg_colour, bg_rect)
    screen.blit(text_surface, text_rect)


screen_bounds = {"MIN":-58,"MAX_B":screen_size.current_h-184,"MAX_R":screen_size.current_w-150}
        

# Pet Class
class Pet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_delay = 15
        self.m_cwd = os.getcwd() # gets the current path to directory HackAlphaX
        self.image_num = 0 # counts which frame of animation it's on
        # loads in a default initial frame to be idle
        self.dir = 0 # 0 is left, 1 is right
        self.image = pygame.image.load(self.m_cwd+"\pet_animations\idle\idle"+str(self.image_num+self.dir*4)+".png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(200,200)) # scale image to size
        self.image_fall = pygame.image.load(self.m_cwd+"\pet_animations\\CF.png").convert_alpha()
        self.image_fall = pygame.transform.scale(self.image_fall,(200,200))
        self.image_pick_up = pygame.image.load(self.m_cwd+"\pet_animations\\PUC.png").convert_alpha()
        self.image_pick_up = pygame.transform.scale(self.image_pick_up,(200,200))
        self.rect = self.image.get_rect() # makes the image an interactable sprite object
        self.rect.x = x # pet sprite coordinates
        self.rect.y = y
        self.advice_text = "" # current active advice text
        self.speed = 10 # how fast pet moves
        self.tracking = 0 # pet follows cursor or not
        self.falling = 0 # checks if pet falling
        self.status_list = ["idle","walk","sleepb","wag","pat"] # list of behaviours (it's ordered so add new moves
                                                   # at the end of the list)
        self.checkin = ["Did you exercise today?", "Did you drink water?", "You got this!", "Make sure to take plenty of breaks!", "For Today's weather in,",response_dict["data"][0]["timezone"]+", there are",response_dict["data"][0]["weather"]["description"],"with temperatures of",str(response_dict["data"][0]["temp"])+"C."]
        self.motivate = 0
        self.status = self.status_list[random.randint(0,3)] # idle as default
        self.status_count = 1 # counter for iterating frames after every tick
    
    def update(self):
        if (self.tracking == 1):
            self.rect.center = pygame.mouse.get_pos()
        elif (self.falling == 1):
            if ((self.rect.y + self.speed)<=screen_bounds["MAX_B"]):
                self.rect.y += self.speed
            else:
                self.falling = 0
        elif self.image_delay < 1:
            if self.motivate and self.advice_text != "":
                speech_bubble(screen, str(self.advice_text), (255, 255, 255), (0, 0, 0), self.rect.midtop, 80)
            self.image_num = (self.image_num+1)%4 # chooses animation (%4 because there are 4 images per animation cycle)
            # label the animations carefully in format [ACTIONNAME][NUMBER FROM 0-3].png
            self.image = pygame.image.load(self.m_cwd+"\pet_animations\\"+self.status+"\\"+self.status+str(self.image_num+self.dir*4)+".png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(200,200))
            self.status_count-= 1 # decreases move counter to acknowledge a move is made
            if (self.status_count < 1): # choose a random new move and the amount of times it does that same action
                                        # given current action is out of moves
                self.dir = 0
                self.status = self.status_list[random.randint(0,3)]
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
            self.image_delay = 15
        else:
            if self.motivate and self.advice_text != "":
                speech_bubble(screen, str(self.advice_text), (255, 255, 255), (0, 0, 0), self.rect.midtop, 40)
            self.image_delay -= 1

# keep track of all the sprites currently existing (i.e. just the pet sprite atm)
all_sprites_list = pygame.sprite.Group()
pet = Pet(random.randint(screen_bounds["MIN"],screen_bounds["MAX_R"]),screen_bounds["MAX_B"])
all_sprites_list.add(pet)

#Sets up timer for quotes
quote = pygame.USEREVENT+1
quote_length = pygame.USEREVENT+2
pygame.time.set_timer(quote, quote_frequency)

# Main game loop
while not done:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit upon click close button
            done = True
        elif event.type == quote:
            #Sets up timer for quotes
            pygame.time.set_timer(quote_length, quote_length_time)
            pet.advice_text = pet.checkin[random.randint(0,4)]
            pet.motivate = True
        elif event.type == quote_length:
            pet.motivate = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x,y = event.pos
                if pet.rect.collidepoint(x,y):
                    pet.tracking = 1
                    pet.dir = 0
                    pet.image = pet.image_pick_up
                    pet.status = pet.status_list[0] # picked up status
            elif event.button == 3:
                pet.status = "pat"
                pet.status_count = 70
                pet.dir = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pet.tracking = 0
                pet.falling = 1
                pet.image = pet.image_fall
                pet.dir = 0
            if event.button == 3:
                pet.status_count = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F10:
                pet.rect.center = ((screen_bounds["MAX_R"]-screen_bounds["MIN"])/2, (screen_bounds["MAX_B"]-screen_bounds["MIN"])/2)
                pet.falling = 1
                pet.image = pet.image_fall


    screen.fill(transparency) # Transparent background
    # --- Game logic should go here
    all_sprites_list.update() # runs the update function for all sprites in the list
    # --- Drawing code should go here
    all_sprites_list.draw(screen) # draws all the sprites onto the screen (must redraw every cycle of loop like so)
    # Updates screen
    pygame.display.flip()
 
    # Determine FPS
    clock.tick(60)