### [ Uniqueness Assessment System (UAS) || Made by Julien 'fetzu' Bono for Le Salon's "Bleu, Sartre et ma mère" exhibition. ]
## [ CLI is cooler with docopt ]
"""
Usage: main.py [-de]
  
  Options:
    -h --help
    -d                Dev mode: shows verbose output.
    -e                English mode.
"""

## [ IMPORTS ]
import os
import datetime
from binarytree import Node, build
from docopt import docopt

# Initializing docopt
if __name__ == '__main__':
    arguments = docopt(__doc__)

## [ CONFIGURATION ]
VERSION = "0.1"
ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
SAVESDIR = os.path.join(ROOTDIR, 'SAVES') # Sets SAVESDIR path (NOTE: This folder should contain ONLY saves with ".UAS" extensions)
SAVESFILENAMEFORMAT = "%Y%m%d%H%M%S" # Sets save file name format (must be the same for all savefiles for the load/save mechanism to work)
POSITIVEANSWERS = ["y", "yes", "o", "oui"]
NEGATIVEANSWERS = ["n", "no", "non"]
if arguments['-e'] is True:
    LANGUAGE = "EN"
else:
    LANGUAGE = "FR"

## [ MISC ]
if os.path.exists(SAVESDIR + "/.DS_Store"): # REMOVE THAT FUCKING DS_STORE FILE ON OS X
  os.remove(SAVESDIR + "/.DS_Store") 

## [ LANGUAGE / TRANSLATIONS ]
if LANGUAGE == "FR":
    WELCOME = f"Bienvenue dans le Uniqueness Assessment System (UAS) version {VERSION}. Le système va vous poser une série de questions afin d'évaluer votre unicité, veuillez répondre par 'o'/'oui' ou 'n'/'non'. Vos réponses seront sauvegardées et ajoutées dans l'arbre à votre gauche toutes les 2 heures."
    QMORE = "Quoi d'autre te rends unique? "
    QPREFIX = "Dirais-tu que: "
    FINISHER = "Merci. Vos réponses ont été sauvegardées et seront analysées."
if LANGUAGE == "EN":
    QMORE = "What else makes you unique? "
    QPREFIX = "Would you say that: "
    FINISHER = "Thank you. Your answers have been saved and will be evaluated."

## [ FILE HANDLING FUNCTIONS ]
def tree_load():
    """
    Loads the latest save of the tree and returns it.
    """    
    # Get latest save (as in: file with higher number) from folder, load it as list and build the tree
    #print(os.listdir(SAVESDIR))
    latest_save = os.path.join(SAVESDIR, str(max([int(f[:f.index('.')]) for f in os.listdir(SAVESDIR)])) + ".UAS")
    tree_loaded = eval(open(latest_save, "r").read())
    tree = build(tree_loaded)
    if arguments['-d'] is True: print(f"Successfully loaded tree from {latest_save}")
    return tree

def tree_save(tree):
    """
    Saves the current tree to a file named YYYYMMDDHHMMSS.UAS inside the SAVESDIR folder.
    """
    # "The time for us is now"
    NOW = datetime.datetime.now()
    # Format the time according to config
    save_filename = os.path.join(SAVESDIR, NOW.strftime(SAVESFILENAMEFORMAT) + ".UAS")
    # Create the file, save current tree inside and close
    save_file = open(save_filename, "w")
    save_file.write(str(tree.values))
    save_file.close()
    if arguments['-d'] is True: print(f"Successfully saved current tree to {save_filename}")

## [ QUESTION/REPONSE FUNCTIONS ]
# NOTE: A tree node is built with the following logic:
#
#          _______Question?______
#         /                      \
# Negative answer           Positive answer
#
def ask_question(nodepointer):
    """
    Takes the current nodepointer (=question / position in the tree) and prompts the user for an answer.
    """    
    if nodepointer == 0:
        question = TREE[nodepointer].value
    else:
        question = QPREFIX + TREE[nodepointer].value + "?"
    answer = input(question + " ")
    check_answer(answer, nodepointer)

def check_answer(answer, nodepointer):
    """
    Takes an answer and a nodepointer (position in the tree), and checks whether the corresponding answer already exists in the tree.
    If the answer does not exist, asks the user why to create a new node.
    If it does, asks the corresponding/next question/move further down the tree.
    """    
    if answer.lower() in POSITIVEANSWERS:
        try:
            next = TREE[(nodepointer*2)+2]
            return ask_question((nodepointer*2)+2)
        except:
            return create_node(nodepointer, "right")
    elif answer.lower() in NEGATIVEANSWERS:
        try:
            next = TREE[(nodepointer*2)+1]
            return ask_question((nodepointer*2)+1)
        except:
            return create_node(nodepointer, "left")

## [ NODE FUNCTIONS ]
def create_node(nodepointer, direction):
    """
    Prompts the user for a question and creates the approriate children to the node.
    """   
    answer = input(QMORE)
    if direction == "right":
        TREE[nodepointer].right = Node(answer)
    elif direction == "left":
        TREE[nodepointer].left = Node(answer)
    print(FINISHER)

## [ MAIN ]
# Loads latest save
TREE = tree_load()

# Prints welcome message
print(WELCOME)

# Launches the loop from root of tree
ask_question(0)

# Saves current tree to disk
tree_save(TREE)

# Prints tree to console
#print(TREE)