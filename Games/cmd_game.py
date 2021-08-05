from os import system, name as OSname
from getkey import getkey, keys
from threading import Thread
from random import randint
from cursor import hide, show
from sys import stdout
from time import sleep

#--------------configs-------------#
speed = [0.20, 0.20, 0.15, 0.10, 0.08, 0.05]
lives = 3
IMG_body = "🚀"
IMG_obstacle = ["❌", "🚫", "⛔️", "🛑", "⚠️"]
IMG_life = "❤️︎︎"
IMG_explode = "☠️"
IMG_empty = " "
#----------------------------------#

hide()
y, x = -6, 2
points, spaces, level = 0, 0, 0
running = True
order = "null"
length = 45
width = 11

world = [[IMG_empty]*length for _ in range(width)]
world[y][x] = IMG_body

def clear(t = 0):
  sleep(t)
  system('cls' if OSname == 'nt' else 'clear')

def printt(string, delay = 0.005):
  for character in string:
    stdout.write(character)
    stdout.flush()
    sleep(delay)
  print()

def display():
  print("\033[H",end="")
  print((IMG_life+" ")*lives, "")
  for row in world:
    print(" ".join(map(str,row[0:-5])))

def scroll():
  global points, spaces, level
  world[y][x] = IMG_empty
  for row in world:
    if row[2] in IMG_obstacle:
      points += 1
    del row[0]
    row.append(IMG_empty)
  if points < 1:
    if spaces <= 0:
      world[y][-1] = IMG_obstacle[0]
      spaces = 7
  elif points < 8:
    if spaces <= 0:
      world[y][-1] = IMG_obstacle[1]
      world[y][-2] = IMG_obstacle[1]
      spaces = 7
    level = 1
  elif points < 80:
    if spaces <= 0:
      world[y][-1] = IMG_obstacle[2]
      world[y][-2] = IMG_obstacle[2]
      world[y][-3] = IMG_obstacle[2]
      spaces = 7
      burstPos = randint(3,9)
      world[burstPos-1][-2] = IMG_obstacle[2]
      world[burstPos][-3] = IMG_obstacle[2]
      world[burstPos+1][-2] = IMG_obstacle[2]
    level = 2
  elif points < 200:
    if spaces <= 0:
      world[y][-1] = IMG_obstacle[3]
      world[y][-2] = IMG_obstacle[3]
      world[y][-3] = IMG_obstacle[3]
      spaces = 7
      burstPos = randint(3,9)
      world[burstPos-1][-2] = IMG_obstacle[3]
      world[burstPos][-3] = IMG_obstacle[3]
      world[burstPos+1][-2] = IMG_obstacle[3]
      if y < -6:
        world[0][-1] = IMG_obstacle[3]
        world[1][-1] = IMG_obstacle[3]
      if y > -6:
        world[-1][-1] = IMG_obstacle[3]
        world[-2][-1] = IMG_obstacle[3]
    level = 3
  else:
    if spaces <= 0:
      world[y][-1] = IMG_obstacle[4]
      world[y][-2] = IMG_obstacle[4]
      world[y][-3] = IMG_obstacle[4]
      world[y][-3] = IMG_obstacle[4]
      spaces = 7
      burstPos = randint(4,8)
      world[burstPos-2][-1] = IMG_obstacle[4]
      world[burstPos-1][-2] = IMG_obstacle[4]
      world[burstPos][-3] = IMG_obstacle[4]
      world[burstPos+1][-2] = IMG_obstacle[4]
      world[burstPos+2][-1] = IMG_obstacle[4]
      if y < -6:
        world[0][-1] = IMG_obstacle[4]
        world[1][-1] = IMG_obstacle[4]
      if y > -6:
        world[-1][-1] = IMG_obstacle[4]
        world[-2][-1] = IMG_obstacle[4]
    level = 4
  spaces += -1

def death():
  global lives, running
  lives += -1
  world[y][x] = IMG_explode
  display()
  if lives <= 0:
        running = False

def update():
  global y, points, order
  if order == "up":
    order = "null"
    y -= 1
  if order == "down":
    order = "null"
    y -= -1
  if y >= 0:
    y -= 1
  try:
    if world[y][x] in IMG_obstacle:
      world[y][x] = IMG_empty
      death()
    else:
      world[y][x] = IMG_body
      display()
  except: y -= -1

def keypress(key):
  global order
  if key == keys.UP or key == "w": order = "up"
  if key == keys.DOWN or key == "s": order = "down"

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
    sleep(speed[level])

  death()
  print("You survived", points, "nukes (ㆆ_ㆆ)" if points < 100 else "nukes (っ＾▿＾)") 

printt("Use W/S or 🠕/🠗 to move", 0.05)
clear(1)

kthread = KeyboardThread(keypress)
run()

while True:
  show()
  awn = input("Want to play again? (press ENTER)\n").lower()
  hide()
  clear()
  if awn == "y" or awn == "yes" or awn == "":
    clear()
    y, x = -6, 2
    points = 0
    lives = 3
    running = True
    kthread = KeyboardThread(keypress)
    run()
  else:
    break
    show()
