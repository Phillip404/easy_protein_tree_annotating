import logging
import urllib.request
import urllib.parse
import time
import json
import argparse
import pandas as pd
from global_var import *

from configparser import ConfigParser

args = args()

def pfam_int():
    global dataframe
    path = args.outfile + '\\info_index.tsv'
    dataframe = pd.read_csv(path,sep='\t', index_col='Random ID')

    dataframe['Domain Overview [Pfamscan]'] = ''
    dataframe['Domain Full Record [Pfamscan]'] = ''


def pfam_arrange():
    # define how many jobs will be submitted
    if len(dataframe) < 250:
        batch_number = int(len(dataframe)//10) + 1
    elif len(dataframe) > 3000:
        logging.info ('Your data volume has exceeded the limit of Pfamscan web service.')
        logging.info ('We highly recommand you to use our stand-alone verison tool')
        exit()
    else:
        batch_number = 25

    # assign sequence in each job equally
    batch_list = []
    seq_each_sub = len(dataframe) // batch_number

    # assign sequence number to batch_list
    for j in range(0, batch_number):
        batch_list.append(seq_each_sub)
    remainder = len(dataframe) - sum(batch_list)

    # assign remained sequence in each job equally
    if remainder != 0:
        for i in range(0,remainder):
            batch_list[i] += 1
    return batch_list



def pfam_post(seq, email=args.email, database=None, evalue=args.pfev, asp=args.pfas, format='json'):
    global job_list
    global args

    params = {'sequence':seq, 'email':email, 'evalue':evalue, 'asp':asp, 'format':format}
    # print(params)

    try:
        # submit job
        # encode parameters into ascII
        data = urllib.parse.urlencode(params)
        # print(data)
        data = data.encode('ascii')

        url = 'https://www.ebi.ac.uk/Tools/services/rest/pfamscan/run'

        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        # read returned job ID
        job_id = response.read().decode('utf-8')
        job_list.append(job_id)
        # print('job id: ' + job_id)
        # print('post')

    except:
        logging.info ('Error: Failed to submit job to Pfamscan sequence search.')
        if len(seq.split('\n')) < 2:
            logging.info ('Error: Please check ./00_Parsed_Fasta/Parsed_Fasta.fasta file under output path.')
        else:
            logging.info ('Error: Unknow reason. Probably because of a bad connection to Pfamscan web service.')
        exit()

    # wait for Pfamscan running
    time.sleep(10)


def pfam_get(job_list):
    # get job status and return result if job finished
    while True:
        for job_id in job_list:

            # get job status
            url = 'https://www.ebi.ac.uk/Tools/services/rest/pfamscan/status/' + job_id

            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req)
            status = response.read().decode('utf-8')
            # print('status: ' + status)
            # wait for job fnish
            if not status == 'FINISHED':
                if len(job_list) <= 2:
                    time.sleep(1)
                elif len(job_list) <= 10:
                    time.sleep(2)
                else:
                    time.sleep(3)

            # get result when job finished
            elif status == 'FINISHED':
                url = 'https://www.ebi.ac.uk/Tools/services/rest/pfamscan/result/' + job_id + '/out'
                req = urllib.request.Request(url)
                response = urllib.request.urlopen(req)
                result = response.read().decode('utf-8')
                # print(result)
                result = json.loads(result)
                read_pfam_result(result)
                job_list.remove(job_id)
                # print(job_list)

        if len(job_list) == 0:
            break

def read_pfam_result(result):
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

            print(dataframe)
            print(dataframe.at[ranID,'Domain Overview [Pfamscan]'])
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
    pform.to_csv(args.outfile + '\\00_Parsed_Fasta\pfamscan_details.tsv',sep='\t')

def pfam_submit(batch_list):
    global dataframe
    # print('submit')

    path = args.outfile + '\\00_Parsed_Fasta\\Parsed_Fasta.fasta'
    sequences = open(path,'r')
    # linecache.getline(sequences,2)
    sequences = sequences.readlines()

    # submit jobs according to sequences number in job_list
    i = 0
    for number in batch_list:
        start = i
        i += number*2
        end = i
        # print(start,end)
        seq = ''.join(sequences[start:end])
        pfam_post(seq)

    del sequences


def pfam_main():
    global dataframe
    pfam_int()

    batch_list = pfam_arrange()
    # print(batch_list)
    global job_list
    job_list = []

    pfam_submit(batch_list)

    pfam_get(job_list)

    # cfg = ConfigParser()
    # cfg.read('config.ini')
    # cfg['FASTA parser']['pfam_job_list'] = str(job_list)

    pfam_form()
    path = args.outfile + '\\info_index.tsv'
    dataframe.to_csv(path,sep='\t')

def pfam_retry():
    job_list = ['pfamscan-R20210702-120931-0879-85148997-p2m']
    pfam_get(job_list)

    # cfg = ConfigParser()
    # cfg.read('config.ini')
    # cfg['FASTA parser']['pfam_job_list'] = str(job_list)

    pfam_form()
    path = args.outfile + '\\info_index.tsv'
    dataframe.to_csv(path,sep='\t')
