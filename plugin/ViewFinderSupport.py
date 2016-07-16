import random
import math
import os

class saveData:
  def __init__(self):
    self.selection=None
    self.repaintList=[]
    self.hud=None
    self.cords=None
    self.file=None
    self.lines=[]
    self.hilights_on=True
    self.hilight_color="Magenta"
    self.selection_type=None
    self.rememberMacro = None
    self.delay = None

class points:
  def __init__(self):
    self.parts=[random.randrange(25),random.randrange(25),random.randrange(25),
                random.randrange(240), random.randrange(240), random.randrange(240)]

  def diff(self, point):
    neg=random.randrange(-1,1,2)
    for i in range(6):
      if(math.fabs(self.parts[i]-points.parts[i])<50):
        point.parts[i]+=self.parts[i]*neg
        neg*=random.randrange(-1,1,2)


class parser():
  def __init__(self):
    self.config = {}
    self.file_path = os.path.dirname(os.path.realpath(__file__))+"\\vf_setup.ini"

  def writeFile(self, hilightSelection, filePersistance, color, delay):
    # if they didn't select a color get color from file
    if(color is None):
      d = saveData()
      self.readFile(d)
      color=d.hilight_color
    if delay < 1:
      delay = 1

    self.config = {'HighlightSelection': hilightSelection,
                              'HighlightColor': color,
                              'Remember Macro File': filePersistance,
                              'Move Delay': delay}

    with open(self.file_path, 'w') as file:
      for key in self.config.keys():
        file.write("%s : %s\n"%(key, self.config[key]))

  def readFile(self, data):

    with open(self.file_path, "r") as file:
        lines=file.readlines()
        for s in lines:
          try:
            key,val=s.split(":")
            self.config[key.strip()]=val.strip()
          except ValueError:
            pass

    data.hilights_on = bool(int(self.config['HighlightSelection']))
    data.hilight_color = str(self.config['HighlightColor'])
    data.rememberMacro = bool(int(self.config['Remember Macro File']))
    data.delay = int(self.config['Move Delay'])