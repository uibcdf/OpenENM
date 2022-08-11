from .enm import ENM
import molsysmt as msm
from openenm import puw
from matplotlib import pyplot as plt

class ANM(ENM):

    def __init__(self, molecular_system, selection='atom_name=="CA"', structure_index=0, cutoff='12 angstroms',
                 syntaxis='MolSysMT'):

        super().__init__(molecular_system, selection=selection, structure_index=structure_index, cutoff=cutoff)

