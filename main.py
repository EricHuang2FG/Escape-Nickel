import pygame, os, random

pygame.init()
WINDOW = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Escape Nickel")
FPS = 60

RED_GRAY = (46, 40, 40)
ASSETSPATH = os.path.abspath(os.getcwd()) + "/Assets/"

class Ground:
    speed = 7

    def __init__(self, x):
        self.picture = pygame.image.load(ASSETSPATH + "ground.png")
        self.x = x
        self.y = WINDOW.get_height() - self.picture.get_height()
        self.width = self.picture.get_width()
        self.height = self.picture.get_height()

    def move(self):
        self.x -= self.speed

    def draw(self):
        WINDOW.blit(self.picture, (self.x, self.y))
    
    def behave(self):
        self.move()
        self.draw()

class Obstacle:
    scale = 0.07

    def __init__(self, x):
        self.rawPicture = pygame.image.load(ASSETSPATH + "obstacle.png")
        if random.randint(1, 2) == 1:
            self.picture = pygame.transform.scale(self.rawPicture, (int(self.rawPicture.get_width() * self.scale), int(self.rawPicture.get_height() * (self.scale))))
        else:
            self.picture = pygame.transform.scale(self.rawPicture, (int(self.rawPicture.get_width() * self.scale), int(self.rawPicture.get_height() * (self.scale + 0.05))))
        self.x = x
        self.y = WINDOW.get_height() - 160 - self.picture.get_height()
        self.width = self.picture.get_width()
        self.height = self.picture.get_height()
        self.speed = Ground.speed
    
    def move(self):
        self.x -= self.speed

    def draw(self):
        WINDOW.blit(self.picture, (self.x, self.y))
    
    def behave(self):
        self.move()
        self.draw()

ground = []
obstacles = [Obstacle(WINDOW.get_width() + int(0.5 * WINDOW.get_width()))]

def generateGround():
    position = 0
    for i in range(3):
        ground.append(Ground(position))
        position += WINDOW.get_width()

def behaveGround():
    for segment in ground:
        segment.behave()
        if segment.x + segment.width < 0:
            segment.x += len(ground) * segment.width

def spawnObstacles():
    position = obstacles[-1].x
    minSpacing = int(WINDOW.get_width() / 4)
    maxSpacing = WINDOW.get_width()
    while len(obstacles) < 4:
        x = position + random.randint(minSpacing, maxSpacing)
        obstacles.append(Obstacle(x))
        position = x

def behaveObstacles():
    for obstacle in obstacles:
        obstacle.behave()
    if obstacles[0].x + obstacles[0].width < 0:
        obstacles.pop(0)

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
            behaveGround()
            spawnObstacles()
            behaveObstacles()

        if game == "fail screen":
            pass
    
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()