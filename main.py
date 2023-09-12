import pygame
import os
import random
pygame.init()

#Global Constants
# SCREEN 설정
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 이미지 상수 값으로 지정
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")),]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

class Dinosaur():
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340 # dino가 덕킹했을 때 y 값이 더 작아지므로 피격 범위 재설정을 위함
    JUMP_VEL = 8.5 # dino가 점프했을 때 피격 범위 재설정을 위함

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        # dino의 초기 자세 지정
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0 # 스텝에 따른 애니메이션 효과를 위함
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0] # 처음 dino이미지를 RUNNING 리스트의 첫 번째 이미지로 설정
        self.dino_rect = self.image.get_rect() # 충돌 여부 확인을 위한 rect 생성(피격 범위)
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        
        if self.step_index >= 10:
            self.step_index = 0

        # 키보드의 입력과 공룡의 현상태에 따른 동작 제어 코드
        if userInput[pygame.K_UP] and not self.dino_jump: # 점프 중이 아니고 UP키를 눌렀을 때 => 점프   * 2단 점프를 방지하기 위해 and not self.dino_jump 추가
            self.dino_duck = False
            self.dino_jump = True
            self.dino_run = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump: # 점프 중이 아니고 DOWN키를 눌렀을 때 => 덕킹
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]): # 점프 중도 아니고 DoWN키도 누르지 않았을 때 => 달리기
            self.dino_duck = False
            self.dino_jump = False
            self.dino_run = True

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5] # 0 0 0 0 0 / 1 1 1 1 1 <반복> 즉 인덱스 값을 0과 1로 반복 시킴
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1 # 0부터 9까지 반복, 10이 되는 순간 초기화 (위 if문에서 확인 가능)
        
    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4 # 8.5 * 4 만큼을 초기 dino rect y값에서 빼줌
            self.jump_vel -= 0.8 # self.jump_vel을 0.8씩 줄이면 점프 높이가 낮아져 땅에 착지 하게 됨
        if self.jump_vel < - self.JUMP_VEL: # self.jump_vel의 값이 - 8.5 (원점으로 돌아오는 값)보다 작아지면 점프 중지 시킴
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL # 다음 점프를 위해 초기화

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud():
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000) # 왼쪽 screen 밖에서 구름이 생성되어 오른쪽으로 이동
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x = game_speed
        if self.x < - self.width: # SCREEN에 더이상 구름이 없을 때
            self.x = SCREEN_WIDTH + random.randint(2600, 3000)
            self.y = random.randint(50, 100)
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image,(self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop() # 리스트의 다음 요소를 반환하고 원래 요소 제거

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300 # SmallCactus보다 길이가 높기 때문에 rect.y값이 더 작음

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect) # bird의 날개 짓 애니메이션 제어 
        self.index += 1


def main(): 
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles # 전역 변수 설정
    run = True
    clock = pygame.time.Clock()
    cloud = Cloud()
    player = Dinosaur()
    game_speed = 14
    points = 0
    x_pos_bg = 0
    y_pos_bg = 380
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0: # 100 단위 당 game_speed를 1씩 올림
            game_speed += 1
        
        text = font.render("points: " + str(points), True, (0,0,0))
        textRect = text.get_rect() # text의 rect 위치 가져오기
        textRect.center = (1000,40) # 점수판 위치 설정
        SCREEN.blit(text, textRect) 

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= - image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run: # run = True 일 때 무한 반복, 
        for event in pygame.event.get(): # 게임 종료 버튼 or Ctrl + C 입력되면 run = False 즉, 무한 반복 종료
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed() # 사용자가 누른 키 저장

        player.draw(SCREEN)
        player.update(userInput) # 사용자가 키를 누를 때마다 Dinosaur update에 반영

    # 장애물 표시 리스트
        if len(obstacles) == 0: # 리스트를 클래스에 넣는 과정
            if random.randint(0,2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS)) 
            elif random.randint(0,2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0,2) == 2:
                obstacles.append(Bird(BIRD))

        for Obstacle in obstacles: # 리스트 요소를 반복
            Obstacle.draw(SCREEN)
            Obstacle.update()
            if player.dino_rect.colliderect(Obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30) # 1초당 30번 화면에 업뎃 (주사율 설정)
        pygame.display.update()

def menu(death_count): # 게임 오버시 뜨는 메뉴 화면 구현
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255)) 
        font = pygame.font.Font("freesansbold.ttf", 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0,0,0))
        elif death_count > 0:
            text = font.render("Press any Key to Start", True, (0,0,0))
            score = font.render("Your Score : " + str(points), True, (0,0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50) # score 크기, 위치 설정
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH//2-20, SCREEN_HEIGHT//2 - 140)) # 시작 시 공룡 이미지
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 종료 버튼 누를 시 프로그램 종료
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)