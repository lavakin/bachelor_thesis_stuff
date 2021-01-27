from chemicals.critical import critical_data_Yaws
from chemicals import CAS_from_any, Tb, Tm, MW
import numpy as np
import pandas as pd
from networkx.algorithms import *
import requests
from pysmiles import read_smiles
import pickle
import calculate_indices
import mathchem

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

def count_atom_occurencies(G):
    vertices_occ = get_vertex_occurencies(G)
    atom_occurencies = {}
    atoms = G.nodes(data='element')
    for i in range(len(vertices_occ)):
        atom_type = atoms[i]
        if atom_type in atom_occurencies:
            atom_occurencies[atom_type] += vertices_occ[i]
        else:
            atom_occurencies[atom_type] = vertices_occ[i]
    atom_occurencies.update(get_edge_occurencies(G))
    """
    for order in range (1,4):
        atom_occurencies['order:' + str(order)] = (len([x for x in G.edges(data='order') if x[2] == order])/(len(G)-1))
    """
    return atom_occurencies
    

def get_vertex_occurencies(G):
    all_shortest_paths = shortest_path(G)
    vertices_occ = [ 0 for x in range(len(G))]
    for paths_from_v in all_shortest_paths.values() :
        for path in paths_from_v.values():
            for v in path:
                vertices_occ[v] += 1    
    vertices_occ = [x/(2*len(G)) for x in vertices_occ]
    return vertices_occ


def get_edge_occurencies(G):
    all_shortest_paths = shortest_path(G)
    atoms = G.nodes(data='element')
    edges_occ = {}
    order =  list(G.edges(data='order'))
    dict_order = {}
    for o in order:
        dict_order[str(o[0]) + '-'+ str(o[1])] = o[2]
        dict_order[str(o[1]) + '-'+ str(o[0])] = o[2]
    for paths_from_v in all_shortest_paths.values() :
        for path in paths_from_v.values():
            for i in range(len(path)-1):
                j = i+1
                vertices = sorted([atoms[path[i]],atoms[path[j]]])
                ord_dict_key = str(path[i]) + '-' + str(path[j])
                dict_key = vertices[0] + str(dict_order[ord_dict_key]) + vertices[1]
                if dict_key in edges_occ:
                    edges_occ[dict_key] += 1/(len(G)-1)
                else:
                    edges_occ[dict_key] = 1/(len(G)-1)
    return edges_occ
           
chemicals = pd.read_pickle("smiles.pickle")
chemicals_data = []
print(chemicals)
    
headers = []
targets = []
i = 0
for index, row in chemicals.iterrows(): 
    i+=1
    if i%200 == 0:
        print(i)
    G = read_smiles(row["smiles"], explicit_hydrogen=True)
    if is_tree(G):
        try:
            g = mathchem.Mol()
            g.read_matrix(nx.to_numpy_matrix(G))
            boiling_point =  Tb(CAS_from_any(row['chemicals']))
            occ = count_atom_occurencies(G)
            if boiling_point == None:
                continue
            occ.update({'boiling_point': boiling_point})
            """
            occ.update({'ecc_index': sum(list(eccentricity(G).keys()))})
            occ.update({'wiener_index': calculate_indices.calculate_wiener(G)})
            #occ.update({'GP_index': calculate_indices.calcuate_pisanski(G)})
            occ.update({'mol_weight': math.sqrt(MW(CAS_from_any(row["chemicals"])))/10})
            occ.update({'mol_length': len(G)})

            dia = diameter(G)
            occ.update({'side_chain': (len(G) - dia)/ dia })
            """
            headers = list(set(headers) | set(occ.keys())) 
            chemicals_data.append(occ)
        except:
            pass
dataset = {x : [] for x in headers}
for chemical in chemicals_data:
    for i in range(len(dataset.keys())):
        if headers[i] in chemical:
            dataset[headers[i]].append(chemical[headers[i]])
        else:
            dataset[headers[i]].append(0)
original_df = pd.DataFrame(dataset)
original_df.to_pickle("boil9.pickle")
print(original_df)

    

