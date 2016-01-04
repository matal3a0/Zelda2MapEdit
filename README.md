# Zelda2MapEdit
A simple overworld editor for Zelda II - The Adventure of Link
Allows you to edit the four maps of the overworld.

Tested on Python 2.7.10

Limitations:
  Only the type of terrain may be edited. Caves, palaces, towns etc. cannot be moved.
  
  Don't exceed the bytesize of the original map. Size is shown in the upper right corner. It may be possible to exceed a few bytes, but not too many, or the game will become corrupt. Due to a small difference in the encoding-algorithm compared to the original game, you will see that the bytesize is larger than the original already from the point you start editing.
  To keep the map size small, use up to 16 tiles of the same type in a row as much as possible, that will make the encoded map data smaller.
