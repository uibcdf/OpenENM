from .enm import ENM
import molsysmt as msm
from openenm import puw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class GNM(ENM):

    def __init__(self, molecular_system, selection='atom_name=="CA"', structure_index=0, cutoff='12 angstroms',
                 syntax='MolSysMT'):

        super().__init__(molecular_system, selection=selection, structure_index=structure_index, cutoff=cutoff)

        self.kirchhoff_matrix = None
        self.eigenvalues = None
        self.eigenvectors = None    # modes
        self.frequencies = None
        self.bfactors = None
        self.correlation_matrix = None
        self._inverse = None

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
        self._inverse = self.eigenvectors @ diag @ self.eigenvectors.T
        # Test: np.allclose(a, a @ inv @ a)

        self.bfactors = self._inverse.diagonal()

        self.correlation_matrix = self._inverse / np.sqrt(np.einsum('ii,jj->ij', self._inverse, self._inverse))

    def show_correlation_matrix(self):

        vmin=self.correlation_matrix.min()
        vmax=self.correlation_matrix.max()
        vmax=max([abs(vmin),vmax])
        cdict = {
            'red'  :  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,1.0,1.0)),
            'green':  ((0.0,0.0,0.0), (0.5,1.0,1.0), (1.0,0.0,0.0)),
            'blue' :  ((0.0,1.0,1.0), (0.5,1.0,1.0), (1.0,0.0,0.0))
            }
        my_cmap = LinearSegmentedColormap('my_colormap', cdict, 1024)
        plt.matshow(self.correlation_matrix,cmap=my_cmap,vmin=-vmax,vmax=vmax)
        plt.colorbar()
        return plt.show()
