# G:
# cd G:\Desktop\Protein Phylogeny Tool project\Code\FASTA parser
# py fasta_parser.py -i ./Hydrogenase_test.fasta -o ./test -tax -dbn -dbd -ts

from fasta_parser import fasta_parser

import logging
import argparse
from configparser import ConfigParser
from global_var import *


args = args()

# def read_config():
#     cfg = ConfigParser()
#     cfg.read('config.ini')
#     if not args.dh:
#         args.dh = cfg.getboolean('FASTA parser','keep_duplicate_headers')
#     if not args.tax:
#         args.tax = cfg.getboolean('FASTA parser','organism_lineage')
#     if not args.dbn:
#         args.dbn = cfg.getboolean('FASTA parser','protein_name_from_database')
#     if not args.dbd:
#         args.dbd = cfg.getboolean('FASTA parser','domian_from_database')
#     if not args.pfs:
#         args.dbd = cfg.getboolean('FASTA parser','pfamscan_search')
#     if not args.pfev:
#         args.pfev = cfg.getfloat('FASTA parser','E-value')
#         if args.pfev > 1:
#             args.pfev = int(args.pfev)
#     if not args.pfas:
#         args.pfas = cfg['FASTA parser']['active_sites']
#     else:
#         args.pfas = 'true'
#     if not args.email:
#         args.email = cfg['FASTA parser']['email']


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

# create log file
create_log()

# parse fasta
fasta_parser()
