import toStructure
import calculate_indices as ind_calc
from chemicals.critical import critical_data_Yaws
from chemicals import CAS_from_any, Tb, Tm
import chemical_classes
import matplotlib.pyplot as plt
from pysmiles import read_smiles


def get_properties(molecule_class, mol_class2):
    wiener = []
    pisanski = []
    boiling_point = [] 

    for (molecule, molec) in zip(molecule_class, mol_class2):
        smiles = toStructure.CIRconvert(molecule)
        mol = read_smiles(smiles, explicit_hydrogen=False)
        mol = toStructure.add_weights(mol)
        #print(mol.nodes(data='order'))
        try:
            boiling_point.append(Tb(CAS_from_any(molec)))
            pisanski.append(ind_calc.calcuate_pisanski(mol))
            wiener.append(ind_calc.calculate_wiener(mol))
        except:
            print(molecule, "not in the database")
    return wiener, pisanski, boiling_point

"""    
wiener, pisanski, melting_point = get_properties(chemical_classes.alkenes)    
plt.plot(melting_point, pisanski, 'ro')
"""

wiener, pisanski, boiling_point = get_properties(chemical_classes.alkynes, chemical_classes.alkanes)  
plt.plot(boiling_point, wiener, 'ro', color='blue', label="alkanes")
#plt.plot(melting_point, wiener, 'ro', color='red', label='wiener')
"""
wiener, pisanski, boiling_point = get_properties(chemical_classes.brom2, chemical_classes.brom)
plt.plot(boiling_point, wiener, 'ro', color='green', label='brom')
#plt.plot(melting_point, wiener, 'ro', color='yellow', label='wiener')
"""
plt.legend()
plt.title('elneg')
plt.xlabel("boiling point")
plt.ylabel("wiener index")
plt.show()


