import molsysmt as msm
from openenm import pyunitwizard as puw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm
from copy import deepcopy
from sklearn.linear_model import LinearRegression

class GaussianNetworkModel():

    def __init__(self, molecular_system, selection='atom_name=="CA"', structure_index=0, cutoff='12 angstroms',
                 syntax='MolSysMT'):

        self.molecular_system = msm.convert(molecular_system, to_form="molsysmt.MolSys", structure_indices=structure_index)

        self.atom_indices = None
        self.n_nodes = 0
        self.cutoff = None
        self.contacts = None
        self.kirchhoff_matrix = None
        self.eigenvalues = None
        self.eigenvectors = None    # modes
        self.frequencies = None
        self.b_factors = None
        self.b_factors_exp = None
        self.scaling_factor = None
        self.sqrt_deviation = None
        self.correlation_matrix = None
        self.inverse = None

        self.make_model(selection=selection, cutoff=cutoff, syntax=syntax)

    def make_model(self, selection='atom_name=="CA"', cutoff='12 angstroms', syntax='MolSysMT'):

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

        # Kirchhoff matrix: eigenvals, eigenvects

        self.kirchhoff_matrix = -self.contacts.astype(int)
        np.fill_diagonal(self.kirchhoff_matrix, self.contacts.sum(axis=1))

        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.kirchhoff_matrix)

        # Frequencies

        self.frequencies = np.sqrt(np.absolute(self.eigenvalues))

        # B-factors and diagonal

        self.b_factors_exp = msm.get(self.molecular_system, element='atom', selection=self.atom_indices, b_factor=True)

           ### scipy.linalg.pinvh would work also
        diag = np.diag(1.0/self.eigenvalues)
        diag[0,0] = 0.0
        self.inverse = self.eigenvectors @ diag @ self.eigenvectors.T

        b_factors_unfitted = self.inverse.diagonal()

        aa=0.0
        bb=0.0

        for ii in range(self.n_nodes):
            aa+=self.b_factors_exp[ii]*b_factors_unfitted[ii]
            bb+=b_factors_unfitted[ii]*b_factors_unfitted[ii]

        self.scaling_factor = aa/bb

        self.b_factors = self.scaling_factor * b_factors_unfitted

        dev=0.0
        for ii in range(self.n_nodes):
            dev+=(self.b_factors_exp[ii]-self.b_factors[ii])**2
        
        self.sqrt_deviation = dev

        # Correlation Matrix

        self.correlation_matrix = self.inverse / np.sqrt(np.einsum('ii,jj->ij', self.inverse, self.inverse))

    def show_contact_map(self):

        plt.matshow(self.contacts, cmap='binary')
        return plt.show()

    def show_best_cutoff(self, minimum='6.0 angstroms', maximum='13.0 angstroms', step='0.1 angstroms'):

        minimum_value = puw.get_value(minimum, standardized=True)
        maximum_value = puw.get_value(maximum, standardized=True)
        step_value = puw.get_value(step, standardized=True)
        length_unit = puw.get_standard_units(dimensionality={'[L]':1})

        backup_cutoff = deepcopy(self.cutoff)

        ctoff=[]
        r_2=[]
        l=1.0*self.n_nodes

        for ii in tqdm(np.arange(minimum_value, maximum_value, step_value)):
            cutoff = puw.quantity(ii, length_unit)
            ctoff.append(cutoff)
            self.make_model(cutoff=cutoff)
            r_2.append((self.sqrt_deviation)/l)

        self.make_model(cutoff=backup_cutoff)

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
        plt.plot(self.b_factors, color="red")
        return plt.show()

    def show_b_factors_dispersion(self):

        x = self.b_factors
        y = self.b_factors_exp

        plt.plot(x, y, 'yo')
        reg = LinearRegression().fit(x.reshape((-1,1)),y)
        b = reg.intercept_
        m = reg.coef_[0]
        plt.axline(xy1=(0, b), slope=m, label=f'$y = {m:.1f}x {b:+.1f}$', ls='--', color='r')

        plt.axis('square')
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.legend()

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

    def view_model(self, protein=True):

        output = msm.view(self.molecular_system)

        if not protein:
            output.clear_representations()

        coordinates = msm.get(self.molecular_system, element='atom', selection=self.atom_indices, coordinates=True)
        coordinates = puw.get_value(coordinates[0], to_unit='angstroms')

        for ii in tqdm(range(self.n_nodes)):
            for jj in range(ii+1, self.n_nodes):
                if self.contacts[ii,jj]:
                    output.shape.add_cylinder(coordinates[ii], coordinates[jj], [0.6, 0.6, 0.6], 0.2)

        return output

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

