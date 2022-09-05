### [ Uniqueness Assessment System (UAS) || Made by Julien 'fetzu' Bono for Le Salon's "Bleu, Sartre et ma mère" exhibition. ]
## [ CLI is cooler with docopt ]
"""
Usage: UAS_TUI.py [-cderst8]
  
  Options:
    -h --help
    -c                CLI mode.
    -d                Dev mode: shows verbose output.
    -e                English mode.
    -r                Render mode. Render and show the loaded tree with graphviz.
    -s                Export mode. Export the loaded tree to a SVG file inside EXPORTSDIR.
    -t                Tree mode. The tree is shown at the end before the screen clears.
    -8                8 bit mode. Because we lovy TTY.
"""

## [ IMPORTS ]
import os
import sys
import time
import datetime
from binarytree import Node, build
from docopt import docopt

# Initializing docopt
if __name__ == '__main__':
    arguments = docopt(__doc__)

# Load TUI or CLI specific dependency accordingly
if arguments['-c'] is False:
    from blessed import Terminal
    term = Terminal()
else:
    import readchar

## [ CONFIGURATION ]
VERSION = "1.1.0"
ROOTDIR = os.path.realpath(os.path.join(os.path.dirname(__file__)))
EXPORTSDIR = os.path.join(ROOTDIR, 'EXPORTS') # Sets directory for SVG exports (NOTE: filename will also use format set by SAVESFILENAMEFORMAT)
GRAPHDIR = os.path.join(ROOTDIR, 'GRAPH', 'TREE') # Sets directory for graphviz export(s)
SAVESDIR = os.path.join(ROOTDIR, 'SAVES') # Sets directory for saves (NOTE: This folder should contain ONLY saves with ".UAS" extensions)
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
    ENTERTHEBLUE = "Pressez une touche pour commencer."
    WELCOME = "Bienvenue dans le Uniqueness Assessment System (UAS). Le système va vous poser une série de questions afin d'évaluer votre unicité, veuillez répondre en pressant 'o' (pour oui)' ou 'n' (pour non). Vos réponses seront sauvegardées et ajoutées dans l'arbre à votre gauche ultérieurement."
    QMORE = "Quoi d'autre vous rends unique? "
    QPREFIX = "Diriez-vous que "
    QSUFFIX = " vous rends unique?"
    INVALIDINPUT = "Réponse invalide, veuillez répondre en pressant 'o' (pour oui) ou 'n' (pour non)."
    TOOMANYERRORS = "Trop d'erreurs de saisie, le programme va redémarrer."
    FINISHER = "Merci. Vos réponses ont été sauvegardées et seront analysées."
if LANGUAGE == "EN":
    ENTERTHEBLUE = "Press any key to start."
    WELCOME = "Welcome to the Uniqueness Assessment System (UAS). The system will ask you a series of questions to evaluate your uniqueness, please answer by pressing 'y' (for yes) or 'n' (for no). Your answers will be saved and added to the tree on your left later."
    QMORE = "What else makes you unique? "
    QPREFIX = "Would you say that: "
    INVALIDINPUT = "Invalid response. Please answer with 'y' (for yes) or 'n' (for no)."
    TOOMANYERRORS = "Too many input errors. Application will restart."
    FINISHER = "Thank you. Your answers have been saved and will be evaluated."

# Wrap the long welcome texts
if arguments['-c'] is False: WELCOMEWARP = term.wrap(WELCOME)

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
    Saves the current tree to a file named according to SAVESFILENAMEFORMAT inside the SAVESDIR folder.
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
def ask_question(nodepointer, errcount = 0):
    """
    Takes the current nodepointer (=question / position in the tree) and prompts the user for an answer.
    If the input is wrong, notify the user.
    If the user manages 3 consecutive wrong inputs, restart the session.
    """    
    if nodepointer == 0:
        question = TREE[nodepointer].value
    else:
        question = QPREFIX + TREE[nodepointer].value + QSUFFIX
    if arguments['-c'] is False:
        with term.hidden_cursor():
            print(termprint((question)))
            with term.cbreak():
                answer = term.inkey()
    else:
        print(question)
        answer = readchar.readchar()
    if answer in POSITIVEANSWERS or answer in NEGATIVEANSWERS:
        check_answer(answer, nodepointer)
    elif errcount == 2:
        end_restart(1)
    else:
        print(termprint((INVALIDINPUT)))
        errcount += 1
        ask_question(nodepointer, errcount)

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

## [ OTHER FUNCTIONS ]
def create_node(nodepointer, direction):
    """
    Prompts the user for a question and creates the approriate children to the node.
    """
    if arguments['-c'] is False:
        answer = input(termprint(QMORE))
    else:
        answer = input(QMORE)
    if direction == "right":
        TREE[nodepointer].right = Node(answer)
    elif direction == "left":
        TREE[nodepointer].left = Node(answer)
    end_restart()

def initialize():
    """
    Initialize the app by loading the latest save of the tree and clearing the screen.
    """
    TREE = tree_load()
    if arguments['-c'] is False:
        print(term.home + term.on_blue + term.clear) if arguments['-8'] is True else print(term.home + term.on_dodgerblue3 + term.clear)
        print(term.white_on_black(term.rjust(f"Uniqueness Assessment System (UAS) v{VERSION}")))
        print(termprint(" "))
        for line in WELCOMEWARP: print(line)
        print(termprint(" "))
    else:
        os.system('clear')
        print(WELCOME)
    return TREE

def end_restart(graceful = 0):
    """
    In case of a graceful finish (user made it to end of current tree and input'd what made them unique), 
    print finish message, save tree and re-set app for next session.
    """
    if graceful == 0:
        tree_save(TREE)
        if arguments['-t'] is True: print(TREE)
        if arguments['-c'] is False:
            print(term.home + term.on_blue + term.clear) if arguments['-8'] is True else print(term.home + term.on_dodgerblue3 + term.clear)
            with term.location(y=term.height // 2):
                print(termprint(term.center(term.bold(FINISHER))))
            with term.hidden_cursor():
                time.sleep(10)
        else:
            print(FINISHER)
            time.sleep(10)
    else: 
        if arguments['-c'] is False:
            print(termprint((TOOMANYERRORS)))
            with term.hidden_cursor():
                time.sleep(10)
        else:
            print(TOOMANYERRORS)
            time.sleep(10)
    main()

def render_tree():
    """
    Renders the tree with GraphViz.
    """
    graph = TREE.graphviz(node_attr={'shape': 'record', 'height': '.1'})
    graph.body
    graph.render(GRAPHDIR, format='png')
    #graph.view()

def render_svg():
    """
    Renders the tree as SVG to a file named according to SAVESFILENAMEFORMAT inside the EXPORTS folder.
    """
    # "The time for us is now"
    NOW = datetime.datetime.now()
    # Format the time according to config
    svg_filename = os.path.join(EXPORTSDIR, NOW.strftime(SAVESFILENAMEFORMAT) + ".SVG")
    # Create the file, save current tree inside and close
    save_file = open(svg_filename, "w")
    save_file.write(TREE.svg())
    save_file.close()
    if arguments['-d'] is True: print(f"Successfully exported svg of current tree to {svg_filename}")

# TUI specific functions
if arguments['-c'] is False:
    def splashscreen():
        """
        Show the splashscreen and wait for enter to initialize
        """
        print(term.home + term.on_blue + term.clear) if arguments['-8'] is True else print(term.home + term.on_dodgerblue3 + term.clear)
        with term.location(y=term.height // 2):
            print(termprint(term.center(term.bold(ENTERTHEBLUE))))
        with term.hidden_cursor():
            with term.cbreak():
                keypress = term.inkey()
        if keypress == term.KEY_ENTER:
            return
        
    def termprint(arg):
        """
        Print in color according to the argument "-8". Default to 24-bit colors, "16 colors" if -8 is passed.
        """
        if arguments['-8'] is True:
            return term.white_on_blue(arg)
        else:
            return term.white_on_dodgerblue3(arg)

## [ MAIN ]
def main():
    # Show splash screen
    if arguments['-c'] is False: splashscreen()

    # Initializes the session (incl. TUI)
    global TREE
    TREE = initialize()

    # If argument "-r" or "-s" have been passed, render the tree accordingly
    if arguments['-r'] is True: render_tree()
    if arguments['-s'] is True: render_svg()

    # Launches the question/response loop from root of tree
    ask_question(0)

    # Saves current tree to disk
    #tree_save(TREE)

    # Prints tree to console
    #print(TREE)

main()
