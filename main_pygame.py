
import pygame
import win32api
import win32con
import win32gui
import random
import os

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

# Pet Class
screen_bounds = {"MIN":-58,"MAX_B":screen_size.current_h-184,"MAX_R":screen_size.current_w-150}
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
        self.speed = 10 # how fast pet moves
        self.status_list = ["idle","walk","sleep"] # list of behaviours (it's ordered so add new moves
                                                   # at the end of the list)
        self.status = self.status_list[random.randint(0,2)] # idle as default
        self.status_count = 1 # counter for iterating frames after every tick
    
    def update(self):
        self.image_num = (self.image_num+1)%4 # chooses animation (%4 because there are 4 images per animation cycle)
        # label the animations carefully in format [ACTIONNAME][NUMBER FROM 0-3].png
        self.image = pygame.image.load(self.m_cwd+"\pet_animations\\"+self.status+str(self.image_num+self.dir*4)+".png")
        self.image = pygame.transform.scale(self.image,(200,200))
        self.status_count-= 1 # decreases move counter to acknowledge a move is made
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



# keep track of all the sprites currently existing (i.e. just the pet sprite atm)
all_sprites_list = pygame.sprite.Group()
pet = Pet(random.randint(screen_bounds["MIN"],screen_bounds["MAX_R"]),screen_bounds["MAX_B"])
all_sprites_list.add(pet)

# Main game loop
while not done:
    # Events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit upon click close button
            done = True
 

    screen.fill(transparency) # Transparent background
    # --- Game logic should go here
    all_sprites_list.update() # runs the update function for all sprites in the list
    # --- Drawing code should go here
    all_sprites_list.draw(screen) # draws all the sprites onto the screen (must redraw every cycle of loop like so)
    # Updates screen
    pygame.display.flip()
 
    # Determine FPS
    clock.tick(4)