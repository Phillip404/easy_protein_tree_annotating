Download
========

Install EPTA from command line
------------------------------

You can install EPTA easily from PIPL or Annaconda

  **Full version**

  .. code-block:: bash

    -conda create -n run_epta python=3.8
    -conda activate run_epta
    -conda install epta

  **Lite version**

  .. code-block:: bash

    -conda create -n run_epta_lite python=3.8
    -conda activate run_epta_lite
    -conda install epta_lite

Download EPTA manually:
--------------------------

You can also download EPTA Lite manually:

      #. Go to our Github page : https://github.com/Phillip404/easy_protein_tree_annotating
      #. Press the green button **'Code'**
      #. Click the subtag **'Download Zip'**
      #. Unzip the zip file
      #. Download **pandas** package
      #. Download **biopython** package
      #. Download **ETE3** package
      #. Open your console, whatever it is
      #. Go to the folder you unzipped EPTA
      #. Run EPTA and check command line flags:

          .. code-block:: bash

            -python3 main.py -h

            .. Caution::

              'python3' could be a different command according to your envorinment.

              For example: python, py, py3

      #. Enjoy your tree building!
