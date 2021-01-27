import pickle
import numpy as np
import pandas as pd


data = (pd.read_pickle("boil9.pickle")).to_dict('list')
print(data)
keys = list(data.keys())
features = list(data.values())
bad_indexes = []
"""
for i in range(len(features)):
    if (len([x for x in features[i] if x!=0 ])< 60 and len(keys[i])<=2):
        bad_indexes.append(i)
    elif (len([x for x in features[i] if x!=0 ])< 40 and len(keys[i])!=1):
        bad_indexes.append(i)
"""
for i in range(len(features)):
    if (len([x for x in features[i] if x!=0 ])< 50):
        bad_indexes.append(i)
        
by_molecules = np.transpose(features)

dictt ={}

to_delete = []

for i in range(len(by_molecules)):
    for index in bad_indexes:
        if by_molecules[i][index]!=0:
            to_delete.append(i)

to_delete = sorted(set(to_delete), reverse=True)

for index in to_delete:
    for key in keys:
        data[key].pop(index)
        
features_to_delete = []

for key, value in data.items():
    if sum(value) == 0:
        features_to_delete.append(key)

for feature in features_to_delete:
    data.pop(feature, None)
        

"""
target_boiling_point = dataset_boiling.pop('boiling_point')
target_melting_point = dataset_metling.pop('melting_point')
"""
print(data)
print(len(list(data.values())[0]))
print(data.keys())
with open('boil9_1.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    
"""
target = data.pop("boiling_point",None)
targ_dict = {}
for i in range(len(target)):
    targ_dict.update({i:target[i]})
features = list(data.values())
by_molecules = np.transpose(features)
dictt = {}
for i in range(len(by_molecules)):
    dictt.update({i:by_molecules[i]})
for i in range(len(features)):
    if len([x for x in features[i] if x!=0]) < 100:
        for f in range(len(features[i])):
            if features[i][f] != 0:
                dictt.pop(f, None)
        targ_dict.pop(i, None)
        
data4 = np.transpose(list(dictt.values()))
print(len(data))
data4 = [x for x in data4 if sum(x)!=0]
final = np.array(data4)
target = list(targ_dict.values())
print(len(final[0]))    
print(len(target))
"""

        
    
