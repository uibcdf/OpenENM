# Names convention

Names must be explicit enough.

## Project name

Following some rules when naming things, helps all of us to read the others code, or to write code
for the others. To be all developers of the UIBCDF and coworkers in the same page, let's try to
collect here some rules and guidelines.

### GitHub repo and Conda env

The name of the project in GitHub will be used as the same name of the Conda environment. Why?
This way you don't need to remember what the conda env name was. When the remote repository is
cloned, a directory in your machine is created with the same name. Once you want to work with a
project, knowing that the name of the directory (same as GitHub repository) is telling you what the
name of the conda env is, makes your life easy.

The name of the repository or the conda environment will be Train-Case stylized: uppercase words
and scores as spaces.

### README file and documents

The head of the main README file in the project repository will be the long version of the name's
project. For example: "UIBCDF Developers' Guide", "BiFREE Tests" or "UIBCDF Academia"

### Package

The package name will be used to import the library in a Python script, Juyter Notebook or ipython
session. The name in this case will be lowercase without spaces. And as it is suggested in the [PEP
8](https://www.python.org/dev/peps/pep-0008/#package-and-module-names), packages names should be
short and simple strings. That's why we can choose a recognizable
string not strictly equal to the project name. 


| Repo name and Conda env | Long name and README name | Short name or Package name |
| ----------------------- | ------------------------- | -------------------------- |
| Project-Name | Project Name | projname |

Sometimes we use repositories to work with other type of content, no necessary a Python library.

| Repo name and Conda env | Long name and README name | Short name or Package name |
| ----------------------- | ------------------------- | -------------------------- |
| Python-Projects-Template | Python Projects Template | python_projects_template |
| Academia | UIBCDF Academia | uibcdf_academia |


## Modules, classes, methods, variables, and others programming elements.

Regarding the coding style, we will try to work stuck to the guide propossed by the [PEP 8](https://www.python.org/dev/peps/pep-0008/).

### Modules

The name of a module will be written with snake case style: lower case letters with underscores as
spaces. See PEP 8 suggestions [here](https://www.python.org/dev/peps/pep-0008/#package-and-module-names) regarding this issue.

### Classes

Python classes will be named following the [CamelCase style](https://es.wikipedia.org/wiki/Camel_case): initial caps and not spaces or symbols between words. For example: 'Atom', 'DynamicObject', 'ProteinInterface'. See PEP 8 indications [here](https://www.python.org/dev/peps/pep-0008/#class-names).

### Exceptions

Exceptions are classes. The naming convention was described in the subsection above, but as [it is
indicated in the PEP 8](https://www.python.org/dev/peps/pep-0008/#class-names), the exception name should have the suffix "Error". These are some
examples: "NotImplementedYetError", "DatabaseNotAvailableError", "BadCallError".

### Methods and functions

Methods' and functions' names should follow the snake case style: lowercase letter with underscores as spaces. This
is the convention suggested int [PEP 8 for methods](https://www.python.org/dev/peps/pep-0008/#function-and-method-arguments).
See some examples here: 'get_number_of_atoms', 'selection', 'check_database_availability'.

### Variables, input arguments and parameters.

As the method names, input arguments and variables are written with lowercase and uncerscores
between words. Again [writting arguments this way is already suggested in PEP
8](https://www.python.org/dev/peps/pep-0008/#function-and-method-arguments), and [the same with
variables](https://www.python.org/dev/peps/pep-0008/#function-and-variable-names).

### Constants

We will follow also the naming recommendations [for constants found in PEP 8](https://www.python.org/dev/peps/pep-0008/#constants). They should be
named with capital letters and underscores as spaces, as for instance 'EPSILON0' or 'BOLTZMANN_CONSTANT_kB'.

### Not public methods and variables

Sometimes variables or methods are defined in modules with a private only use. They are not meant
to be used by users, they were only included to be used by the developers. They are
usually named private or internal. In this case we will add an underscore at the beginning. Why?
as it is mentioned in the [PEP 8](https://www.python.org/dev/peps/pep-0008/#descriptive-naming-styles):

> _single_leading_underscore: weak "internal use" indicator. E.g. from M import * does not import
> objects whose names start with an underscore.

Type | Public | Internal
---- | ------ | --------
Modules | api\_file\_pdb | \_api\_file\_pdb
Classes | SmallMolecule | \_SmallMolecule
Exceptions | NotImplementedYetError | \_NotImplementedYetError
Methods and functions | get\_dihedral\_angles | \_get\_dihedral\_angles
Variables, arguments and parameters | atom\_name | \_atom\_name
Constants | AVOGADRO\_CONSTANT_NA | \_AVOGADRO\_CONSTANT_NA




