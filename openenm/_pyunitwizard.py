# Configure PyUnitWizard

import pyunitwizard

standards = [
    'nm',      # length: nanometer
    'ps',      # time: picosecond
    'K',       # temperature: kelvin
    'mole',    # amount: mole
    'amu',     # mass: atomic mass unit
    'e',       # charge: elementary charge
    'kJ/mol',  # energy: kilojoules/mole
    'N',       # force: newton
    'degrees'  # angles: degree
]

pyunitwizard.configure.set_default_form('pint')
pyunitwizard.configure.set_default_parser('pint')
pyunitwizard.configure.set_standard_units(standards)


