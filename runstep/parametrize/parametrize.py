
from ..runstep import runstep

import os
import time
from .html import mostrar_tabla,dataframize,setvalue,init_table
import copy
from importlib import import_module 
import numpy as np

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

    """
    Ejecuta un conjunto de simulaciones parametrizadas y guarda resultados.

    Parameters
    ----------
    params : dict
        Diccionario con la configuración de la simulación. Debe contener:
        - "fcn": str, nombre de la función principal de simulación.
        - "module": str, nombre del módulo donde se define la función.
        - "default": dict, parámetros por defecto de la simulación.
        - "vars": dict, variables a parametrizar (con sus paths y valores).
        - "output_folder": str, carpeta de salida.
        - "df" (opcional): DataFrame con combinaciones de parámetros.
    output_folder : str
        Carpeta raíz donde se almacenarán los resultados.
    callback : callable, optional
        Función de callback para actualizar el estado durante la ejecución.

    Returns
    -------
    dict
        Diccionario con la información de la ejecución, que incluye:
        - "vars": variables utilizadas
        - "df": DataFrame de combinaciones
        - "paths": rutas de simulación
        - "finished": bool, si terminó la ejecución
        - "simulations": lista de rutas a las simulaciones
        - "json": estado completo del proceso

    Example
    -------
```python
from runstep.parametrize.parametrize import parametrize
import numpy as np
params = {
    "height"  : 2,    # Height [mm]
    "width"   : {
        "first":3,    # Width [mm]
        "second":1.0, # Width [mm]
            },
    }

vars = {"L": {"span": np.linspace(0, 45, 2)   , "path": ["height"]},
        "r": {"span": np.linspace(0.1, 0.5, 2), "path": ["width", "first"]}}

params_parametrize = {"default": params,
                      "vars": vars,
                      "module": "runstep.parametrize.dummy",
                      "fcn": "dummy_function"}

parametrize(params_parametrize,["output"])
``` 

    See Also
    --------
dummy_function

    """
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
    
    if "df" in params.keys():
        df = params["df"]
    else:
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

            sv = df[ivar][i]
            if type(sv) == np.int64:
                sv = int(sv)
            setvalue(params_loop,vars[ivar]["path"],sv)
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