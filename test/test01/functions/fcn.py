from runstep.runstep import runstep,address

@runstep(address(__file__))
def fcn(params,output_folder):

    print(params)

    return params