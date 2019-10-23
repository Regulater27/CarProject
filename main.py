from flask import Flask, request, jsonify
import pandas as pd
from fuzzywuzzy import fuzz

# Init app
app = Flask(__name__)

@app.route('/Car3', methods=['POST'])
# Function to parse data and return python array of PAS_IDs
def get_inputs():
    # Recieve JSON data as dictionary
    inputs = request.get_json()
    
    # Create an empty array to store potential PAS_IDs
    guess_PAS_ID = []
    
    # Get real PAS_ID reference data
    data = pd.read_csv('Make model standardisation PoC v2 Revised - Sheet1.csv')
    data = data.dropna()
    data['Fuel'] = data['Fuel'].str.upper()
    data['Make'] = data['Make'].str.upper()
    
    # Create an empty array to store potential PAS_IDs
    guess_PAS_ID = []
            
    # Create VARs to hold input data
    fuel = inputs.get('rc_fuel_desc')
    maker = inputs.get('rc_maker_desc')
    model = inputs.get('rc_maker_model')
    cap = inputs.get('rc_cubic_cap')
          
    # Filter data by input fuel type
    if 'NOT APPLICABLE' not in fuel:
        if 'HYBRIDDIESELELE' not in fuel:
            data = data[~data.Fuel.str.contains('HYBRIDDIESELELE')]
            if 'DIESEL/HYBRID' not in fuel:
                data = data[~data.Fuel.str.contains('DIESEL/HYBRID')]
                if 'DIESEL' not in fuel:
                    data = data[~data.Fuel.str.contains('DIESEL')] 
        if 'PETROL/LPG' not in fuel:
            data = data[~data.Fuel.str.contains('PETROL/LPG')]
            if 'PETROL/HYBRID' not in fuel:
                data = data[~data.Fuel.str.contains('PETROL/HYBRID')]
                if 'PETROL/CNG' not in fuel:
                    data = data[~data.Fuel.str.contains('PETROL/CNG')]
                    if 'PETROL' not in fuel:
                        data = data[~data.Fuel.str.contains('PETROL')]
        if 'ELECTRIC' not in fuel:
            data = data[~data.Fuel.str.contains('ELECTRIC')]
            data = data[~data.Fuel.str.contains('ELECTRICITY')]
            data = data[~data.Fuel.str.contains('ELECTRIC(Battery)')]
    
    # Create maker types
    data['Model'] = data['Model'].str.upper()
    car_types = ['MARUTI', 'TATA', 'HYUNDAI', 'TOYOTA', 'HONDA', 'MAHINDRA', 'FORD', 'CHEVROLET', 'NISSAN', 'RENAULT', 'VOLK', 'FIAT', 'SKODA', 'BMW', 'AUDI', 'MERCEDES', 'LAND', 'VOLVO', 'JAGUAR', 'MITSUBISHI', 'PORSCHE', 'BENTLEY', 'FERRARI', 'DATSUN', 'MINI', 'HINDUSTAN', 'IMCL', 'MASERATI', 'FORCE', 'JEEP', 'LAMB', 'ROLLS', 'ASTON', 'DAEWOO', 'ISUZU', 'LEXUS', 'SSANG', 'HUMMER', 'ASHOK', 'BUGATTI', 'MAYBACH', 'CADILLAC', 'REVA', 'DC', 'EICHER', 'INFINITI', 'SAN']
    
    # Filter by unusual makes
    if maker == 'OTHERS':
        for a in car_types:
            if a in model:
                data = data[data.Make.str.contains(a)]            
    if maker == '':
        for b in car_types:
            if b in model:
                data = data[data.Make.str.contains(b)]
    if maker == 'ARRAY':
        for z in car_types:
            if z in model:
                data = data[data.Make.str.contains(z)]
    if 'GEN' in maker:
         data = data[data.Make.str.contains('CHEVROLET')]
    
    # Filter for all makers in Make DF
    for c in car_types:
        if c in maker:
            data = data[data.Make.str.contains(c)]
    
    # Filter on Transmission Type
    if 'AMT' in model:
        data = data[data.Transmission.str.contains('Automatic')]
    if 'CVT' in model:
        data = data[data.Transmission.str.contains('Automatic')]
    
    # Filter on Model and Variant using fuzzywuzzy
    data['Variant'] = data['Variant'].str.upper()    
        
    if len(data) == 1:
        guess_PAS_ID = data.iloc[0, 0].tolist()
    else:
        data['ModelVariant'] = data['Model'] + ' ' + data['Variant']
        fuzzyscores = []
        for e in data['ModelVariant']:
            fuzzyscores.append(fuzz.token_sort_ratio(model, e))
        data['fuzz'] = fuzzyscores
        is_100 = data['fuzz']==100
        data100 = data[is_100]
        guess_PAS_ID = data100['PAS ID'].tolist()
    
    if not guess_PAS_ID:
        data = data.nlargest(5, 'fuzz')
        guess_PAS_ID = data['PAS ID'].tolist()   
        
    return jsonify({'PAS_ID' : guess_PAS_ID})

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=567, debug=True)
