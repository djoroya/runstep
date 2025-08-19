from .runstep import simpath
import glob,os,shutil

join = os.path.join
def purge():

    error_simulations = glob.glob(join(simpath(),"*","error.log"))
    error_simulations = [os.path.dirname(f) for f in error_simulations]

    nlen = len(error_simulations)
    print("Purging {} simulations with error logs".format(nlen))

    for sim in error_simulations:
        shutil.rmtree(sim)    

