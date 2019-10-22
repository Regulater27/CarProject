from flask import Flask, request, jsonify
import pandas as pd

# Init app
app = Flask(__name__)

@app.route('/Car3', methods=['POST'])
# Function to parse data and return python array of PAS_IDs
def get_inputs():
    # Recieve JSON data as dictionary
    inputs = request.get_json()
    
    # Create an empty array to store potential PAS_IDs
    guess_PAS_ID = []
        
    # Test inputs
# =============================================================================
#     inputs = {"rc_fuel_desc" : "PETROL",
#               "rc_maker_desc" : "MARUTI SUZUKI INDIA LTD",
#               "rc_maker_model" : "ZEN MPI LX",
#               "rc_cubic_cap" : "60"}
#         
# =============================================================================
    # Get real PAS_ID reference data and clean data
    data = pd.read_csv('Make model standardisation PoC v2 Revised - Sheet1.csv')
    data = data.dropna()
    data['Fuel'] = data['Fuel'].str.upper()
    
    # Create VARs to hold input data
    fuel = inputs.get('rc_fuel_desc')
    maker = inputs.get('rc_maker_desc')
    model = inputs.get('rc_maker_model')
    cap = inputs.get('rc_cubic_cap')
    
    # Filter by fuel type
    if 'NOT APPLICABLE' not in fuel:
        if 'HYBRIDDIESELELE' not in fuel:
            data = data[~data.Fuel.str.contains('HYBRIDDIESELELE')]
            if 'DIESEL/HYBRID' not in fuel:
                data = data[~data.Fuel.str.contains('DIESEL/HYBRID')]
                if 'DIESEL' not in fuel:
                    data = data[~data.Fuel.str.contains('DIESEL')] 
        if 'PETROL/LNG' not in fuel:
            data = data[~data.Fuel.str.contains('PETROL/LNG')]
            if 'PETROL/HYBRID' not in fuel:
                data = data[~data.Fuel.str.contains('PETROL/HYBRID')]
                if 'PETROL/CNG' not in fuel:
                    data = data[~data.Fuel.str.contains('PETROL/CNG')]
                    if 'PETROL' not in fuel:
                        data = data[~data.Fuel.str.contains('PETROL')]
    # Filter by make
#    if 'MARUTI' not in maker:
#        data = data[~data.Make.str.contains('MARUTI')]
        
#    if 'ZEN MPI LX' in model:
#        data = data[data.Model.str.contains('ZEN MPI LX')]
    
    # Put potential PAS_IDs into a python list    
    guess_PAS_ID = data.iloc[0:5, 0].tolist()

    return jsonify({'PAS_ID' : guess_PAS_ID})

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=567, debug=True)
