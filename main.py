import pygame, os, random, math

pygame.init()
WINDOW = pygame.display.set_mode((900, 500))
pygame.display.set_caption("Escape Nickel")
FPS = 60

RED_GRAY = (112, 92, 89)
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

class Bullet:
    vx = 4
    scale = 0.04

    def __init__(self, x, y):
        self.rawPicture = pygame.image.load(ASSETSPATH + "bullet.png")
        self.scaledPicture = pygame.transform.scale(self.rawPicture, (int(self.rawPicture.get_width() * self.scale), int(self.rawPicture.get_height() * self.scale)))
        self.x = x
        self.y = y
        self.width = self.scaledPicture.get_width()
        self.height = self.scaledPicture.get_height()
        self.vy = random.randint(-2, 2)
        self.picture = pygame.transform.rotate(self.scaledPicture, -(math.atan(self.vy / self.vx) * 180) / math.pi)

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        WINDOW.blit(self.picture, (self.x, self.y))
    
    def behave(self):
        self.move()
        self.draw()

class Car:
    scale = 0.17

    def __init__(self):
        self.pictures = []
        self.bullets = []
        for i in range(1, 7):
            rawPicture = pygame.image.load(ASSETSPATH + "car00" + str(i) + ".png")
            picture = pygame.transform.scale(rawPicture, (int(rawPicture.get_width() * self.scale), int(rawPicture.get_height() * self.scale)))
            self.pictures.append(picture)
        self.width = self.pictures[0].get_width()
        self.height = self.pictures[0].get_height()
        self.x = 15
        self.y = WINDOW.get_height() - 160 - self.height
        self.lastUpdateTime = 0
        self.pictureUpdatePeriod = 70 # Unit: ms
        self.frame = 0
        self.lastFiringTime = 0
        self.reloadTime = 3000 # Unit: ms
    
    def getBullets(self):
        return self.bullets

    def fire(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastFiringTime >= self.reloadTime:
            numBullets = random.randint(1, 3)
            for i in range(numBullets):
                self.bullets.append(Bullet(self.x + 155, self.y + 50))
            self.lastFiringTime = currentTime
    
    def draw(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastUpdateTime >= self.pictureUpdatePeriod:
            if self.frame == 5:
                self.frame = 0
            else:
                self.frame += 1
            self.lastUpdateTime = currentTime
        WINDOW.blit(self.pictures[self.frame], (self.x, self.y))
    
    def behave(self):
        self.fire()
        self.draw()
        for bullet in self.bullets:
            bullet.behave()
        self.bullets = [i for i in self.bullets if not i.x > WINDOW.get_width()]

class Character:
    scale = 0.2

    def __init__(self, name):
        self.pictures = []
        self.name = name
        try:
            if self.name == "Elwood":
                fileNameStart = "elwood00"
                self.x = WINDOW.get_width() - (WINDOW.get_width() // 4)
            elif self.name == "Turner":
                fileNameStart = "turner00"
                self.x = WINDOW.get_width() - (WINDOW.get_width() // 4) - 40
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print("ERROR: File name doesn't exist")
        for i in range(1, 7):
            rawPicture = pygame.image.load(ASSETSPATH + fileNameStart + str(i) + ".png")
            picture = pygame.transform.scale(rawPicture, (int(rawPicture.get_width() * self.scale), int(rawPicture.get_height() * self.scale)))
            self.pictures.append(picture)
        self.width = self.pictures[0].get_width()
        self.height = self.pictures[0].get_height()
        self.y = WINDOW.get_height() - 160 - self.height
        self.groundHeight = self.y
        self.vx = 3
        self.vy = 11
        self.ay = 0.5
        self.canJump = True
        self.lastUpdateTime = 0
        self.pictureUpdatePeriod = 70 # Unit: ms
        self.frame = 0
    
    def jump(self):
        if not self.canJump:
            self.y -= self.vy
            self.vy -= self.ay
            if self.y >= self.groundHeight:
                self.y = self.groundHeight
                self.canJump = True
                self.vy = 11
    
    def move(self, keys, obstacles):
        if self.name == "Elwood":
            if keys[pygame.K_RIGHT]: 
                if self.x + self.width < WINDOW.get_width() and not self.collideWithObstacles(obstacles):
                    self.x += self.vx
            if keys[pygame.K_LEFT]: 
                self.x -= self.vx
            if keys[pygame.K_UP] and self.canJump:
                self.canJump = False
        else:
            if keys[pygame.K_d]:
                if self.x + self.width < WINDOW.get_width() and not self.collideWithObstacles(obstacles):
                    self.x += self.vx
            if keys[pygame.K_a]:
                self.x -= self.vx
            if keys[pygame.K_w] and self.canJump:
                self.canJump = False
        self.jump()
    
    def collidesWith(self, object):
        if self.x <= object.x:
            left = self
            right = object
        else:
            left = object
            right = self
        return ((left.x + left.width > right.x and left.x + left.width < right.x + right.width) and ((left.y > right.y and left.y < right.y + right.height) or (left.y + left.height > right.y and left.y + left.height < right.y + right.height))) or ((left.x < right.x and left.x + left.width > right.x + right.width) and ((left.y > right.y and left.y < right.y + right.height) or (left.y + left.height > right.y and left.y + left.height < right.y + right.height))) or (left.x + left.width > right.x + right.width and left.y < right.y and left.y + left.height > right.y + right.height)

    def collideWithObstacles(self, obstacles):
        hasCollision = False
        for obstacle in obstacles:
            if self.collidesWith(obstacle):
                self.x -= Ground.speed
                hasCollision = True
        return hasCollision

    def draw(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastUpdateTime >= self.pictureUpdatePeriod:
            if self.frame == 5:
                self.frame = 0
            else:
                self.frame += 1
            self.lastUpdateTime = currentTime
        WINDOW.blit(self.pictures[self.frame], (self.x, self.y))

    def behave(self, keys, obstacles):
        self.move(keys, obstacles)
        self.collideWithObstacles(obstacles)
        self.draw()

ground = []
obstacles = [Obstacle(WINDOW.get_width() + int(0.5 * WINDOW.get_width()))]
elwood = Character("Elwood")
turner = Character("Turner")
car = Car()

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
    maxSpacing = WINDOW.get_width() + (WINDOW.get_width() // 3)
    while len(obstacles) < 4:
        x = position + random.randint(minSpacing, maxSpacing)
        obstacles.append(Obstacle(x))
        position = x

def behaveObstacles():
    for obstacle in obstacles:
        obstacle.behave()
    if obstacles[0].x + obstacles[0].width < 0:
        obstacles.pop(0)

def behaveCharacters(keys, obstacles):
    elwood.behave(keys, obstacles)
    turner.behave(keys, obstacles)

def playerIsKilled():
    if elwood.collidesWith(car) or turner.collidesWith(car):
        return True
    for bullet in car.getBullets():
        if elwood.collidesWith(bullet) or turner.collidesWith(bullet):
            return True
    return False

def returnToStartScreen(keys):
    return keys[pygame.K_ESCAPE]

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
    deathScreenText = pygame.image.load(ASSETSPATH + "you_died.png")
    generateGround()

    while run:
        keys = pygame.key.get_pressed()
        fps.tick(FPS)
        run = checkRun()

        if game == "start screen":
            pass

        if game == "game screen":
            drawGameBackground()
            behaveGround()
            spawnObstacles()
            behaveCharacters(keys, obstacles)
            behaveObstacles()
            car.behave()
            if playerIsKilled():
                deathScreenStartTime = pygame.time.get_ticks()
                game = "death screen"
            if returnToStartScreen(keys):
                game = "start screen"
        
        if game == "death screen":
            currentTime = pygame.time.get_ticks()
            if currentTime - deathScreenStartTime > 4000:
                game = "fail screen"
            WINDOW.blit(deathScreenText, ((WINDOW.get_width() // 2) - (deathScreenText.get_width() // 2), (WINDOW.get_height() // 2) - (deathScreenText.get_height() // 2)))

        if game == "fail screen":
            pass
    
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()