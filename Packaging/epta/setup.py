# cd Protein_Phylogeny_Tool_project/Program/Packaging_materials/epta/
# python3 setup.py install
# conda-build .
from setuptools import setup, find_packages

setup(name = 'epta', version = '1.0', author = 'Xuran Zhao',\
packages = find_packages('./'),\
python_requires='>=3.8',\
# package_dir={'': './',},\
package_data={'standalone':['*.ini'],'standalone.test':['*.fasta']},\
include_package_data=True,\
entry_points={'console_scripts':['epta = standalone.main:run_epta',]},\
)
# install_requires=["biopython == 1.79","pandas == 1.2.3",],
