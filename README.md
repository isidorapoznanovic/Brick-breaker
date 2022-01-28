# Brick-breaker
Brick-breaker is a simple old school game written in python.

# Requirements
- Python 3.10.2
- matplotlib 3.5.1
- numpy 1.21.5
- pygame 2.1.2
- Notice: python version 3.10.2 is advisable, but not required.

  ~~~
  pip install -r requirements.txt
  ~~~

# Start game
Game can be started simply by:
  
  ~~~
  python run.py
  ~~~
  
If you would like to change number of balls or bricks, run game with:
  
  ~~~
  python run.py -balls 2 -rows 3 -cols 4
  ~~~
  
If you would like to choose number of balls in graphic environment, and play again without running over and over again:

  ~~~
  python run.py -g
  ~~~
  
For random velocities at start of a game, run game along with `-r` argument.

![alt text](https://github.com/isidorapoznanovic/Brick-breaker/blob/master/2022-01-28_17-54.png)
