"""
OpenENM
This must be a short description of the project
"""

# versioningit
from ._version import __version__

__documentation_web__ = 'https://www.uibcdf.org/OpenENM'
__github_web__ = 'https://github.com/uibcdf/OpenENM'
__github_issues_web__ = __github_web__ + '/issues'

from . import config

from ._pyunitwizard import pyunitwizard

from .gaussian_network_model import GaussianNetworkModel
from .anisotropic_network_model import AnisotropicNetworkModel
