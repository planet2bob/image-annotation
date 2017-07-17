# image-annotation

bounding box annotation tool
minimum working version

------

requires python imaging library (PIL)
only tested on windows so far

------

usage:

 1. change the zoom variable in annotation.py to a suitable number
 2. run annotation.py
 2. select directory that contains images you want to annotate
 3. wait as it processes, then maximize window
 4. click one time at the top, bottom, left, and right of the bounding box in any order
 5. repeat until all images in the directory are finished
 6. annotations are written as [filename]: (leftx, topy, rightx, bottomy) with 0, 0 being the top left corner

