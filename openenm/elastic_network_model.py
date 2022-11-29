import molsysmt as msm
from openenm import pyunitwizard as puw
import numpy as np
from matplotlib import pyplot as plt

class ElasticNetworkModel():

    def __init__(self, molecular_system, selection='atom_name=="CA"', structure_index=0, cutoff='12 angstroms',
                 syntax='MolSysMT'):

        self.molecular_system = msm.convert(molecular_system, to_form="molsysmt.MolSys",
                                            structure_indices=structure_index)

        self.atom_indices = msm.select(self.molecular_system, selection=selection,
                                       syntax=syntax)

        self.b_factors_exp = msm.get(self.molecular_system, element='atom', selection=self.atom_indices, b_factor=True)

        self.cutoff = puw.standardize(cutoff)

        self.contacts = None
        self.n_nodes = 0

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

        self.n_nodes = self.contacts.shape[0]

        np.fill_diagonal(self.contacts, False)


    def show_contact_map(self):

        plt.matshow(self.contacts, cmap='binary')
        return plt.show()

