# cd Protein_Phylogeny_Tool_project/Program/Packaging_materials/epta/
# python3 setup.py install
# conda-build .
import os
import sys

# check os platform
if sys.platform.startswith('linux') or sys.platform.startswith('darwim'):
    delimiter  = '/'
elif sys.platform.startswith('win32'):
    delimiter  = '\\'
else:
    delimiter  = '/'

from setuptools import setup, find_packages

setup(name = 'epta-lite', version = '1.0', author = 'Xuran Zhao',\
packages = find_packages(where='.%s' % (delimiter)),\
python_requires='>=3.8',\
# package_dir={'': './',},\
package_data={'lite':['*.ini'],'lite.test':['*.fasta']},\
include_package_data=True,\
entry_points={'console_scripts':['epta = lite.main:run_epta',]},\
)
# install_requires=["biopython == 1.79","pandas == 1.2.3",],
