# generalized_chess
Capstone mini-project exploring the potential for an AI agent that can work on custom versions of chess

Create a virtual environment with python
```Bash
python -m venv venv
```

Before running the application, you must add the relevant environment variables to the directory. In this case, this would be creating a '.env' file in the root of the directory and adding the following variables:

```
OPENAI_API_KEY=<your openai api key>
```

After adding the environment variables, you can activate the virtual environment


```Bash
source venv/bin/activate
```


Install the required libraries
```Bash
pip install -r requirements.txt
```


Running the application
```Bash
python game_ui.py
```

Command to build
```Bash
python -m PyInstaller game_ui.py --onefile --noconsole
```



# Mac Instructions

Create a virtual environment
```Bash
python3 -m venv venv
```
if that doesn't work, replace python3 with py or python and it should hopefully create the virtual environment

Activating the environment
```Bash
source venv/bin/activate
```

Install requirements
```Bash
pip install -r requirements.txt
```

run the game
```Bash
python3 game_ui.py
```
replace python3 with python or py if it's not working


# Game Tutorial

## Game Setup

Making a piece

<img src='./tutorials/Tutorial_new_piece.gif'>

Making a board

<img src='./tutorials/Tutorial_new_board.gif'>

To play the game

<img src='./tutorials/Tutorial_play_game.gif'>


# Showcasing the Reinforcement learning implementation through open_spiel on a minimized version of chess (4x4 board)

## Showing a random game using the open_spiel implementation and api

<img src='./tutorials/Random game.gif'>

## Showing a game using the open_spiel implementation and api with a trained model

<img src='./tutorials/Human play against AZ.gif'>

# Showcasing the Reinforcement learning implementation through open_spiel on a minimized version of chess (4x4 board)

<img src='./tutorials/Training AZ agent instance.gif'>


## Installing open_spiel

https://github.com/google-deepmind/open_spiel/blob/master/docs/windows.md
https://github.com/google-deepmind/open_spiel/blob/master/docs/install.md

For windows, after installing, export the path to the built open_spiel folder for pythonpath

```Bash
export PYTHONPATH=$PYTHONPATH:/path/to/open_spiel
export PYTHONPATH=$PYTHONPATH:/path/to/open_spiel/build/python
```


To run all the tests, run the following command

```Bash
pytest Tests/*
```