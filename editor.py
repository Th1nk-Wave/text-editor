import __graphics as graphics
import __gui as gui
import __getkey as getkey
import threading
import time
import math
import random






class editor:
  def __init__(self,width,height) -> None:
    self.height = height
    self.width = width

    self.offset_x = 0
    self.offset_y = 0
    self.lines_length_offset = 0

    self._last_offset = 0
    self._last_lines_length = 0

    self.cursor_position_x = 0
    self.cursor_position_y = 0


    self.context_corner_x = 0
    self.context_corner_y = 0
    
    self.context_cursor_position_x = 0
    self.context_cursor_position_y = 0
    self.context_constraint_x = 0
    self.context_constraint_y = 0
    self.context_offset_x = 0
    self.context_offset_y = 0
    
    
    self.cursor_status = 0

    self.lines = ["please load a file" for y in range(height)]
    self.context_content = []
    self.textcolormap = [[False for x in range(width*2)] for y in range(height)]

    self.window = graphics.window(width,height,(50,50,50))

    self.fps_limit = 30
    self.fps_step_time = 1./self.fps_limit
    
    self.prev_time = 0
    self.curr_time = 0
    self.accum = 0
    self.count = 0
    self.delta_time = 0
    self.fps = 0

  def load_file(self, filepath):
    with open(filepath,"r") as f:
      self.lines = []
      for line in f.readlines():
        self.lines.append(line.strip("\n"))


  
  def start(self):
    self.window.remove_text()
    self.render_numbers()
    def get_key():
      while True:
        print("input thread control              ")
        key = getkey.getkey()
        self.handle_input(key)
        self.render()

    key_thread = threading.Thread(target=get_key,daemon=True)
    key_thread.start()

    total = 0
    while True:
      
      if total % 15 == 0:
        self.randomize_colors()
        self.render_lines()
        self.render_cursor()
      self.window.update()
      self.window.render()
      
      self.prev_time = self.curr_time
      self.curr_time = time.perf_counter()
      self.delta_time = self.curr_time - self.prev_time
      self.accum += self.delta_time
      self.count += 1

      if self.accum >= 1.0:
        self.accum -= 1.0
        print("utility thread control - fps:",round(1/self.delta_time))
        self.count = 0

      while time.perf_counter() < (self.curr_time + self.fps_step_time):
        total+=1
        time.sleep(self.fps_step_time)



  def render(self):
    self.window.remove_text()
    if self.cursor_status == 0:
      self.render_numbers()
      self.render_lines()
      self.render_cursor()
    self.window.update()
    self.window.render()

  def render_numbers(self):
    _lines_length = len(self.lines)
    for y in range(self.offset_y,_lines_length):
      if y in range(self.offset_y,self.height+self.offset_y):
        self.window.add_text(0,y-self.offset_y,str(y+1),(50,50,50))
        for x in range(self.lines_length_offset // 2 +1):
          self.window.plot(x,y-self.offset_y,(100,100,100))
        self.window.plot(self.lines_length_offset // 2 + 1,y-self.offset_y,(50,50,50))
        self.window.plot(self.lines_length_offset // 2 + 1,min(y-self.offset_y+1, self.height-1),(50,50,50))
      
  def render_lines(self):
    for ypos, line in enumerate(self.lines):
      if ypos in range(self.offset_y,self.height+self.offset_y):
        for xpos, x in enumerate(line):
          if xpos-self.offset_x < (self.width*2)-(self.lines_length_offset // 2 + 1)*2 and xpos-self.offset_x >= 0:
            self.window.add_text((xpos+(self.lines_length_offset // 2 + 1)*2)-self.offset_x,ypos-self.offset_y,x,(self.textcolormap[ypos-self.offset_y][xpos-self.offset_x]))
    _last_line_rel_to_screen = len(self.lines)-self.offset_y
    if _last_line_rel_to_screen < self.height:
      self.window.add_text((self.lines_length_offset // 2 + 1)*2,_last_line_rel_to_screen,"",(255,255,255))
      for x in range(math.log10(len(self.lines)).__floor__() // 2 +1):
        self.window.plot(x,_last_line_rel_to_screen,(50,50,50))

  def render_cursor(self):
    self.window.add_text(self.cursor_position_x+(self.lines_length_offset // 2 + 1)*2,self.cursor_position_y,"|",(200,240,255))

  def render_context_lines(self):
    for y, line in enumerate(self.context_content):
      self.window.add_text(self.context_corner_x*2,self.context_corner_y+y,line,(255,0,0))

  def randomize_colors(self):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    for ypos, _ in enumerate(self.textcolormap):
      for xpos, _ in enumerate(_):
        self.textcolormap[ypos][xpos] = (r,g,b)

  
  def handle_input(self,key):
    
    if key == "\x1b[A":
      self.curs_up()
    elif key == "\x1b[B":
      self.curs_down()
    elif key == "\x1b[C":
      self.curs_right()
    elif key == "\x1b[D":
      self.curs_left()

    elif key == "\n":
      self.new_line()
    elif key == "\x7f":
      self.remove_letter()
    elif key == "\t":
      self.open_context((self.cursor_position_x+4)//2,self.cursor_position_y,10,10,[])


    elif len(key) == 1:
      if key != "`":
        self.add_letter(key)

  def curs_up(self):
    if self.cursor_status == 0:
      if self.cursor_position_y > 0:
        self.cursor_position_y -= 1
      elif self.offset_y > 0:
        self.offset_y -= 1

      self.cursor_position_x = min(self.cursor_position_x,len(self.lines[self.cursor_position_y+self.offset_y]) - self.offset_x)
      if self.cursor_position_x < 0:
        if len(self.lines[self.cursor_position_y+self.offset_y]) > (self.width*2)//3:
          self.offset_x = len(self.lines[self.cursor_position_y+self.offset_y]) - (self.width*2)//3
          self.cursor_position_x = (self.width*2)//3
        else:
          self.cursor_position_x = len(self.lines[self.cursor_position_y+self.offset_y])
          self.offset_x = 0
      
    elif self.cursor_status == 1:
      if self.context_cursor_position_y > 0:
        self.context_cursor_position_y -= 1
      elif self.context_offset_y > 0:
        self.context_offset_y -= 1

  def curs_down(self):
    if self.cursor_status == 0 and ((self.cursor_position_y + self.offset_y) < len(self.lines)-1):
      if self.cursor_position_y < self.height-1:
        self.cursor_position_y += 1
      else:
        self.offset_y += 1

      self.cursor_position_x = min(self.cursor_position_x,len(self.lines[self.cursor_position_y+self.offset_y]) - self.offset_x)
      if self.cursor_position_x < 0:
        if len(self.lines[self.cursor_position_y+self.offset_y]) > (self.width*2)//3:
          self.offset_x = len(self.lines[self.cursor_position_y+self.offset_y]) - (self.width*2)//3
          self.cursor_position_x = (self.width*2)//3
        else:
          self.cursor_position_x = len(self.lines[self.cursor_position_y+self.offset_y])
          self.offset_x = 0
    
    elif self.cursor_status == 1 and ((self.context_cursor_position_y + self.context_offset_y) < len(self.context_content)-1):
      if self.context_cursor_position_y < self.context_constraint_y:
        self.context_cursor_position_y += 1
      else:
        self.context_offset_y += 1

  def curs_left(self):
    if self.cursor_status == 0:
      if self.cursor_position_x + self.offset_x > 0:
        if self.cursor_position_x > 0:
          self.cursor_position_x -= 1
        else:
          self.offset_x -= 1

      elif self.cursor_position_y + self.offset_y > 0:
        if self.cursor_position_y > 0:
          self.cursor_position_y -= 1
        else:
          self.offset_y -= 1
        self.cursor_position_x = min(self.width*2 - 5,len(self.lines[self.cursor_position_y+self.offset_y]))
        self.offset_x = len(self.lines[self.cursor_position_y+self.offset_y]) - self.cursor_position_x

    elif self.cursor_status == 1:
      if self.context_cursor_position_x + self.context_offset_x > 0:
        if self.context_cursor_position_x > 0:
          self.context_cursor_position_x -= 1
        else:
          self.context_offset_x -= 1

      elif self.context_cursor_position_y + self.context_offset_y > 0:
        if self.context_cursor_position_y > 0:
          self.context_cursor_position_y -= 1
        else:
          self.context_offset_y -= 1
        self.context_cursor_position_x = len(self.context_content[self.context_cursor_position_y+self.context_offset_y])

  def curs_right(self):
    if self.cursor_status == 0:
      if (self.cursor_position_x+self.offset_x) < len(self.lines[self.cursor_position_y+self.offset_y]):
        if self.cursor_position_x < (self.width*2)-(self.lines_length_offset // 2 + 1)*2-1:
          self.cursor_position_x += 1
        else:
          self.offset_x += 1
      
      elif (self.cursor_position_y+self.offset_y) < len(self.lines)-1:
        if self.cursor_position_y < self.height-1:
          self.cursor_position_y += 1
        else:
          self.offset_y += 1
        self.cursor_position_x = 0
        self.offset_x = 0

    elif self.cursor_status == 1:
      if self.context_cursor_position_x + self.context_offset_x < len(self.context_content[self.context_cursor_position_y+self.context_offset_y]):
        if self.context_cursor_position_x < self.context_constraint_x:
          self.context_cursor_position_x += 1
        else:
          self.context_offset_x += 1

      elif self.context_cursor_position_y+self.context_offset_y < len(self.context_content)-1:
        if self.context_cursor_position_y < self.context_constraint_y:
          self.context_cursor_position_y += 1
        else:
          self.context_offset_y += 1
        self.context_cursor_position_x = 0
        self.context_offset_x = 0

  def add_letter(self,key):
    if self.cursor_status == 0:
      newline = list(self.lines[self.cursor_position_y+self.offset_y])
      newline.insert(self.cursor_position_x + self.offset_x,key)
      self.lines[self.cursor_position_y+self.offset_y] = "".join(newline)

      if self.cursor_position_x < (self.width*2)-(self.lines_length_offset // 2 + 1)*2-1:
        self.cursor_position_x += 1
      else:
        self.offset_x += 1

  def remove_letter(self):
    if self.cursor_status == 0:
      if self.lines[self.cursor_position_y+self.offset_y] != "":
        if self.cursor_position_x + self.offset_x > 0:
          new_line = list(self.lines[self.cursor_position_y+self.offset_y])
          new_line.pop(self.cursor_position_x+self.offset_x-1)
          self.lines[self.cursor_position_y+self.offset_y] = "".join(new_line)
          if self.cursor_position_x > 0:
            self.cursor_position_x -= 1
          else:
            if self.offset_x > (self.width*2)//3:
              self.offset_x -= (self.width*2)//3
              self.cursor_position_x += (self.width*2)//3 - 1
            else:
              self.cursor_position_x = self.offset_x - 1
              self.offset_x = 0

        elif self.cursor_position_y + self.offset_y > 0:
          if len(self.lines[self.cursor_position_y+self.offset_y-1]) < ((self.width*2)//3)*2:
            self.cursor_position_x = len(self.lines[self.cursor_position_y+self.offset_y-1])
          else:
            self.offset_x = len(self.lines[self.cursor_position_y+self.offset_y-1]) - (self.width*2)//3
            self.cursor_position_x = (self.width*2)//3

          self.lines[self.cursor_position_y+self.offset_y-1] = self.lines[self.cursor_position_y+self.offset_y-1] + self.lines[self.cursor_position_y+self.offset_y]
          self.lines.pop(self.cursor_position_y+self.offset_y)
          self.cursor_position_y-=1
          #TEST HERE
          self.lines_length_offset = math.log10(len(self.lines)).__floor__()
      elif self.cursor_position_y + self.offset_y > 0:
        self.lines.pop(self.cursor_position_y+self.offset_y)
        self.cursor_position_y-=1
        #TEST HERE
        self.lines_length_offset = math.log10(len(self.lines)).__floor__()
        if len(self.lines[self.cursor_position_y+self.offset_y]) < ((self.width*2)//3)*2:
          self.cursor_position_x = len(self.lines[self.cursor_position_y+self.offset_y])
        else:
          self.offset_x = len(self.lines[self.cursor_position_y+self.offset_y]) - (self.width*2)//3
          self.cursor_position_x = (self.width*2)//3

      if self.cursor_position_y < 0:
        if len(self.lines) > self.height//3:
          self.cursor_position_y = self.height//3 - 1
          self.offset_y -= self.height//3
        else:
          self.cursor_position_y = self.offset_y - 1
          self.offset_y = 0
            
  def new_line(self):
    if self.cursor_position_x > 0:
      first_half, second_half = self.lines[self.cursor_position_y+self.offset_y][:self.cursor_position_x+self.offset_x], self.lines[self.cursor_position_y+self.offset_y][self.cursor_position_x+self.offset_x:]
      self.lines[self.cursor_position_y+self.offset_y] = second_half
      self.lines.insert(self.cursor_position_y+self.offset_y,first_half)
      self.cursor_position_x = 0
      self.offset_x = 0
    else:
      self.lines.insert(self.cursor_position_y+self.offset_y,"")
    if self.cursor_position_y >= self.height-1:
      self.offset_y += 1
      #TEST HERE
      self.lines_length_offset = math.log10(len(self.lines)).__floor__()
    else:
      self.cursor_position_y += 1
      #TEST HERE
      self.lines_length_offset = math.log10(len(self.lines)).__floor__()



  def open_context(self,x,y,x_constraint,y_constraint,content):
    self.cursor_status = 1
    self.context_constraint_x = x_constraint
    self.context_constraint_y = y_constraint
    self.context_content = content
    
    x_dist_from_edge = x - self.width//2
    y_dist_from_edge = y - self.height//2


    if y_dist_from_edge*2 <= y_constraint:
      corner_y = y + y_constraint - 1
    else:
      corner_y = y - y_constraint - 1

    if x_dist_from_edge*2 <= x_constraint:
      corner_x = x + x_constraint - 1
    else:
      corner_x = x - x_constraint - 1

    self.context_corner_x = min(corner_x,x)
    self.context_corner_y = min(corner_y,y)


    top_corner_x = min(x,corner_x)
    top_corner_y = min(y,corner_y)
    bottem_corner_x = max(x,corner_x)
    bottem_corner_y = max(y,corner_y)
    
    #self.window.box(x,y,corner_x,corner_y,(70,70,70))

    
    text1 = gui.text(0,0,"text number 1",(255,0,0))
    text2 = gui.text(0,1,"text number 2",(0,0,255))
    listOBJ = gui.list(0,0,bottem_corner_x-top_corner_x,bottem_corner_y-top_corner_y,(70,70,70),"preset")
    listOBJ.content.append(text1)
    listOBJ.content.append(text2)

    guipart = gui.gui(top_corner_x,top_corner_y,0,bottem_corner_x-top_corner_x,bottem_corner_y-top_corner_y)
    guipart.content.append(listOBJ)

    self.window.render_gui(guipart)
    self.window.update()
    self.window.render()





