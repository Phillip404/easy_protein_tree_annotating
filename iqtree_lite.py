import os
import requests
import xml.etree.ElementTree as ET
import time
import logging
import argparse
from global_var import args

args = args()

def iqtree_lite():

    logging.info('Initializing IQ-Tree...')

    # define infile
    path = ''.join(args.outfile.rsplit('/',1)) + '/01_Sequence_Alignment/'
    # print(path)

    infile = path + 'trimAl_FASTA.fasta'

    outpath = ''.join(args.outfile.rsplit('/',1)) + '/02_Tree_File/'
    if not os.path.exists(outpath):
        os.mkdir(outpath)

    # SH test
    if int(args.alrt)  == 0:
        sh_info = 'Disable'
    else:
        sh_info = 'Enable'

    # test mode
    test_mod = str(args.iqmod).upper()

    # rcluster
    if args.rcluster == 0:
        rcluster_info = 'Disable'
    else:
        rcluster_info = str(args.rcluster) + '%'


    logging.info('='*20)
    logging.info('IQ-tree parameters:')
    logging.info('Run mode: %s    Rcluster percentage: %s' % (test_mod, rcluster_info))
    logging.info('Bootstrap mode: Ultrafast    Bootstrap number: %s' % (int(args.boots)))
    logging.info('SH-like test: %s    SH-like test replicates: %s' % (sh_info, int(args.alrt)))
    logging.info('='*20)
    logging.info('Running IQ-tree...')
    logging.info('This process takes a bit longer time, please wait...')

    start = time.perf_counter()

    # post job
    headers = {
        'cipres-appkey': 'EPTA-CF81D2F792D849FA89C1427A76E38ED3',
    }

    files = {
        'tool' : (None, 'IQTREE_XSEDE_EXPANSE'),
        'input.infile_' : ('trimAl_FASTA.fasta', open(infile, 'rb')),
        'vparam.abayes_test_' : (None, '0'),
        'vparam.extract_datefile_' : (None, '0'),
        'vparam.fix_branchlengths_' : (None, '0'),
        'vparam.invariable_sites_' : (None, 'estimate'),
        'vparam.lbp_test_' : (None, '0'),
        'vparam.median_approximation_' : (None, '0'),
        'vparam.no_mlpairwise_' : (None, '0'),
        'vparam.optimize_weights_' : (None, '0'),
        'vparam.parametrical_test_' : (None, '0'),
        'vparam.per_sitefile_' : (None, '0'),
        'vparam.per_sitewplfile_' : (None, '0'),
        'vparam.per_sitewslfile_' : (None, '0'),
        'vparam.per_sitewslmfile_' : (None, '0'),
        'vparam.per_sitewslmrfile_' : (None, '0'),
        'vparam.per_sitewslrfile_' : (None, '0'),
        'vparam.per_sitewspmfile_' : (None, '0'),
        'vparam.per_sitewspmrfile_' : (None, '0'),
        'vparam.per_sitewsprfile_' : (None, '0'),
        'vparam.print_sitestats_' : (None, '0'),
        'vparam.runtime_' : (None, '1'),
        'vparam.sequence_type_' : (None, 'AA'),
        'vparam.sh_test_' : (None, '1'),
        'vparam.slower_NNI_' : (None, '0'),
        'vparam.specify_runtype_' : (None, '2'),
        'vparam.specify_safe_' : (None, '0'),
        'vparam.thorough_estimation_' : (None, '0'),
        'vparam.unbiased_test_' : (None, '0'),
        'vparam.use_fasttreesearch_' : (None, '0'),
        'vparam.use_nj_' : (None, '0'),
        'vparam.use_random_' : (None, '0'),
        'vparam.which_iqtree_' : (None, '212'),
        'vparam.write_ancestralseqs_' : (None, '0'),
        'vparam.write_locally_optimal_' : (None, '0'),
        'vparam.write_loglikelihoods_' : (None, '0'),
        'vparam.write_sitelikelihoods_' : (None, '0'),
        'vparam.specify_model_' : (None, '%s' % (test_mod)),
        'vparam.specify_prefix_' : (None, 'IQ-tree'),
    }



    # bootstrap
    if int(args.boots)  != 0:
        files['vparam.bootstrap_type_'] = (None, 'bb')
        files['vparam.num_bootreps_'] = (None, '%s' % (int(args.boots)))

    # SH test
    if int(args.alrt)  != 0:
        files['vparam.num_replicates_'] = (None, '%s' % (str(args.alrt)))

    # rcluster
    if args.rcluster != 0:
        files['vparam.select_rcluster_'] = (None, '-rcluster')
        files['vparam.specify_rclusterval_'] = (None, '%s' % (str(args.rcluster)))




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
            # print('Job finished.')
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
        if str(tag.find('filename').text).startswith('IQ-tree') is True and str(tag.find('filename').text).endswith('.gz') is False:
            filename = tag.find('filename').text
            file_id = tag.find('outputDocumentId').text

            # download result file
            headers = {'cipres-appkey': 'EPTA-CF81D2F792D849FA89C1427A76E38ED3',}

            response = requests.get('https://cipresrest.sdsc.edu/cipresrest/v1/job/z77434/'+job_handle+'/output/'+file_id, headers=headers, auth=('z77434', '123123321z'), stream=True)

            # print (response.content)
            # print('Downloading result file.')

            outfile = open(outpath + filename, 'w')
            outfile.write(response.content.decode('utf8'))

    end = time.perf_counter()
    runtime = end - start
    logging.info('IQ-tree processing done. Runtime: %s second\n' % (round(runtime,2)))

    check_point = path + '/check_point.log'
    file_check = outpath + '/IQ-tree.contree'
    with open(check_point, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('iqtree') == -1 and os.path.exists(file_check) and os.path.getsize(file_check) >= 1:
            check_point.write('iqtree\n')

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

    iqtree_lite()
