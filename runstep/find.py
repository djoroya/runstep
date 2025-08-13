from runstep.simpath import simpath
from loadsavejson.loadjson_plain import loadjson_plain
import glob,os
join = os.path.join



def isdone(ism1):

    """
    Check if a simulation JSON file has been completed.
    """
    ism1_path = join(simpath(), ism1, "params.json")
    return os.path.exists(ism1_path)

def compare(ism1, ism2,avoid_simulation_path=True):
    """
    Compare two simulation JSON files for equality, ignoring the 'simulation_path' key.
    """
    ism1_path = join(simpath(), ism1,"init.json")
    ism2_path = join(simpath(), ism2,"init.json")

    if not os.path.exists(ism1_path) or not os.path.exists(ism2_path):
        return False
    ism1 = loadjson_plain(ism1_path)
    ism2 = loadjson_plain(ism2_path)

    if avoid_simulation_path:

        pop_list = ["simulation_path"]
        for ipop in pop_list:
            ism1.pop(ipop, None)
            ism2.pop(ipop, None)

    return ism1 == ism2

def compare_json_vs_simulation(initjson, ism2,avoid_simulation_path=True):

    ism2_path = join(simpath(), ism2,"init.json")
    if not os.path.exists(ism2_path):
        return False
    ism2 = loadjson_plain(ism2_path)

    if avoid_simulation_path:

        pop_list = ["simulation_path","simulation_path_abs"]
        for ipop in pop_list:
            initjson.pop(ipop, None)
            ism2.pop(ipop, None)

    return initjson == ism2

def lj(ism1):
    """
    Load a JSON file and return its content as a dictionary.
    """
    ism1_path = join(simpath(), ism1, "params.json")
    return loadjson_plain(ism1_path)

def find_from_initjson(initjson,avoid_simulation_path=True):
    """
    Find the first simulation JSON file that matches the given initjson.
    """
    findings = []

    simulations = glob.glob(join(simpath(),"*"))
    simulations = [s.split(os.sep)[-1] for s in simulations]

    for ism2 in simulations:
        if compare_json_vs_simulation(initjson, ism2,avoid_simulation_path=avoid_simulation_path):
            if isdone(ism2):
                # if the simulation is done, add it to the findings
                # otherwise, skip it
                # if ism2 is not already in findings, add it        
                if lj(ism2)["function"]["name"] != "parametrize":
                    if ism2 not in findings:
                        findings.append(ism2)

    # warnings 
    if len(findings) > 1:
        print(f"Warning: Multiple matches found for {initjson}: {findings}")
    elif len(findings) == 0:
        print(f"Warning: No match found for {initjson}")

    if findings:
        return findings
    else:
        return []

def find(ism1,verbose=True):
    """
    Find the first simulation JSON file that matches the given path.
    """
    findings = []

    # remove ism1 from the list of simulations
    #if does not exist, it will not be removed 
    #give error

    # if not isdone(ism1):
    #     print(f"Warning: {ism1} is not done yet.")
    #     return []
    # if not ism1 in simulations:
    #     print(f"Warning: {ism1} does not exist in the simulations list.")
    #     return []
    pr = print if verbose else lambda *args, **kwargs: None
    simulations = glob.glob(join(simpath(),"*"))
    simulations = [s.split(os.sep)[-1] for s in simulations]

    simulations_copy = simulations.copy()
    if ism1 in simulations_copy:
        simulations_copy.remove(ism1)

    for ism2 in simulations_copy:
        if compare(ism1, ism2,avoid_simulation_path=True):
            findings.append(ism2)
    # warnings 
    if len(findings) > 1:
        pr(f"Warning: Multiple matches found for {ism1}: {findings}")
    elif len(findings) == 0:
        pr(f"Warning: No match found for {ism1}")
    else:
        pr(f"Match found for {ism1}: {findings[0]}")

    if findings:
        return findings
    else:
        return []

