import os
import requests
import xml.etree.ElementTree as ET
import time
import logging
import argparse
from global_var import args

args = args()

def trimal_lite():

    logging.info('Initializing trimAl...')

    # define infile
    path = ''.join(args.outfile.rsplit('/',1)) + '/01_Sequence_Alignment/'
    # print(path)

    if args.muscle:
        filename = 'Alignment_MUSCLE.fasta'
        infile = path + 'Alignment_MUSCLE.fasta'
    elif args.mafft:
        filename = 'Alignment_MAFFT.fasta'
        infile = path + 'Alignment_MAFFT.fasta'
    else:
        infile = path + 'Alignment_MAFFT.fasta'

    outfile = path + 'trimAl_FASTA.fasta'


    # trimal run mod
    tmode = str(args.tmod)
    if tmode != 'automated1':
        mode = tmode
    else:
        mode = 'automated1'

    # remove spurious sequences (residue overlap/sequence overlap)
    if args.rmss != 'none':
        residue = args.rmss.split('/')[0]
        sequence = args.rmss.split('/')[1]
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

    # post job
    headers = {
        'cipres-appkey': 'EPTA-CF81D2F792D849FA89C1427A76E38ED3',
    }

    files = {
        'tool' : (None,'TRIMAL_XSEDE'),
        'input.infile_' : (filename, open(infile, 'rb')),
        'vparam.out_htmlfilename_' : (None, '0'),
        'vparam.print_scc_' : (None, '0'),
        'vparam.print_sct_' : (None, '0'),
        'vparam.print_sgc_' : (None, '0'),
        'vparam.print_sgt_' : (None, '0'),
        'vparam.print_sident_' : (None, '0'),
        'vparam.runtime_' : (None, '0.5'),
        'vparam.select_colnumbering_' : (None, '0'),
        'vparam.select_complementary_' : (None, '0'),
        'vparam.select_numcores_' : (None, '1'),
        'vparam.specify_automated1_' : (None, '0'),
        'vparam.specify_gappyout_' : (None, '0'),
        'vparam.specify_noallgaps_' : (None, '0'),
        'vparam.specify_nogaps_' : (None, '0'),
        'vparam.specify_resoverlap_' : (None, '0'),
        'vparam.specify_seqoverlap_' : (None, '0'),
        'vparam.specify_strict_' : (None, '0'),
        'vparam.specify_strictplus_' : (None, '0'),
    }


    # run mode
    if tmode == 'gappyout':
        files['vparam.specify_automated1_'] = (None, '1')
    elif tmode == 'strict':
        files['vparam.specify_strict_'] = (None, '1')
    elif tmode == 'strictplus':
        files['vparam.specify_strictplus_'] = (None, '1')
    else:
        files['vparam.specify_automated1_'] = (None, '1')

    if args.rmss != 'none':
        files['vparam.specify_resoverlap_'] = (None, str(residue))
        files['vparam.specify_seqoverlap_'] = (None, str(sequence))





    response = requests.post('https://cipresrest.sdsc.edu/cipresrest/v1/job/z77434', headers=headers, files=files, auth=('z77434', '123123321z'))
    # print (response.text)

    # parse XML file to find job handle
    root = ET.XML(response.text)
    for tag in root.iter('jobHandle'):
        job_handle = tag.text
        # print('Job successfully submitted.')
        # print('Job is running.')

    # check job status
    # job status prompt staetment
    job_stat = 'QUEUE'
    while True:
        # job status prompt staetment
        memory = job_stat

        time.sleep(10)
        headers = {'cipres-appkey': 'EPTA-CF81D2F792D849FA89C1427A76E38ED3',}

        response = requests.get('https://cipresrest.sdsc.edu/cipresrest/v1/job/z77434/'+job_handle, headers=headers, auth=('z77434', '123123321z'))

        # print (response.text)

        root = ET.XML(response.text)
        for tag in root.iter('jobStage'):
            job_stat = tag.text
            if job_stat == 'COMPLETED':
                stop = True
            else:
                if memory != job_stat:
                    print('Job status: '+job_stat)
                    stop = False
        if stop == True:
            print('Job status: '+job_stat)
            break

    # fetch result file list
    headers = {
        'cipres-appkey': 'EPTA-CF81D2F792D849FA89C1427A76E38ED3',
    }

    response = requests.get('https://cipresrest.sdsc.edu/cipresrest/v1/job/z77434/'+job_handle+'/output', headers=headers, auth=('z77434', '123123321z'))

    # print (response.text)
    # test_file = open('urltest.txt','w')
    # print (response.text,file=test_file)

    # rind result file id
    root = ET.XML(response.text)
    for tag in root.iter('jobfile'):
        # print(str(tag.find('filename').text))
        if tag.find('filename').text == 'STDOUT':
            filename = tag.find('filename').text
            file_id = tag.find('outputDocumentId').text

            # download result file
            headers = {'cipres-appkey': 'EPTA-CF81D2F792D849FA89C1427A76E38ED3',}

            response = requests.get('https://cipresrest.sdsc.edu/cipresrest/v1/job/z77434/'+job_handle+'/output/'+file_id, headers=headers, auth=('z77434', '123123321z'), stream=True)

            # print (response.content)
            # print('Downloading result file.')

            outfile = open(outfile, 'w')
            outfile.write(response.content.decode('utf8'))

    end = time.perf_counter()
    runtime = end - start
    logging.info('trimAl processing done. Runtime: %s second\n' % (round(runtime,2)))

    path = args.outfile + 'check_point.log'
    with open(path, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('trimal') == -1:
            check_point.write('trimal\n')

# test
if __name__ == '__main__':
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

    trimal_lite()
