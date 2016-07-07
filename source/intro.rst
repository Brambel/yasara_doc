Introduction
************
   
This documentation is for the python portion of the Yasara api.
Much of this information was obtained by infering arguments from 
the method signitures and the Yasara CLI commands.  As such this
information is gerunteed to be incomplete.

============
Restrictions
============

If you want to add a class to your plugin please bear in mind that it
cannot be defined in the plugin itself.  It will have to be in a seperate
python file that you import to your plugin.  The line " #YASARA PLUGIN "
must come first, this can be followed by the author, tital, and any other
notes you wish to make.  Also note that method definitions must come before
the if structures but after the menu definitions.  Keep in mind that all
indents within a plugin must be two spaces, not four, this is enforced by Yasara.

An example of the necisary structure.
::
 # YASARA PLUGIN
 # Title:  Fee Fie Foe Fum
 # Author: King Lear
 #-----------------------------------
 
 """
 MainMenu: Effects
   PullDownMenu after Text: Bill's plug
     SubMenu: Atom Zoom
       AtomSelectionWindow: The Round
       Request: play
 """
 import yasara
 from players import Goneril, Regan, Cordelia
 
 def foo():
   print("I smell the blood of an english man!")
 
 if yasara.request is "play":
   foo()
 
 
 yasara.plugin.end()
::

A you can see this starts with the YASARA PLUGIN identifier, followed by the `Menu Placment`_, then imports, functions,the yasara `Main If Structure`_, and then `Closeing the Plug`_.

=============
Menu Placment
=============

TODO

=================
Main If Structure
=================

TODO 

=================
Closeing the Plug
=================

TODO

