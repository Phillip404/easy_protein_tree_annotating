###  python3 ete3_epta.py -i ./test2-lite/ -o ./test2-lite/ -tax -bl -bs -bif -dom -leg

from ete3 import Tree, TreeStyle, Face, AttrFace, TextFace, PhyloTree, SeqMotifFace, TreeStyle, add_face_to_node, NodeStyle, RectFace
# from ete3 import Tree
import pandas as pd
import os
import logging
import argparse
from global_var import args
import time


args = args()

def annotate_name():
    path = ''.join(args.outfile.rsplit())
    index = path + '/info_index.tsv'
    dataframe = pd.read_csv(index, sep='\t')

    contree = path.rstrip('/') + '/02_Tree_File/IQ-tree.contree'
    # folder = args.outfile.rstrip('/') + '/02_Tree_File'
    treefile = open(contree,'r')
    treefile = ''.join(treefile.readlines())
    # print(treefile)

    new_treefile = open(path + '/02_Tree_File/new_IQ-tree.contree','w')



    t = Tree(treefile)
    for node in t.iter_descendants('postorder'):
        if node.is_leaf():
            i = 0
            for name in dataframe['Random ID']:
              if name == node.name:
                  id = dataframe['ID'][i]
                  # taxonomy = ';'.join(dataframe['Organism Lineage'][i].split(';')[1:])
                  # if len(taxonomy.split(';')) > 5:
                  #     taxonomy = ';'.join(taxonomy.split(';')[:5]) + ';' + taxonomy.split(';')[-1]
                  treefile = treefile.replace(node.name, id)
              else:
                  i += 1


    print(treefile, file=new_treefile)
    # print(treefile)

# count every domain
def check_domain_times():
    domain_dict = {}
    for name in pfam_df['hmm_name']:
        if name not in domain_dict:
            domain_dict[name] = 1
        else:
            domain_dict[name] += 1
    domain_dict = sorted(domain_dict.items(),key=lambda item:item[1],reverse=True)
    domain_list = []
    for item in domain_dict:
        domain_list.append(item[0])
    # print (domain_dict)
    # print (domain_list)
    return (domain_list)

def reroot():
    bif_file = open(path + 'bif_log.txt','r')
    for line in bif_file:
        line = line.strip()
        bif_num = line.split('\t')[0]
        children_list = eval(line.split('\t')[1])

        if int(bif_num) == args.reroot:
            children_list[0] = children_list[0].strip()
            children_list[1] = children_list[1].strip()
            # A = children_list[0]
            # B = children_list[1]
            return(children_list)




def ete3_drawing():

    annotate_name()

    global path
    path = ''.join(args.outfile.rsplit())
    index = path + 'info_index.tsv'
    dataframe = pd.read_csv(index, sep='\t')
    new_tree = path + '/02_Tree_File/new_IQ-tree.contree'
    t = PhyloTree(new_tree)

    ts = TreeStyle()

    #set not style
    nstyle = NodeStyle()
    nstyle['shape'] = 'square'
    nstyle['size'] = 1
    nstyle['fgcolor'] = 'black'
    for n in t.traverse():
       n.set_style(nstyle)

    ts.show_leaf_name = False

    if args.bl:
        ts.show_branch_length = True

    if args.bs:
        ts.show_branch_support = True

    ts.scale = 750*args.xzoom
    ts.branch_vertical_margin = 15*args.yzoom

    # color_list = ['LightCoral', 'Gold', 'Aquamarine', 'YellowGreen', 'Pink', 'Tan', 'Orange', 'Orchid', 'DarkSeaGreen', 'SkyBlue']
    color_list = args.color_list
    tax_color_list = ['#6B8E23', '#3498DB', '#BF6EE0', '#D25852', '#D47500', '#AA8F00', '#03A678', '#006080', '#AA0000', '#807D67']

    # taxonomy back ground color
    if args.tax:
        total_seq = len(dataframe['Organism Lineage'])
        num_standard = round(total_seq*0.5*0.2) - 5
        p = 0
        # print(num_standard)
        for i in range(0,6):
            tax_num = {}
            tax_num_final = {}
            for j in range(0,total_seq):
                try:
                    tax = dataframe['Organism Lineage'][j]
                    tax = ';'.join(tax.split(';')[1:]).strip()
                    # print(tax)
                    if len(tax.split(';')) > 6:
                        tax = ';'.join(tax.split(';')[:5]) + ';' + ';'.join(tax.split(';')[-2:-1]).strip()
                    tax = tax.split(';')[i].strip()
                    if tax not in tax_num:
                        tax_num[tax] = 1
                    else:
                        tax_num[tax] = tax_num[tax] + 1
                except:
                    pass

            try:
                del tax_num['']  # remove UNKONW sequence
            except:
                pass

            for key in tax_num:
                if tax_num[key] >= num_standard:
                    tax_num_final[key] = tax_num[key]
            # print(tax_num_final)

            p += 1
            # print(p)
            # print(i)
            if len(tax_num_final) >= p:
                class_num = i
                # print(tax_num_final)
                sort_list = sorted(tax_num_final.items(),key=lambda x:x[1], reverse=True) # sort taxonomy class dictionary
                tax_num_sort = [a for a,b in sort_list]
                # print(tax_num_sort)
                # break

    for node in t:
        if node.is_leaf():
            i = 0
            for ID in dataframe['ID']:
                # annotate taxonomy
                if args.tax:
                    if ID == node.name:
                      taxonomy = ';'.join(dataframe['Organism Lineage'][i].split(';')[1:]).strip()
                      if len(taxonomy.split(';')) > 6:
                          taxonomy = ';'.join(taxonomy.split(';')[:5]) + ';' + ';'.join(taxonomy.split(';')[-2:-1]).strip()
                      elif taxonomy.strip() == '':
                          taxonomy = 'Unknow'
                      # add tax name face
                      tax_face = TextFace(taxonomy,fstyle='italic')
                      tax_face.margin_left = 30

                      try:
                          tax_class = taxonomy.split(';')[class_num].strip()  # class_num comes from the result of back ground color loop
                          tax_color = tax_num_sort.index(tax_class)
                          tax_color = tax_color_list[tax_color]
                          tax_face = TextFace(taxonomy,fstyle='italic')
                          if node.is_leaf() and node.name == 'NPU90158.1':
                            node.img_style["bgcolor"] = tax_color
                            # print(tax_color)
                          # tax_face.background.color=tax_color
                      except:
                          tax_face = TextFace(taxonomy,fstyle='italic')
                          node.img_style["bgcolor"] = 'white'


                      node.add_face(tax_face, column=0, position='aligned')
                    else:
                      i += 1
            # annotate domains

            if args.dom:
                global pfam_df
                pfam_df = pd.read_csv('pfamscan_details.tsv', sep='\t')

                # the order of domain list based on times that a domain shows in all proteins
                domain_list = check_domain_times()

                j = 0
                # empty list to combine domain motifs
                simple_motifs = []

                # specified motif align test
                # chosen motif: Fe_hyd_lg_C
                # simple_motif list example:
                # [[17, 92, '[]', None, 10, 'Aquamarine', 'Aquamarine', 'arial|1|black|Fer2_4'], [99, 136, '[]', None, 10, 'YellowGreen', 'YellowGreen', 'arial|1|black|NADH-G_4Fe-4S_3'], [240, 523, '[]', None, 10, 'LightCoral', 'LightCoral', 'arial|1|black|Fe_hyd_lg_C'], [532, 586, '[]', None, 10, 'Gold', 'Gold', 'arial|1|black|Fe_hyd_SSU']]
                # start_dom = 'Fe_hyd_lg_C'
                # p = 0
                # for ID in pfam_df['seq_id']:
                #     if ID == node.name:
                #         print (str(pfam_df['hmm_name'][p]))
                #         if str(pfam_df['hmm_name'][p]) == start_dom:
                #             x = start_dom_start = pfam_df['alignment_start'][p]
                #             y = start_dom_end = pfam_df['alignment_end'][p]
                #             print(p)
                #             print(x,y)
                #         p += 1
                #     else:
                #         p += 1

                for ID in pfam_df['seq_id']:
                    if ID == node.name:
                        start = pfam_df['alignment_start'][j]
                        end = pfam_df['alignment_end'][j]
                        domain_name = pfam_df['hmm_name'][j]
                        col_num = domain_list.index(domain_name)
                        # print(col_num)
                        # if domain_name == start_dom:
                        #     x = start_dom_start = start
                        #     y = start_dom_end = end
                        #     start = 0
                        #     end = end - start
                        if  col_num < 10:
                            if 2>1:
                                domain_name = ''
                            simple_motifs.append([start,end,'[]', None, 10, color_list[col_num], color_list[col_num], 'arial|1|black|%s'%(domain_name)])
                        else:
                            simple_motifs.append([start,end,'[]', None, 10, 'LightGrey', 'LightGrey', 'arial|1|black|%s'%(domain_name)])
                            # simple_motifs.append([start-10,end+10,'[]', None, 10, 'Snow', 'Gainsboro', 'arial|1|black|%s'%(domain_name)])
                        j += 1
                    else:
                        j += 1
                # print(simple_motifs)
                if not len(simple_motifs) == 0:
                    # set sequence face attributes
                    seqFace = SeqMotifFace(seq=None, motifs=simple_motifs, seq_format='()')
                    seqFace.margin_left = 30
                    node.add_face(seqFace, 1, 'aligned')

    for n in t.traverse():
       if not node.is_leaf():
           node.img_style["bgcolor"] = 'red'

    # add bifurcate number face
    bif_file = open(path + 'bif_log.txt','w')
    bif_num = 1
    for node in t.traverse():
        if len(node.children) >= 2:
            child_list = []
            for child in node.children:
                child_list.append(str(child.describe))
            # if bif_num == 41:
            #     print(child_list)

            node_info = "%s\t%s" % (bif_num,child_list)
            print(node_info, file=bif_file)
            bif_num += 1
            if args.bif:
                bif_face = TextFace(str(bif_num),fsize=8,ftype='Verdana',fstyle='normal',fgcolor='navy',penwidth='5',bold=False)
                node.add_face(bif_face, column=0, position='branch-top')


    # reroot the tree
    if args.reroot:
        children_list = reroot()
        # print(children_list)


        for node in t.traverse():
            # print(str(node.describe))
            # print(children_list[0])
            node_desc = str(node.describe)
            y = children_list[0]
            if node_desc == children_list[0]:
                A = node
                # print(A)
            if node_desc == children_list[1]:
                B = node
                # print(B)

        ancestor = t.get_common_ancestor(A,B)
        t.set_outgroup(ancestor)

    # add legend face
    if args.dom and args.leg:
        # print(domain_list)
        if len(domain_list) >= 10:
            lgd_elem = 10
        elif len(domain_list) < 10:
            lgd_elem =  len(domain_list)
        for q in range (0,lgd_elem):
            # ts.legend.add_face(RectFace(width=ts.scale*2, fgcolor=color_list[q], bgcolor=color_list[q], column=0, row=q))
            ts.legend.add_face(RectFace(width=ts.scale/4, height=ts.scale/40, fgcolor=color_list[q], bgcolor=color_list[q]), column=0)
            ts.legend.add_face(TextFace(domain_list[q]), column=1)
        ts.legend_position = 4

    # render the tree
    # image_path = path + ''.join(''.join(args.infile.split('/')[-1]).split('.')[:-1]) + '.png'
    image_path = path + 'tree_image.%s' % str(args.format).lower()
    t.render(image_path, h=100*i, dpi=300, tree_style=ts)
    # t.show(tree_style=ts)

# ete3_drawing()

def ete3_run():
    logging.info('Initializing ETE3...')

    branch_suppor = branch_length = bifurcate_number = ''
    if args.bs:
        branch_suppor = 'Branch support: show    '
    if args.bl:
        branch_length = 'Branch length: show    '
    if args.bif:
        bifurcate_number = 'Bifurcation number: show'
    paramters = branch_suppor + branch_length + bifurcate_number

    logging.info('='*20)
    logging.info('ETE3 parameters:')
    logging.info('Branch legnth scale: %s    Branch separation scale: %s' % (args.xzoom, args.yzoom))
    if args.bif or args.bl or args.bs:
        logging.info(paramters)

    logging.info('='*20)
    logging.info('Running ETE3...')


    # run ete3
    start = time.perf_counter()

    ete3_drawing()

    end = time.perf_counter()
    runtime = end - start
    logging.info('ETE3 processing done. Runtime: %s second\n' % (round(runtime,2)))

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

    ete3_run()
