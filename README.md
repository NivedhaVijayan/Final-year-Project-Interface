# Final-year-Project-Interface

## Requirements:
- python3
- redis db
- Training dataset from google drive/shared privately
- Trained model from GPU from google drive/shared privately
- Media folder and RCNN folder from google drive/shared privately

## Setup : 
 - Step 1 - Clone the repository
 - Step 2 - Create a virtual environment ```virtualenv -p python3 fypenv```
 - Step 3 - Install the dependencies from requirements.txt ```pip3 install -r requirements.txt```
 - Step 4 - Create a folders named ```functions``` inside the mainapp folder.
 - Step 5 - Place the ```RCNN``` folder inside the functions folder.
 - Step 6 - Now download the media folder and place it in the project root directory.
 - Step 7 - Run the command makemigrations and migrate command
 - Step 8 - Run ```python3 manage.py runserver```
 - Step 9 - Open browser and go to http://localhost:8000/
 
 The videos and navigations options will be displayed in the browser.
  
  

