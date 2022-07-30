import molsysmt as msm

class ENM():

    def __init__(self, molecular_system, structure_index=0, selection='atom_name=="CA"', cutoff='12 angstroms',
                 syntax='MolSysMT'):

        self.molecular_system = molecular_system
        self.selection = selection
        self.syntax = syntax
        self.cutoff = cutoff
        self.structure_index = structure_index

        self.contacts = None

        # Start getting the contact map

        self.initialize_contacts()

    def initialize_contacts(self):

        contacts = msm.structure.get_contacts(self.molecular_system,
                                              selection=self.selection,
                                              structure_indices=self.structure_index,
                                              threshold=self.cutoff, syntaxis=self.syntax)

        self.contacts = contacts[0]

