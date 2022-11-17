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

-pas
^^^^^^^^^^^^^^^^

Enable active sites prediction in Pfamscan.


Make alignment
--------------
MAFFT
""""""""""""""""""""
-mafft
^^^^^^^^^^^^^^^^
-matrix
^^^^^^^^^^^^^^^^
-op
^^^^^^^^^^^^^^^^
-ep
^^^^^^^^^^^^^^^^
-retree
^^^^^^^^^^^^^^^^
-maxiterate
^^^^^^^^^^^^^^^^
-ffts
^^^^^^^^^^^^^^^^

MUSCLE
""""""""""""""""""""
-muscle
^^^^^^^^^^^^^^^^

trimAl
""""""""""""""""""""
-trimal
^^^^^^^^^^^^^^^^
-tmod
^^^^^^^^^^^^^^^^
-rmss
^^^^^^^^^^^^^^^^

Make phylogenetic tree
----------------------

-iqtree
^^^^^^^^^^^^^^^^
-iqmod
^^^^^^^^^^^^^^^^
-boots
^^^^^^^^^^^^^^^^
-rcluster
^^^^^^^^^^^^^^^^
-mtree
^^^^^^^^^^^^^^^^
-bnni
^^^^^^^^^^^^^^^^


Tree Annotating
---------------
-xzoom
^^^^^^^^^^^^^^^^
-yzoom
^^^^^^^^^^^^^^^^
-bs
^^^^^^^^^^^^^^^^
-bl
^^^^^^^^^^^^^^^^
-bif
^^^^^^^^^^^^^^^^
-leg
^^^^^^^^^^^^^^^^
-reroot
^^^^^^^^^^^^^^^^
-marktax
^^^^^^^^^^^^^^^^
-format
^^^^^^^^^^^^^^^^
