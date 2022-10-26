import os
import logging
import argparse
from global_var import args
import time

args = args()


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
# #####################################TEST####################################

def trimAl_standalone():
    logging.info('Initializing trimAl...')

    # define infile
    path = ''.join(args.outfile.rsplit('/',1)) + '/01_Sequence_Alignment/'
    # print(path)

    if args.muscle:
        infile = path + 'Alignment_MUSCLE.fasta'
    elif args.mafft:
        infile = path + 'Alignment_MAFFT.fasta'
    else:
        infile = path + 'Alignment_MAFFT.fasta'

    outfile = path + 'trimAl_FASTA.fasta'

    # compose command line

    cmd = ''
    # trimal run mod
    tmode = str(args.tmod)
    if tmode != 'automated1':
        cmd+= '-%s ' % (tmode)
        mode = tmode
    else:
        cmd+= '-automated1 '
        mode = 'automated1'

    # remove spurious sequences (residue overlap/sequence overlap)
    if args.rmss != 'none':
        residue = args.rmss.split('/')[0]
        sequence = args.rmss.split('/')[1]
        cmd += '-resoverlap %s -seqoverlap %s' % (residue,sequence)
        rmss = 'Remove spurious sequences:    Residue overlap threshold: %s    Sequence overlap threshold: %s' % (residue,sequence)
    else:
        rmss = 'Remove spurious sequences: none'

    # print(cmd)

    logging.info('='*20)
    logging.info('trimAl parameters:')
    logging.info('Run mode: %s' % (mode))
    logging.info(rmss)
    logging.info('='*20)
    logging.info('Running trimAl...')


    # run trimAl
    start = time.perf_counter()
    os.system('trimal -in %s -out %s -fasta %s' % (infile,outfile,cmd))
    end = time.perf_counter()
    runtime = end - start
    logging.info('trimAl processing done. Runtime: %s second\n' % (round(runtime,2)))

    path = args.outfile + 'check_point.log'
    with open(path, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('trimal') == -1:
            check_point.write('trimal\n')

# trimAl_standalone()
