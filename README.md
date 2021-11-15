Github link: https://github.com/Maxime-Mahdavian/COMP472_Assignment2.git

This code runs with the PyPy runtime environment. More specifically, it was 
run on PyPy 3.10 which uses a version of Python 3.7. You can download it from the 
PyPy project website to install it on windows, or use your packgae manager on 
Linux.

Other packages needed for the code is the os, time, argparse, numpy, random and math
packages. If not already installed on your system, you can install them with the pip
package manager. 

Here is how to run the code, and the required positional arguments:

usage: test [-h] n b s d1 d2 t a p1 p2 [coordinate [coordinate ...]]

positional arguments:
  n           Size of the board
  b           Number of blocks
  s           The winning line-up size
  d1          Maximum depth of the adversarial search for player 1
  d2          Maximum depth of the adversarial search for player 2
  t           Maximum allowed time (in seconds) for your program to return a
              move
  a           True for alphabeta and False for minimax
  p1          Human for playable player, AI for computer
  p2          Human for playable player, AI for computer
  coordinate  Coordinates of the block, first digit is X coordinate and second
              digit is the Y coordinate

optional arguments:
  -h, --help  show this help message and exit

