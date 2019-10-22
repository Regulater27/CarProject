import pandas as pd


# Get PAS_ID standard data fram
data = pd.read_csv('Make model standardisation PoC v2 Revised - Sheet1.csv')


inputs = {"rc_fuel_desc" : "INTERNAL_LPG_CNG",
              "rc_maker_desc" : "MARUTI SUZUKI INDIA LTD",
              "rc_maker_model" : "ZEN MPI LX",
              "rc_cubic_cap" : "60"}

# Get real PAS_ID reference data
data = pd.read_csv('Make model standardisation PoC v2 Revised - Sheet1.csv')
data = data.dropna()
data['Fuel'] = data['Fuel'].str.upper()
data['Make'] = data['Make'].str.upper()
print(data.tail())
print(len(data))
# Create an empty array to store potential PAS_IDs
guess_PAS_ID = []
        
# Create VARs to hold input data
fuel = inputs.get('rc_fuel_desc')
maker = inputs.get('rc_maker_desc')
model = inputs.get('rc_maker_model')
cap = inputs.get('rc_cubic_cap')
    
print(fuel)        
# Filter data by input fuel type
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
if 'MARUTI' in maker:
    data = data[data.Make.str.contains('MARUTI')]

    
print(data)
print(len(data))
