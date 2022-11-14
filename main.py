from .cmd_check import cmd_check
from .check_point import check_point, file_rmv
from .fasta_parser import fasta_parser
from .pfamscan_standalone import pfam_main
from .mafft_standalone import mafft_standalone
from .muscle_standalone import muscle_standalone
from .trimal_standalone import trimAl_standalone
from .iqtree_standalone import iqtree_standalone
from .ete3_epta import ete3_run

from .multi_align_lite import muilt_align
from .pfamscan_lite import run_pfamscan
from .trimal_lite import trimal_lite
from .iqtree_lite import iqtree_lite

import sys
import os
import time
import logging
import argparse
from .global_var import args

global args
args = args()

# create log file
def create_log():
    # issue a log files
    log_file = args.outfile + '/log_file.log'

    if not os.path.exists(log_file):
        open(log_file,'a+')


    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=log_file,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # add timestamp to console if asked
    logging.getLogger('').addHandler(console)
###############################################################################


def epta_standalone():


    # check out path
    if not os.path.exists(args.outfile):
        os.makedirs(args.outfile)

    start = time.perf_counter()

    # create log file
    create_log()

    logging.info('EPTA 1.0     Novermber 31st, 2022\nDeveloper Xuran Zhao\n')

    # check command line
    cmd_check()

    #check point
    new_start = None
    if not args.redo:
        new_start = check_point()
    elif args.redo:
        file_rmv()

    # print(new_start)

    wokrflow = ['fasta_parser','pfam_scan', 'multiple_alignment', 'trimal', 'iqtree', 'ete3']
    # parse fasta
    if new_start in wokrflow[:1] or new_start == None:
        fasta_parser()
        logging.info('')

    # pfamScan
    if args.pfam and (new_start in wokrflow[:2] or new_start == None):
        pfam_main()
        logging.info('')

    # mulitiple sequence alignment
    if new_start in wokrflow[:3] or new_start == None:
        if args.muscle:
            muscle_standalone()
            logging.info('')
        else:
            mafft_standalone()
            logging.info('')

    # trimal
    if new_start in wokrflow[:4] or new_start == None:
        trimAl_standalone()
        logging.info('')

    # tree making
    if new_start in wokrflow[:5] or new_start == None:
        iqtree_standalone()
        logging.info('')

    # tree drawing
    ete3_run()
    logging.info('')

    end = time.perf_counter()
    runtime = end - start
    logging.info('All proces done. Total runtime: %s second\n' % (round(runtime,2)))

def epta_lite():
    # check out path
    if not os.path.exists(args.outfile):
        os.makedirs(args.outfile)

    start = time.perf_counter()

    # create log file
    create_log()

    logging.info('EPTA beta     August 15th, 2022\nDeveloper Xuran Zhao\n')

    # check command line
    cmd_check()

    #check point
    new_start = None
    if not args.redo:
        new_start = check_point()
    elif args.redo:
        file_rmv()
    elif args.remake:
        new_start = 'ete3'

    # print(new_start)

    wokrflow = ['fasta_parser','pfam_scan', 'multiple_alignment', 'trimal', 'iqtree', 'ete3']
    # parse fasta
    if new_start in wokrflow[:1] or new_start == None:
        fasta_parser()
        logging.info('')

    # pfamScan
    if args.pfam and (new_start in wokrflow[:2] or new_start == None):
        run_pfamscan()
        logging.info('')

    # mulitiple sequence alignment
    if new_start in wokrflow[:3] or new_start == None:
        muilt_align()

    # trimal
    if new_start in wokrflow[:4] or new_start == None:
        trimal_lite()
        logging.info('')

    # tree making
    if new_start in wokrflow[:5] or new_start == None:
        iqtree_lite()
        logging.info('')

    # tree drawing
    ete3_run()
    logging.info('')

    end = time.perf_counter()
    runtime = end - start
    logging.info('All proces done. Total runtime: %s second\n' % (round(runtime,2)))

def run_epta():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwim'):
        if args.lite:
            epta_lite()
        else:
            epta_standalone()
    elif sys.platform.startswith('win32'):
        epta_lite()


if __name__ == '__main__':
    run_epta()
