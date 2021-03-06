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

.. highlight:: python
   :linenothreshold: 5

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
 
 if (yasara.request == "play"):
   foo()
 
 
 yasara.plugin.end()


A you can see this starts with the YASARA PLUGIN identifier, followed by the `Menu Placment`_, then imports, functions,the yasara `Main If Structure`_, and then `Closeing the Plug`_.

We will be hitting the high points, especially gotcha issues, but our understanding is far from complete and you may find the original docs usefull.  We will try to link the relevent sections of the Yasara documentation when possible.

See :download:`original docs <Plugins.pdf>`.


=============
Menu Placment
=============

The portion of the code contained in """ is how you determin where you menu will sit and what will happen when they select the option.  In this example

::

 """
 MainMenu: Effects
   PullDownMenu after Text: Bill's plug
     SubMenu: Theater
       AtomSelectionWindow: The Round
       Request: play
 """
 
we are placing our menu item under the "Effects" tab, in the "PullDownMenu" specifying that it will come after the "Text" item on the list.  It's name will be "Bills Plug".  then we tell Yasara that when you click Bill's Plug you will get a SubMenu who's name is Theater.  So from the main menu bar at the top of Yasara you would select Effects==>Bill's Plug==>Theater .  After defining the location of our menu item we tell Yasara what we want to happen when it's selected.  In this case it opens an "AtomSelectionWindow" who title is The Round.  The final line is the Request.  This is the signal that Yasara will send when they select ok in the AtomSelectionWindow and it's what we will be catching in the IF statments that make up the body of the program.

=================
Main If Structure
=================

::

 if (yasara.request == "play"):
   foo()
   
 if (yasara.request == "stop"):
   for x in range(5):
     print("the show must go on!")
 
 if (yasara.request == "fire"):
   print("shows over")


The first thing you may notice is that the actual if statments are not very pythonesc.  That is because this is the only way that yasara will evaluate them correctly.  Other if statments inside your methods can be written if not is None: but not these.  The yasara.request field holds the value assigned by the event listner when the user selected clicked on a menu item.  This needs to mirror the string you selected for Request in the above section.  You can put whatever code you want within the if block, and depending on your plugs structure you can also use if else, do not use a closing else statment.

=================
Closeing the Plug
=================

the final line in any plugin must be 

::

 yasara.plugin.end()
 
without it things get strange and broken very fast.

