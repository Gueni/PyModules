

Sim_param 	= {
				'tSim'	    	: 0.02 ,        #simulation time
				'maxStep'		: 1e-3 ,        #maximum step size
				'rel_tol'		: 1e-3          #relative tolerance
            }
	

model_param = {
				'L'	    	: 50e-6 ,        #Inductance value
            }				


ModelVars ={    'Sim_param'     :   Sim_param   ,
                'model_param'   :   model_param
            }