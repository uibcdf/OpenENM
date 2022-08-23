from .elastic_network_model import ElasticNetworkModel
import molsysmt as msm
from openenm import pyunitwizard as puw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm

class GaussianNetworkModel(ElasticNetworkModel):

    def __init__(self, molecular_system, selection='atom_name=="CA"', structure_index=0, cutoff='12 angstroms',
                 syntax='MolSysMT'):

        super().__init__(molecular_system, selection=selection, structure_index=structure_index, cutoff=cutoff)

        self.kirchhoff_matrix = None
        self.eigenvalues = None
        self.eigenvectors = None    # modes
        self.frequencies = None
        self.b_factors = None
        self.scaling_factor = None
        self.sqrt_deviation = None
        self.correlation_matrix = None
        self.inverse = None

        if self.contacts is not None:
            self.rebuild()

    def rebuild(self):

        self.kirchhoff_matrix = -self.contacts.astype(int)
        np.fill_diagonal(self.kirchhoff_matrix, self.contacts.sum(axis=1))

        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.kirchhoff_matrix)

        self.frequencies = np.sqrt(np.absolute(self.eigenvalues))

        # scipy.linalg.pinvh would work also
        diag = np.diag(1.0/self.eigenvalues)
        diag[0,0] = 0.0
        self.inverse = self.eigenvectors @ diag @ self.eigenvectors.T
        # Test: np.allclose(a, a @ inv @ a)

        self.b_factors = self.inverse.diagonal()

        self.correlation_matrix = self.inverse / np.sqrt(np.einsum('ii,jj->ij', self.inverse, self.inverse))

        self.fitt_b_factors()

    def fitt_b_factors(self):

        aa=0.0
        bb=0.0

        for ii in range(self.n_nodes):
            aa+=self.b_factors_exp[ii]*self.b_factors[ii]
            bb+=self.b_factors[ii]*self.b_factors[ii]

        aa=aa/bb

        bb=0.0
        for ii in range(self.n_nodes):
            bb+=(self.b_factors_exp[ii]-aa*self.b_factors[ii])**2
        
        self.scaling_factor = aa
        self.sqrt_deviation = bb

    def show_best_cutoff(self):

        from copy import deepcopy

        backup_cutoff = deepcopy(self.cutoff)

        ctoff=[]
        r_2=[]
        l=1.0*self.n_nodes

        for ii in tqdm(np.arange(6.0,13.0,0.1)):
            cutoff = puw.quantity(ii, 'angstroms')
            ctoff.append(cutoff)
            self.calculate_contacts(cutoff)
            self.rebuild()
            r_2.append((self.sqrt_deviation)/l)

        self.calculate_contacts(backup_cutoff)
        self.rebuild()

        unit = puw.get_unit(ctoff[0])
        ctoff = np.array([puw.get_value(ii) for ii in ctoff])
        ctoff = puw.quantity(ctoff, unit)

        unit = puw.get_unit(r_2[0])
        r_2 = np.array([puw.get_value(ii) for ii in r_2])
        r_2 = puw.quantity(r_2, unit)

        plt.plot(ctoff,r_2,'yo')
        plt.ylabel('<R^2>|atom')
        plt.xlabel('Cut Off (A)')
        self.best_cutoff=[]
        self.best_cutoff.append(ctoff)
        self.best_cutoff.append(r_2)
        return plt.show()

    def show_b_factors(self):

        plt.plot(self.b_factors_exp, color="blue")
        plt.plot(self.scaling_factor*self.b_factors, color="red")
        return plt.show()

    def show_dispersion_b_factors(self):

        plt.plot(self.b_factors,self.b_factors_exp,'yo')
        plt.plot(self.b_factors,self.scaling_factor*self.b_factors,'r--')
        return plt.show()

    def show_inverse(self):

        plt.gray()
        plt.matshow(self.inverse,cmap='binary')

        return plt.show()

    def show_correlation_matrix(self, mode='norm'):

        vmin=self.correlation_matrix.min()
        vmax=self.correlation_matrix.max()

        if mode=='norm2':

            vmax=max([abs(vmin),vmax])
            vmin=-vmax

        elif mode=='norm':

            vmax=1.0
            vmin=-1.0

        elif mode=='raw':

            pass

        cdict = {
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }

        my_cmap = LinearSegmentedColormap('my_colormap', cdict, 1024)

        plt.matshow(self.correlation_matrix,cmap=my_cmap,vmin=-vmax,vmax=vmax)

        plt.colorbar()

        return plt.show()

    def write(self):

        f_map = open('contact_map.oup','w')
        
        for ii in range(self.n_nodes):
            for jj in range(ii+1,self.n_nodes):
                if self.contact_map[ii][jj] == True :
                    f_map.write("%s %s \n" %(self.system.atom_indices[ii],self.atom_indices[jj]))
        f_map.close()

        f_vects = open('gnm_vects.oup','w')

        f_vects.write("%s Modes, %s Nodes \n" %(len(self.n_nodes),len(self.n_nodes)))
        f_vects.write(" \n")
        for ii in range(self.n_nodes):
            for jj in range(self.n_nodes):
                f_vects.write("%s %f \n" %(self.atom_indices[jj], self.eigenvectors[ii][jj]))
            f_vects.write(" \n")

