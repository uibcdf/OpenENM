import molsysmt as msm

class ENM():

    def __init__(self, molecular_system, selection='atom_name=="CA"', cutoff='12 angstroms',
                 syntax='MolSysMT'):

        self.molecular_system = molecular_system
        self.selection = selection
        self.syntax = syntax
        self.cutoff = cutoff

        self.contact_map = None

        # Start getting the contact map

        self.initialize_contact_map()

    def initialize_contact_map(self):

        self.contact_map = msm.structure.get_contacts(self.molecular_system,
                                                      selection=self.selection,
                                                      threshold=self.cutoff, syntaxis=self.syntax)

