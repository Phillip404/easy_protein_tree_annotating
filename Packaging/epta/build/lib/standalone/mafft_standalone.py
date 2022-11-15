import os
import logging
import argparse
from .global_var import args
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

def mafft_standalone():
    logging.info('Initializing MAFFT...')

    # define file path
    path = ''.join(args.outfile.rsplit())
    # print(path)
    infile = path + '/00_Parsed_Fasta/Parsed_Fasta.fasta'
    # outfile = path + '01_Sequence_Alignment/Alignment_MAFFT.fasta'
    outfolder = path + '/01_Sequence_Alignment/'
    outfile = path + '/01_Sequence_Alignment/Alignment_MAFFT.fasta'
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    # matrix: bl 30 45 62 80, jtt 100 200
    if args.matrix.startswith('bl'):
        bl_number = args.matrix.split('bl')[1]
        matrix_cmd = '--bl %s' % (bl_number)
    elif args.matrix.startswith('jtt'):
        jtt_number = args.matrix.split('jtt')[1]
        matrix_cmd = '--jtt %s' % (jtt_number)
    op = float(args.op)
    ep = float(args.ep)
    retree = int(args.retree)
    maxiter = int(args.maxiterate)
    ffts = str(args.ffts)
    # ffts cmd line for mafft
    if ffts == 'localpair':
        ffts_cmd = '--localpair'
    elif ffts == 'genafpair':
        ffts_cmd = '--genafpair'
    elif ffts == 'globalpair':
        ffts_cmd = '--globalpair'
    else:
        ffts_cmd = ''

    # ffts mode for stderr
    if ffts_cmd != '':
        ffts_mode = ffts_cmd.rsplit('--')[0]
    else:
        ffts_mode = 'none'

    logging.info('='*20)
    logging.info('MAFFT parameters:')
    logging.info('Gap open penalty: %s    Gap extension penalty: %s' % (op, ep))
    logging.info('Tree rebuilding number: %s    Max iterate: %s' % (retree, maxiter))
    logging.info('Matrix: %s    FFTS mode: %s' % (args.matrix, ffts_mode))
    logging.info('='*20)
    logging.info('Running MAFFT...')

    # run MAFFT
    start = time.perf_counter()
    os.system('mafft --auto --amino --quiet --op %s --ep %s --retree %s %s --maxiterate %s %s %s > %s'\
    % (op, ep, retree, matrix_cmd, maxiter, ffts_cmd, infile, outfile))
    end = time.perf_counter()
    runtime = end - start
    logging.info('MAFFT processing done. Runtime: %s second\n' % (round(runtime,2)))

    path = args.outfile + 'check_point.log'
    with open(path, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('multiple_alignment') == -1:
            check_point.write('multiple_alignment\n')

# mafft_standalone()
