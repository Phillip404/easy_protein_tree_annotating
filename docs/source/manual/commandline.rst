Commandline Reference
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

-standalone
^^^^^^^^^^^^^^^^^^^^^^

Run standalone mode. (Only for standalone version)

-lite
^^^^^^^^^^^^^^^^^^^^^^

Run lite mode. (Only for standalone version)

-test
^^^^^^^^^^^^^^^^^^^^^^

Run test mode.

-redo
^^^^^^^^^^^^^^^^

Skip manually confirm for check point checking, automatically rerun the full pipeline.

-remake
^^^^^^^^^^^^^^^^

According to exsisting output file, remake the tree image only.


Parse FASTA
-----------

-dh
^^^^^^^^^^^^^^^^

Keep duplicate headers.

-tax
^^^^^^^^^^^^^^^^

Search for taxonomy information for each sequence in Entrenz database.

-name
^^^^^^^^^^^^^^^^

Search for protein name for each sequence in Entrenz database.


-pfam
^^^^^^^^^^^^^^^^

Run Pfamsacn (domain prediction) for each sequence and then annotate protein domians on the tree.

-pev [E-value]
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


Make alignment
--------------
MAFFT
""""""""""""""""""""
-mafft
^^^^^^^^^^^^^^^^
Enable MAFFT

-matrix
^^^^^^^^^^^^^^^^
Score matrix for align sequences.

  **Avaliable Matrix**::

    bl30
    bl45
    bl62
    bl80
    jtt100
    jtt200

-op
^^^^^^^^^^^^^^^^
Gap Open penalty.

-ep
^^^^^^^^^^^^^^^^
Gap extension penalty.

-retree
^^^^^^^^^^^^^^^^
Tree rebuilding number.

  **Avaliable Value**::

    0
    1
    2
    5
    10
    20
    50
    80
    100 (long run)

-maxiterate
^^^^^^^^^^^^^^^^
Maximum number of iterations to perform when refining the alignment.

  **Avaliable Value**::

    0
    1
    2
    5
    10
    20
    50
    80
    100 (long run)

-ffts
^^^^^^^^^^^^^^^^
Perform fast fourier transform.

  **Avaliable Mode**::

    localpair
    globalpair
    genafpair

MUSCLE
""""""""""""""""""""
-muscle
^^^^^^^^^^^^^^^^
Enable muscle.

trimAl
""""""""""""""""""""
-trimal
^^^^^^^^^^^^^^^^
Enable trimal.

-tmod
^^^^^^^^^^^^^^^^
trimal run mode.

  **Avaliable Mode**::

    automated1
    gappyout
    strict
    strictplus

-rmss
^^^^^^^^^^^^^^^^
Remove spurious sequences (residue overlap/sequence overlap).

Residue overlap means the minimum overlap of a positions with other positions in the column
to be considered a "good position".

Sequence overlap means the minimum percentage of "good positions" that a sequence must have in
order to be conserved.

Make phylogenetic tree
----------------------

-iqtree
^^^^^^^^^^^^^^^^
Enable iqtree.

-iqmod
^^^^^^^^^^^^^^^^
Run mode of iqtree.

  **Avaliable Mode**::

    TEST
    TESTNEW
    One or more spicified models

-boots
^^^^^^^^^^^^^^^^
Bootstrap number.

-rcluster
^^^^^^^^^^^^^^^^
Specify the percentage for the relaxed clustering algorithm to speed up the computation instead of
the default slow greedy algorithm.

-mtree
^^^^^^^^^^^^^^^^
Turn on full tree search for each model considered, to obtain more accurate result.

-bnni
^^^^^^^^^^^^^^^^
Perform an additional step to further optimize UFBoot trees by nearest neighbor interchange (NNI) based
directly on bootstrap alignments.

Tree Annotating
---------------
-xzoom
^^^^^^^^^^^^^^^^
Horizontal magnification, default is 1.

-yzoom
^^^^^^^^^^^^^^^^
Vertical magnification, default is 1.

-bs
^^^^^^^^^^^^^^^^
Show bootstrap support value.

-bl
^^^^^^^^^^^^^^^^
Show genomic distance value.

-bif
^^^^^^^^^^^^^^^^
Show bifurcate number.

-leg
^^^^^^^^^^^^^^^^
Generate domain legend.

-reroot
^^^^^^^^^^^^^^^^
Reroot the tree.

-marktax
^^^^^^^^^^^^^^^^
Color branches according to taxonomy.

-format
^^^^^^^^^^^^^^^^
Output image format.

  **Avaliable Type**::

    png
    pdf
    svg
