# YASARA PLUGIN
# Title:    View Finder Tools
# Author:   James Ebert
#-----------------------------------
# this will be found under Effect->(last item)
# allows you to select and atom or residue and a macro file.  you can then automatically populate
# different zoom ins of your selection to be saved and used later.  During use it will color the atoms
# so you know exactly what you have selected and will then recolor them based on their Element settings.
# the first time during a session that you use the tool it will ask you for the macro file you wish to
# use.  after that the macro file will be remembered and will not need to be input until Yasara is closed.
# the highlight color can be changed under the config option, the highlighting can also be turned off under the
# config option.  Persistence of the macro file can also be turned off under settings, which will require you
# to specify a macro file every time you use the tool.
"""
MainMenu: Effects
  PullDownMenu after Text: View Finder Tools
    SubMenu: Atom Zoom
      AtomSelectionWindow: Pick select the Atom that you would like to view
      Request: AtomZoom
    SubMenu: Residue Zoom
      ResidueSelectionWindow: Please select the Residue that you would like to view
      Request: ResidueZoom
    SubMenu: Configuration
      CustomWindow: Set configuration options for this plugin
        Width: 600
        Height: 400
        CheckBox:     X=50, Y=48, Text="Highlights On",Default=Yes
        CheckBox:     x=300, Y=48, Text="Remember Macro File",Default=Yes
        NumberInput:  X=390,Y= 100,Text="Move Delay",Default=50,Min=-1,Max=200
        List:         X=100, Y=100, Text="Highlight Color"
                      Width=180, Height=180, MultipleSelections=No
                      Options = 6,  Text="Magenta"
                                    Text="Red"
                                    Text="Green"
                                    Text="Blue"
                                    Text="Cyan"
                                    Text="Grey"
        TextCen:      X= 300,Y= 320,Text="Close the window to exit without saving changes"
        Button:       X=300,Y=350, Text="OK"
      Request: Config
"""
import yasara
import random
import ntpath
from ViewFinderSupport import (saveData, points, parser)

MARKER = "# Last line to be deleted\n"
PlugName = "ViewFinder"
ATOM = "Atom"
RESIDUE = "Res"

def stopMacroFile():
  if not yasara.storage:
    yasara.storage = saveData()  # create storage object

  parser().readFile(yasara.storage)  # get user settings
  if yasara.storage.rememberMacro is False or yasara.storage.file is None:
    # TODO figure out a way around this crash, report sent to YASARA, it's in their code
    file = yasara.ShowWin("FileSelection","Select your running Macro please", "No", "*.mcr") #show file window
    yasara.storage.file = str(file[1]) # save file
    yasara.storage.file.replace("/","\\\\")

  # replace collections with clean copies
  yasara.storage.lines = ["\n" + MARKER]
  yasara.storage.repaintList= []
  yasara.storage.repaintWith=None

  # prevent the stop macro popup,
  try:
    yasara.run("RecordMacro %s,append=Yes"%yasara.storage.file) #ensure their macro is running so yasara doesn't puke
    yasara.run("StopMacro")
  except:
    print("no macro running")

def cleanFile():
  # we need to clean  up the first bach of lines that were written when the user opened our macro
  file = open(yasara.storage.file, "r")
  lines = file.readlines()
  file.close()
  start = None
  # since we can't count on knowing our plugs path we use the second line and just back up one
  target = "ShowWin FileSelection,Title=Select your running Macro please,\"No\",\"*.mcr\"\n"
  if target in lines:         # check to see if this is the first time they've started the plug
    start = lines.index(target)-1
  elif lines.count("# StopPlugin\n")>1: #rare occurrence with macro persistence getting switched on and off
    indexes=[]
    delete=[]
    print(lines)
    for i in range(len(lines)):
      if PlugName in lines[i]:  # we get a pair of runplug stopplug lines we need to delete
        delete.append(i+1)
        delete.append(i)
      elif "# StopPlugin\n" in lines[i]: # we can have multiple occurrences of this which would cause a problem
        indexes.append(i)
    indexes.pop() # remove last match, we'll need to keep him
    for i in indexes:
      lines[i]="\n" # replace duplicates with a blank
    for i in delete:
      lines[i]="\n"


  if start is None and "# StopPlugin\n" in lines: # check to see if they have run the plug more then once
    start = lines.index("# StopPlugin\n")
  elif start is None:                       # first time, and no macro was recording
    start = 0

  end = lines.index(MARKER)+1
  for x in range(start,end):
    print(lines[x])
    lines[x]="\n" # replace with a blank line

  file = open(yasara.storage.file, "w")
  for line in lines:
    if line is not "\n":
      file.write(line)
  file.close()

def zoomAtom():
  # this will bundle a standard atom zoom and recording for the macro
  yasara.ZoomAtom(yasara.storage.selection, 1, "No")
  yasara.storage.lines.append("ZoomAtom %s, steps = 1,Wait=NO\n"%yasara.storage.selection)

def zoomResidue():
  yasara.ZoomRes(yasara.storage.selection, 1, "No")
  yasara.storage.lines.append("ZoomRes %s,steps = 1,Wait=NO\n"%yasara.storage.selection)

def recordRotate():
  point = points() # generate a set of points
  yasara.AutoMoveTo(point.parts[0], point.parts[1], point.parts[2], steps=1)    # move the screen
  yasara.AutoRotateTo(point.parts[3], point.parts[4], point.parts[5], steps=1)  # rotate screen
  # store the commands
  yasara.storage.lines.append("AutoMoveTo X={0},Y={1},Z={2},Steps=1,Wait=NO\n"
                              .format(point.parts[0],point.parts[1],point.parts[2]))
  yasara.storage.lines.append("AutoRotateTo Alpha={0},Beta={1},Gamma={2},Steps=1,Wait=NO\n"
                              .format(point.parts[3],point.parts[4],point.parts[5]))

def replayAtom():
  recordRotate()  # record our rotation
  zoomAtom()      # zoom back in on atom

def replayProtein():
  recordRotate()
  zoomResidue()

def commonButtons():
  yasara.PrintHUD()  # pass output to hud
  yasara.ShowButton("Close Without Write", y=450, color="Yellow", width=200, height=40)
  yasara.ShowButton("Close", y=150, color="Red", width=100, height=40)


def closeUp():
  # edit step time one final command
  s = yasara.storage.lines[-1].replace("steps = 1,Wait=NO\n", "steps = %i\n# "%yasara.storage.delay)
  yasara.storage.lines[-1] = s

  # now we write everything back to the macro file
  with open(yasara.storage.file, "a") as file:
    file.writelines(yasara.storage.lines)
  cleanFile()

  # reshow HUD
  yasara.HUD(show="obj")

  # restart the macro recorder
  yasara.run("RecordMacro {0},append=Yes".format(yasara.storage.file))

def closeNoWrite():
  yasara.storage.lines=[yasara.storage.lines[0],"\n# "] #dump all lines except the marker and add the hanging comment
  with open(yasara.storage.file, "a") as file:
    file.writelines(yasara.storage.lines)
  cleanFile()


  yasara.HUD(show="obj")
  yasara.run("RecordMacro {0},append=Yes".format(yasara.storage.file))

def recolor():
  if yasara.storage.selection_type == ATOM:
    for atom in yasara.storage.repaintList:
      yasara.ColorAtom(atom, "Element")
  elif yasara.storage.selection_type == RESIDUE:
    for res in yasara.storage.repaintList:
      yasara.ColorRes(res, "Element")

if(yasara.request == "Config"):
  if len(yasara.selection[0].list) is 0:
    yasara.selection[0].list = [None]
  parser().writeFile(yasara.selection[0].checkbox[0], yasara.selection[0].checkbox[1],
                     yasara.selection[0].list[0], yasara.selection[0].number[0])

if(yasara.request == "AtomZoom"):

  stopMacroFile()                       # stop macro, setup storage if first run
  yasara.storage.selection_type = ATOM  # set type of selection were working on
  atomSelect = yasara.selection[0].atom # grab selected atoms
  if yasara.storage.hilights_on:
    for atom in atomSelect: # iterate through atoms
      yasara.storage.repaintList.append(atom.number.inyas)
      yasara.ColorAtom(atom.number.inyas, yasara.storage.hilight_color) # color each so we know what were looking at

  yasara.storage.selection =  atomSelect[0].number.inyas

  zoomAtom() # initial zoom
  commonButtons()
  yasara.ShowButton("Recenter Atom View", y=90, color="Red", width=200, height=40)

if(yasara.request=="ResidueZoom"):

  stopMacroFile()
  yasara.storage.selection_type=RESIDUE
  residueSelect = yasara.selection[0].residue

  if yasara.storage.hilights_on:
    for res in residueSelect:
      yasara.storage.repaintList.append(res.number.inyas)
      yasara.ColorRes(res.number.inyas, yasara.storage.hilight_color)

  yasara.storage.selection = residueSelect[0].number.inyas

  zoomResidue()
  commonButtons()
  temp=yasara.ShowButton("Recenter Protein View", y=90, color="Red", width=200, height=40)

if(yasara.request == "RecenterAtomView"):
  replayAtom() # method that will handle retrying the zoom in
if(yasara.request == "RecenterProteinView"):
  replayProtein()

if(yasara.request == "Close"):
  if yasara.storage.hilights_on:
    recolor()
  closeUp()
  if yasara.storage.rememberMacro is False:
    yasara.storage.file=None

if(yasara.request == "CloseWithoutWrite"):
  if yasara.storage.hilights_on:
    recolor()
  closeNoWrite()
  if yasara.storage.rememberMacro is False:
    yasara.storage.file = None

yasara.plugin.end()
