from pathlib import Path
import os
print(f"Current Dir: {os.getcwd()}")
DATA_DIR = Path("./data")
print(f"Data Dir Absolute: {DATA_DIR.absolute()}")
print(f"Files in Data Dir: {list(DATA_DIR.glob('*'))}")
