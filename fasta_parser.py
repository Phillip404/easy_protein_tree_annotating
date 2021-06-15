import time
import os
import sys
import string
import random
import logging
from datetime import datetime
from Bio import SeqIO
import pandas as pd
import argparse

########## Parsing arguments ###########
desc=''''''
parser=argparse.ArgumentParser(description=desc)
parser.add_argument('-i',metavar='Input_File',help='Input your file here',dest='infile')
parser.add_argument('-o',metavar='Output_File',help='Output file name',dest='outfile')
parser.add_argument('-dh',help='Keep duplicate headers in FASTA file.', action='store_true')
parser.add_argument('-fl',metavar='Filter_length', help='How long you want to filter sequences?',dest='filter_length', required=False)
parser.add_argument('-tax',help='Search for taxonomy information for each sequence.', action='store_true')
parser.add_argument('-dbn',help='Search for identification information (protein name and organism) for each sequence.', action='store_true')
parser.add_argument('-dbd',help='Search for domain information for each sequence in Entrenz database (no evalue and bit score).', action='store_true')
parser.add_argument('-pfs',help='Run Pfamsacn (domain prediction) for each sequence.', action='store_true')
args=parser.parse_args()
########################################

# function gives unique 16-bit string
def generate_random_str(randomlength,randID_dic):

    while True:
        # string.digits = 0123456789
        # string.ascii_letters = 26 lowercases and 26 uppercases
        str_list = random.sample(string.digits + string.ascii_letters,randomlength)
        random_str = ''.join(str_list)

        # make sure random ID is unique
        dic_length = len(randID_dic)
        randID_dic[random_str] = ''

        if len(randID_dic) == dic_length + 1:
            return (random_str)
            break

# check the input file
def infile_process():
    if args.infile:
            if os.path.isdir(args.infile):
                logging.info ('Input folder detected')
                load_infolder()
            elif os.path.isfile(args.infile):
                logging.info ('Input file detected')
                load_infile(args.infile)
            else:
                logging.error ('-'*20 + 'Error: input file do not exist!' + '-'*20)
                exit()
    else:
        logging.error ('-'*20 + 'Error: Please enter the input file or folder!' + '-'*20)
        exit()

# check output directory
def outfile_check():
    # create a new folder if output directory does not exist
    if not os.path.exists(args.outfile.rstrip()):
        os.makedirs(args.outfile.rstrip())
    else:
        # Let user decide whether they want to continue
        while True:
            # if continue, delete all file with open('a') property
            check = input('Output directory is existed, do you want to continue? (Y/N) : ')
            if check == 'Y':
                # record input action in log
                logging.debug ('Output directory is existed, do you want to continue? (Y/N) : Y')

                # specify path of parsed fasta file
                path = args.outfile.rstrip() + './00_Parsed_Fasta/Parsed_Fasta.fasta'
                # if the file exist, delete it so that a new empty one will be create later
                # I do that because I used open(,'w+') in gz reader, it requires a empty file to write in
                if os.path.exists(path):
                    os.remove(path)
                break
            # if they dont, quit
            elif check == 'N':
                print('Quiting',end = '')
                for i in range(3):
                    print('.',end = '',flush = True)
                    time.sleep(0.05)
                exit()

def load_infile(filename):
    global dataframe
    logging.info ('='*40)
    if len(filename.split('.')) >= 2 and filename.split('.')[-2] + filename.split('.')[-1] == 'targz':
        logging.info ('input file name: %s' % (os.path.basename(filename)))
        logging.info ('input file format: tar.gz')
        logging.info ('Extracting and processing tar.gz file...')
        # express file
        read_targz(filename)
        logging.info ('\nDone.')
    elif len(filename.split('.')) >= 1 and filename.split('.')[-1] == 'gz':
        logging.info ('input file name: %s' % (os.path.basename(filename)))
        logging.info ('input file format: gunzip')
        logging.info ('Extracting and processing gunzip file...')
        # read gunzip file
        read_gz(filename)
        logging.info ('\nDone.')
    else:
        logging.info ('Input file name: %s' % (os.path.basename(filename)))
        logging.info ('Input file format: FASTA / plain text')
        logging.info ('Loading FASTA file...')
        # read and record data in dataframe from input file/files
        read_fasta(filename)
        logging.info ('\nDone.')

def load_infolder():
    # get path of input folder
    path = os.path.abspath(args.infile)
    # get file list
    files= os.listdir(args.infile)
    # logging.info ('='*20)
    for file in files:
        # check file
        if os.path.isfile(path + '\\' + file):
            # read file in input folder
            load_infile(path + '\\' + file)

# function reads gunzip file
def read_gz(gzfile):
    import gzip
    # express file
    with gzip.open(gzfile, 'rt') as gf:
        # create temp file to store data against header
        with open('temp','w+') as of:
            for line in gf:
                if line != '':
                    line = line.rstrip()
                    # find headers
                    if line.startswith('>'):
                        # Point to the beginning of the file
                        of.seek(0)
                        # read sequences data
                        dataframe = read_fasta(of)
                        # Point to the beginning of the file again
                        of.seek(0)
                        # Erase everying to store next header and sequences
                        of.truncate()
                    print(line,file=of)
            # read sequences data once more at the end of the file
            of.seek(0)
            dataframe = read_fasta(of)
            of.seek(0)
            of.truncate()
            of.close()
            os.remove('temp')

def read_targz(targzfile):
    import tarfile

    with tarfile.open(targzfile, 'r:gz') as tf:
        # create temp file to store data against header
        with open('temp','w+') as of:
            # extract archive by file
            for member in tf.getmembers():
                f = tf.extractfile(member)
                if f is not None:
                    for line in f:
                        # convert binary data in archive to string
                        line = str(line.rstrip())[2:-2]
                        if line != '':
                            # find headers
                            if line.startswith('>'):
                                # Point to the beginning of the file
                                of.seek(0)
                                # read sequences data
                                dataframe = read_fasta(of)
                                # Point to the beginning of the file again
                                of.seek(0)
                                # Erase everying to store next header and sequences
                                of.truncate()
                        # print(line)
                        print(line,file=of)
            # read sequences data once more at the end of the file
            of.seek(0)
            dataframe = read_fasta(of)
            of.seek(0)
            of.truncate()
            of.close()
            os.remove('temp')

# function reads data from a fasta file
def read_fasta(fasta):
    global dataframe

    # create output folder and file
    outpath = args.outfile.rstrip() + '/00_Parsed_Fasta/'
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    outfasta = open(outpath + 'Parsed_Fasta.fasta','a')

    # count sequences in fasta file, using in progress bar
    sequence_count = 0
    for seq_record in SeqIO.parse(fasta,'fasta'):
        sequence_count += 1

    currently_done = 0

    progress_detail = {'In_Database':0}
    if args.tax: progress_detail['Taxon'] = 0
    if args.dbn: progress_detail['Name'] = 0
    if args.dbd: progress_detail['Domain'] = 0

    # read sequences
    for seq_record in SeqIO.parse(fasta,'fasta'):

        header = str(seq_record.description)

        # duplicate headers check
        if not args.dh:
            for headers in dataframe['Header']:
                if header in headers:
                    continue

        # skip local sequences
        if header.startswith('lcl|'):
            continue

        # give a unique random ID to every sequence
        ranID = generate_random_str(16,randID_dic)
        # information from sequence header in the order of :
        # header, ID, name, taxon, {domain_db}
        sequence_attrb = read_header(seq_record, ranID)

        # quick_search = threading.Thread(targe)

        ID = sequence_attrb[0]
        name = sequence_attrb[1]
        taxon = sequence_attrb[2]
        domain_db = sequence_attrb[3]

        # output data
        # add sequence information to dataframe and parsed fasta file
        record_info = pd.DataFrame([[header,ID,name]], columns=['Header', 'ID', 'Name'], index=[ranID])
        if args.tax:
            record_info['Organism Lineage'] = [taxon]
        if args.dbd:
            record_info['Domain Information'] = [domain_db]

        dataframe = dataframe.append(record_info)

        # output sequences with random IDs to 'Parsed_Fasta.fasta'.
        print('>%s\n%s' % (ranID,seq_record.seq), file=outfasta)


        # record progress of database search
        if args.tax or args.dbn or args.dbd:
            currently_done += 1

            if taxon or domain_db: progress_detail['In_Database'] += 1

            if taxon: progress_detail['Taxon'] += 1

            if name != 'Description In Database Not Found': progress_detail['Name'] += 1

            if domain_db: progress_detail['Domain'] += 1

            progress_bar(sequence_count,currently_done,progress_detail)

    if args.tax or args.dbn or args.dbd:
        sys.stderr.write('\n')
        logging.debug('Searching in database...')

        logging.info('Database Search Done.\n%s in %s proteins founded in Database.' % (progress_detail['In_Database'],sequence_count))
        if args.tax: logging.info('%s of them have organism lineage.' % (progress_detail['Taxon']))
        if args.dbn: logging.info('%s of them have name or description.' % (progress_detail['Name']))
        if args.dbd: logging.info('%s of them have domain information.' % (progress_detail['Domain']))

    # read and parse local sequences
    logging.info('\nChecking local sequence...')
    local_seq_count, local_seq_tax = 0, 0
    for seq_record in SeqIO.parse(fasta,'fasta'):
        header = str(seq_record.description)
        if str(seq_record.description).startswith('lcl|'):
            local_seq_count += 1
            ranID = generate_random_str(16,randID_dic)
            sequence = seq_record.seq
            ID = ''.join( [x for x in header.split('|') if x.find('[ID]') != -1]).replace('[ID]','').lstrip()
            name = ''.join( [x for x in header.split('|') if x.find('[NAME]') != -1]).replace('[NAME]','').lstrip()

            record_info = pd.DataFrame([[header,ID,name]], columns=['Header', 'ID', 'Name'], index=[ranID])

            if args.tax:
                try:
                    taxon = ''.join( [x for x in header.split('|') if x.find('[TAXON]') != -1]).replace('[TAXON]','').lstrip()
                    record_info['Organism Lineage'] = [taxon]
                    local_seq_tax += 1
                except:
                    pass

            dataframe = dataframe.append(record_info)
            print('>%s\n%s' % (ranID,seq_record.seq), file=outfasta)

    logging.info('Local Sequence Check Done.')
    if local_seq_count > 0:
        logging.info('%s local sequences have been found.' % (local_seq_count))
        if args.tax: logging.info('%s of them have orgism lineage.' % (local_seq_tax))


    return(dataframe)

# retrive information from FASTA headers and search in databases if correspond flags inputed
def read_header(record, ranID):
    taxon, domain_db = False, False

    ID = str(record.id)
    name = str(record.name)

    # add taxonomy information if asked
    if (args.tax and ID) or args.dbn or args.dbd:
        # return search result in entrez in the order of [organism_lineage, protein_name, domain_dict]
        entrez_result = entrez_search(ID)

        # get organism lineage
        if args.tax:
            taxon = entrez_result[0]

        # if function returns a name of protein, take it as the new name in dataFrame
        if args.dbn and entrez_result[1]:
            name = entrez_result[1]
        else:
            name = 'Description In Database Not Found'

        # get a dict with element formation of 'domain_name' = 'location'
        if args.dbd:
            domain_db = entrez_result[2]

    return(ID, name, taxon, domain_db)

# retrive organism lineage using Etrenz
def entrez_search(accID):
    from Bio import Entrez

    # annouce I'm using entrens module in a tool
    Entrez.tool = 'MyLocalScript'
    # visit Entrez with API key to boost quiry sbumit
    Entrez.api_key = '9fd2a1797ace2bfec0aae67bda7f4a530009'
    # Always tell NCBI who you are
    Entrez.email = 'xu2742zh-s@student.lu.se'

    organism_lineage = False
    protein_name = False
    domain_dict = False

    # try find target in protein database
    try:
        # search database ID of target accession number
        handle = Entrez.esearch(db='protein',term=accID, retmode='xml')
        # print(accID)
        record = Entrez.read(handle)
        record = record['IdList'][0]
        # retrive protein info from database and find organism info
        handle = Entrez.efetch(db='protein',id=record , retmode='xml')
        record = Entrez.read(handle)

        if args.tax or args.dbn:
            protein_name = record[0]["GBSeq_definition"]
            record_b = record[0]["GBSeq_organism"]
            # print(record)

            # search database ID of target organism
            handle = Entrez.esearch(db='Taxonomy',term=record_b)
            record_b = Entrez.read(handle)
            # print(record_b)
            # print(record_b['IdList'])
            record_b = record_b['IdList'][0]
            # print(record)
            # retrive taxonomy lineage from database
            handle = Entrez.efetch(db='Taxonomy', id=record_b, retmode='xml')
            organism_lineage = Entrez.read(handle)[0]['Lineage']


        if args.dbd:
            # dict to store domain name and location info
            domain_dict = {}
            # retrive feature table of target protein
            record_a = record[0]['GBSeq_feature-table']
            for features in record_a:
                # found all domains marked as 'Region'
                if features['GBFeature_key'] == 'Region':
                    # retrive start and end information
                    location = features['GBFeature_location']
                    for tags in features['GBFeature_quals']:
                        if tags['GBQualifier_name'] == 'note':
                            # retrive domain name and ID
                            name = tags['GBQualifier_value']

                            # add new record to the dict
                            domain_dict[name] = location

                            # mark this domain to do domain count
                            domain = marked_domain(name)
                            if domain in domain_count:
                                domain_count[domain_count.index(domain)].domain_counts += 1
                            else:
                                domain_count.append(domain)
                    # print (domain_dict)


    except:
        # code of these two flag are binded
        if args.tax or args.dbn:
            # try find target in identical protein group (IPG) database
            try:
                # search database ID of target accession number
                handle = Entrez.esearch(db='ipg',term=accID, retmode='xml')
                # print(accID)
                record = Entrez.read(handle)
                record = record['IdList'][0]
                # retrive protein info from database and find organism info
                handle = Entrez.efetch(db='ipg', rettype='ipg', id=record, retmode='xml')
                record = Entrez.read(handle)
                record = dict(dict(record)['IPGReport'])['Product']

                protein_name = record.attributes['name']
                record = record.attributes['taxid']

                # retrive taxonomy lineage from database
                handle = Entrez.efetch(db='Taxonomy', id=record, retmode='xml')
                organism_lineage = Entrez.read(handle)[0]['Lineage']
                protein_name += ' [%s]' % organism_lineage.split(';')[-1].lstrip()
            except:
                pass

    # If there are structure information in database but no domain information there, treat it as not found.
    if not domain_dict or len(domain_dict)<1:
        domain_dict = False


    return(organism_lineage, protein_name, domain_dict)

## domain related coding
# represent each domain as a class instance, using in domain number count
class marked_domain:

    domain_counts = 1

    def __init__(self, name):
        self.name = name.split(';')[0]
        self.id = name.split(';')[1].lstrip()

    def __eq__(self, other):
        return self.name == other.name and \
               self.id == other.id

    def __hash__(self):
        return hash((self.name, self.id))


    def __repr__(self):
        rep = 'domain: %s id: %s' % (self.name, self.id)
        return rep

def progress_bar(total, current, detail, width=60, symbol='▮'):
    assert len(symbol) == 1

    each_pct = total/width

    pct = current/total

    bar_length = int(pct * width)

    bar = '|%s%s|' % (symbol*bar_length, ' '*(width-bar_length))

    general = '%s/%s' % (current, total)

    info = ''
    for arguments in detail:
        info += '%s: %s ' % (arguments.lstrip().replace('_',' '), detail[arguments])

    full_bar = (bar + ' ' + general + ' ' + info).lstrip()
    sys.stderr.write(full_bar + '\r')
    sys.stderr.flush()

def fasta_parser():
    global dataframe
    global randID_dic
    # build a empty dataframe to save data
    dataframe = pd.DataFrame(columns=['Header', 'ID', 'Name'])
    if args.tax:
        taxonomy = []
        dataframe["Organism Lineage"] = taxonomy
    if args.dbd:
        # a list record all domains and count how many times they appeared
        domain_count = []

        domains = []
        dataframe["Domain Overview [NCBI]"] = domains

    if args.pfs:
        # a list record all domains and count how many times they appeared
        domain_count = []

        domains = []
        domains_detail = []
        dataframe["Domain Overview [Pfamsacn]"] = domains
        dataframe["Domain Full Record [Pfamsacn]"] = domains_detail

    # build a empty dictionary to save random ID
    randID_dic = {}

    # output directory check
    outfile_check()

    # check and process input files
    infile_process()
    logging.info ('='*40)
    logging.info ('All FASTA files parsed.')
    dataframe.index.name = 'Random ID'

    # output dataframe
    index_path = args.outfile + '\\info_index.tsv'
    dataframe.to_csv(path_or_buf=index_path,sep='\t')
