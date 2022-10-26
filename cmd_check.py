import logging
import argparse
import sys
from global_var import args
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config.ini')

args = args()
def cmd_check():
    # mafft
    # matrix
    if not args.matrix.startswith('bl') or args.matrix.startswith('jtt'):
        logging.error('Error: Invalid matrix number for MAFFT')
        sys.exit(1)

    # muscle
    mafft = cfg.getboolean('Multiple Alignment','run_MAFFT')
    muscle = cfg.getboolean('Multiple Alignment','run_MUSCLE')
    if mafft and muscle:
        logging.error('Error: \'run_MAFFT\' and \'run_MUSCLE\' in config file cannot be both setted as True.')
        sys.exit(1)

    # trimAl
    # run mode
    trimal_mod_list = ['nogaps','noallgaps','gappout','strict','strictplus','automated1']
    if not args.tmod in trimal_mod_list:
        logging.error('Error: trimAl automatic run mode invalid.')
        sys.exit(1)

    # remove spurious sequence
    if not args.rmss == 'none':
        rmss_value = range(0,1)
        residue = args.rmss.split('/')[0]
        sequence = args.rmss.split('/')[1]
        if not residue in value and sequence in value:
            logging.error('Error: residue overlap and sequence overlap for trimAl to remove spurious sequences must in range 0 to 1.')
            sys.exit(1)

        # fast fourier transform
        ffts_list = ['none','localpair','genafpair','globalpair']
        if not args.ffts in ffts_list:
            logging.error('Error: invalid fast fourier transform mode for trimAl.')
            sys.exit(1)

    # IQ-tree
    # SH test
    # if int(args.alrt) == 0 and args.bnni:
    #     logging.error('Error: Bootstrap is required to perform additional tree optimize.')
    #     sys.exit(1)
    #
    # elif int(args.alrt) < 1000:
    #     logging.error('Error: replicates of SH-like test must >= 1000.')
    #     sys.exit(1)

    # Bootstrap number
    elif int(args.boots) < 1000:
        logging.error('Error: bootstrap number of IQ-tree must >= 1000.')
        sys.exit(1)
    else:
        pass
