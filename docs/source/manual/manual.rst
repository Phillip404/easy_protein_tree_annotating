Manual
========

Before you start
----------------

Configuration file
^^^^^^^^^^^^^^^^^^

A configuration file named 'Config.ini' can be found under the root path of the EPTA folder,
which stores all default command-related parameters. Users can edit it manually to change
the default settings of the tool.

Additionally, EPTA generates a 'Config.ini' file in the input file path after a run. Thus, if
one needs to run EPTA multiple times using the same input file, edit configuration file in the
input file path is also a option.

Log file
^^^^^^^^^^

EPTA automatically generates a log file that records everything that happened during a run.
Users can find the log under the output path of each run.

Also, a configuration log will be automatically generated in the output path that allows user
check or confirm configuration of a run.



Make a tree from FASTA file
---------------------------
An annotated phylogenetic tree can be built directly from FASTA file, and able to add protein ID, description,
organism lineage, protein domain are able to be added to the tree.

Example command-line
^^^^^^^^^^^^^^^^^^^^

Under construction



Input file
^^^^^^^^^^

A '-i' flag is what we used to declare input file, which is obligatorily required. The inputted file can be a FASTA file
in plain text format, or contained in a gunzip or tar.gz compressed file, or a folder contains any the
aforementioned file types.

  Input a FASTA file:

  .. code-block:: bash

    epta -i test_fasta.fasta -o ./test

  Input a gunzip file:

  .. code-block:: bash

    epta -i test_fasta.gz -o ./test

  Input a tar.gz file:

  .. code-block:: bash

    epta -i test_fasta.tar.gz -o ./test

  Input a folder:

  .. code-block:: bash

    -ls ./fasta_files
    'test_fasta.fasta' 'test_fasta.gz' 'test_fasta.tar.gz'

    epta -i ./fasta_files -o ./test

Output path
^^^^^^^^^^^

A '-i' flag is what we used to store output file, which is obligatory required.

Our tool will automatically detect whether the output path exists and if it is,
you will see the following caution:

  .. code-block:: text

    Output directory is existed, do you want to continue? (Y/N)

  .. Caution::

    Once the user input **Y** and **press enter**, all tool-related files, including the previous dataframe,
    parsed fasta file, etc., will be **removed** from that path.

If you would like to skip manual confirmation, add **-redo** flag in your command line.

Check point
^^^^^^^^^^^

EPTA will automatically generates a check point after it starting a run. You will
see the following caution if any check point file has been found in the output path:

.. code-block:: text

  Output directory is existed, do you want to read check point? (Y/N)

To continue the run from the place where last run ended, input **Y** and press enter.

Same as output path check, if you would like to skip manual confirmation, add **-redo**
flag in your command line.

Parse FASTA
^^^^^^^^^^^

Sequence recognition
""""""""""""""""""""

We introduced Biopython module to distinguish sequence info. By default, protein name and ID
will be extracted from sequence headers automatically. Users do not need any command-line flags to make
it happen.

Dataframe
"""""""""

Our tool will generate a human-readable dataframe called ‘info_index.tsv’ in tsv format under the output
path after parse all inputted files. Furthermore, if users choose to run Pfamscan, an independent tsv
file named ‘Pfamscan_result.tsv’ will be generated under the output path in order to inspect all
domain-related data.

For a line in the dataframe file, index is a unique random ID assigned by EPTA, and columns are arranged
as:

  .. table::

    =========   ======  ======  ==========  ================  ============================  ============================  =====================
    Random ID   Header   ID     Name        Organism Lineage  Domain Information[database]  Domain Information[Pfamscan]  Pfamscan JSON data
    =========   ======  ======  ==========  ================  ============================  ============================  =====================
    \           \       \
    =========   ======  ======  ==========  ================  ============================  ============================  =====================



If a parameter is not requested, the following columns will move forward in order.

Duplicate headers?
""""""""""""""""""

If you want to keep all duplicate sequence in your file, add **-dh** command to your
command line.

Local data?
"""""""""""

Local sequences that contained in FASTA file need to be marked with a **'lcl|'** identifier, in order to extract
information from it **automatically**. Protein name, ID, and taxonomy can be directly included in a header with specific
identifiers and splited with a vertical bar ('|'), while the order of their **arrangements doesn't matter**. And,
Pfamscan data should be included in another file if you do not want to fetch domain information or run Pfamscan
by EPTA, and the format of domain information should be in a JSON format which is the same with Pfamscan's result.

  Parameter identifiers:

    .. table::

      =========   ===========
      Parameter   Identifiers
      =========   ===========
      Name        [NAME]
      ID          [ID]
      Taxonomy    [TAXON]
      =========   ===========

  Example of a local sequence:


  .. code-block:: text
    :linenos:

      >lcl| [ID]]OAO11745.1 | [NMAE]hydrogenase | [TAXON] cellular organisms; Eukaryota; Sar; Stramenopiles; Bigyra; Opalozoa; Opalinata; Blastocystidae; Blastocystis; Blastocystis sp. subtypes; Blastocystis sp. subtype 1
      MLSRLSRIATTKSMLVMNAARSFAAEAQGKLVSVKINGNEYKVPEGMTVLEACQAQGIHVPFVCHHPRLKPLGKCRVCVVEIRGDEFPIKTSCNTKVEEGMDIWTNSPKARSASNEALKTLMAGTPIDTKFKTMEMDEVLTESADDCYALHRDMSRCVDCKRCARACSELQGMNVLENNPQEGGFPVVPTGYHLLKDTECISCGQCNVVCPTGAIVEQSHIPRVKQAMKAGKVMVMQTAPATRVAFGENFGREPGEITTGKMIACAKALGFQYVFDTNFGADMTIMEEGTELLERIKNNGPFPMFTSCCPGWVNMAEKCYPEILPNLSSCRSPHMMVGSTLKTYWAKKMNLKPEDIYVVSLMPCTAKKDEIERKNMWLDEKTPFVDAVLTTKELGDFCKQEGITNWDNMAEMPFDTPLGTSSGAGDIFGVSGGVMEAALRTAYQLQTGKPLEKIVVDEARGLDGTKRFSVDMNGKKINCAVVHSKFARELVENVKAGKEDLQFVEVMACPGGCISGGGQPHSNRADTIEKRMNAIYKIDAGKTLRRSMDNPEIQTLYKEFFEKPNSHKAHELLHTTYAPQYVRSREEKVEEPAEAGGEGGEGSDVGEDGVTILYGSETGTTAKAAKALQSKFKAAGISSAVIPMNKIDVESLPEKKKLVLMTCTYGAGEFPAMAQEFWENLSDESLDDDFLEGVEFGVFGLGSKAFKQFCEAAHQLDERMEELGAERVVDCGEGNEKDPQQYKTAFEPWSKEAVEAFK

  Example of a domain information format:

  .. code-block:: text
    :linenos:

      >lcl| [ID]]OAO11745.1
      [{"model_length":"82","align":["#HMM       pvtltfDGkevtvpeGdtvasAllangvdvprsckygrprgelcaggeCrnClVeveg..epnvracstpvedGlkvetqt","#MATCH      v+++++G+e++vpeG tv++A++a+g++vp  c++      l++ g+Cr C+Ve+ g   p   +c t+ve+G+ + t++","#PP        6899********************************....789*************86215556*************9986","#SEQ       LVSVKINGNEYKVPEGMTVLEACQAQGIHVPFVCHH----PRLKPLGKCRVCVVEIRGdeFPIKTSCNTKVEEGMDIWTNS"],"env":{"to":"108","from":"29"},"name":"Fer2_4","acc":"PF13510.6","sig":1,"evalue":"1.4e-17","desc":"2Fe-2S iron-sulfur cluster binding domain","hmm":{"to":"81","from":"3"},"act_site":null,"type":"Domain","bits":"63.5","clan":"CL0486","seq":{"to":"107","from":"31","name":"EMBOSS_001"}},{"model_length":"52","align":["#HMM       rCigCgaCvaaCp....vkaieldeeenekgt.....ekveidpekClgCgaCvavCPtga","#MATCH     rC+ C++C++aC+    ++++e +++  e g+      +  ++ ++C++Cg+C  vCPtga","#PP        8***********87544555555543..333433322333667899*************98","#SEQ       RCVDCKRCARACSelqgMNVLENNPQ--EGGFpvvptGYHLLKDTECISCGQCNVVCPTGA"],"env":{"to":"214","from":"156"},"name":"Fer4_7","acc":"PF12838.7","sig":1,"evalue":"3.2e-06","desc":"4Fe-4S dicluster domain","hmm":{"to":"52","from":"1"},"act_site":null,"type":"Domain","bits":"27.6","clan":"CL0344","seq":{"to":"214","from":"156","name":"EMBOSS_001"}},{"model_length":"243","align":["#HMM       kvvvqvAPavrvalgeefglsv.aattgklvaalrklGfdkVfdtafgadltimeeasellerleeeeklpmitScCPgwvkyvekkypellpnlssvkSPqqilgaliKkylaek.....ekivvVsimPCtaKklEaareefksag..rdvDavlTtrElaellkeagidl.akleeeeldnplgessgagki...................................egvkeaevelegktlkvavvnGlknikklleklkageakydfiEvmaCpgGCigGg","#MATCH      +v+q+APa+rva+ge+fg ++ + ttgk++a+ + lGf++Vfdt+fgad+timee++eller++++ + pm+tScCPgwv+++ek ype+lpnlss++SP++++g+ +K+y+a+k     e+i+vVs+mPCtaKk E++r+++  ++    vDavlTt+El++  k++gi+  +++ e ++d+plg+ssgag i                                   +g+k+ +v+++gk++++avv+  k +++l+e++kag+ + +f+EvmaCpgGCi Gg","#PP        689***************************************************************99****************************************************************************9855579*******************9655****************************************************************************96.889*****************************8","#SEQ       VMVMQTAPATRVAFGENFGREPgEITTGKMIACAKALGFQYVFDTNFGADMTIMEEGTELLERIKNNGPFPMFTSCCPGWVNMAEKCYPEILPNLSSCRSPHMMVGSTLKTYWAKKmnlkpEDIYVVSLMPCTAKKDEIERKNMWLDEktPFVDAVLTTKELGDFCKQEGITNwDNMAEMPFDTPLGTSSGAGDIfgvsggvmeaalrtayqlqtgkplekivvdearglDGTKRFSVDMNGKKINCAVVHS-KFARELVENVKAGKEDLQFVEVMACPGGCISGG"],"env":{"to":"517","from":"232"},"name":"Fe_hyd_lg_C","acc":"PF02906.14","sig":1,"evalue":"7.5e-87","desc":"Iron only hydrogenase large subunit, C-terminal domain","hmm":{"to":"243","from":"2"},"act_site":null,"type":"Domain","bits":"291.0","clan":"No_clan","seq":{"to":"517","from":"233","name":"EMBOSS_001"}},{"model_length":"56","align":["#HMM       dvrkkRakalykiDkkkklrkSheNpevkklYkeflgeplsekahelLHThYtd","#MATCH     d+++kR++a+ykiD+ k+lr+S +Npe++ lYkef+++p+s+kahelLHT+Y +","#PP        789*************************************************76","#SEQ       DTIEKRMNAIYKIDAGKTLRRSMDNPEIQTLYKEFFEKPNSHKAHELLHTTYAP"],"env":{"to":"580","from":"525"},"name":"Fe_hyd_SSU","acc":"PF02256.17","sig":1,"evalue":"6.2e-24","desc":"Iron hydrogenase small subunit","hmm":{"to":"55","from":"2"},"act_site":null,"type":"Domain","bits":"83.8","clan":"No_clan","seq":{"to":"579","from":"526","name":"EMBOSS_001"}},{"model_length":"143","align":["#HMM       ilYgSetGnteklAkqlaeelgehgfnadvvslsdydeslseieeealllvvtsTfgnGdppengesffqdllelkgdeledgdlsgvrfavfglGdsayenFcaagkkldekleelGaerllkllegdednqegqeeafrkW","#MATCH     ilYgSetG+t k Ak+l+ +++++g+++ v+ ++++d  +++++e++ l++ t T+g G++p  ++ +f++ l +++  l+d+ l+gv+f vfglG++a ++Fc+a+++lde++eelGaer++  +eg+e++ + +++af+ W","#PP        89***********************************..68*********************7777.8888888885..67777***********************************************99********99","#SEQ       ILYGSETGTTAKAAKALQSKFKAAGISSAVIPMNKID--VESLPEKKKLVLMTCTYGAGEFPAMAQ-EFWENLSDES--LDDDFLEGVEFGVFGLGSKAFKQFCEAAHQLDERMEELGAERVVDCGEGNEKDPQQYKTAFEPW"],"env":{"to":"749","from":"612"},"name":"Flavodoxin_1","acc":"PF00258.25","sig":1,"evalue":"1.5e-33","desc":"Flavodoxin","hmm":{"to":"143","from":"1"},"act_site":null,"type":"Domain","bits":"116.0","clan":"CL0042","seq":{"to":"749","from":"612","name":"EMBOSS_001"}}]


  .. Hint::

    A local sequence tag and a [ID] block is the minimun requirment for EPTA to recognize a sequence.

Taxonomy information
""""""""""""""""""""

When using a '-tax' flags to enable the taxonomy finding functionality, EPTA can fetch organism lineage
automatically from the NCBI database with a given protein ID, and the taxonomy information will be stored
in dataframe in the following format:

  .. code-block:: text

    cellular organisms; Eukaryota; Sar; Stramenopiles; Bigyra; Opalozoa; Opalinata; Blastocystidae; Blastocystis; Blastocystis sp. subtypes; Blastocystis sp. subtype 1

Once a sequence has organism lineage, it would be easy for show species or select proteins from organism under a certain classification in later process.


  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax


Protein name from database
"""""""""""""""""""""""""""""""""

EPTA can search protein name according to accession numbers from Entrez database.
To enable this function, add **-name** flag to the command line.

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -name


Run PfamScan
""""""""""""

EPTA introduced PfamScan to allow users annotate protein domains on the tree.

Add **'-pfam'** flag to the command line to run PfamScan and enable domain annotating.

Pfamscan search can provide name, accession number, hit sequence, envelope, e-value, bit score, and active site of a protein domain.
Which is a recommended way to obtain protein domain information.

Alongside **'-pfam'** flag, **'-pev [E-value]'** and **'-pas'** [active sites] can be used to spicify a e-value and to enable active site functionality
in Pfamscan search. Meanwhile, both shortened domain data in the dataframe and a human-readable tsv file will be automatically generated after a
Pfamscan search in order to provide detailed information of protein domains.

We also introduced the '-em' flag for users to provide an email address for receive protein messages from web services (for example, you are
temporarily banned).

  Example of Pfamscan result in dataframe:

  .. code-block:: text

    {'Iron only hydrogenase large subunit, C-terminal domain; PF02906.14; evalue=1.3e-42; bits=146.1': '1...186', 'Iron hydrogenase small subunit; PF02256.17; evalue=4.3e-26; bits=90.7': '195...249', 'Flavodoxin; PF00258.25; evalue=2.5e-31; bits=108.8': '276...415', 'FAD binding domain; PF00667.20; evalue=3.9e-42; bits=144.3': '458...666', 'Oxidoreductase NAD-binding domain ; PF00175.21; evalue=2.2e-10; bits=41.1': '701...800'}

  Example of Pfamscan details form:

  .. code-block:: text

                     seq_name   seq_id     alignment_start  alignment_end  envelope_start  envelope_end  hmm_acc     hmm_name     hmm_desc                                               type   hmm_start  hmm_end  hmm_length  bit score  E-value  significance  clan  predicted_active_site_residues

    i6j8l50wKOrP7Xpz GIQ79514.1 GIQ79514.1 1                186            1               186           PF02906.14  Fe_hyd_lg_C  Iron only hydrogenase large subunit, C-terminal domain Domain 104        243      243         146.1      1.3e-42  1             No_clan
    i6j8l50wKOrP7Xpz GIQ79514.1 GIQ79514.1 195              249            194             249           PF02256.17  Fe_hyd_SSU   Iron hydrogenase small subunit                         Domain 2          56       56          90.7       4.3e-26  1             No_clan
    i6j8l50wKOrP7Xpz GIQ79514.1 GIQ79514.1 276              415            276             415           PF00258.25  Flavodoxin_1 Flavodoxin                                             Domain 1          143      143         108.8      2.5e-31  1             CL0042

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -name -pfam -pev 10 -pas -em test@example.com

.. Caution::
  According to the rule of the Pfamscan web service, one can submit at most 3000 sequences in a maximum of 30 batch jobs when using the Lite version.

  Therefore, if you have more than 1500 sequences that need to run Pfamscan search, please do not run our tool again immediately
  after keyboard interrupting a run that has already submit sequences to the server.

Multiple sequence alignment
-------------------------------
EPTA introduced MAFFT and MUSCLE as multiple sequence alignment programs. The default
program is MAFFT, which could be changed in the configuration file.

After run multiple sequence alignment, trimAl was introduced to provide further sequence
trim.

.. Hint::

  If both MAFFT and MUSCLE are set as default program, MAFFT is the prioritized one.


MAFFT
^^^^^^^^^^^

Run MAFFT
""""""""""""""""""""
MAFFT will automatically run, do not need extra command line flags. However, users
still able to run MAFFT manually by adding **'-mafft'** flag.

Command-line example:

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name -pfam -mafft

There are also several command line flags for changing paramters of MAFFT:

  **Matrix**

  Commnad line flag of matrix selecting is **'-matrix [Matrix Abbreviation]'**,
  identical to the command line flag '--bl' or '--jtt' of MAFFT.

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -name -pfam -mafft -matrix bl62

  **Opening Score And Extension Score**

  Commnad line flag of opening score setting is **'-op [Number]'**, identical to the command
  line flag '--op' of MAFFT.

  Commnad line flag of extension score setting is **'-ep [Number]'**, identical to the command
  line flag '--ep' of MAFFT.

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -name -pfam -mafft -op 1.53 -ep 0.123


  **Tree Rebuilding Number**

  Commnad line flag of tree rebuilding number is **'-retree [Number]'**, identical to the command
  line flag '--retree' of MAFFT. This flag can determine the guide tree built times in the progressive
  stage.

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -name  -pfam -em test@example.com -mafft -retree 2

  **Max Iterate Number**

  Commnad line flag of maximum iteration is **'-maxiterate [Number]'**, identical to the command
  line flag '--maxiterate' of MAFFT. This flag can determine the cycles number of iterative refinement.

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -name  -pfam -em test@example.com -mafft -maxiterate 2

  **Fast Fourier Transform Algorithm**

  Commnad line flag of choose FFTS (Fast Fourier Transform) method is **'-ffts [Mode]'**,
  identical to the command line flag '--localpair', '--genafpair' and '--globalpair' of MAFFT.
  For each command, **'-ffts localpair'** stands for the Smith-Waterman algorithm, **'-ffts genafpair'**
  stands for generalized affine gap cost, **'-ffts globalpair'** stands for Needleman-Wunsch
  algorithm.

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -name  -pfam -em test@example.com -mafft -ffts localpair


MUSCLE
^^^^^^^^^^^

Run MUSCLE
""""""""""""""""""""
To run MUSCLE as the multiple sequence alignment program, add **-muscle** flag to
the command line. MUSCLE will automatically run, do not need any parameter settings.

Command-line example:

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -muscle

trimAl
^^^^^^^^^^^

Run trimAl
""""""""""""""""""""
As the default setting, trimAl automatically runs in the EPTA pipline. One can also
manually add **-trimal** flag to the command line to run trimAl.

**trimAl Run Mode**

Commnad line flag of selecting trimAl run mode **'-tmod [Mode]'**. There are four
mode selectable, 'automated1', 'gappyout', 'strict', and 'strictplus', identical to
corresponding command of trimAl command line. Only 'automated1' mode is accessable in
the Lite mode.

Command-line example:

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -mafft -trimal -tmod automated1

**Remove Spurious Sequences**

The flag **'-rmss [Residue overlap/Sequence overlap]'** able to remove spurious
sequences when triming multiple alignment sequences. **Residue overlap** is identical to
the flag '-resoverla' of trimAl, in charge of keep "good positions" according to
a given minimum overlap of a positions with other positions in the column. **Sequence overlap**
is identical to the flag '-seqoverlap' of trimAl, which means a minimum percentage of
"good positions" that a sequence must have in order to be conserved.

Command-line example:

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -mafft -trimal -rmss 0.75/80

Make a tree from alignment file
-------------------------------

EPTA implements IQ-tree as the tree building program in the pipeline. When running
EPTA standalone version with large dataset (>500), be aware that IQ-tree need corresponding
large memory space to run.

Run IQ-tree
""""""""""""""""""""
As the default setting, IQ-tree automatically runs in the EPTA pipline. One can also
manually add **-iqtree** flag to the command line to run IQ-tree.

**IQ-tree Run Mode**

EPTA provide three run mode for users to select model: **'-iqmod TEST'**, **-iqmod TESTNEW**
and **-iqmod [A specific model]**. They are based on IQ-tree's command line, 'TEST' mode provides
automatic model selection in a basic model list, similarly, 'TESTNEW' automatically select model
from a advanced list. Users can also choose on known best model from the two list before. For more
details of models, please check the model list of IQ-tree:

`Model selection <http://www.iqtree.org/doc/Tutorial#choosing-the-right-substitution-model>`_
`Substitution models <http://www.iqtree.org/doc/Substitution-Models>`_

Command-line example:

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -mafft -trimal -iqmod TEST

  epta -i ./fasta_files -o ./test -tax -name  -pfam -mafft -trimal -iqmod LG+I+G4

**Bootstrap**

EPTA assessing branch support via ultrafast bootstrap of IQ-tree. The minimun number of
ultrafast bootstrap is 1000. The command flag of bootstrap is **-boost [bootstrap numbr]**, default
value set as 1000.

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -mafft -trimal -iqmod TEST -boots 1000

**Reduce Runtime**

To reduce runtime and computational burden, EPTA introduced **-rcluster [percentage]** flag, which implements
by IQ-tree, derived from the *relaxed hierarchical clustering algorithm*. This flag specify a percentage for the
relaxed clustering algorithm, in order to speed up the computation by reduce the percentage of partition schemes.
For example, **-rcluster 10** means only top 10% of partition schemes are considered in the running. This function
is turned off in the default setting.

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -mafft -trimal -iqmod TEST -boots 1000 -rcluster 10

**Tree Optimize**

EPTA provides two command flags to enhance tree quality by increase run time. **-mtree** turns full tree search on to
increse the accuracy, and **-bnni** performs an additional step to further optimize UFBoot trees by nearest neighbor
interchange (NNI) based directly on bootstrap alignments. . One point needs to be awared is that both flags significantly
increase the run time.

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -mafft -trimal -iqmod TEST -boots 1000 -mtree -bnni

Annotate a tree file
--------------------------

**Annotate Taxonomy**
""""""""""""""""""""

By adding **-tax** flag in the command line, EPTA can automatically annotate taxonomy of all sequences' species.
The maximum rank of the organism lineage EPTA can annotating on the phylogenetic tree is six. Any organism lineage
that longer than six rank will be shortened to that number. Given that the full organism lineage from NCBI commomly
starts with kingdom, EPTA intercepts the second to the last rank. If the full lineage longer than six rank (in the most cases)
, EPTA will intercept the second rank to the fifth rank and append the last rank then, which is the name of that specie.
For example:

  .. code-block:: text
    :linenos:

    Full organism lineage:
    cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Enterobacteriaceae; Escherichia; Escherichia coli

    EPTA annotated organism lineage:
    Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Enterobacteriaceae; Escherichia coli

Correspondingly, if there are local sequence in the input file, pleas ensure that the full organism is attached.

Besides annotate taxonomic information on the tree image, EPTA is also capable to color tree branches depends on taxonomic
rank by adding **-marktax** in the command line.

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -marktax

**Annotate Domain**

By adding **-pfam** flag in the command line, EPTA can automatically annotate domains of all sequences. The top 10
frequent domain will be colored, and the rest domains will be annotated in gray. What's more, for colored domains,
besides show domain names on each domain face, **-leg** command can make a lengend in the right bottom corner of the
image to illustrate domain names and corresponding color.

.. code-block:: bash

  epta -i ./fasta_files -o ./test -pfam -leg

**Image Size**
""""""""""""""""""""

Command flag **-xzoom [Magnification]**, **-yzoom [Magnification]** are introduced to adjust the image size horizontally and
vertically. The basic magnification is 1. The default DPI of output png image is 300, and do not change with image size.

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -xzoom 1.5 -yzoom 1.5

**Branch Setting**
""""""""""""""""""""

There are three attribute value of branches in EPTA, genetic distance, bootstrap value, and bifurcate number, corresponding
to the following commands: **-bl** (branch length), **-bs** (branch support), and **-bif** (bifurcation). None of them is enabled
in the defualt setting. Therefore, users need to enable corresponding command flag to show the value on tree image.

.. code-block:: bash

  epta -i ./fasta_files -o ./test -tax -name  -pfam -bl -bs -bif
