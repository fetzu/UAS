## [ IMPORTS ]
import os
import datetime
from binarytree import Node, build

## [ CONFIGURATION ]
ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
SAVESDIR = os.path.join(ROOTDIR, 'SAVES') # Sets SAVESDIR path (NOTE: This folder should contain ONLY saves with ".UAS" extensions)
SAVESFILENAMEFORMAT = "%Y%m%d%H%M%S" # Sets save file name format (must be the same for all savefiles for the load/save mechanism to work)
POSITIVEANSWERS = ["y", "yes"]
NEGATIVEANSWERS = ["n", "no"]

## [ MISC ]
if os.path.exists(SAVESDIR + "/.DS_Store"): # REMOVE THAT FUCKING DS_STORE FILE ON OS X
  os.remove(SAVESDIR + "/.DS_Store") 

## [ FILE HANDLING FUNCTIONS ]
def tree_load():
    """
    Loads the latest save of the tree and returns it
    """    
    # Get latest save (as in: file with higher number) from folder, load it as list and build the tree
    print(os.listdir(SAVESDIR))
    latest_save = os.path.join(SAVESDIR, str(max([int(f[:f.index('.')]) for f in os.listdir(SAVESDIR)])) + ".UAS")
    tree_loaded = eval(open(latest_save, "r").read())
    tree = build(tree_loaded)
    print(f"Successfully loaded tree from {latest_save}")
    return tree

def tree_save(tree):
    """
    Saves the current tree to a file named YYYYMMDDHHMMSS.UAS inside the SAVESDIR folder
    """
    # "The time for us is now"
    NOW = datetime.datetime.now()
    # Format the time according to config
    save_filename = os.path.join(SAVESDIR, NOW.strftime(SAVESFILENAMEFORMAT) + ".UAS")
    # Create the file, save current tree inside and close
    save_file = open(save_filename, "w")
    save_file.write(str(tree.values))
    save_file.close()
    print(f"Successfully saved current tree to {save_filename}")

## [ QUESTION/REPONSE FUNCTIONS ]
# NOTE: A tree node is built with the following logic:
#
#          _______Question?______
#         /                      \
# Negative answer           Positive answer
#
def ask_question(nodevalue):
    """
    Takes the current nodevalue (=question / position in the tree) and prompts the user for an answer.
    """    
    question = TREE[nodevalue].value
    answer = input(question + " ")
    check_answer(answer, nodevalue)

def check_answer(answer, nodevalue):
    """
    Takes an answer and a nodevalue (position in the tree), and checks whether the corresponding answer already exists in the tree.
    If the answer does not exist, asks the user why to create a new node.
    If it does, asks the corresponding/next question/move further down the tree.
    """    
    if answer in POSITIVEANSWERS:
        if (nodevalue + 2) is None:
            print("Does not Exist") #TODEL
        else:
            print("Does exist") #TODEL
            ask_question(nodevalue+2)
    if answer in NEGATIVEANSWERS:
        if (nodevalue + 1) is None:
            print("Does not Exist") #TODEL
        else:
            print("Does exist") #TODEL
            ask_question(nodevalue+1)

## [ MAIN ]
# Loads latest save
TREE = tree_load()

ask_question(0)

# Saves current tree to disk
#tree_save(TREE)

# Prints tree to console
#print(TREE)