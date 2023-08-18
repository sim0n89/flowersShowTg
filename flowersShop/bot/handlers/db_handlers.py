import sqlite3
from pathlib import Path
import os
import sys
from config_data.config import load_config
from os import path


config = load_config()
root_dir = Path(__file__).parent.parent.parent
db_path = os.path.join(root_dir, config.db.path)
conn = sqlite3.connect(db_path, check_same_thread=False)
