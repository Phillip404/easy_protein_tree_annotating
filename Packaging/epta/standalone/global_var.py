import argparse
import os
import sys
from configparser import ConfigParser

def args():

    ########## Parsing arguments ###########
    desc=''''''
    parser=argparse.ArgumentParser(description=desc)
    parser.add_argument('-lite',help='Run Lite mode.',action='store_true')
    parser.add_argument('-standalone',help='Run standalone mode.',action='store_true')
    if not '-test' in sys.argv:
        parser.add_argument('-i',metavar='Input_File',help='Input your file here',dest='infile',required=True)
        parser.add_argument('-o',metavar='Output_File',help='Output file name',dest='outfile',required=True)
    else:
        parser.add_argument('-i',metavar='Input_File',help='Input your file here',dest='infile')
        parser.add_argument('-o',metavar='Output_File',help='Output file name',dest='outfile')
    parser.add_argument('-dh',help='Keep duplicate headers in FASTA file.',action='store_true')
    parser.add_argument('-tax',help='Search for taxonomy information for each sequence.',action='store_true')
    parser.add_argument('-name',help='Search for protein name for each sequence.',action='store_true')
    # parser.add_argument('-dom',help='Search for domain information for each sequence in Entrenz database (no evalue and bit score).', action='store_true')
    parser.add_argument('-pfam',help='Run Pfamsacn (domain prediction) for each sequence.',action='store_true')
    parser.add_argument('-pev',metavar='PfamScan E-value',help='Spicify a e-value of Pfamscan search.',type=str)
    parser.add_argument('-pas',help='Enable active sites prediction in Pfamscan.',action='store_true')
    parser.add_argument('-em',metavar='Email address',help='Email address that you want receive potential information from web tools.',dest='email')
    parser.add_argument('-muscle',help='Run MUSCLE (multiple alignment).',action='store_true')
    parser.add_argument('-mafft',help='Run MAFFT (multiple alignment).',action='store_true')
    parser.add_argument('-matrix',metavar='MAFFT matrix type',help='Spicify a matrix type of MAFFT alignment.',type=str)
    parser.add_argument('-op',metavar='MAFFT opening score',help='Spicify a gap oppening penalty of MAFFT alignment.',type=float)
    parser.add_argument('-ep',metavar='MAFFT extension score',help='Spicify a gap extension penalty of MAFFT alignment.',type=float)
    parser.add_argument('-retree',metavar='MAFFT tree rebuilding number',help='Tree rebuilding number of MAFFT.',type=int)
    parser.add_argument('-maxiterate',metavar='MAFFT max iterate number',help='Max iterate number of MAFFT.',type=int)
    parser.add_argument('-ffts',metavar='MAFFT fast fourier transform algorithm',help='Mode of fast fourier transform.',type=str)
    parser.add_argument('-trimal',help='Run trimAl (multiple alignment trim).',action='store_true')
    parser.add_argument('-tmod',metavar='trimAl run mode',help='Run mode of trimAl.',type=str)
    parser.add_argument('-rmss',metavar='trimAl Residue overlap/Sequence overlap',help='Remove spurious sequences (residue overlap/sequence overlap). Overlap score between 0 to 1.',type=str)
    parser.add_argument('-iqtree',help='Run IQ-tree (tree building).',action='store_true')
    parser.add_argument('-iqmod',metavar='IQ-tree test mod',help='Test mod of IQ-tree.')
    # parser.add_argument('-alrt',metavar='IQ-tree SH-like test replicates (>=1000)',help='Number of replicates (>=1000) to perform SH-like approximate likelihood ratio test.',type=int)
    parser.add_argument('-boots',metavar='IQ-tree Bootstrap number',help='Bootstrap number of IQtree (must >= 1000).',type=int)
    parser.add_argument('-rcluster',metavar='Rcluster percentage',help='Rcluster percentage(0 to 100).',type=int)
    parser.add_argument('-mtree',help='Turn on full tree search for model testing of IQ-tree.',action='store_true')
    parser.add_argument('-bnni',help='Turn on additional optimize of IQ-tree.',action='store_true')
    parser.add_argument('-xzoom',metavar='Branch length scale',help='Value of X zoom(default=1, decimal possible).',type=float)
    parser.add_argument('-yzoom',metavar='Branch vertical margin',help='Value of Y zoom(default=1, decimal possible).',type=float)
    parser.add_argument('-bs',help='Show branch support in tree drawing.',action='store_true')
    parser.add_argument('-bl',help='Show branch length in tree drawing.',action='store_true')
    parser.add_argument('-bif',help='Show bifurcation number in tree drawing.',action='store_true')
    parser.add_argument('-leg',help='Generate domain legend.',action='store_true')
    parser.add_argument('-reroot',metavar='Reroot the tree',help='Reroot the tree according to bifurcation number.',type=int)
    parser.add_argument('-redo',help='Redo all processing',action='store_true')
    parser.add_argument('-format',metavar='Tree image format',help='Format of ETE3 output image.')
    parser.add_argument('-marktax',help='Mark taxonomy information on the tree.',action='store_true')
    parser.add_argument('-remake',help='Rebuilding the tree only.',action='store_true')
    parser.add_argument('-test',help='Run with test file.',action='store_true')
    args=parser.parse_args()
    ########################################

    # check os platform
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        delimiter  = '/'
    elif sys.platform.startswith('win32') and args.standalone:
        print('Running Standalone Mode detected, only Lite Mode supported on Windows.')
        print('Setting run mode to Lite Mode.')
        args.standalone = False
        args.lite = True
    elif sys.platform.startswith('win32'):
        delimiter  = '\\'
    else:
        delimiter  = '/'
    args.delim = delimiter



    # get absolute path
    script_path = __file__
    if script_path.find(delimiter) != -1:
        abs_dir = script_path[:script_path.rfind(delimiter)] + delimiter
    else:
        abs_dir = './'
    args.abspath = abs_dir

    # set test file path for test mode
    if args.test:
        # set test file path
        test_path = abs_dir.rstrip(delimiter) + delimiter + 'test' + delimiter + 'test.fasta'
        test_config = abs_dir + delimiter.rstrip(delimiter) + 'Config.ini'
        test_out = './EPTA_test/'
        args.infile = test_path
        # print(args.infile)
        args.outfile = test_out

    # ensure input and output path format is correct
    if os.path.isdir(args.infile) and not args.infile.endswith(delimiter):
        args.infile = args.infile + delimiter

    if not args.outfile.endswith(delimiter):
        args.outfile = args.outfile + delimiter

    # config file check
    if os.path.isdir(args.infile):
        cfg_path = args.infile.rstrip(delimiter) + delimiter + '/Config.ini'
    elif os.path.isfile(args.infile):
        cfg_path = delimiter.join(args.infile.split(delimiter)[:-1]) + '/Config.ini'
    elif args.test:
        cfg_path = test_config
    else:
        cfg_path = args.infile.rstrip(delimiter) + delimiter + '/Config.ini'
    args.cfg_path = cfg_path

    if os.path.isfile(cfg_path):
        pass
    else:
        cfg_file = open('%sConfig.ini'%(abs_dir),'r') # ./standalone/
        cfg_content = cfg_file.read()
        new_cfg_file = open(cfg_path,'w')
        new_cfg_file.write(cfg_content)

    # output config log
    if not os.path.exists(args.outfile):
        os.makedirs(args.outfile)
    cfg_file = open(cfg_path,'r')
    cfg_content = cfg_file.read()
    new_path = args.outfile + 'Config.log'
    new_cfg_file = open(new_path,'w')
    new_cfg_file.write(cfg_content)

    # load config file
    cfg = ConfigParser()
    cfg.read(cfg_path)

    if not args.lite:
        args.lite = cfg.getboolean('General','run_mode_lite')
    if not args.standalone:
        args.standalone = cfg.getboolean('General','run_mode_standalone')
    if not args.dh:
        args.dh = cfg.getboolean('FASTA parser','keep_duplicate_headers')
    if not args.tax:
        args.ta = cfg.getboolean('FASTA parser','organism_lineage')
    if not args.name:
        args.name = cfg.getboolean('FASTA parser','protein_name_from_database')
    # if not args.dom:
    #     args.dom = cfg.getboolean('FASTA parser','domain_from_database')
    args.dom = False
    if not args.pfam:
        args.pfam = cfg.getboolean('FASTA parser','pfamscan_search')
    if not args.pev:
        args.pev = cfg['FASTA parser']['E-value']
    if not args.pas:
        args.pas = cfg.getboolean('FASTA parser','active_sites')
    if not args.email:
        args.email = cfg['FASTA parser']['email'].replace('\'','')
    if not args.muscle:
        args.muscle = cfg.getboolean('Multiple Alignment','run_MUSCLE')
    if not args.mafft:
        args.mafft = cfg.getboolean('Multiple Alignment','run_MAFFT')
    if not args.matrix:
        args.matrix = cfg['Multiple Alignment']['MAFFT_matrix'].replace('\'','')
    if not args.op:
        args.op = cfg.getfloat('Multiple Alignment','MAFFT_gapopen')
    if not args.ep:
        args.ep = cfg.getfloat('Multiple Alignment','MAFFT_gapext')
    if not args.retree:
        args.retree = cfg.getint('Multiple Alignment','tree_rebuilding')
    if not args.maxiterate:
        args.maxiterate = cfg.getint('Multiple Alignment','max_iterate')
    if not args.ffts:
        args.ffts = cfg['Multiple Alignment']['perfrom_ffts'].replace('\'','')
    if not args.trimal:
        args.trimal = cfg.getboolean('Multiple Alignment','run_trimAl')
    if not args.tmod:
        args.tmod = cfg['Multiple Alignment']['auto_mode'].replace('\'','')
    if not args.rmss:
        args.rmss = cfg['Multiple Alignment']['remove_specious'].replace('\'','')
    if not args.iqtree:
        args.iqtree = cfg.getboolean('Tree Building','run_iqtree')
    if not args.iqmod:
        args.iqmod = cfg['Tree Building']['test_mod'].replace('\'','')
    # if not args.alrt:
    #     args.alrt = cfg.getint('Tree Building','SH_like_Test')
    if not args.boots:
        args.boots = cfg.getint('Tree Building','bootstrap_number')
    if not args.rcluster:
        args.rcluster = cfg.getint('Tree Building','rcluster')
    if not args.mtree:
        args.mtree = cfg.getboolean('Tree Building','full_tree_search')
    if not args.bnni:
        args.bnni = cfg.getboolean('Tree Building','additional_optimize')
    if not args.xzoom:
        args.xzoom = cfg.getint('Tree Visualizing','branch_length_scale')
    if not args.yzoom:
        args.yzoom = cfg.getint('Tree Visualizing','branch_separation_scale')
    if not args.bs:
        args.bs = cfg.getboolean('Tree Visualizing','show_branch_support')
    if not args.bl:
        args.bl = cfg.getboolean('Tree Visualizing','show_branch_length')
    if not args.bif:
        args.bif = cfg.getboolean('Tree Visualizing','show_bifurcation_number')
    if not args.leg:
        args.leg = cfg.getboolean('Tree Visualizing','motif_legend')
    if not args.format:
        args.format = cfg['Tree Visualizing']['format'].replace('\'','')



    args.dom_color_list = eval(cfg['Tree Visualizing']['dom_color_list'])
    args.tax_color_list = eval(cfg['Tree Visualizing']['tax_color_list'])

    # print(args)
    return args

# args()
