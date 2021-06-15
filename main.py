# G:
# cd G:\Desktop\Protein Phylogeny Tool project\Code\FASTA parser
# py fasta_parser.py -i ./Hydrogenase_test.fasta -o ./test -tax -dbn -dbd -ts

from fasta_parser import fasta_parser

import logging
import argparse
from configparser import ConfigParser





########## Parsing arguments ###########
desc='''Input file process module'''
parser=argparse.ArgumentParser(description=desc)
parser.add_argument('-i',metavar='Input_File',help='Input your file here',dest='infile')
parser.add_argument('-o',metavar='Output_File',help='Output file name',dest='outfile')
parser.add_argument('-dh',help='Keep duplicate headers in FASTA file.', action='store_true')
parser.add_argument('-fl',metavar='Filter_length', help='How long you want to filter sequences?',dest='filter_length', required=False)
parser.add_argument('-tax',help='Search for taxonomy information for each sequence.', action='store_true')
parser.add_argument('-dbn',help='Search for identification information (protein name and organism) for each sequence.', action='store_true')
parser.add_argument('-dbd',help='Search for domain information for each sequence in Entrenz database (no evalue and bit score).', action='store_true')
parser.add_argument('-pfs',help='Run Pfamsacn (domain prediction) for each sequence.', action='store_true')
args=parser.parse_args()
########################################
# read config file
def read_config():
    cfg = ConfigParser()
    cfg.read('config.ini')
    if not args.dh:
        args.dh = cfg.getboolean('FASTA parser','keep_duplicate_headers')
    if not args.filter_length:
        args.filter_length = cfg.getint('FASTA parser','filter_length')
    if not args.tax:
        args.tax = cfg.getboolean('FASTA parser','organism_lineage')
    if not args.dbn:
        args.dbn = cfg.getboolean('FASTA parser','protein_name_from_database')
    if not args.dbd:
        args.dbd = cfg.getboolean('FASTA parser','domian_from_database')

# create log file
def create_log():
    # issue a log files
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=args.outfile + '/log_file.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add timestamp to console if asked
    logging.getLogger('').addHandler(console)
###############################################################################
# read config file
read_config()

# create log file
create_log()

fasta_parser()
