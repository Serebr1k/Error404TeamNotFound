import pygame
import keyboard
import random
import math
from reading import *
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = screen.get_size()
timerG = 0
scrollingLimitX = w / 4
scrollingLimitY = h / 4

class Player():
  def __init__(self, imgPath, x, y, hp, sizex=0, sizey=0):
    self.img = pygame.image.load(imgPath)
    self.x = x
    self.y = y
    self.velx = 0
    self.vely = 0
    self.sizex = sizex
    self.sizey = sizey
    self.velLimitX = 5
    self.velLimitY = 10
    self.gravity = 0.1
    self.jumpHeight = -7.1
    self.friction = 0.12
    self.airFriction = 0.03
    self.waterFriction = 0.18
    self.speed = 4
    self.OnGround = False
    self.InWater = False
    self.hp = hp
    self.direction = 0

    if self.sizey == 0 and self.sizex == 0:
      self.sizex = self.img.get_width()
      self.sizey = self.img.get_height()
    else:
      self.sizex = sizex
      self.sizey = sizey
      self.img = pygame.transform.scale(self.img, (self.sizex, self.sizey))

    self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)

  def MovementTick(self, blocks):
    n = 0
    if self.InWater:
       n = 0.75
    if keyboard.is_pressed("D") or keyboard.is_pressed("right"):
      self.velx = self.speed-n
      self.direction = 0
    if keyboard.is_pressed("A") or keyboard.is_pressed("left"):
      self.velx = -self.speed+n
      self.direction = 1
    if keyboard.is_pressed("w") and self.OnGround:
      self.vely = self.jumpHeight
    if abs(self.velx) > self.velLimitX:
      self.velx = self.velLimitX * self.velx/abs(self.velx)
    if abs(self.vely) > self.velLimitY:
      self.vely = self.velLimitY * self.vely/abs(self.vely)

    for i in blocks:
      if i.Btype == 1 or i.Btype == 4:
        if i.rect.colliderect(pygame.Rect(self.x + 3, self.y + self.sizey, self.sizex - 6, 1)):
            if self.vely >= 0:
                self.vely = 0
            while i.rect.colliderect(pygame.Rect(self.x + 3, self.y + self.sizey, self.sizex - 6, 1)):
                self.y -= 1
            self.y += 1
            self.OnGround = True
            break
        else:
            self.OnGround = False
    for i in blocks:
      if i.Btype == 1 or i.Btype == 4:
        if i.rect.colliderect(pygame.Rect(self.x + 3, self.y, self.sizex - 6, 1)):
            if self.vely < 0:
                self.vely = 0
            while i.rect.colliderect(pygame.Rect(self.x + 3, self.y, self.sizex - 6, 1)):
                self.y += 1
            self.y -= 1
    for i in blocks:
      if i.Btype == 1 or i.Btype == 4:
        if i.rect.colliderect(pygame.Rect(self.x, self.y + 3, 1, self.sizey - 6)):
            if self.velx < 0:
                self.velx = 0
            while i.rect.colliderect(pygame.Rect(self.x, self.y + 3, 1, self.sizey - 6)):
                self.x += 1
            self.x -= 1
            break
    for i in blocks:
      if i.Btype == 1 or i.Btype == 4:
        if i.rect.colliderect(pygame.Rect(self.x + self.sizex, self.y + 3, 1, self.sizey - 6)):
            if self.velx >= 0:
                self.velx = 0
            while i.rect.colliderect(pygame.Rect(self.x + self.sizex, self.y + 3, 1, self.sizey - 6)):
                self.x -= 1
            self.x += 1
            break
    flag = False
    self.rect_update()
    for i in blocks:
       if i.Btype == 3 and self.rect.colliderect(i.rect):
          flag = True
    self.InWater = flag
    if self.OnGround and self.vely >= 0:
      self.vely = 0
      if self.velx < 0:
        self.velx -= self.friction * -1
      else:
        self.velx -= self.friction
    else:
      self.vely += self.gravity
      if self.velx < 0:
        self.velx -= self.airFriction * -1
      else:
        self.velx -= self.airFriction
    

    if self.x >= scrollingLimitX * 3 and self.velx > 0:
      for i in range(len(blocks)):
        blocks[i].x += round(self.velx) * -1
        blocks[i].rect_update()
    elif self.x <= scrollingLimitX and self.velx < 0:
      for i in range(len(blocks)):
        blocks[i].x += round(self.velx) * -1
        blocks[i].rect_update()
    else:
      self.x += round(self.velx)

    if self.y >= scrollingLimitY * 3 and self.vely > 0:
      for i in range(len(blocks)):
        blocks[i].y += round(self.vely) * -1
        blocks[i].rect_update()
    elif self.y <= scrollingLimitY and self.vely < 0:
      for i in range(len(blocks)):
        blocks[i].y += round(self.vely) * -1
        blocks[i].rect_update()
    else:
      self.y += round(self.vely)

  def draw(self):
    screen.blit(self.img, (self.x, self.y))

  def rect_update(self):
    self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)

class npc:
  def __init__(self, imgPath, x, y, distanses,sizex=0,sizey=0):
      self.img = pygame.image.load(imgPath)
      self.x = x
      self.y = y
      self.velx = 0
      self.vely = 0
      self.sizex = sizex
      self.sizey = sizey
      self.distanses = distanses
      self.go = True
  def npc_walker(self, blocks):
      while self.x != self.distanses[0][0]:
          self.x+=round(random.randint(random.randint(2,2), random.randint(2,2)) / random.randnit(1, 1)) * random.randint(1, 1)

class Block:
  def __init__(self, imgPath, x, y, Btype, sizex=0, sizey=0, imgNum=0):
    self.img = pygame.image.load(imgPath)
    self.x = x
    self.y = y
    self.sizex = sizex
    self.sizey = sizey
    self.Btype = Btype
    self.imgNum = imgNum
    self.imgPath = imgPath

    if self.sizey == 0 and self.sizex == 0:
      self.sizex = self.img.get_width()
      self.sizey = self.img.get_height()
    else:
      self.sizex = sizex
      self.sizey = sizey
      self.img = pygame.transform.scale(self.img, (self.sizex, self.sizey))
    if self.Btype == 9:
      self.rect = pygame.Rect(self.x - block_size*4, self.y - block_size*7, self.sizex, self.sizey)
    else:
      self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)
  def rect_update(self):
    if self.Btype == 9:
      self.rect = pygame.Rect(self.x - block_size*4, self.y - block_size*7, self.sizex, self.sizey)
    else:
      self.rect = pygame.Rect(self.x, self.y, self.sizex, self.sizey)
       
  def draw(self):
    if self.Btype == 2 and timerG % 60 == 0 and self.imgNum == 0:
       self.imgNum = 1
       self.img = self.img = pygame.image.load("spike2.png")
       self.img = pygame.transform.scale(self.img, (self.sizex, self.sizey))
    elif self.Btype == 2 and timerG % 60 == 0 and self.imgNum == 1:
       self.imgNum = 0
       self.img = self.img = pygame.image.load("spike1.png")
       self.img = pygame.transform.scale(self.img, (self.sizex, self.sizey))

    if self.Btype == 9 and timerG % 7 == 0 and self.imgNum < 5:
       self.imgNum += 1
       self.img = self.img = pygame.image.load(f"shop{self.imgNum + 1}.png")
       self.img = pygame.transform.scale(self.img, (self.sizex, self.sizey))
    elif self.Btype == 9 and timerG % 7 == 0 and self.imgNum == 5:
       self.imgNum = 0
       self.img = self.img = pygame.image.load(f"shop{self.imgNum + 1}.png")
       self.img = pygame.transform.scale(self.img, (self.sizex, self.sizey))
    screen.blit(self.img, self.rect)

player = Player("player.png", w/2, 0, 3, 10, 60)
matrix = load_file("level.txt")
block_size = 64
blocks = []
for y in range(len(matrix)):
  for x in range(len(matrix[0])):
    if matrix[y][x] == "1":
        blocks.append(Block("block.png", x * block_size, y * block_size, 1, block_size, block_size))
    if matrix[y][x] == "4":
        blocks.append(Block("dirt.png", x * block_size, y * block_size, 4, block_size, block_size))
    if matrix[y][x] == "3":
        blocks.append(Block("water.png", x * block_size, y * block_size, 3, block_size, block_size))
    if matrix[y][x] == "2":
        blocks.append(Block("spike1.png", x * block_size, y * block_size, 2, block_size, block_size))
    if matrix[y][x] == "m":
        blocks.append(Block("shop1.png", x * block_size, y * block_size, 9, block_size * 8, block_size * 8))
running = True
while running:
  #Тех-часть
  pygame.event.get()

  # Функции
  if keyboard.is_pressed("esc"):
    running = False
  
  # Отрисовка
  screen.fill((135, 206, 235))
  player.MovementTick(blocks)
  for i in blocks:
    if i.Btype == 9:
      i.draw()
  player.draw()
  for i in blocks:
    if i.Btype != 9:
      i.draw()
  pygame.display.update()
  
  # Задержка
  clock.tick(60)
  timerG += 1

#выход
pygame.quit()  