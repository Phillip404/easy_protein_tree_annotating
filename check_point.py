import os
import logging
import argparse
from global_var import args
import time

args = args()

global delimiter
delimiter = args.delim

# #####################################TEST####################################
# def create_log():
#     # issue a log files
#     logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(message)s',
#                         datefmt='%m-%d %H:%M',
#                         filename=args.outfile + '/log_file.log',
#                         filemode='w')
#     console = logging.StreamHandler()
#     console.setLevel(logging.INFO)
#     # add timestamp to console if asked
#     logging.getLogger('').addHandler(console)
# ###############################################################################
#
# # create log file
# create_log()
#
# #############################################################################


def check_info():
    path = args.outfile + 'check_point.log'
    if os.path.exists(path):
        with open(path, mode='r') as check_point:
            printed = False
            record = ''.join(check_point.readlines())
            new_start = 'fasta_parser'
            # print(record.find('fasta_parser'))
            progress = 'No progress have been made in previous run.'
            start_point = 'Start point of current run: FASTA parser'
            # fasta_parser
            if record.find('fasta_parser') != -1:
                progress = 'Previous progress: FASTA paser'
                if args.pfam:
                    start_point = 'Start point of current run: PfamScan'
                else:
                    start_point = 'Start point of current run: multiple alignment'
            else:
                logging.info(progress)
                logging.info(start_point)
                logging.info('')
                printed = True
                new_start = 'fasta_parser'

            # pfam_scan
            if args.pfam and record.find('fasta_parser') != -1:
                progress = 'Previous progress: PfamScan'
                start_point = 'Start point of current run: multiple alignment'
            elif args.pfam and record.find('pfam_scan') == -1 and printed == False:
                logging.info(progress)
                logging.info(start_point)
                logging.info('')
                printed = True
                new_start = 'pfam_scan'
            else:
                pass
            # multiple_alignment
            if record.find('multiple_alignment') != -1:
                progress = 'Previous progress: multiple alignment'
                start_point = 'Start point of current run: trimAl'
            elif record.find('multiple_alignment') == -1 and printed == False:
                logging.info(progress)
                logging.info(start_point)
                logging.info('')
                printed = True
                new_start = 'multiple_alignment'
            else:
                pass
            # trimal
            if record.find('trimal') != -1:
                progress = 'Previous progress: trimAl'
                start_point = 'Start point of current run: IQ-TREE'
            elif record.find('trimal') == -1 and printed == False:
                logging.info(progress)
                logging.info(start_point)
                logging.info('')
                printed = True
                new_start = 'trimal'
            else:
                pass
            # iqtree
            if record.find('iqtree') != -1:
                progress = 'Previous progress: IQ-TREE'
                start_point = 'Start point of current run: ETE3'
                logging.info(progress)
                logging.info(start_point)
                logging.info('')
                new_start = 'ete3'
            elif record.find('iqtree') == -1 and printed == False:
                logging.info(progress)
                logging.info(start_point)
                new_start = 'iqtree'
            else:
                pass
    else:
        open(path, mode='w')
        progress = 'No progress have been made in previous run.'
        start_point = 'Start point of current run: FASTA parser'
        logging.info(progress)
        logging.info(start_point)
        new_start = 'fasta_parser'

    return(new_start)

def check_point():
    outfile = args.outfile.rstrip() + '00_Parsed_Fasta'
    if args.remake:
        new_start = 'ete3'
        return(new_start)
    elif os.path.isdir(outfile) or os.path.isfile(outfile):
        while True:
            # if continue, delete all file with open('a') property
            check = input('Output directory is existed, do you want to read check point? (Y/N) : ')
            if check.upper() == 'Y':
                # record input action in log
                logging.debug ('Output directory is existed, do you want to read check point? (Y/N) : Y')

                logging.info('Checking progress of previous run...')

                new_start = check_info()

                return(new_start)

                break
            # if not, continue
            elif check.upper() == 'N':
                new_start = None
                return(new_start)
                break

def file_rmv():
    if args.redo:
        # specify path of parsed fasta file
        path = args.outfile.rstrip() + '00_Parsed_Fasta%sParsed_Fasta.fasta' % (delimiter)
        path2 = args.outfile.rstrip() + 'check_point.log'
        # if the file exist, delete it so that a new empty one will be create later
        # I do that because I used open(,'w+') in gz reader, it requires a empty file to write in
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(path2):
            os.remove(path2)
