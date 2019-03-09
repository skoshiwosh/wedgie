# wedgie
Python script to systemtically vary Maya node attributes and render each version automatically

This tool is based on concept of a color gamma wedge, a process done in the early days of film when multiple plates 
needed to be matched using optical printers.

These scripts should be considered work in progress.

Files:

wedgit.py
	•	return numeric list of values based on input min/max value and scale factor or start value, step size and number of steps
  
wedgitui.py
	•	user interface using PySide2 for creating wedge values created from functions in wedgit.py
	•	script is incomplete but ultimately should have buttons to create and connect wedge node
  
mkwdg.py
	•	create Maya locator node and add extra attributes to contain wedge values created from wedgit functions
	•	connect wedge locator node wedge attributes to node attribute to be wedged
	•	increment wedge index

