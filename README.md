
# *Bouncy Boomerang* by Mykyta Shvets

![A preview of the game](
https://raw.githubusercontent.com/BJNick/cs30-final-project/master/screenshots/game_preview.gif)

### [Itch.io page](https://bjnick.itch.io/bouncy-boomerang)
### [Download the executable](https://bjnick.itch.io/bouncy-boomerang#download)

## CS30 Final Project Outline

### Documentation:

#### Code comments

* Download full source code [here](https://github.com/BJNick/cs30-final-project/archive/refs/heads/master.zip).
* Python files on GitHub:

  * [main.py][main]
  * [grid_world.py][grid] 
  * [tiles.py][tiles]
  * [moving_entities.py][entities] 
  * [pathfinding.py][pathfinding]
  
#### User guide

* See [user_guide.md](https://github.com/BJNick/cs30-final-project/blob/master/user_guide.md) and 
[developing_notes.md](https://github.com/BJNick/cs30-final-project/blob/master/developing_notes.md)

### Code content:

#### Use of lists, tuples, dictionaries
  
* Tiles are stored in a **dictionary** based on their position **tuple** - (row, column)
    
    *See [grid_world.py][grid], lines 20, 60 and 121*
  
* Enemies are stored in a **list**
    
    *See [grid_world.py][grid], lines 25, 56, 87*

* The function MovingEntity.draw_sprite() returns a **tuple** of a Surface and a Rect

    *See [moving_entities.py][entities], lines 81, 218 and 314*

#### Looping (definite and indefinite)
  
* An **indefinite** while loop in *[main.py][main] (line 182)* repeats until the user exits the program using the quit button

* **Definite** for loops in *[grid_world.py][grid] (lines 73, 87, 89)* iterate through a list and repeat for each element of the list

#### My own modules

* The project uses 4 modules that I developed myself:
    
    * [grid_world.py][grid] 
    * [tiles.py][tiles]
    * [moving_entities.py][entities] 
    * [pathfinding.py][pathfinding]
    
* These modules are imported in my main program in *[main.py][main] (line 16)*.

#### Recursion

* Recursion is used for implementing a merge sort and a binary search.
    
    *[pathfinding.py][pathfinding], lines 14 and 47*

#### OOP

![Class diagram](https://raw.githubusercontent.com/BJNick/cs30-final-project/master/screenshots/class_diagram.png)

The project has the following class hierarchy:

* Game *[main.py, line 32][main]*
* Grid *[grid_world.py, line 16][grid]*
* Tile *[tiles.py, line 18][tiles]*
    * Corner *[tiles.py, line 42][tiles]*
    * ActiveTile *[tiles.py, line 62][tiles]*
        * Spikes *[tiles.py, line 78][tiles]*
        * Switch *[tiles.py, line 111][tiles]*
        * Exit *[tiles.py, line 148][tiles]*
* MovingEntity *[moving_entities.py, line 20][entities]*
    * Player *[moving_entities.py, line 125][entities]*
    * Boomerang *[moving_entities.py, line 229][entities]*
    * Enemy *[moving_entities.py, line 355][entities]*
    * Coin *[moving_entities.py, line 490][entities]*
    
Indented classes are subclasses of the class above. For example, Spikes is a subclass of ActiveTile which in turn is a subclass of Tile.

#### Sorting and searching

* A [Breadth First Search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search) algorithm is used by enemies to navigate through the map towards the player. 
  
    *See [pathfinding.py][pathfinding], lines 118-177* 

* A **merge sort** is used to sort a list of graph nodes for the BFS. 
  
    *See [pathfinding.py][pathfinding], lines 14 and 164* 

* A **binary search** is used in BFS to quickly check whether a tuple is in the *already_explored* list, and to find the index of where such tuple could be inserted. 
  
    *See [pathfinding.py][pathfinding], lines 47, 137*

### Process

#### Project Journal

* [Open Google Doc](https://docs.google.com/document/d/1uhiq7ggPfLxg2BzxfUWRfkhlujJoJRuuBfaPWRTfISU/edit?usp=sharing) (Restricted access)

#### Versioning

* This git repository. [See the list of commits and changes.](https://github.com/BJNick/cs30-final-project/commits/master)

#### References / Credits

* Made with [Pygame](https://www.pygame.org/wiki/about)
* Music: [Bounce by Metre](https://freemusicarchive.org/music/Metre/oscillate/bounce)  
* Tile sets: [Pixel_Poem Dungeon Tileset](https://pixel-poem.itch.io/dungeon-assetpuck) and
* [Castle Brick [Connecting Tileset]](https://opengameart.org/content/castle-brick-connecting-tileset-16x16)
* Font: [Disposable Droid BB](https://www.1001fonts.com/disposabledroid-bb-font.html)

Additional sources are listed in the [Project Journal](https://docs.google.com/document/d/1uhiq7ggPfLxg2BzxfUWRfkhlujJoJRuuBfaPWRTfISU/edit?usp=sharing).

[main]: https://github.com/BJNick/cs30-final-project/blob/master/main.py
[grid]: https://github.com/BJNick/cs30-final-project/blob/master/grid_world.py
[tiles]: https://github.com/BJNick/cs30-final-project/blob/master/tiles.py
[entities]: https://github.com/BJNick/cs30-final-project/blob/master/moving_entities.py
[pathfinding]: https://github.com/BJNick/cs30-final-project/blob/master/pathfinding.py
