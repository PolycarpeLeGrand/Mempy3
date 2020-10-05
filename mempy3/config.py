"""Config file for Mempy3

Global setting for the project, mainly to manage storage paths
Relies on pathlib.Path
"""

from pathlib import Path


BASE_PROJECT_PATH = Path.cwd()
BASE_STORAGE_PATH = Path('D:/m3data/')


if __name__ == '__main__':
    print(f'Base project path: {BASE_PROJECT_PATH}')
    print(f'Base storage path: {BASE_STORAGE_PATH}')

