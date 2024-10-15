import sys
import __gui as gui

class window:
  def __init__(self,width,height,bgcolor):
    self.width = width
    self.height = height
    self.toUpdate = [False for i in range(height)]
    self.toRender = [True for i in range(height)]
    self.renderSTR = []
    self.pixmap = [[bgcolor for x in range(width)] for y in range(height)]
    self.textmap = ["  "*width for y in range(height)]
    self.textcolormap = [[False for x in range(width*2)] for y in range(height)]

    self._textcolchanges = 0
    
    #pre update
    for y in self.pixmap:
      lineSTR = ""
      oldrgb = []
      for x in y:
        rgb = x
        if rgb == oldrgb:
          lineSTR += "  "
        else:
          lineSTR += f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m  "
        oldrgb = rgb
      self.renderSTR.append(lineSTR + "\033[0m")

  def update(self):
    self._textcolchanges = 0
    for y, needUpdate in enumerate(self.toUpdate):
      oldrgb = ()
      oldTextrgb = ()
      if needUpdate:
        lineSTR = ""
        for xpos, x in enumerate(self.pixmap[y]):
          charSTR = ""
          currentTextrgb = False
          
          textrgb1 = self.textcolormap[y][xpos*2]
          char1 = self.textmap[y][xpos*2]
          if textrgb1 and textrgb1 != oldTextrgb:
            charSTR+=f"\033[38;2;{textrgb1[0]};{textrgb1[1]};{textrgb1[2]}m"
            self._textcolchanges += 1
            currentTextrgb = textrgb1
          else:
            currentTextrgb = oldTextrgb
          charSTR+=char1

          textrgb2 = self.textcolormap[y][xpos*2+1]
          char2 = self.textmap[y][xpos*2+1]
          if textrgb2 and textrgb1 != textrgb2:
            charSTR+=f"\033[38;2;{textrgb2[0]};{textrgb2[1]};{textrgb2[2]}m"
            self._textcolchanges += 1
            currentTextrgb = textrgb2
          charSTR+=char2
          
          rgb = x
          if rgb == oldrgb:
            lineSTR += charSTR
          else:
            lineSTR += f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m{charSTR}"
          oldrgb = rgb
          oldTextrgb = currentTextrgb
        self.renderSTR[y] = lineSTR
        self.toUpdate[y] = False

  def render(self):
    _temp = ""
    for y, needRender in enumerate(self.toRender):
      if needRender:
        sys.stdout.write(f"\033[{y + 1};0H" + self.renderSTR[y])
        _temp += f"\033[{y + 1};0H" + self.renderSTR[y]
        self.toRender[y] = False
    sys.stdout.write("\033[" + str(self.height + 1) + ";0H")
    _temp += "\033[" + str(self.height + 1) + ";0H"
    print("length of render command:",len(_temp),"       ")
    print("text color changes:",self._textcolchanges,"       ")

  def plot(self,x,y,color=(0,0,0)):
    self.toUpdate[y] = True
    self.toRender[y] = True
    self.pixmap[y][x] = color

  def line(self,x1,y1,x2,y2,color=(0,0,0)):
    dx = x2 - x1
    dy = y2 - y1
    isSteep = abs(dy) > abs(dx)
    if isSteep:
      x1, y1 = y1, x1
      x2, y2 = y2, x2
    if x2 < x1:
      x1, x2 = x2, x1
      y1, y2 = y2, y1
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    y = y1
    for x in range(x1, x2 + 1):
      if isSteep:
        self.plot(y,x,color)
      else:
        self.plot(x,y,color)
      error -= abs(dy)
      if error < 0:
        y += ystep
        error += dx

  def add_text(self,x,y,text,color):
    self.textcolormap[y][x]=color
    self.toUpdate[y]=True
    self.toRender[y]=True
    new = list(self.textmap[y])
    new[x:len(text)+x] = list(text)
    self.textmap[y] = "".join(new)

  def remove_text(self):
    self.textmap = ["  "*self.width for y in range(self.height)]
    self.textcolormap = [[False for x in range(self.width*2)] for y in range(self.height)]
  
  def box(self,x1,y1,x2,y2,color):
    step_x = 1 if x2>x1 else -1
    step_y = 1 if y2>y1 else -1
    for y in range(y1,y2+1,step_y):
      if y<self.height:
        self.toUpdate[y] = True
        self.toRender[y] = True
      for x in range(x1,x2+1,step_x):
        if x<self.width and y<self.height:
          self.pixmap[y][x] = color

  def render_gui(self,guipart:gui.gui | gui.list):
    def render_content(listpart:gui.list,indent_x,indent_y):
      for part in listpart.content:
        if (part.x < guipart.width and part.y < guipart.height):
          if isinstance(part,gui.text):
            self.add_text((part.x+indent_x)*2,part.y+indent_y,part.text,part.texcolor)
          elif isinstance(part,gui.button):
            self.add_text(guipart.x+part.x+indent_x,guipart.y+part.y+indent_y,part.text,part.texcolor)
     
    for part in guipart.content:
      if (part.x < guipart.width and part.y < guipart.height):
        if isinstance(part,gui.text):
          self.add_text(guipart.x+part.x,guipart.y+part.y,part.text,part.texcolor)
        elif isinstance(part,gui.button):
          self.add_text(guipart.x+part.x,guipart.y+part.y,part.text,part.texcolor)
          self.line(guipart.x+part.x,guipart.y+part.y,guipart.x+part.x+part.width,guipart.y+part.y+part.height,part.bgcolor)
        elif isinstance(part,gui.list):
          self.box(guipart.x+part.x,guipart.y+part.y,guipart.x+part.x+part.width,guipart.y+part.y+part.height,part.bgcolor)
          render_content(part,guipart.x+part.x,guipart.y+part.y)