import pygame

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("particlesjones")
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == quit:
            running = False
    
    screen.fill((30, 30, 40))
    
    pygame.display.flip()
    clock.tick(60)