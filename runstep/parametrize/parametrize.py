
from ..runstep import runstep

import os
import time
from .html import mostrar_tabla,dataframize,setvalue,init_table
import copy
from importlib import import_module 

class cont():
    def __init__(self,fcn):
        self.i = 0
        self.fcn = fcn
        self.nsteps = 20
    def run(self,nstep=None):
        if nstep is None:
            self.i += 1
            self.fcn(self.i)
        else:    
            self.nsteps = nstep

@runstep()
def parametrize(params,output_folder,callback=None):

    # main_path is the path where the vars.json will be saved
    # Run is a function that runs the simulation. It must have two arguments:
    # -params: a dictionary with the parameters
    # -output_folder: the path where the simulation will be run
    # vars is a dictionary with the variables to parametrize
    # default is a function that returns a dictionary with the default values
    main_path  = output_folder
    Run_name   = params["fcn"]
    Run_module = params["module"]
    default    = params["default"]
    vars       = params["vars"]
    # mkdir simulations inside main_path

    card_path = params["output_folder"]
    sims_path = os.path.join(card_path,"simulations")
    sims_path_list = sims_path.split(os.sep)

    if sims_path_list[0] == "":
        sims_path_list[0] = os.sep

    Run = import_module(Run_module).__dict__[Run_name]
    
    df = dataframize(vars)

    json = { "vars" : vars,
             "df"   : df   ,
             "paths": []   ,
             "finished": False  }
    
    procesos = [ "Exp-"+str(i+1) for i in df.index.values]
    procesos = init_table(vars,procesos,df)


    # format vars columns .4e
    for ivar in vars.keys():
        procesos[ivar] = procesos[ivar].astype(type(vars[ivar]["span"][0]))
        if type(vars[ivar]["span"][0]) != str:
            # if not int
            if type(vars[ivar]["span"][0]) != int:
                procesos[ivar] = procesos[ivar].map(lambda x: "{:.2e}".format(x))


    all_params = []
    callback = dict()
    nsteps_list = []
    times = [0]
    for i in range(len(df)):
        params_loop = copy.deepcopy(default)

        t = time.time()
        c = cont(None)
        c.fcn    = lambda j: mostrar_tabla(procesos,i,j-1,c.nsteps,times)
        callback = c.run
        error = False

        for ivar in vars.keys():
            setvalue(params_loop,vars[ivar]["path"],df[ivar][i])
        # 
        try:
            Run(params_loop,sims_path_list,callback=callback)
        except Exception as e:
            error = True
            print("Error in Run function")
            # save error message in txt file

        nsteps_list.append(c.i)
        t = time.time() - t
        procesos["time"][i] = "{:.2f}".format(t)

        procesos["Status"][i] = "✅" if not error else "❌"        
        if not error:
            mostrar_tabla(procesos,i,c.nsteps-1,c.nsteps,times)
        else:
            mostrar_tabla(procesos,i,c.i-1,c.nsteps,times)

        all_params.append(params_loop["simulation_path"])
        times.append(t)

    json["finished"] = True
    params["simulations"] = all_params
    params["json"] = json
    params["df"] = df

    return json