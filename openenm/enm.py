import molsysmt as msm
from openenm import puw
import numpy as np
from matplotlib import pyplot as plt

class ENM():

    def __init__(self, molecular_system, selection='atom_name=="CA"', structure_index=0, cutoff='12 angstroms',
                 syntax='MolSysMT'):

        self.molecular_system = msm.convert(molecular_system, to_form="molsysmt.MolSys",
                                            structure_indices=structure_index)

        self.atom_indices = msm.select(self.molecular_system, selection=selection,
                                       syntax=syntax)

        self.cutoff = puw.standardize(cutoff)

        self.contacts = None

        # Start getting the contact map

        self.calculate_contacts()

    def calculate_contacts(self, cutoff=None):

        if cutoff is not None:
            self.cutoff = puw.standardize(cutoff)

        contacts = msm.structure.get_contacts(self.molecular_system,
                                              selection=self.atom_indices,
                                              structure_indices=0,
                                              threshold=self.cutoff)

        self.contacts = contacts[0]

        np.fill_diagonal(self.contacts, False)


    def show_contact_map(self):

        plt.matshow(self.contacts, cmap='binary')
        return plt.show()

