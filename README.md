# generalized_chess
Capstone mini-project exploring the potential for an AI agent that can work on custom versions of chess

Create a virtual environment with python
```Bash
python -m venv venv
```

Install the required libraries
```Bash
pip install -r requiremments.txt
```
Before running the application, you must add the relevant environment variables to the directory. In this case, this would be creating a '.env' file in the root of the directory and adding the following variables:

```
OPENAI_API_KEY=<your openai api key>
```

After adding the environment variables, you can activate the virtual environment
```Bash
source venv/bin/activate
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

