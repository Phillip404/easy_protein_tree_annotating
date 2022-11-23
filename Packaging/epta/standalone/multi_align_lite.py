import os
import time
import logging
import argparse
from .global_var import args

import urllib.request
import urllib.parse
import json
import pandas as pd

# args = args()
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

global args
args = args()

global delimiter
delimiter = args.delim

def mafft():
    logging.info('Initializing MAFFT...')

    if args.infile.endswith('.fasta') or args.infile.endswith('.FASTA'):
        args.infile = delimiter.join(args.infile.rstrip(delimiter).split(delimiter)[:-1])

    in_file = args.outfile + '%s00_Parsed_Fasta%sParsed_Fasta.fasta' % (delimiter, delimiter)
    out_path = args.outfile + '%s01_Sequence_Alignment%s' % (delimiter, delimiter)
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    seq = open(in_file).read()

    # matrix: bl 30 45 62 80, jtt 100 200
    # nbtree: 0 1 2 5 10 20 50 80 100
    email = str(args.email)
    matrix = str(args.matrix)
    op = str(float(args.op))
    ep = str(float(args.ep))
    retree = str(int(args.retree))
    maxiter = str(int(args.maxiterate))
    ffts = str(args.ffts)

    params = {'sequence':seq, 'email':email, 'stype':'protein', 'format':'fasta', 'matrix':matrix,
    'gapopen':op, 'gapext':ep, 'order':'aligned', 'nbtree':retree, 'treeout':'true', 'maxiterate':maxiter,
    'ffts':ffts}

    logging.info('='*20)
    logging.info('MAFFT parameters:')
    logging.info('Gap open penalty: %s    Gap extension penalty: %s' % (op, ep))
    logging.info('Tree rebuilding number: %s    Max iterate: %s' % (retree, maxiter))
    logging.info('Matrix: %s    FFTS mode: %s' % (matrix, ffts))
    logging.info('='*20)
    logging.info('Running MAFFT...')

    # submit job
    start = time.perf_counter()
    # encode parameters into ascII
    data = urllib.parse.urlencode(params)
    data = data.encode('ascii')

    url = 'https://www.ebi.ac.uk/Tools/services/rest/mafft/run'

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    # read returned job ID
    job_id = response.read().decode('utf-8')
    # print(job_id)

    time.sleep(10)

    while True:
        url = 'https://www.ebi.ac.uk/Tools/services/rest/mafft/status/' + job_id

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        status = response.read().decode('utf-8')
        # print('status: ' + status)
        # wait for job fnish
        if status == 'RUNNING':
                time.sleep(3)

        # get result when job finished
        elif status == 'FINISHED':
            url = 'https://www.ebi.ac.uk/Tools/services/rest/mafft/result/' + job_id + '/out'
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            logging.info ('MAFFT processing done.')
            # print(result)
            break

        elif status == 'ERROR':
            logging.info ('ERROR: an error occurred attempting to get the job status from EMBL-EBI web service.')
            exit()
        elif status == 'FAILURE':
            logging.info ('ERROR: EMBL-EBI web service - the job failed.')
            exit()
        else:
            logging.info ('ERROR: an unknow faliure has occurred.')
            exit()

    out_file = open(out_path+'Alignment_MAFFT.fasta','w')
    print(result,file=out_file)

    end = time.perf_counter()
    runtime = end - start
    logging.info('MAFFT processing done. Runtime: %s second\n' % (round(runtime,2)))

    path = args.outfile + 'check_point.log'
    with open(path, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('multiple_alignment') == -1:
            check_point.write('multiple_alignment\n')

def muscle():
    logging.info('Initializing Muscle...')

    if args.infile.endswith('.fasta') or args.infile.endswith('.FASTA'):
        args.infile = delimiter.join(args.infile.rstrip(delimiter).split(delimiter)[:-1])

    in_file = args.outfile + '%s00_Parsed_Fasta%sParsed_Fasta.fasta' % (delimiter, delimiter)
    out_path = args.outfile + '%s01_Sequence_Alignment%s' % (delimiter, delimiter)

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    seq = open(in_file).read()
    email = args.email

    params = {'sequence':seq, 'email':email, 'format':'fasta', 'tree':'none'}

    logging.info('='*20)
    logging.info('Muscle parameters:')
    logging.info('Default')
    logging.info('='*20)
    logging.info('Running Muscle...')

    # submit job
    start = time.perf_counter()
    # encode parameters into ascII
    data = urllib.parse.urlencode(params)
    data = data.encode('ascii')

    url = 'https://www.ebi.ac.uk/Tools/services/rest/muscle/run'

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    # read returned job ID
    job_id = response.read().decode('utf-8')

    time.sleep(10)

    while True:
        url = 'https://www.ebi.ac.uk/Tools/services/rest/muscle/status/' + job_id

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        status = response.read().decode('utf-8')
        print('Job status: '+status)
        # wait for job fnish
        if status == 'RUNNING':
                time.sleep(3)

        # get result when job finished
        elif status == 'FINISHED':
            url = 'https://www.ebi.ac.uk/Tools/services/rest/muscle/result/' + job_id + '/aln-fasta'
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            # print(result)
            logging.info ('MUSCLE processing done.')
            break
            # print(result)
        elif status == 'ERROR':
            logging.info ('ERROR: an error occurred attempting to get the job status from EMBL-EBI web service.')
            exit()
        elif status == 'FAILURE':
            logging.info ('ERROR: EMBL-EBI web service - the job failed.')
            exit()
        else:
            logging.info ('ERROR: an unknow faliure has occurred.')
            exit()

    out_file = open(out_path+'Alignment_MUSCLE.fasta','w')
    print(result,file=out_file)

    end = time.perf_counter()
    runtime = end - start
    logging.info('Muscle processing done. Runtime: %s second\n' % (round(runtime,2)))

    path = args.outfile + 'check_point.log'
    with open(path, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('multiple_alignment') == -1:
            check_point.write('multiple_alignment\n')

def muilt_align():
    if args.muscle :
        muscle()
    elif args.mafft:
        mafft()


# muilt_align()
