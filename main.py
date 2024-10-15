print("STILL IN DEVELOPMENT!!! REMOVE THE IMPORT EDITOR AND EXIT() IN MAIN TO SEE THE OLDER WORKING VERSION")

import editor

edit = editor.editor(40,40)
edit.load_file("test.txt")
edit.start()


exit()

import __graphics
import __getkey
import random
import time

height = 30
width = 40
window = __graphics.window(width,height,(50,50,50))

curs_pos_x = 0
curs_pos_y = 0
prevposx = 0
prevposy = 0
prevcolor = (0,0,0)


offset = 0

lines = [""]
textcolormap = [[False for x in range(width*2)] for y in range(height)]
#textcolormap = [[(0,0,0)]]

lines_rendering = 0

def load_file():
  global lines
  with open("testy.py","r") as f:
    lines = []
    for line in f.readlines():
      lines.append(line.strip("\n"))



def render_lines():
  global lines_rendering
  for ypos, line in enumerate(lines):
    if ypos in range(offset,height+offset):
      for xpos, x in enumerate(line):
        window.add_text(xpos+4,ypos-offset,x,(textcolormap[ypos-offset][xpos]))
      lines_rendering+=1
  if len(lines)-offset < height:
    window.add_text(4,len(lines)-offset,"",(255,255,255))

def render_numbers():
  for y in range(offset,len(lines)):
    if y in range(offset,height+offset):
      window.add_text(0,y-offset,str(y+1),(50,50,50))

def render_cursor():
  global prevposx
  global prevposy
  global prevcolor
  window.plot(prevposx,prevposy,prevcolor)
  prevcolor = window.pixmap[curs_pos_y][curs_pos_x//2+2]
  prevposx = curs_pos_x//2+2
  prevposy = curs_pos_y
  window.plot(curs_pos_x//2+2,curs_pos_y,(200,200,200))
  window.add_text(curs_pos_x+4,curs_pos_y,"|",(200,240,255))
  #window.add_text(curs_pos_x+4,curs_pos_y,"|",(200,240,255))


def randomcolor():
  global textcolormap
  for ypos, y in enumerate(lines):
    if ypos in range(offset,height+offset):
      for xpos in range(len(y)):
        textcolormap[ypos-offset][xpos] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
  
  
render_cursor()
render_numbers()
render_lines()
window.box(0,0,1,height,(67,67,67))

load_file()
window.update()
window.render()
print("press any key")
while True: 
  #print("")
  key = __getkey.getkey()
  print(list(key),"                   ")
  if key == "\n":
    if curs_pos_x > 0:
      first_half, second_half = lines[curs_pos_y+offset][:curs_pos_x], lines[curs_pos_y+offset][curs_pos_x:]
      lines[curs_pos_y+offset] = second_half
      lines.insert(curs_pos_y+offset,first_half)
      curs_pos_x=0
    else:
      lines.insert(curs_pos_y+offset,"")
    if curs_pos_y >= height-1:
      offset+=1
    else:
      curs_pos_y+=1
    
  elif key == "\t":
    newline = list(lines[curs_pos_y])
    newline.insert(curs_pos_x,"  ")
    lines[curs_pos_y] = "".join(newline)
    curs_pos_x+=2
    
  elif key == "\x7f":
    if lines[curs_pos_y+offset]!="":
      if curs_pos_x > 0:
        newline = list(lines[curs_pos_y+offset])
        newline.pop(curs_pos_x-1)
        lines[curs_pos_y+offset] = "".join(newline)
        curs_pos_x-=1
      elif curs_pos_y+offset > 0:
        curs_pos_x = len(lines[curs_pos_y+offset-1])
        lines[curs_pos_y+offset-1] = lines[curs_pos_y+offset-1] + lines[curs_pos_y+offset]
        lines.pop(curs_pos_y+offset)
        if curs_pos_y > height//2 or offset < 1:
          curs_pos_y-=1
        else:
            offset-=1
    else:
      if curs_pos_y + offset > 0:
        lines.pop(curs_pos_y+offset)
        if curs_pos_y > height//2 or offset < 1:
          curs_pos_y-=1
        else:
            offset-=1
        curs_pos_x=len(lines[curs_pos_y+offset])

  elif key == "\x1b[C":
    if curs_pos_x < len(lines[curs_pos_y+offset]):
      curs_pos_x+=1
    elif curs_pos_y+offset < len(lines)-1:
      if curs_pos_y < height-1:
        curs_pos_y+=1
      else:
        offset+=1
      curs_pos_x = 0

  elif key == "\x1b[D":
    if curs_pos_x > 0:
      curs_pos_x-=1
    elif curs_pos_y + offset > 0:
      if curs_pos_y > 0:
        curs_pos_y-=1
      else:
        offset-=1
      curs_pos_x = len(lines[curs_pos_y+offset])
      
  elif key == "\x1b[A":
    if curs_pos_y+offset > 0:
      if curs_pos_y > 0:
        curs_pos_y-=1
      else:
        offset-=1
      curs_pos_x = min(curs_pos_x,len(lines[curs_pos_y+offset]))
      
  elif key == "\x1b[B":
    if curs_pos_y+offset < len(lines)-1:
      if curs_pos_y >= height-1:
        offset+=1
      else:
        curs_pos_y+=1
      curs_pos_x = min(curs_pos_x,len(lines[curs_pos_y+offset]))

  elif key == "\x1b[6~":
    offset+=1
  elif key == "\x1b[5~":
    offset-=1
  
  elif len(key)==1:
    if key == "`":
      window.box(curs_pos_x//2+2,curs_pos_y,width//2,height//2,(100,100,100))
      window.update()
      window.render()
      curs_box_pos_y = curs_pos_y
      while True:
        print("")
        key = __getkey.getkey()
        if key == "\x1b[A":
          if curs_box_pos_y > curs_pos_y:
            curs_box_pos_y-=1
        if key == "\x1b[B":
          if curs_box_pos_y < height//2:
            curs_box_pos_y+=1
          
        window.box(curs_pos_x//2+2,curs_pos_y,width//2,height//2,(100,100,100))
        window.line(curs_pos_x//2+2,curs_box_pos_y,width//2,curs_box_pos_y,(150,150,150))
        window.update()
        window.render()
    else:
      newline = list(lines[curs_pos_y+offset])
      newline.insert(curs_pos_x,key)
      lines[curs_pos_y+offset] = "".join(newline)
      color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
      curs_pos_x+=1


  start = time.perf_counter()
  window.remove_text()
  end = time.perf_counter()
  print("window clear time:",end-start,"        ")

  start = time.perf_counter()
  randomcolor()
  end = time.perf_counter()
  print("color gen time:",end-start,"        ")

  start = time.perf_counter()
  render_numbers()
  end = time.perf_counter()
  print("number render time:",end-start,"        ")

  start = time.perf_counter()
  render_lines()
  end = time.perf_counter()
  print("line render time:",end-start,"        ")

  start = time.perf_counter()
  render_cursor()
  end = time.perf_counter()
  print("cursor render time:",end-start,"        ")

  start = time.perf_counter()
  window.update()
  window.render()
  end = time.perf_counter()
  print("graphics window update and render time:",end-start,"        ")
  
  print("lines:",len(lines),"       ")
  print(f"lines in render: {lines_rendering}            ")
  lines_rendering=0