from runstep.runstep import runstep
def autorunstep(model,params,output_folder):
    
    @runstep(model.__module__,model.__name__)
    def AutoModel(params,output_folder):
        
        model(params,params["output_folder"])

        return params
    
    return AutoModel(params,output_folder)