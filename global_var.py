import argparse
from configparser import ConfigParser

def args():
    ########## Parsing arguments ###########
    desc=''''''
    parser=argparse.ArgumentParser(description=desc)
    parser.add_argument('-i',metavar='Input_File',help='Input your file here',dest='infile',required=True)
    parser.add_argument('-o',metavar='Output_File',help='Output file name',dest='outfile',required=True)
    parser.add_argument('-dh',help='Keep duplicate headers in FASTA file.',action='store_true')
    parser.add_argument('-tax',help='Search for taxonomy information for each sequence.',action='store_true')
    parser.add_argument('-dbn',help='Search for protein name for each sequence.',action='store_true')
    parser.add_argument('-dbd',help='Search for domain information for each sequence in Entrenz database (no evalue and bit score).', action='store_true')
    parser.add_argument('-pfs',help='Run Pfamsacn (domain prediction) for each sequence.',action='store_true')
    parser.add_argument('-pfev',metavar='E-value',help='Spicify a e-value of Pfamscan search.',type=float)
    parser.add_argument('-pfas',help='Enable active sites prediction in Pfamscan.',action='store_true')
    parser.add_argument('-em',metavar='Email address',help='Email address that you want receive potential information from web tools.',dest='email')
    parser.add_argument('-pretry',action='store_true')
    args=parser.parse_args()
    ########################################

    # read config file
    cfg = ConfigParser()
    cfg.read('config.ini')
    if not args.dh:
        args.dh = cfg.getboolean('FASTA parser','keep_duplicate_headers')
    if not args.tax:
        args.tax = cfg.getboolean('FASTA parser','organism_lineage')
    if not args.dbn:
        args.dbn = cfg.getboolean('FASTA parser','protein_name_from_database')
    if not args.dbd:
        args.dbd = cfg.getboolean('FASTA parser','domian_from_database')
    if not args.pfs:
        args.dbd = cfg.getboolean('FASTA parser','pfamscan_search')
    if not args.pfev:
        args.pfev = cfg.getfloat('FASTA parser','E-value')
        if args.pfev > 1:
            args.pfev = int(args.pfev)
    if not args.pfas:
        args.pfas = cfg['FASTA parser']['active_sites'].replace('\'','')
    else:
        args.pfas = 'true'
    if not args.email:
        args.email = cfg['FASTA parser']['email'].replace('\'','')
    ########################################

    return args
