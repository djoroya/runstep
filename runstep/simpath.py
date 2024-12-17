
import os,sys

folder = os.path.dirname(__file__)

if "RUNSTEP_FOLDER" in os.environ:
    folder = os.environ["RUNSTEP_FOLDER"]
    # mkdir folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    # simulations
    if not os.path.exists(os.path.join(folder,"simulations")):
        os.makedirs(os.path.join(folder,"simulations"))

def simpath():
    return os.path.join(folder,"simulations")