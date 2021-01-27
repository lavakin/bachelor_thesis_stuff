from pysmiles import read_smiles
from networkx.algorithms import isomorphism
import networkx as nx
import sys
import requests 
from PIL import Image
import urllib
import ssl
import calculate_indices as ind_calc
from chemicals.critical import critical_data_Yaws
from chemicals import CAS_from_any, Tb
from mendeleev import element

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
  

def CIRconvert(ids):
    response = requests.get('https://opsin.ch.cam.ac.uk/opsin/' + ids + '.smi')
    resp = response.text
    if len(resp) < 2000:
        urllib.request.urlretrieve('https://opsin.ch.cam.ac.uk/opsin/' + ids.replace(" ", "+") + '.png', "sample.png")
        #img = Image.open("sample.png")
        #img.show()
        return resp
    else:
        resp = requests.get('http://cactus.nci.nih.gov/chemical/structure/' + ids + '/smiles', verify = False).text
        if "Page not found" not in resp:
            return resp
 
        else:
            print(ids, "Que??")
            sys.exit("Not a valid structure, please try again")

def add_weights(G):
    for e in G.edges:
        v1 = G.nodes(data='element')[e[0]]
        v2 = G.nodes(data='element')[e[1]]
        weight = 0
        if v1 == 'C' and v2 == 'C':
            weight = 1
        elif (v1 == 'H' and v2 == 'C') or (v1 == 'C' and v2 == 'H'):
             weight = 1
        else:
            weight = 10
            
        G[e[0]][e[1]]['weight'] = weight
    print(G.edges(data='order'))
    return G
        

"""
smiles = CIRconvert(sys.argv[1])
print(smiles)
mol = read_smiles(smiles, explicit_hydrogen=True)

# atom vector (C only)
print(mol.nodes(data='element'))
# adjacency matrix
print(nx.to_numpy_matrix(mol))
print((nx.average_shortest_path_length(mol)* len(mol)*(len(mol)-1))/2)
GM = isomorphism.GraphMatcher(mol, mol)
for i in GM.isomorphisms_iter():
	print(i)
ind_calc.calcuate_pisanski(mol)

print(critical_data_Yaws[1:30])
"""
