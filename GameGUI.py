import pygame
import tkinter
import main

pygame.init()

# Set basic colors
color_black = 0, 0, 255
# Set screen dimensions
size = width, height = 640, 480
# Create screen
screen = pygame.display.set_mode(size)
done = False
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))   


while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

    pygame.draw.rect(screen, color_black, (50,80,50,50), 5)
    pygame.draw.rect(screen, color_black, (540,80,50,50), 5)
    pygame.draw.rect(screen, color_black, (240,50,150,50), 5)

    button("GO!",150,450,100,50,color_black,color_black,)
    
    
    pygame.display.flip()
