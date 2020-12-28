import networkx as nx
import requests
from proteingraph import read_pdb
import sys
file_name = sys.argv[1] + ".pdb"
response = requests.get('https://files.rcsb.org/download/' + file_name,allow_redirects=True)
open("pdbs/"+file_name, 'wb').write(response.content)
p = read_pdb("pdbs/"+file_name)
print(nx.to_numpy_matrix(p))
