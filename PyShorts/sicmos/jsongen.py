import json
import os

bsim3_params    = {
        'Vth0'      : 1.0,          #? Threshold voltage at 300K [V]
        'kT'        : 2e-3,         #? Vth temp coefficient [V/K]
        'mu0'       : 500e-4,       #? Effective mobility at 300K [m^2/Vs]
        'mu_exp'    : 1.5,          #? Mobility degradation exponent
        'Cox'       : 3.45e-3,      #? Oxide capacitance per unit area [F/m^2]
        'W'         : 100e-6,       #? Transistor width [m]
        'L'         : 1e-6,         #? Channel length [m]
        'lambda'    : 0.02,         #? Channel length modulation [1/V]
        'Cj0'       : 1e-12,        #? Zero-bias junction capacitance [F]
        'Vbi'       : 0.7,          #? Built-in potential [V]
        'm'         : 0.5           #? Grading coefficient
    }
param_meta      = {
                'Vth0': {
                    'equation'        : 'Threshold voltage at 300K',
                    'unit'            : 'V',
                    'description'     : 'Threshold voltage of the MOSFET at 300 K',
                    'source'          : 'Device datasheet or experimental extraction'
                },
                'kT': {
                    'equation'        : 'Vth temperature coefficient',
                    'unit'            : 'V/K',
                    'description'     : 'Coefficient for threshold voltage temperature dependence',
                    'source'          : 'Device datasheet or model parameter'
                },
                'mu0': {
                    'equation'        : 'Effective mobility at 300K',
                    'unit'            : 'm^2/V·s',
                    'description'     : 'Carrier mobility in channel at 300 K',
                    'source'          : 'Model parameter from literature or datasheet'
                },
                'mu_exp': {
                    'equation'        : 'Mobility degradation exponent',
                    'unit'            : 'dimensionless',
                    'description'     : 'Exponent modeling mobility dependence on temperature',
                    'source'          : 'Fitted parameter from experiments'
                },
                'Cox': {
                    'equation'        : 'ε_ox / t_ox',
                    'unit'            : 'F/m^2',
                    'description'     : 'Capacitance of gate oxide per unit area',
                    'source'          : 'Calculated from oxide thickness and permittivity'
                },
                'W': {
                    'equation'        : 'Transistor width',
                    'unit'            : 'm',
                    'description'     : 'Channel width of the MOSFET',
                    'source'          : 'Design layout parameter'
                },
                'L': {
                    'equation'        : 'Channel length',
                    'unit'            : 'm',
                    'description'     : 'Channel length of the MOSFET',
                    'source'          : 'Design layout parameter'
                },
                'lambda': {
                    'equation'        : 'Channel length modulation',
                    'unit'            : '1/V',
                    'description'     : 'Coefficient modeling channel length modulation effect',
                    'source'          : 'Extracted from device characteristics'
                },
                'Cj0': {
                    'equation'        : 'Zero-bias junction capacitance',
                    'unit'            : 'F',
                    'description'     : 'Capacitance of reverse-biased junction at zero bias',
                    'source'          : 'Device datasheet or junction modeling'
                },
                'Vbi': {
                    'equation'        : 'Built-in potential',
                    'unit'            : 'V',
                    'description'     : 'Built-in voltage of the PN junction',
                    'source'          : 'Physical constant or device parameter'
                },
                'm': {
                    'equation'        : 'Grading coefficient',
                    'unit'            : 'dimensionless',
                    'description'     : 'Exponent describing junction capacitance voltage dependence',
                    'source'          : 'Device physics or datasheet'
                }
            }
def merge_params_to_json(params, metadata, output_path):
    combined_dict = {}
    for key, value in params.items():
        combined_dict[key] = {
            "value"      : value,
            "equation"   : metadata[key].get("equation", ""),
            "unit"       : metadata[key].get("unit", ""),
            "description": metadata[key].get("description", ""),
            "source"     : metadata[key].get("source", "")
        }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined_dict, f, indent=4)


json_path = "PyShorts/sicmos/sicmos_BSIM3v3.json"
merge_params_to_json(bsim3_params, param_meta, json_path)
