# Chopped_Simulation
CMU 15-112 Term Project. Game simulation of popular cooking competition "Chopped"
Description:
The project is a simulation game inspired by the highly popular Food Network cooking competition, Chopped, in which competitors are given a basket of several mystery ingredients and challenged to create a dish utilizing them. 

How to run:

Run the 'littleCulinary.py' file. You may need to download chrome driver (linked here for free download https://drive.google.com/file/u/6/d/1clx-obQg_xdqi3OnZjREGon2vyjQwXiK/view?usp=sharing) and change the driver location in webScraping.py to redirect to this path. If this download doesn't work, it may be because you need to download a Chrome driver specific to your computer type; full list of downloads here: https://chromedriver.chromium.org/downloads

You may need to change image location, although it should be adapted to run on user's location.

littleCulinary.py should import from webScraping.py and classesOfFood.py and characterInformation.py. characterInformation.py has functions that pull from data files "savedRecipes.txt", "userpass.txt", "leaderboard.txt". Files use images stored in the images folder. Demo video is under demo-video.txt. 
 
Which libraries: 

selenium, PIL, cmu 112 graphics, tkinter


Shortcut features:
During the cooking mode, instead of waiting for the timer to run out, you can click 'n' and move onto the scoring page. Press "w" to trigger win/loss screen and get to leaderboard. When logging in you need to click on the user rectangle, press enter, click on the password rectangle, click enter, and then either log in or register. 

Plz enjoy!!
