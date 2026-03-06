from pathlib import Path


# Base directory of the project
# This goes two levels up from this file:
# src/ptracker/config.py -> project root
BASE_DIR = Path(__file__).resolve().parents[2]


# Data directory
DATA_DIR = BASE_DIR / "data"


# JSON database file
DATA_FILE = DATA_DIR / "tracker_data.json"


# Logs directory 
LOG_DIR = BASE_DIR / "logs"


# Log file
LOG_FILE = LOG_DIR / "prodi.log"