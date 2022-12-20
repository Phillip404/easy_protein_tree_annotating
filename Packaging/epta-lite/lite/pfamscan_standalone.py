import os
import sys
import logging
import argparse
from .global_var import args
import time
import json
import pandas as pd

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
def pfam_int():
    global dataframe
    path = args.outfile + 'info_index.tsv'
    dataframe = pd.read_csv(path,sep='\t', index_col='Random ID')

    dataframe['Domain Overview [Pfamscan]'] = ''
    dataframe['Domain Full Record [Pfamscan]'] = ''

def read_pfam_result(result):
    global delimiter
    for domain in result:
        domain = dict(domain)
        # data type check
        if domain['type'] == 'Domain':
            # parse pfamscan result
            acc = domain['acc']
            desc = domain['desc']
            ranID = dict(domain['seq'])['name']
            seq = dict(domain['seq'])['from'] + '...' + dict(domain['seq'])['to']
            evalue = domain['evalue']
            bits = domain['bits']

            # create a brief version store in dataframe for user to view
            brief_tag = '%s; %s; evalue=%s; bits=%s' % (desc, acc, evalue, bits)
            brief_position = seq

            # print(dataframe)
            # print(dataframe.at[ranID,'Domain Overview [Pfamscan]'])
            breif_info = dataframe.at[ranID,'Domain Overview [Pfamscan]']
            full_info = str(dataframe.at[ranID,'Domain Full Record [Pfamscan]'])

            # record domain data in dataframe
            if breif_info == '':
                breif_info = {}
                breif_info[brief_tag] = brief_position
                dataframe.at[ranID,'Domain Overview [Pfamscan]'] = breif_info

                dataframe.at[ranID,'Domain Full Record [Pfamscan]'] = domain

            else:
                breif_info = dict(breif_info)
                breif_info[brief_tag] = brief_position
                dataframe.at[ranID,'Domain Overview [Pfamscan]'] = breif_info

                full_info += ',' + str(domain)
                dataframe.at[ranID,'Domain Full Record [Pfamscan]'] = full_info
                # print(full_info)

def pfam_form():
    global dataframe
    global delimiter

    # dataframe = pd.read_csv('./test/info_index.tsv',sep='\t')
    # create a new dataframe for pfamscan data
    pform = pd.DataFrame(columns=['seq_name','seq_id','alignment_start','alignment_end','envelope_start','envelope_end',\
    'hmm_acc','hmm_name','hmm_desc','type','hmm_start','hmm_end','hmm_length','bit score','E-value','significance',\
    'clan','predicted_active_site_residues'])

    # read rows in info_index and convert it into the new dataframe
    for row in dataframe.iterrows():
        data = row[1]['Domain Full Record [Pfamscan]']
        data = '[%s]' % data
        data = data.replace('\'','\"').replace('None','null')
        dataframe.at[row[0],'Domain Full Record [Pfamscan]'] = data
        data = json.loads(data)


        seq_name = row[1]['Name']
        seq_id = row[1]['ID']

        for domain in data:
            # print(domain)
            domain = dict(domain)


            ranID = dict(domain['seq'])['name']

            record = pd.DataFrame([[seq_name,seq_id]], columns=['seq_name', 'seq_id'], index=[ranID])

            # parse pfamscan result
            record['alignment_start'] = dict(domain['seq'])['from']
            record['alignment_end'] = dict(domain['seq'])['to']
            record['envelope_start']= dict(domain['env'])['from']
            record['envelope_end'] = dict(domain['env'])['to']
            record['hmm_acc'] = domain['acc']
            record['hmm_name'] = domain['name']
            record['hmm_desc'] = domain['desc']
            record['type'] = domain['type']
            record['hmm_start'] = dict(domain['hmm'])['from']
            record['hmm_end'] = dict(domain['hmm'])['to']
            record['hmm_length'] = domain['model_length']
            record['bit score'] = domain['bits']
            record['E-value'] = domain['evalue']
            record['significance'] = domain['sig']
            record['clan'] = domain['clan']
            record['predicted_active_site_residues'] = domain['act_site']
            # print(record)

            pform = pform.append(record)

    # print(pform)
    pform.to_csv(args.outfile + '%s00_Parsed_Fasta%spfamscan_details.tsv',sep='\t') % (delimiter, delimiter)

def run_pfamscan():
    global delimiter
    logging.info('Initializing PfamScan...')

    # define file path
    path = ''.join(args.outfile.rsplit(delimiter,1))
    # print(path)
    infile = path + '%s00_Parsed_Fasta%sParsed_Fasta.fasta' % (delimiter, delimiter)
    # outfile = path + '01_Sequence_Alignment/Alignment_MAFFT.fasta'
    outfile = path + '%s00_Parsed_Fasta%spfamscan_json.json' % (delimiter, delimiter)

    delimiter = args.delim

    abs_dir = args.abspath

    # check local Pfam database
    pdata_path = abs_dir + 'Pfam_data' + delimiter

    # print(pdata_path)
    if not os.path.exists(pdata_path + 'Pfam-A.hmm'):
        logging.info('Downloading Pfam-A.hmm...')
        os.system('wget -P %s ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam31.0/Pfam-A.hmm.gz && gunzip %sPfam-A.hmm.gz && hmmpress %sPfam-A.hmm'\
         % (pdata_path, pdata_path, pdata_path))
        # os.system('wget -P %s ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam31.0/Pfam-A.hmm.gz' % (pdata_path))
        logging.info('Download complete.')

    if not os.path.exists(pdata_path + 'Pfam-A.hmm.dat'):
        logging.info('Downloading Pfam-A.hmm.dat...')
        os.system('wget -P %s ftp://ftp.ebi.ac.uk/pub/databases/Pfam/releases/Pfam31.0/Pfam-A.hmm.dat.gz && gunzip %sPfam-A.hmm.dat.gz'\
         % (pdata_path, pdata_path))
        logging.info('Download complete.')

    # check active site flag
    if args.pas == True:
        active_sites = ' -as'
    else:
        active_sites = ''

    # remove old output file
    if os.path.exists(outfile):
        os.remove(outfile)

    # run pfam
    logging.info('='*20)
    logging.info('PfamScan parameters:')
    logging.info('E-value: %s    Active site: %s' % (args.pev, str(args.pas)))
    logging.info('='*20)
    logging.info('Running PfamScan...')

    start = time.perf_counter()
    os.system('pfam_scan.pl -fasta %s -dir %s -outfile %s -json -e_dom %s -e_seq %s%s > %s'  % (infile, pdata_path, outfile, args.pev, args.pev, active_sites, outfile))
    with open(outfile,'r') as result:
        # read json # require perl-json package
        # print(dir(result))
        # print(result.readlines)
        result = json.load(result)
        # parse json
        read_pfam_result(result)
    end = time.perf_counter()
    runtime = end - start
    logging.info('PfamScan processing done. Runtime: %s second\n' % (round(runtime,2)))


    path = args.outfile + 'check_point.log'
    with open(path, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('pfam_scan') == -1:
            check_point.write('pfam_scan\n')

def pfam_main():
    pfam_int()
    run_pfamscan()
    pfam_form()
