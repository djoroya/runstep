import shutil,os
join = os.path.join
from loadsavejson.loadjson import loadjson

simulations =  lambda : os.getenv("RUNSTEP_SIMULATIONS")

def deletesim(json_file):
    
    sim_params = loadjson(json_file)
    simulation_path = sim_params["simulation_path"]
    delete_sim_key(simulation_path)

    
def delete_sim_key(simulation_path):

    sim_path_abs = join(simulations(),simulation_path)

    sim_params_path = join(sim_path_abs,"init.json")
    if not os.path.exists(sim_params_path):
        print("Simulation {} not found".format(simulation_path))
        return
    else:
        sim_params   = loadjson(sim_params_path)

    if os.path.exists(sim_path_abs):
        print("Sim_params: ",sim_params)
        
        if "settings_step" not in sim_params:
            sim_params["settings_step"] = dict()
            sim_params["settings_step"]["has_children"] = False
            sim_params["settings_step"]["has_parent"] = False
            sim_params["settings_step"]["verbose"] = False
        

        if sim_params["settings_step"]["has_children"]:
            print("==============================")
            print("Simulation {} has children".format(simulation_path))
            # load params 
            params = loadjson(join(sim_path_abs,"params.json"))
            dependencies = params["dependencies"]
            for ikey in dependencies.keys():
                isimkey = dependencies[ikey]
                delete_sim_key(isimkey)

            print("Children of {} deleted".format(simulation_path))
            print("==============================")

        shutil.rmtree(sim_path_abs)
        print("Simulation {} deleted".format(simulation_path))

    else:
        print("Simulation {} not found".format(simulation_path))
