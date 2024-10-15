

class gui:
  def __init__(self,x,y,z,width,height,content=[]):
    self.x = x
    self.y = y
    self.z = z
    self.width = width
    self.height = height
    self.content = content



class list:
  def __init__(self,x,y,width,height,bgcolor,sort_type):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.bgcolor = bgcolor
    self.sort_type = sort_type
    self.content = []

  def sort(self,reversed):
    if self.sort_type == "alphabet":
      self.content.sort(key= lambda text: text,reverse=reversed)
    elif self.sort_type == "preset":
      self.content.sort(key= lambda sort_val: sort_val,reverse=reversed)

class text:
  def __init__(self,x,y,text,texcolor,sort_val=0):
    self.x = x
    self.y = y
    self.text = text
    self.texcolor = texcolor
    self.sort_val = sort_val

class button:
  def __init__(self,x,y,width,height,text,bgcolor,texcolor,func,sort_val=0):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.text = text
    self.bgcolor = bgcolor
    self.texcolor = texcolor
    self.func = func
    self.sort_val = sort_val