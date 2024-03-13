import pygame
from pygame import mixer
pygame.init()
screen_size = pygame.display.Info()
width = screen_size.current_w
height = screen_size.current_h
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("UnderArad")
font = pygame.font.Font('freesansbold.ttf', 32)

try:
    icon = pygame.image.load("images/icon.jpg")
except:
    raise FileNotFoundError("File: \"icon.jpg\" not found!")
else:
    pygame.display.set_icon(icon)



wallpaper = pygame.display.set_mode((width, height))
try:
    picture = pygame.image.load("images/background.jpeg")
except:
    raise FileNotFoundError("File: \"background.jpeg\" not found!")
else:
    picture = pygame.transform.scale(picture, (width, height))
    rect = picture.get_rect()
    rect = rect.move((0, 0))

try:
    player_image = pygame.image.load("images/arad_face_default.png")
except:
    raise FileNotFoundError("File: \"arad_face_default.png\" not found!")


class Player:
    def __init__(self, inName):
        self.health = 100
        self.name = inName
        self.x = 100
        self.y = 100
        self.horizontal_movement = 0 # total movement (left + right)
        self.vertical_movement = 0 #    //      //    (up + down)
        self.left = 0
        self.right = 0
        self.down = 0
        self.up = 0
    def display(self, image, went_left):
        """
            attrs:
                image : player's image
                went_left : whether the last movement was towards left or not
        """
        self.horizontal_movement = self.left + self.right
        self.vertical_movement = self.up + self.down
        self.x += self.horizontal_movement
        self.y += self.vertical_movement
        if self.horizontal_movement > 0:
            pass
        elif self.horizontal_movement < 0 or went_left: 
            # if the player is going towards the left side or it's last movement was towards the left side
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, (self.x, self.y))


class Button:
    def __init__(self, location, image_file_location, hover_image_file_location):
        """
            attrs: 
                location : a tuple containing the X and Y components of the button
                image_file_location : default button's image
                hover_image_file_location : hovered button's image
        """
        self.file_loc = image_file_location
        self.hover_image = pygame.image.load(hover_image_file_location)
        self.button_image = pygame.image.load(image_file_location)
        self.location = (location[0] - self.button_image.get_width() / 2, location[1] - self.button_image.get_height() / 2)
        # the center of the button is placed at the given location, not the top left corner of it.
        
    def blit_button(self):
        """
            blits the image on the screen, capable of changing while hovered
        """
        mouse_position = pygame.mouse.get_pos()
        image = self.button_image
        if mouse_position[0] >= self.location[0] and \
                mouse_position[0] <= self.location[0] + self.button_image.get_width() and \
                mouse_position[1] >= self.location[1] and \
                mouse_position[1] <= self.location[1] + self.button_image.get_height():
            image = self.hover_image # if it was hovered
        screen.blit(image, (self.location[0], self.location[1], image.get_width(), image.get_height()))
    

    def clicked(self):
        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] >= self.location[0] and \
                mouse_position[0] <= self.location[0] + self.button_image.get_width() and \
                mouse_position[1] >= self.location[1] and \
                mouse_position[1] <= self.location[1] + self.button_image.get_height():
            return True # if it was clicked
        else:
            return False

        


def main_menu():
    pygame.display.set_caption("Menu")
    at_menu = True
    start_button = Button((width/2, height/2), "images/start_button.png", "images/start_button_hover.png")
    while at_menu:
        screen.fill("black")
        start_button.blit_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                at_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    at_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.clicked():
                    at_menu = False
        pygame.display.update()

main_menu()


def gameplay():
    running = True
    player_name = "Arad"
    player = Player(player_name)
    was_moving_left = False
    while running:
        screen.fill((194, 8, 6)) # default color
        wallpaper.blit(picture, rect)
        player.display(player_image, was_moving_left)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_a:
                    player.left = -2
                    was_moving_left = True
                if event.key == pygame.K_d:
                    player.right = 2
                    was_moving_left = False
                if event.key == pygame.K_w:
                    player.up = -2
                if event.key == pygame.K_s:
                    player.down = 2

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.left = 0
                if event.key == pygame.K_d:
                    player.right = 0
                if event.key == pygame.K_s:
                    player.down = 0
                if event.key == pygame.K_w:
                    player.up = 0
        pygame.display.update()

gameplay()