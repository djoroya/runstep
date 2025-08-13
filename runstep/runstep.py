
import os,sys
from runstep.createFolder     import createFolder
from runstep.path_gen   import path_gen
from runstep.find import find_from_initjson
import time
import traceback
import colorama
import datetime
from loadsavejson.loadjson import loadjson
from loadsavejson.loadjson_plain import loadjson_plain
from loadsavejson.savejson  import savejson
from runstep.common import common
join = os.path.join
import shutil
error_msg = {0:"Correct Execution",
             1:"Something went wrong"}

# ENVIRONMENT VARIABLES

# TAKE THE MAIN PATH FROM ENV 
from runstep.simpath import simpath

simulations = lambda : simpath()


def runstep():
    def decorator(func):
        def wa(*args, **kwargs):
            # take params
            params        = args[0]
            output_folder = args[1]
            # Create the output folder
            params["function"] = {
                "name":func.__name__,
                "file":func.__module__
            }
            params["metadata"] = common()
            #output_folder = os.path.abspath(output_folder)
            # assert list
            if not isinstance(output_folder,list):
                raise Exception("output_folder must be a list")
            params["output_folder"] = output_folder
            
            # if exists simulation_path, use it
            # # becouse it is a previous simulation
            # the idea is to use the same simulation_path 
            if "simulation_path" not in params.keys():
                params["simulation_path"] = path_gen()


            simulation_path = join(simulations(),
                                params["simulation_path"])
            

            createFolder(simulation_path)
            if os.name == "nt":
                if output_folder[0] == "c:":
                    output_folder[0] = "C:\\"
                output_folder = join(*output_folder)
            else:
                output_folder = join(*output_folder)
            createFolder(output_folder)
            # save params in init.json
            json_path = join(output_folder,params["simulation_path"]+".json")
            print("Saving params in: ",json_path)
            params.pop("output_folder")
            savejson(params,json_path)
            # save init.json in simulation_path
            json_path_init = join(simulation_path,"init.json")
            savejson(params,json_path_init)

            params["output_folder"] = output_folder
            
        
            params["simulation_path_abs"] = simulation_path
            params["metadata"]["init_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Execute the function
            t = time.time()
            current_folder = os.getcwd()

            # interchanging the folder
            spa = params["simulation_path_abs"]
            of  = params["output_folder"]
            params["simulation_path_abs"] = of
            params["output_folder"]       = spa

            sfind = find_from_initjson(loadjson_plain(json_path_init))
            # if sfind is not None, it means a matching simulation was found
            if len(sfind) > 0:
                os.chdir(current_folder)

                print(f"Found matching simulation for {params['simulation_path']}: {sfind}")
                # copy all file from sfind folder simulation_path to output_folder
                params_load = loadjson(join(simulations(),sfind[0],"params.json"))
                # copy all keys from params_load to params
                def merge_dicts_recursive(target, source):
                    for key, value in source.items():
                        if (
                            key in target
                            and isinstance(target[key], dict)
                            and isinstance(value, dict)
                        ):
                            merge_dicts_recursive(target[key], value)
                        else:
                            target[key] = value

                merge_dicts_recursive(params, params_load)

                # remove the folder 
                print(f"Removing folder {spa} ")
                print(f"because a matching simulation was found.")
                shutil.rmtree(spa, ignore_errors=True)    
                return 

            else:
                print(f"No matching simulation found for {params['simulation_path']}, creating new one.")
                try:
                    func(*args, **kwargs)
                    err = 0
                except Exception as e:
                    os.chdir(current_folder)
                    print(colorama.Fore.RED + "Error in step: " + func.__name__)
                    traceback.print_exc()
                    print(colorama.Fore.RESET) 
                    # save the error in error.log in output_folder
                    error_log = os.path.join(spa,"error.log")
                    with open(error_log,"w") as f:
                        f.write(traceback.format_exc())
                    raise Exception(e)
                    err = 1
            os.chdir(current_folder)

            # Compute the elapsed time
            elapsed = time.time() - t
            # remove settings

            # Save the params
            params["metadata"]["error"]     = err
            params["metadata"]["error_msg"] = error_msg[err]
            params["metadata"]["elapsed"] = elapsed
            params["metadata"]["final_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # params["root_folder"] = os.path.abspath(output_folder).replace(output_folder,"")

            # pop simulation_path_abs
            # recover the original values
            params["output_folder"] = of
            params["simulation_path_abs"] = spa
            params.pop("simulation_path_abs")
            params.pop("output_folder")
            json_path = os.path.join(spa,"params.json")
            savejson(params,json_path)

            # info.json
            params_info = dict()
            params_info["elapsed"] = elapsed
            params_info["error"] = err
            params_info["final_time"] = params["metadata"]["final_time"] 
            # if key comment exists, add it
            if "comment" in params.keys():
                params_info["comment"] = params["comment"]

            json_path = os.path.join(spa,"info.json")
            savejson(params_info,json_path)

            
        return wa
    return decorator


def lj(*x):

    file = join(simulations(),*x, "params.json")
    if os.path.exists(file):
        return loadjson(file)
    else:
        raise Exception("Simulation not found")

def lj_init(*x):

    file = join(simulations(),*x, "init.json")
    if os.path.exists(file):
        return loadjson(file)
    else:
        raise Exception("Simulation not found")
    
def lj_info(*x):

    file = join(simulations(),*x, "info.json")
    if os.path.exists(file):
        return loadjson(file)
    else:
        raise Exception("Simulation not found")