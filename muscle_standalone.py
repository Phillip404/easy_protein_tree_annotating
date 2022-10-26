import os
import logging
import argparse
from global_var import args
import time

args = args()
#
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
def enumerate_count(file):
    with open(file) as infile:
        for count, line in enumerate(infile,1):
            pass
    return count



def muscle_standalone():
    logging.info('Initializing Muscle...')

    # define file path
    path = ''.join(args.outfile.rsplit())
    print(path)
    # print(path)
    infile = path + '/00_Parsed_Fasta/Parsed_Fasta.fasta'
    # outfile = path + '01_Sequence_Alignment/Alignment_Muscle.fasta'
    outfolder = path + '/01_Sequence_Alignment/'
    outfile = path + '/01_Sequence_Alignment/Alignment_MUSCLE.fasta'
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    index_path = args.outfile + 'info_index.tsv'
    count = enumerate_count(index_path)
    if count >= 2000:
        maxiter = ' -maxiters 2'
    else:
        maxiter = ''


    logging.info('='*20)
    logging.info('Muscle parameters:')
    logging.info('Default')
    logging.info('='*20)
    logging.info('Running Muscle...')

    # run Muscle
    start = time.perf_counter()
    os.system('muscle -in %s -out %s%s' % (infile, outfile,maxiter))
    end = time.perf_counter()
    runtime = end - start
    logging.info('Muscle processing done. Runtime: %s second\n' % (round(runtime,2)))

    path = args.outfile + 'check_point.log'
    with open(path, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('multiple_alignment') == -1:
            check_point.write('multiple_alignment\n')

# Muscle_standalone()
