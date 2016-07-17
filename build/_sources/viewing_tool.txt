View Finder Break Down
***********************

This section looks at the methods in the View Finder tool.  It's broken down first by the sectinos of the main if statment (labeld by the Yasara request used, listed in the order they apear in the code), then supporting methods within ViewFinder.py (arranged alphabeticly) and ending with the supporting classes found in ViewFinderSupport.py


======
Config
======

The plugin jumps here after the user clicks "ok" on the custom config menu

.. highlight:: python
   :linenothreshold: 5

we use 

::

	Yasara.selection[0].list
	

to access the options the user picked

::

	if len(yasara.selection[0].list) is 0:
		yasara.selection[0].list = [None]
	

This check is done to ensure that we have an entry for the the color selection.  Yasara sets this to an empty array if the user didn't select a color from this list.  This would raise an access exception in the next line.

we call the parser object and write the user selections to the vf_setup.ini

========
AtomZoom
========

This is where the plugin goes after the Atom Zoom option has been selected and 1 or more atoms have been picked from the Atom selection window.

the first thing we do is call the stopMacroFile method to ensure that their macro has been stoped.  when we return we are also gerunteed to have a saveData object in memory at yasara.storage.

we then set the selection_type in memory to ATOM so that when we go to undo the recoloring we'll be able to call the appropriate method.  We use a constant flag rather then attaching the required method directly because Yasara does not like methods attached to variables.

We check storage to make sure that the user has the hilighting option selected in the .ini file and then zip through the list of selected atoms changing their color.  we also store the atom identfier in the save data so we can reset them to the proper default color when the user is finished wtih this selection.  

::
	
	yasara.storage.selection_type = ATOM  
	atomSelect = yasara.selection[0].atom 
	if yasara.storage.hilights_on:
		for atom in atomSelect:
			yasara.storage.repaintList.append(atom.number.inyas)
			yasara.ColorAtom(atom.number.inyas, yasara.storage.hilight_color)
	

After the coloring we save the first atom in the selection (because this is the atom we will actually zoom in on.  If we zoom more then one atom Yasara will only pan with no rotation.  This severly limits the views we get.  If the entire selection is not in view after a zoom it is better for the user to save the move and then zoom out).  we then zoom in on the target atom.  the last two lines display the buttons in the hud for the user.


============
Residue Zoom
============

The structure of this method works in the same way as Atom Zoom.  Due to the structure of yasara plugins it was decided that it was better to duplicate a large portion of the code rather then to write very convoluted code that would make common features of atom and residue zoom reusable.

================
RecenterAtomView
================

This is the request sent by the Recenter Atom View button created at the end of the Atom View if statment.  in Yasara buttons created for the hud use the name of the button with spaces trimed as teh request.  This statment just recalls the replay atom method.

=====================
Recenter Residue View
=====================

Works exactly the same as Recenter Atom View.


=====
Close
=====

This is tied to the Close button that apears in the hud.  we check to see if we hilighted any atoms or residues and if so we call a method to recolor them.  Since recoloring is done based on the default element color we need to check if we are hilighting as the user may have turned off highlighting due to custom colors scheme that we don't have acess to and so we can't recolor correctly.

we then call the close up method which will make sure to clean up the macro file and then restart the macro recorder.   the last thing we do is check if they are specifying the mecro file every run, if so we clear the macro path from the persistant memory.

::
	
	if yasara.storage.hilights_on:
		recolor()
	closeUp()
	if yasara.storage.rememberMacro is False:
		yasara.storage.file=None
	

The decision was made to use a flag (yasara.storage.selection_type) to support recoloring because we would have needed two close buttons otherwise since yasara defaults the request target (yasara.request) that the hud buttons send.


===================
Close Without Write
===================

This method makes sure that we clean all of our writes from the macro file and don't write the zoom information to the file.  Again the first thing we do is check for recoloring, then we call the CloseNoWrite method which takes care of clean up for us, then check the macro flag to see if we wipe the file path.

=========
cleanFile
=========

This method is responsable for making sure that the macro file is in working order when the plugin is finished. 

First we read the whole file into an array so we can cut out lines we don't need.

The biggest portion of this method is concernd with first getting the indexs for where the trash is located in our lines array and then we cut it out before re writing the file.

::
	
	target = "ShowWin FileSelection,Title=Select your running Macro please,\"No\",\"*.mcr\"\n"
	if target in lines:
		start = lines.index(target)-1
	elif lines.count("# StopPlugin\n")>1:
		indexes=[]
		delete=[]
		for i in range(len(lines)):
			if PlugName in lines[i]:
			delete.append(i+1)
			delete.append(i)
			elif "# StopPlugin\n" in lines[i]: 
				indexes.append(i)
		indexes.pop() # remove last match, we'll need to keep him
		for i in indexes:
			lines[i]="\n" # replace duplicates with a blank
		for i in delete:
		lines[i]="\n"
		
	if start is None and "# StopPlugin\n" in lines: 
		start = lines.index("# StopPlugin\n")
	elif start is None:    
		start = 0
	

First we setup a target line incase they had the macro running and this is the first time they are running the plugin since starting Yasara.  If thats the case then our initial load and macro file selection will have been printed to the macro file before we could stop it.  We don't know where the user will have installed our plugin, so it's safer to use the second line to look for this possibility since it's not dependent on the install.

At line 4 we look to see if we have multiple stop plugin lines.  This happens if they have macro persistance turned off.  This isn't a big deal in itself but we do end up with the possiblity of a line to start our plugin and to stop our plugin that have not been commented out.  this will acuse the macro to stop when run so we want to make sure to clean that up.  we set up an array of indexes that will hold the location of all the "# StopPlugin \n" lines and a second one to hold the location of hte uncomented start and stop lines.  we then look through the array and make a not of these occurances.
At line 13 we remove the last instance of a commented out stopPlugin line.  this is because it is normaly used as our marker for where to start cleaning up from, we allways need at least one of these lines in the macro file.
Next all of the unneeded lines are replaced wtih a blank line.
At line 19 we check to see if we have found a start index above (if either of our corner cases were true) if not then we start at the stopPlugin line because that is the last thing in the file since the last time we ran.  Otherwise we start at the begining of the file since this is a new file, they didn't have the plugin running when we started.

We set the end index by looking for our marker string ("# Last line to be deleted\n") which was the first thing in our list of lines to write (added to lines in stopMacroFile), this allows us to find where the good information starts.

we then go through the lines and replace anything between our two markers with blank lines, then we write the file back and skip any blank lines, effectivly deleting the unnecesary lines.

============
closeNoWrite
============

This method dumps all of our recorded changes so that the results of hte macro file are not changed by our plugin (there will be some unavoidable changes to the file itself but it will run the same before and after our plugin).  we then clean up the file, repaint the hud, and restart the macro.

=======
closeUp
=======

This method edits the last line so that we get the proper effect.  we change the step time from 1 to whatever the user specified in the .ini file (or through the config menu) and we delete the Wait = No (because it defaults as yes).  Finally we append a '#' after the line break, this way the final "StopPlugin" gets commented out.  We have to do this because that line is written to the macro file after our plugin closes, we have no way to delete it.  we then let cleanFile clean up the macro file for us, reset the yasara hud to remove our buttons, and then start the macro recording again.

=============
commonButtons
=============

creates the buttons common to both the protine and atom tools.  we call print hud so that our buttons are displayed in the hud on the right side.  Then we create a close and a close without writ button, their targets are defined by their name (unforturnetly this is enforced by Yasara in python plugins which is what necesitated work arounds with recoloring highlighted atoms and residues).

=======
recolor
=======

This method handles recoloring for both atoms and residues.  This is because of how yasara handles hud buttons created by python plugs (see `closeUp`_ for more details).  After checking if we're working with Atoms or Residues we then set the objects in the repaintList to the color defined by the yasara Element sheet, basicly it is their default color as defined by the project.

============
recordRotate
============

The heart and soul of this plugin, Random Rotation.  This method spins the view randomly, but because yasaras view is a relative to previous moves with no absolut position availible, we have to record every move we make so that we can get back to the view the user finaly selects.

First we generate a set of random points, then we move the view int he XYZ with AutoMoveTo.  Then we rotate the view in the ABG.

Finaly we write these movements to the list of lines for the macro.  The important thing about these lines is that the steps are set to 1 and Wait is set to No.  This way when the macro runs all of our moves and zooms will happen in a single move (form start point to end point) and they will all happen at the same time. In this way all the relative positiong is maintained but the user only see the final zoom.

==========
replayAtom
==========

This method just bundels together a rotation and a zoom for the atom.

=============
replayProtein
=============

This method just bundels together a rotation and a zoom for the residue.

=============
stopMacroFile
=============

This method primarily ensures that there is not a macro recording while the plugin runs but it is also responsable for doing initial setup and poling the config file.

First we cehck that there is an active saveData object in storage, if not we initialise one.  This will only be done the first time that the plugin is used since opening Yasara.

After reading in the user settings we check to see if we need to ask for the macro file that they are recording to.  If they are not currently recording then we set up a new macro file.  

::

	yasara.storage.lines = ["\n" + MARKER]
	yasara.storage.repaintList= []
	yasara.storage.repaintWith=None
	

This code is reseting the lines we need to write to the macro file and our information needed for repainting atoms or residues.

Finaly we ensure that the macro is stoped.  we start out by running the macro, because yasara will automaticly close a running macro and start a new one, however if you try to stop a macro and none is running you get an error message.  This way can let the user start our plug with or without a running macro and they don't have to deal with a pop up.

========
zoomAtom
========

This method just calles the yasara.ZoomAtom method on our selected atom and then appends a ZoomAtom command to our list of lines to be written when the plugin closes.

===========
zoomResidue
===========

Works exactly the same as zooAtom but just calles and writes methods appropriate for a residue.

========
saveData
========

Data Members
============

selection --> The first Atom or residue selected by the user.  This is what will be used when we do the zoom.
repaintList --> List of items that were hilighted, used to reset the color when the user is finished
file --> The file path for the selected macro, allows us to reuse the same macro file without asking the user which file each time.
lines --> the lines that we are going to be writing to the macro file at the end
hilights_on --> Flag pulled from the vf_setup.ini telling us if the user wishes to highlight their selection
hilight_color --> Color that the user wants to use to highlight with.
selection_type --> Tells us if we're working with Atoms or Residues for recoloring at the end.
rememberMacro --> Flag pulled from config file telling us if they want to specify the macro each time or if we should remember it.
delay --> How long the user wants to the zoom to take, pulled from the config file.

======
points
======

Data Members
============

parts --> List of points [x, y, z, alpha, beta, gama] where the random range is [25, 25, 25, 240, 240, 240].  XAZ are a flat translation and ABG are a rotation in degrese.

Methods
=======

diff(self, point):
------------------
point --> another instance of the point class to compare against
This method is used to make sure that two consecutive translations are not too close together.  Because the movments are made at random there is a chance that consectuive points end up close to each other.

::

	neg=random.randrange(-1,1,2)
	for i in range(6):
		if(math.fabs(self.parts[i]-points.parts[i])<50):
			point.parts[i]+=self.parts[i]*neg
			neg*=random.randrange(-1,1,2)
			if i > 2:
				self.parts[i]%=25
			elif self.parts[i]<0:
				self.parts[i]%=180
			else:
				self.parts[i]%=360

neg is a modifier to see if we flip the sign.
we then go point by point and make sure that the diffrence is above 50, if not then we add the difrence together (after mulstiplying by the possible negative number).  Once we use neg we roll the dice again to see if we flip the sign before the next compare (to avoid a string of all neg, all pos, or flip flop numbers).  We then need to check that by combining our numbers they didn't get too big (or two small).  We limit the XYZ to 25, ABG are limited to 360 in the positive direction, and 180 in the negative by Yasara so we cut them down as well.

======
parser
======

We had some compatability issues with the configparser module.  This classes use of a dictionary and the way we write to the file closley mirros the use of configparser incase some one needs or wants to reimpliment the module.

Data Members
============

config --> a dictionary to hold the diffrent peramiters found in our .ini file.  Because our ini file is so short we do not use section headers, so we have a simple dictionary instead of a dictionary of dictionaries.

file_path --> we grab a copy of the path to this .py sheat.  The ini file is required to be in the plugin directory with this module.  This only works in windows, if you move to a linux or apple system you will need to check the os.

Methods
=======

writeFile(hilightSelection, filePersistance, color, delay):
-----------------------------------------------------------
hilightSelection --> boolean value, wheather or not highlighting will be used.

filePErsistance --> boolean value, wheather or not we will remember what macro file is being used.

color --> the color to highlight selected Atoms or Residue, if nothing was selected in in the pop up window, it defaults to the value already in the file.

delay --> how long the zoom should take, if it's less then 1 we set it to one otherwise Yasara will gripe.

we load config with the value paris (a ':' is used to deliminate identifiers from values).  we then open the file, write the key -> value pairs, and close the file.

readFile (data):
----------------
data --> a saveData object to store the values in once we read them from the file.

open the file, read all lines, split them into key --> value on the ':' delimiter, pass them into the config dictionary, then read from the dictionary to the saveData obj.  pretty self explanitory stuff.  incase some one addes the [default] header for an .ini file we put this in a try catch block, this way we can skip the bad split and unknown key.

