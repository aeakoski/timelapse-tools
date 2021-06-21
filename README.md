# Timelapse tools

## Install
- Python3
- pip3
  - pillow
  - tqdm
  - shutil


## Prereq
- Ubuntu
- Folder `photos` with photos named YYYYmmddhhMMSS...jpg

## Run
From the project home folder, run `python img.py` to creates an mp4 containing all the photos filtered from the photos tabs


## Features
This tool filters:
- Photos taken before a specific date
- Photos taken during the night
- Equalizes the brightness of all photos to a specific hard coded value calculated using the mean brightness of a random photo
