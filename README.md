# Zelda2MapEdit
A simple overworld editor for Zelda II - The Adventure of Link.
Allows you to edit the four maps of the overworld.

Tiles can be changed by selecting the appropriate terrain icon from the top and clicking on the map. Tiles can be "painted" by holding down left mouse button and moving mouse over the map.

Locations such as caves, towns can be moved by click and drag with right mouse button.

Tested on Python 2.7.10

Limitations:
  Moving Palace 6 and New Kasuto is not yet supported. Saving a rom will most likely break these, and they have to be hexedited manually. Make sure a single desert tile (04) exists at the location for Palace 6 and a single forest (06) exists at the location for New Kasuto. Then you should be ok.
  
  Make sure the size (bytes) of your map matches the original map. Size is shown in the upper right corner. This is extra important in East Hyrule, otherwise you will experience shifting south of Palace 6. The other maps map be small. It may also be possible to exceed a few bytes, but not too many, or the game will become corrupt. 
The encoding of the original game map is not optimal, so you will see that the size differs from the original already from the point you start editing.
  To keep the map size small, use up to 16 tiles of the same type in a row as much as possible, that will make the encoded map data smaller.


Sources of information:

Message board at romhacking.net
http://datacrystal.romhacking.net/wiki/Zelda_II:_The_Adventure_of_Link:List_of_areas
http://datacrystal.romhacking.net/wiki/Zelda_II:_The_Adventure_of_Link:ROM_map
http://www.bwass.org/romhack/zelda2/
