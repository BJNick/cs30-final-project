
# Developing notes

### Level Map Data Files

The level map data files such as [level_1_map_data.csv](https://github.com/BJNick/cs30-final-project/blob/master/levels/level_1_map_data.csv) in the 
*[/levels/](https://github.com/BJNick/cs30-final-project/tree/master/levels)* 
folder contain comma separated values for each tile on the grid.
These files can be easily opened in Excel or similar table editors, which makes creating levels a lot easier.

Here are screenshots of Level 1 and its data table side by side.

![A screenshot of level 1 in game](https://raw.githubusercontent.com/BJNick/cs30-final-project/master/screenshots/level_1.jpg)

Data table:

![A screenshot of level 1 data table](https://raw.githubusercontent.com/BJNick/cs30-final-project/master/screenshots/level_1_table.jpg)

### Level Text Files

The level text data files such as [tutorial_1_text.csv](https://github.com/BJNick/cs30-final-project/blob/master/levels/tutorial_1_text.csv) have lines composed of
a string, and two float values (row, column) separated by commas. These files can also be opened in Excel, and are used for adding hint text in the levels.

Contents of tutorial_1_text.csv:

    Move using [WASD] or arrow keys. While you're moving; press,0.75,1
    [Space] to throw a boomerang; and [Space] again to catch it.,1.25,1
    You can activate switches,10.75,1
    with a boomerang throw,11.25,1
    Reach the exit,10.75,11
    to continue,11.25,11

Result:

![A screenshot of tutorial 1](https://raw.githubusercontent.com/BJNick/cs30-final-project/master/screenshots/tutorial_1.jpg)

### Sprites

The 
*[/sprites/](https://github.com/BJNick/cs30-final-project/tree/master/sprites)* folder contains images for each tile/entity that are used in the game. They are saved in .png format to preserve transparency since some tiles (switch, spikes) can be drawn on top of others.

![Screenshot of the sprites folder](
https://raw.githubusercontent.com/BJNick/cs30-final-project/master/screenshots/sprites_folder.jpg)

### Other Assets

Additional assets that are not pictures go in the 
*[/assets/](https://github.com/BJNick/cs30-final-project/tree/master/assets)* folder. Currently there is a music file for playback in the game, and a font file to display pixel-style text.
