import os
import logging
import argparse
from global_var import args
import time

args = args()

global delimiter
delimiter = args.delim
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

#############################################################################

def iqtree_standalone():
    logging.info('Initializing IQ-tree...')

    # define file path
    path = ''.join(args.outfile.rsplit())
    # print(path)
    infile = path + '%s01_Sequence_Alignment%strimAl_FASTA.fasta' % (delimiter,delimiter)
    # outfile = path + '01_Sequence_Alignment/Alignment_MAFFT.fasta'
    prefix = path + '%s02_Tree_File%sIQ-tree' % (delimiter, delimiter)
    outfolder = path + '%s02_Tree_File%s' % (delimiter, delimiter)
    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    # bootstrap
    if int(args.boots)  == 0:
        bootstrap = ''
    else:
        bootstrap = '-bb %s ' % (int(args.boots))

    # SH test
    # if int(args.alrt)  == 0:
    #     sh_test = ''
    #     sh_info = 'Disable'
    # else:
    #     sh_test = '-alrt %s ' % (int(args.alrt))
    #     sh_info = 'Enable'

    # full tree search
    if args.mtree == True:
        mtree = '-mtree '
        mtree_info = 'Enable'
    else:
        mtree = ''
        mtree_info = 'Disable'

    # test mode
    test_mod = str(args.iqmod).upper()

    # additional optimize
    if args.bnni == True:
        bnni = '-bnni '
        bnni_info = 'Enable'
    else:
        bnni = ''
        bnni_info = 'Disable'

    # rcluster
    if args.rcluster == 0:
        rcluster = ''
        rcluster_info = 'Disable'
    else:
        rcluster = '-rcluster %s' % (args.rcluster)
        rcluster_info = str(args.rcluster) + '%'


    logging.info('='*20)
    logging.info('IQ-tree parameters:')
    logging.info('Run mode: %s    Full tree search: %s' % (test_mod, mtree_info))
    logging.info('Bootstrap mode: Ultrafast    Bootstrap number: %s' % (int(args.boots)))
    # logging.info('SH-like test: %s    SH-like test replicates: %s' % (sh_info, int(args.alrt)))
    logging.info('Additional tree optimize: %s    Rcluster percentage: %s' % (bnni_info, rcluster_info))
    logging.info('='*20)
    logging.info('Running IQ-tree...')
    logging.info('This process takes a bit longer time, please wait...')

    # run IQ-tree
    start = time.perf_counter()
    os.system ('iqtree -redo -nt 2 -st AA -m %s -s %s --prefix %s %s%s%s%s' \
    % (test_mod, infile, prefix, bootstrap, mtree, bnni, rcluster))
    end = time.perf_counter()
    runtime = end - start
    logging.info('IQ-tree processing done. Runtime: %s second\n' % (round(runtime,2)))

    check_point = path + '%scheck_point.log' % (delimiter)
    file_check = outfolder + '%sIQ-tree.contree' % (delimiter)
    with open(check_point, mode='a+') as check_point:
        record = ''.join(check_point.readlines())
        if record.find('iqtree') == -1 and os.path.exists(file_check) and os.path.getsize(file_check) >= 1:
            check_point.write('iqtree\n')

# iqtree_standalone()
