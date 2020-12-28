from pysmiles import read_smiles
import networkx as nx
import sys
import requests 
from PIL import Image
import urllib
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
  

def CIRconvert(ids):
    response = requests.get('https://opsin.ch.cam.ac.uk/opsin/' + ids + '.smi')
    resp = response.text
    if len(resp) < 2000:
        urllib.request.urlretrieve('https://opsin.ch.cam.ac.uk/opsin/' + ids.replace(" ", "+") + '.png', "sample.png")
        img = Image.open("sample.png")
        img.show()
        return resp
    else:
        resp = requests.get('http://cactus.nci.nih.gov/chemical/structure/' + ids + '/smiles', verify = False).text
        if "Page not found" not in resp:
            return resp
 
        else:
            print("Que??")
            sys.exit("Not a valid structure, please try again")
              


smiles = CIRconvert(sys.argv[1])
print(smiles)
mol = read_smiles(smiles, explicit_hydrogen=True)

# atom vector (C only)
print(mol.nodes(data='element'))
# adjacency matrix
print(nx.to_numpy_matrix(mol))
