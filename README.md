# PRODI

PRODI is a command-line productivity tracker built in Python.  
The program allows users to create tasks, track time, pause and resume tasks, finish tasks, and view productivity reports.

## Features

- Start a new task
- Choose one of three categories: Work, Study, Workout
- Add an optional task name
- Add optional expected time
- Pause and resume ongoing tasks
- Finish tasks and save completion percentage
- View ongoing tasks
- Generate daily, weekly, and monthly reports
- Save task data in a JSON file
- Log important events using a custom logger

## Project Structure

``` id="t4ncgo"
project/
│
├── src/
│   ├── ptracker/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── cli.py
│   │   ├── config.py
│   │   └── logger.py
│   │
│   └── tracker_core/
│       ├── __init__.py
│       ├── models.py
│       ├── storage.py
│       └── reports.py
│
├── data/
│   └── tracker_data.json
│
├── tests/
│   └── test_reports.py
│
├── requirements.txt
├── README.md
└── .gitignore. 


Set the Python path 
Bash
export PYTHONPATH=src

How to run:
python -m ptracker.main


