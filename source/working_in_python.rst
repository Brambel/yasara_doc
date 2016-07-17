Playing with Python
*******************

here's where we will talk about the python implimentation of the Yasara methods.  I'll try to put it in alphabetical order but to be honest, my letters arn't that good so be prepared to use that ctrl-f magic.

==========
Methods
==========

AutoMoveTo(x=None, y=None, z=None, steps=None, wait=None):
----------------------------------------------------------

All moves are relative to current position, there is no exposed aboslute position.

x --> X position to translate to.

y --> Y position to translate to.

z --> Z position to translate to.

steps --> how many steps between the start and stop position.  must be grater then zero, by using a step of 1 we make an instantanious move. default is 1.

wait --> if we wait for the previous camera move to finish before we start this one.  Defautl is Yes.

AutoRotateTo(alpha=None, beta=None, gamma=None, steps=None, wait=None):
-----------------------------------------------------------------------

All rotations are relative to current position, there is no exposed aboslute position.

alpha --> X rotation to translate to.

beta --> Y rotation to translate to.

gama --> Z rotation to translate to.

steps --> how many steps between the start and stop position.  must be grater then zero, by using a step of 1 we make an instantanious move. default is 1.

wait --> if we wait for the previous camera move to finish before we start this one.  Defautl is Yes.

ColorAtom(selection1, first=None, second=None, segments=None, mapcons=None, filename=None):
------------------------------------------------------------------------------------------------------

PASS we'll get back to it.

PrintHUD():
-----------

This allows us display buttons to the HUD, which is the right menu superimposed over the modlel.

run(command):
-------------

this allows us to use comands not support by the python interface.  it's slow because we go from the python thread to anacond to c++, so don't use it unelss theres no other way to get to the command you need.  starting and stoping macro records are just such commands.

command --> this is the yanacond command

ShowButton(text, x=None, y=None, width=None, height=None, border=None, color=None, action=None):
-----------------------------------------------------------------------------------------------------

text --> text on the button, in python this is also the yasara.request that will be provided to catch the buttons behavior.

x --> x position of the top left corner

y --> y position of the top left corner

width --> pixel width of the button

height --> pixel height of the button

border -->  boolean value, if the button has a border or not

color --> color the button is suposed to be, in python these color are incorrect, it does not display as the selected color.

ShowWin(selection1, title, *arglist2):
--------------------------------------

This will generate a window of whatever type you need.

selection1 --> the type of window, there are a set of key words to determin your window type.

title --> The title you want to apper at the top of the window.

*arglist2 --> the arguemtns to pass in, this is determind by the window type.

please see the yasara documentation <PUT A LINK HERE> since I'm not typing out everything they already said.

ZoomAtom(selection1, steps=None, wait=None):
--------------------------------------------

This zooms in on an atom or a group of atoms.  If more then one atom is selcted it will not rotate the view, it is a straight XYZ pan.

selection1 --> the atom or group of atoms, we use yasara.selection[0].number.inyas to denote the atom, we make sure to select the first atom to zoom on.

steps --> how many steps between the start and stop position.  must be grater then zero, by using a step of 1 we make an instantanious move. default is 1.

wait --> if we wait for the previous camera move to finish before we start this one.  Defautl is Yes.

ZoomRes(selection1, steps=None, wait=None):
-------------------------------------------

This is exactly the same as <ZoomAtom MAKE SURE TO LINK>, except we target residues, unfortuently the underlying c++ is not smart enough to let us use a single method for all these variations.
 
============
Data Members
============

yasara.storage
--------------

persistant storage, your plugin can use this repeatedly betwen calls, so long as Yasara is not closed.  It is a single location so you need to assign an object to it that can hold everything you need.

yasara.request
--------------

<GET BACK TO IT>