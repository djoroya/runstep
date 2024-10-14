import glob, shutil
from runstep.simpath import simpath
import os

folder_path = simpath()
join = os.path.join

def remove_error():

    files_in  = glob.glob(join(folder_path,"**","init.json"),recursive=True)
    files_out = glob.glob(join(folder_path,"**","params.json"),recursive=True)

    files_in  = [ os.sep.join(f.split(os.sep)[:-1]) for f in files_in]
    files_out = [ os.sep.join(f.split(os.sep)[:-1]) for f in files_out]

    # select the files that are not in the output folder
    files = [f for f in files_in if f not in files_out]

    # remove files with error 
    for f in files:
        if os.path.exists(f):
            shutil.rmtree(f) 