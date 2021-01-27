import pickle
import numpy as np


def delete_none(dataset, target):
    to_delete = [x for x in range(len(target)) if target[x] == None]
    to_delete = sorted(to_delete, reverse=True)
    print(len(to_delete))
    for index in to_delete:
        for key in dataset.keys():
            dataset[key].pop(index)
    return dataset

data = {}
with open('boil_point_dataset.pickle', 'rb') as handle:
    data = pickle.load(handle)

print(len(list(data.values())[0]))

print(data.keys())
dataset_boiling = delete_none(data, data['boiling_point'])
print(len(list(dataset_boiling.values())[0]))
  
with open('boil_dataset.pickle', 'wb') as handle:
    pickle.dump(dataset_boiling, handle, protocol=pickle.HIGHEST_PROTOCOL)
    


    
