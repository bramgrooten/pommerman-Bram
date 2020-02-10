# Pommerman

Serpentine tutorials for explaining Pommerman, for more information see the wiki 
[Pommerman](https://apple.serpentineai.nl/education/public-introduction#setup) page.

These instructions assume that you have installed Python and Pycharm, in case 
you do not have installed this, check the link above for those setup guides.

## Pycharm venv and git

### Setup Git

Now that the project is loaded we are going to tell git to apply version control. 
There are two options:

1. Add the project to GitHub using:
	* `VCS` --> `Import into version control` --> `Share Project on GitHub`
  	* Enter your credentials and repository name
1. Add to a local version management, that applies only to the current device.
	* In the menu bar go to  `VCS` --> `Import into version control` --> `Create Git repository` 
  	* select the (toplevel) pommerman folder.
    * Enter the following commands in the terminal (located at the bottom)
```git
git status
git add .
git commit -m "Setup pommerman"
```
    
GitHub is the safest place to put the data, it will be synced with the GitHub 
servers and can be easily cloned to other devices. If the files are local, you 
can always upload it to GitHub afterwards.

In case you used option two, the above git commands add all the current files to 
the git version management and it is for now not important to know what each 
command does in case you are interested in what the commands do take a look at 
[git commands](https://confluence.atlassian.com/bitbucketserver/basic-git-commands-776639767.html).


### Creating a new virtual environment

Now that we have version control for this project, we are also going to add
a virtual environment specific for this project, so that if packages would change
the code will still work.

For creating a new virtual environment do the following:
- Go to File (left top of Pycharm)
- Settings
- Project: pommerman
- Project Interpreter
- The wheel icon (on the right top)
- Add
- Optionally change the name or location of the virtual environment (venv)
- Press OK
- Press Apply


                              
### Installing requirments (packages)

now that we have added a virtual environment we are going to load the required packages
into the newly created environments. Now go back to the terminal
(this is located at the left bottom of Pycharm) and check if you are in 
the venv. By default you should see the following on windows.

```cmd
(pommerman) C:\Path\to\project\pommerman>
```

If you do not see the brackets with your venv name, press the plus which is 
located at the left top of the terminal panel. This tells Pycharm to create
a new terminal that should be updated.

For installing all the packages we type the following command

```cmd
pip install -r requirements.txt
```

## Test setup

After having installed everything we have to test if it is working as expected.

Everything that is needed to run a game is located in the `serpentine` folder. 
In this folder the `run.py` can be used to run a game, where the agent located in `my_agent.py`,
is participating as the left top player.

By entering the following command in the terminal the game will run and you should
see that the left top player is not doing anything. (For early termination press `CTRL + C`.) 

```cmd
python serpentine/run.py
```

Alternatively you can right click on `run.py` and press `Run 'run'`.


In case of errors or problems feel free to contact the education commission or
ask other Serpentine members for help.

## Building your bot


This is everything required to start making your own Pommerman Agent. 
For the following steps check the first lesson, where the game will be 
explained and how we can make the bot move!

- [Lesson 1 *Game explanation and moving the bot*](https://apple.serpentineai.nl/en/education/pommerman_introduction/lesson-1)
