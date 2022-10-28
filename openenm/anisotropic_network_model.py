import molsysmt as msm
from openenm import pyunitwizard as puw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm
from copy import deepcopy
from sklearn.linear_model import LinearRegression
import nglview as nv


class AnisotropicNetworkModel(ElasticNetworkModel):

    def __init__(self, molecular_system, selection='atom_name=="CA"', structure_index=0, cutoff='9 angstroms', stiffness=None,
                 syntax='MolSysMT'):

        self.molecular_system = msm.convert(molecular_system, to_form="molsysmt.MolSys", structure_indices=structure_index)
 
        self.atom_indices = None
        self.n_nodes = 0
        self.cutoff = None
        self.stiffness = None
        self.contacts = None
        self.hessian_matrix = None
        self.eigenvalues = None
        self.eigenvectors = None
        self.frequencies = None
        self.modes = None 
        self.b_factors = None
        self.b_factors_exp = None
        self.scaling_factor = None
        self.sqrt_deviation = None
        self.correlation_matrix = None    
        self.inverse = None

        self.make_model(selection=selection, cutoff=cutoff, syntax=syntax)

        if selection is not None:
            self.atom_indices = msm.select(self.molecular_system, selection=selection, syntax=syntax)

        if cutoff is not None:
            self.cutoff = puw.standardize(cutoff)

        # contacts

        contacts = msm.structure.get_contacts(self.molecular_system,
                                              selection=self.atom_indices,
                                              structure_indices=0,
                                              threshold=self.cutoff)

        self.contacts = contacts[0]

        self.n_nodes = self.contacts.shape[0]

        np.fill_diagonal(self.contacts, False)

        # Hessian matrix: eigenvals, eigenvects

        self.hessian_matrix = np.zeros((3*self.n_nodes, 3*self.n_nodes), dtype=float)

        coordinates = msm.get(self.molecular_system, element='atom', selection=self.atom_indices, structure_indices=0, coordinates=True)
        coordinates = puw.get_value(coordinates[0])

        for ii in range(self.n_nodes):
            iii = ii*3
            for jj in range(ii):
                if self.contacts[ii,jj]:
                    jjj = jj*3

                    rij = coordinates[ii]-coordinates[jj]
                    distance2 = np.dot(rij, rij)

                    for kk in range(3):
                        for gg in range(3):

                            val_aux = -(coordinates[jj][kk]-coordinates[ii][kk])*(coordiantes[jj][gg]-coordinates[ii][gg])/distance2

                            ## Sub matrix Hij
                            self.hessian_matrix[iii+kk, jjj+gg]=val_aux
                            self.hessian_matrix[jjj+gg, iii+kk]=val_aux
                        
                            #Sub matrix Hii:
                            self.hessian_matrix[iii+kk, iii+gg]-=val_aux
                            self.hessian_matrix[jjj+gg, jjj+kk]-=val_aux

        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.hessian_matrix)

        # Frequencies and modes

        self.frequencies = None

        self.modes = np.zeros(shape=(self.n_nodes*3, self.n_nodes, 3), dtype=float)

        for aa in range(self.n_nodes*3):
            for ii in range(self.n_nodes):
                iii=ii*3
                for jj in range(3):
                    self.modes[aa,ii,jj]=self.eigenvects[aa,iii+jj]

    def show_contact_map(self):

        plt.matshow(self.contacts, cmap='binary')
        return plt.show()

    def structures_from_harmonic_oscilation_around_mode(amplitude=8.0, steps=60, bonds_constrained=False):



