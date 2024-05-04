import pygame, os

pygame.init()
WINDOW = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Escape Nickel")
FPS = 30

RED_GRAY = (46, 40, 40)
ASSETSPATH = os.path.abspath(os.getcwd()) + "/Assets/"

class Ground:
    def __init__(self, x):
        self.picture = pygame.image.load(ASSETSPATH + "ground.png")
        self.x = x
        self.y = WINDOW.get_height() - self.picture.get_height()
        self.width = self.picture.get_width()
        self.height = self.picture.get_height()
        self.speed = 10

    def move(self):
        self.x -= self.speed

    def draw(self):
        WINDOW.blit(self.picture, (self.x, self.y))
    
    def behave(self):
        self.move()
        self.draw()

ground = []

def generateGround():
    position = 0
    for i in range(3):
        ground.append(Ground(position))
        position += WINDOW.get_width()

def moveGround():
    for segment in ground:
        segment.behave()
        if segment.x + segment.width < 0:
            segment.x += len(ground) * segment.width

def checkRun():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def drawGameBackground():
    WINDOW.fill(RED_GRAY)

def main():
    fps = pygame.time.Clock()
    game = "game screen" # Temporary
    run = True
    generateGround()

    while run:
        fps.tick(FPS)
        run = checkRun()

        if game == "start screen":
            pass

        if game == "game screen":
            drawGameBackground()
            moveGround()

        if game == "fail screen":
            pass
    
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()