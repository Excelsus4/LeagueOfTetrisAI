# LeagueOfTetrisAI
Tetris AI League, puts two Tetris-playing codes together and let them compete with each other.
## Languages
This project only supports Python 3.0 for now, support on other languages are on plan, please feel free to contribute.
# How to use
This project runs on Python so probably you will need python to run it. As far as I know, there aren't any external modules(even numpy) used in the core. But you may want to correct me if I'm wrong.
## Windows
Run the WindowsRun.bat file on your computer with files fully downloaded.
## Other Languages
Please contribute on how to use this project on other operating systems.
# First step for your AI
If you clone my project, you will probably see the Clean_New_AI_Template.py in the scirpt folder. This is the simplest form of AI you will probably get(which will simply drop the block in the center). Yes, there are a lot of comments but its just comments, which basically is also explained here. When you run the core, it will load chm.py and chl.py and let them compete each other. So the first thing you will want to do is change your bot file(Clean_New_AI_Template.py or choose one from the library for edit) to either chm.py or chl.py. Then start modify the file as your wish!
## Protocol
If you open any bot file, you will probably see ai class with CONST_NAME and compute method(any other members are not essential). CONST_NAME is just a string constant for display and you probably want to change this to a name of your wish. Compute method is the most important part where you will implement your algorithm. There are 4 arguments received by the "main" routine(for those who aren't familiar with python, the first argument "self" isn't really an argument but a reference to the class).
### myMap
This is a 20 by 10 integer list of the game board which the AI is playing on, this means that this is probably one of the most important thing you will want to compute on and determine where your AI puts the block in what orientation. Any blank location will be expressed as 0 and block will be expressed as 1 to 7(each integer represents a color)
### opMap
This is the opponent's game board but for now there is no interaction between the players so this wouldn't matter so much.
### current
This is the block ON HAND so is also the most important thing you want to compute with. It is expressed as 4 by 4 integer list in similar form with Map.
## next
For those complicated algorith that want to compute with one more step, here is your "next block". This will be your next "current" when you place your current.
## Return
Your algorithm have to return two integer value, each for position and rotation. For simplicity, no movements are allowed during the drop so you will only allowed to choose the position and rotation then the block will be instantly dropped(sorry for that first hole made when the block is S or Z). The value range is -3 to 9 for position and 0 to 3 for rotation. If your algorithm place the block on invalid position(like out of the board), your bot will lose instantly.
# Configuration
Speed of the game, board size and the block shape is defined in tetris/defs.py file. Feel free to change the speed of the game but be wise to change board size and block shape since some bot codes will only operate on the default config.
# Contribution
## My bot for the public
If you made a nice bot and want to show them, feel free to put your code in the botLibrary folder and make a pull request, and your 
## Refine on the Tetris Core
This is a little bit complicated but I will try my best :) so feel free to make a pull request.
# List of Bot Library
###### afk.py by EExcelsus
###### eebot1.py by EExcelsus
###### eebot2.py by EExcelsus
###### ptme.py by EExcelsus
