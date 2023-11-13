import sys
import map3
import map5
import Button
import pygame

height = 800
width = 800

# initialize the GUI game
screen = pygame.display.set_mode((width, height))
img = pygame.image.load('./some_images/download.jpg')
pygame.display.set_caption('DRAGON-FANG')
pygame.display.set_icon(img)
font = pygame.font.Font('freesansbold.ttf', 40)
theme = (0, 0, 0)
text = (255, 255, 255)

three_img = pygame.image.load('firstbutton.jpg').convert_alpha()
five_img = pygame.image.load('secondbutton.jpg').convert_alpha()

# create button variable
first_button = Button.Button(50, 200, three_img, 0.8)
second_button = Button.Button(450, 200, five_img, 0.8)


if __name__ == "__main__":
    run = True
    while run:
        screen.fill((0, 0, 0))
        msg = font.render('Choose a map to play', True, text, theme)
        msgRect = msg.get_rect()
        msgRect.center = (400, 600)
        screen.blit(msg, msgRect)

        if first_button.draw(screen):
            map3.Main()
        if second_button.draw(screen):
            map5.Main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    sys.exit()
