import msvcrt as con
import os
import random
import time

def sqrt(x: int) -> int:
    i = 1
    while i*i <= x:
        i += 1
    return i-1


EXIT = b'\x1b'
LEFT = [b'a', b'A']
RIGHT = [b'd', b'D']
DOWN = [b's', b'S']
UP = [b'w', b'W']

TEXT = ""

SWIDTH = 28 #screen width
SHEIGHT = 10 #screen height
WORLDSIZE = 100
PLAIN =[]


FIRE_SPRITE = ["M", "w", "W"]


def createPlain() -> None:
    global PLAIN
    random.seed(time.time())
    for i in range(WORLDSIZE):
        v = []
        for j in range(WORLDSIZE):
            n = random.randint(0,1000)
            if n%12 == 2:
                v.append("O")
            if n % 40 == 3:
                v.append("M")
            else:
                v.append("^")
        PLAIN.append(v)

def expandFire() -> None:
    dx = [0,1,0,-1]
    dy = [-1,0,1,0]
    for i in range(SHEIGHT):
        for j in range(SWIDTH):
            for x in range(len(dx)):
                r = random.randint(0,20)
                if i+dy[x] >= 0 and j+dx[x] >= 0 and i+dy[x] < SHEIGHT and j+dx[x] < SWIDTH and (PLAIN[i+dy[x]][j+dx[x]] == "M" or PLAIN[i+dy[x]][j+dx[x]] == "W") and PLAIN[i][j] == "^" and r % 3 == 1:
                    PLAIN[i][j] = "7"
    for i in range(SHEIGHT):
        for j in range(SWIDTH):
            if PLAIN[i][j] == "7":
                n = random.randint(0, 100)
                if n % 2 == 0:
                    PLAIN[i][j] = "M"
                else:
                    if n % 3 == 0:
                        PLAIN[i][j] = "W"
                    else:
                        PLAIN[i][j] = "w"

def changeFire() -> None:
    for i in range(SHEIGHT):
        for j in range(SWIDTH):
            if PLAIN[i][j] in FIRE_SPRITE:
                for x in range(len(FIRE_SPRITE)):
                    if FIRE_SPRITE[x] == PLAIN[i][j]:
                        PLAIN[i][j] = FIRE_SPRITE[(x+1)%len(FIRE_SPRITE)]
                        break

def uncutGrass() -> bool:
    for i in range(SHEIGHT):
        for j in range(SWIDTH):
            if PLAIN[i][j] == "^":
                return True
    return False

def printPlain(x: int = 0, y: int = 0) -> None:
    global PLAIN
    if player.distanceWalked % 10 == 0 and player.distanceWalked != 0:
        expandFire()
    changeFire()
    for i in range(SHEIGHT):
        for j in range(SWIDTH):
            if i == y and j ==x:
                if PLAIN[i][j] == "^":
                    PLAIN[i][j] = "-"
                    player.score += 1
                if PLAIN[i][j] == "O":
                    player.hp -= 10
                    player.LASTHIT = "YOU FELL IN A HOLE"
                if PLAIN[i][j] in FIRE_SPRITE:
                    player.hp -= 20
                    player.LASTHIT = "YOU CAUGHT AFLAME"
                print("x", end="")
            else:
                print(PLAIN[i][j], end = "")
        print()

class Player:
    MAXHP = 100
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.level = 1
        self.hp = 100
        self.posx = 0
        self.posy = 0
        self.distanceWalked = 0
        self.LASTHIT = ""
        self.score = 0
    def printareHP(self):
        BARS = ""
        for x in range(self.hp//10):
            BARS += "<3"
        for x in range(self.hp//10,self.MAXHP//10):
            BARS += " X"
        return f"[{self.hp}+][{BARS}]"
    def where(self):
        #current position of player
        return [self.posx, self.posy]
    def levelup(self):
        if sqrt(self.distanceWalked)**2 == self.distanceWalked:
            self.level += 1
    def update(self, s:str):
        #move player based on key pressed
        if s in RIGHT or s in LEFT or s in DOWN or s in UP:
            self.distanceWalked += 1
        if s in RIGHT and self.posx+1>=0 and self.posx+1<SWIDTH:
            self.posx += 1
        if s in DOWN and self.posy+1>=0 and self.posy+1<SHEIGHT:
            self.posy += 1
        if s in UP and self.posy-1>=0 and self.posy-1<SHEIGHT:
            self.posy -= 1
        if s in LEFT and self.posx-1>=0 and self.posx-1<SWIDTH:
            self.posx -= 1
        if s == b't':
            global TEXT
            mess = input(f"{self.name}[{self.level}]>")
            TEXT += (self.name + f"[{self.level}]>")
            TEXT += mess+"\n"
        self.levelup()

player = Player("Alex", 12)
createPlain()
while True:
    n = con.getch()
    player.update(n)
    os.system("cls")
    print(player.distanceWalked, sqrt(player.distanceWalked)**2 == player.distanceWalked)
    print(player.printareHP())
    print(f"GRASS CUT: {player.score}")
    printPlain(player.where()[0], player.where()[1])
    print("Walking through the tall grass...")
    print(TEXT)
    if n == EXIT:
        os.system("cls")
        print(player.distanceWalked, sqrt(player.distanceWalked)**2 == player.distanceWalked)
        print(player.printareHP())
        printPlain(player.where()[0], player.where()[1])
        print(f"[GAME QUIT]")
        break
    if player.hp <= 0:
        os.system("cls")
        print(player.distanceWalked, sqrt(player.distanceWalked)**2 == player.distanceWalked)
        print(player.printareHP())
        printPlain(player.where()[0], player.where()[1])
        print(f"[{player.LASTHIT} AND DIED]")
        break
    if not uncutGrass():
        os.system("cls")
        print(player.distanceWalked, sqrt(player.distanceWalked)**2 == player.distanceWalked)
        print(player.printareHP())
        printPlain(player.where()[0], player.where()[1])
        print(f"[ALL GRASS WAS CUT]")
        break
