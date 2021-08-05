from os import system, name as OSname
from getkey import getkey, keys
from threading import Thread
from random import randint
from cursor import hide, show
from sys import stdout
from time import sleep

#--------------configs-------------#
speed = 0.3
IMG_body = "🥺"
IMG_obstacle = "🆒"
IMG_empty = " "
#----------------------------------#

hide()
y, x = -6, 2
spaces, points = 0, 0
running = True
order = "null"
length = 20
width = 11

world = [[IMG_empty]*length for _ in range(width)]
world[-1] = [IMG_obstacle]*length
world[y][x] = IMG_body

def clear(t = 0):
  sleep(t)
  system('cls' if OSname == 'nt' else 'clear')

def printt(string, delay = 0.005):
  for character in string:
    stdout.write(character)
    stdout.flush()
    sleep(delay)
  print("")

def display():
  print("\033[H",end="")
  print(points)
  for row in world:
    print(" ".join(map(str,row)))

def scroll():
  global spaces
  world[y][x] = IMG_empty
  if spaces == 0:
    pos = 0
    top = randint(0,4)
    if top == 0:
      bottom = randint(3,6)
    else:
      bottom = randint(5,7)
    for row in world:
      del row[0]
      if pos < top:
        row.append(IMG_obstacle)
      elif pos > bottom:
        row.append(IMG_obstacle)
      else:
        row.append(IMG_empty)
      pos += 1
    spaces = randint(3,8)
  else:
    for row in world:
      del row[0]
      row.append(IMG_empty)
    spaces += -1
  world[-1][-1] = IMG_obstacle
  
def death():
  global IMG_body, y, x
  IMG_body = "😵"
  x += -1
  while y < -2:
    world[y][x] = IMG_empty
    y += 1
    world[y][x] = IMG_body
    display()
    sleep(speed)
  y = -2
  world[y][x] = IMG_body
  display()

def update():
  global y, points, running, order
  if order == "flap":
    order = "null"
    y -= 3
  else:
    y -= -1
  try:
    if world[y][x] == IMG_obstacle:
      running = False
    else:
      world[y][x] = IMG_body
      if world[-2][2] == IMG_obstacle:
        points += 1
      display()
  except: y -= -3

def keypress(key):
  global order
  if key == keys.UP or key == " ": order = "flap"

class KeyboardThread(Thread):
    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while running:
            self.input_cbk(getkey())

def run():
  while running:
    scroll()
    update()
    sleep(speed)

  death()
  print("You died with", points, "points :(" if points < 1 else "points :)") 

printt("Use [ space ] or 🠕 to move", 0.05)
clear(1)

kthread = KeyboardThread(keypress)
run()

while True:
  show()
  awn = input("Want to play again?\n").lower()
  hide()
  clear()
  if awn == "y" or awn == "yes" or awn == "":
    clear()
    y, x = -6, 2
    points = 0
    IMG_body = "🟨"
    running = True
    kthread = KeyboardThread(keypress)
    run()
  else:
    break
