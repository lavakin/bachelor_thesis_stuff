import requests
from chemicals.critical import critical_data_Yaws
import numpy as np
import pickle
import pandas as pd


def get_smiles(ids):
    try:
        response = requests.get('https://opsin.ch.cam.ac.uk/opsin/' + ids + '.smi')
        resp = response.text
        if len(resp) < 2000:
            return resp
        else:
            return None
    except:
        return None

smiles = []
chemicals_array = []
chemicals = np.array(critical_data_Yaws.Chemical)

i=0
for chemical in chemicals:
    i+=1
    if i%20 == 0:
        print(i)
    smile = get_smiles(chemical)
    if smile == None:
        continue
    smiles.append(smile)
    chemicals_array.append(chemical)
    
original_df = pd.DataFrame({'chemicals': chemicals_array, 'smiles': smiles})

original_df.to_pickle("smiles.pickle")
