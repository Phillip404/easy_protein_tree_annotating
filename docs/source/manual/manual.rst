Use EPTA
========

Before you start
----------------

Configuration file
^^^^^^^^^^^^^^^^^^

A configuration file named 'Config.ini' can be found under the root path of the EPTA folder,
which stores all default command-related parameters. Users can edit it manually to change
the default settings of the tool.

Log file
^^^^^^^^^^

Our tool automatically generates a log file that records everything that happened during a run.
Users can find the log under the output path of each run.

Play with EPTA
^^^^^^^^^^^^^^

We provide a set of test files to help users get familiar with how to use our tool,
you can find them in the 'test_file' folder under the root path. Feel free to play
a little with EPTA!



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

    Only a local sequence tag and a [ID] block would be fine for EPTA to recognize a sequence.

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

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -dbn

Protein domains from database
"""""""""""""""""""""""""""""

For those proteins who have domain data recorded in NCBI database, EPTA can retrieve that data for users by command-line
flag '-dbd' (database domain).

Database retrieve functionality only gets domain position, domain name, and Pfam ID of that domain. In addition, there are
considerable proportion of proteins on NCBI **DO NOT** have domain data. Therefore, Pfamsacn search functionality are recommanded to
use to gain domain data.

  Example of domain data retrieves from database:

  .. code-block:: text

    {'2Fe-2S iron-sulfur cluster binding domain; pfam13510': '29..108', '4Fe-4S dicluster domain; cl19102': '148..222', '[FeFe] hydrogenase, group A; TIGR02512': '149..522', 'Iron only hydrogenase large subunit, C-terminal domain; pfam02906': '232..520', 'Iron hydrogenase small subunit; pfam02256': '526..577', 'Flavodoxin; pfam00258': '611..748'}

  Command-line example:

  .. code-block:: bash

    epta -i ./fasta_files -o ./test -tax -dbn -dbd

Run Pfamscan
""""""""""""

Given that not all proteins on NCBI have their domain information, '-pfs' flag is introduced to run Pfamscan to gain domain information.

Pfamscan search can provide name, accession number, hit sequence, envelope, e-value, bit score, and active site of a protein domain.
Which is a recommended way to obtain protein domain information.

Alongside '-pfs' flag, '-pfev [E-value]' and '-pfas' can be used to spicify a e-value and to enable active site functionality in Pfamscan
search. Meanwhile, both shortened domain data in the dataframe and a human-readable tsv file will be automatically generated after a
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

    epta -i ./fasta_files -o ./test -tax -dbn -dbd -pfs -pfev 10 -pfas -em test@example.com

.. Caution::
  According to the rule of the Pfamscan web service, one can submit at most 3000 sequences in a maximum of 30 batch jobs.

  Therefore, if you have more than 1500 sequences that need to run Pfamscan search, please do not run our tool again immediately
  after keyboard interrupting a running that has already submit sequences to the server, and better to wait for at least 10 minutes before the next run.

Make a tree from alignment file
-------------------------------

Under construction

Annotate a tree file
--------------------------

Under construction

Commands
========

General
-------

-i [file or path]
^^^^^^^^^^^^^^^^^^^^^^

Specify input file in normal, gunzip, or tar.gz, or a path includes all needed input files.

-o [file or path]
^^^^^^^^^^^^^^^^^^^^^^

Specify output path.

-em [email address]
^^^^^^^^^^^^^^^^^^^^^^

Email address that you want receive potential information from web tools.


Parse FASTA
-----------

-dh
^^^^^^^^^^^^^^^^

Keep duplicate headers.

-tax
^^^^^^^^^^^^^^^^

Search for taxonomy information for each sequence in Entrenz database.

-dbn
^^^^^^^^^^^^^^^^

Search for protein name for each sequence in Entrenz database.

-dbd
^^^^^^^^^^^^^^^^

Search for domain information for each sequence in Entrenz database (no evalue and bit score)

-pfs
^^^^^^^^^^^^^^^^

Run Pfamsacn (domain prediction) for each sequence.

-pfev [E-value]
^^^^^^^^^^^^^^^^

E-value of Pfamscan search.

    **Avaliable E-value**::

      50
      20
      10
      5
      2
      1
      0.1
      0.01
      0.001
      0.0001
      1e-5
      1e-10
      1e-50
      1e-100
      1e-300

-pfas
^^^^^^^^^^^^^^^^

Enable active sites prediction in Pfamscan.


Make alignment
--------------

Under construction

Make phylogenetic tree
----------------------

Under construction

Tree Annotating
---------------

Under construction
