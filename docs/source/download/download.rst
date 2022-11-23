Download
========

Before Installation
------------------------------
EPTA needs Conda and Bioconda channel to complete the installation.

  **Download Conda**:

  `Conda Download Tutorial <https://conda.io/projects/conda/en/latest/user-guide/install/download.html>`_

  `Mniconda Download (Recommended) <https://docs.conda.io/en/latest/miniconda.html>`_

  `Anaconda Download <https://www.anaconda.com/products/distribution>`_

  **Add Bioconda Channel**:

  .. code-block:: bash

    conda config --add channels defaults
    conda config --add channels bioconda
    conda config --add channels conda-forge
    conda config --set channel_priority strict

  `Bioconda Homepage <https://bioconda.github.io/>`_

Install EPTA
------------------------------

Standalone Version (**Linux**):

  .. code-block:: bash

    conda create -n epta python=3.8
    conda activate epta
    conda config --set channel_priority flexible
    conda install -c phillip404 epta -y

Lite version:

  **Linux & MacOS**

  .. code-block:: bash

    conda create -n epta-lite python=3.8
    conda activate epta-lite
    conda config --set channel_priority flexible
    conda install -c phillip404 epta-lite -y

  **Windows (>=Windows 10)**

  .. code-block:: bash

    conda create -n epta-lite python==3.8.13
    conda activate epta-lite
    conda config --set channel_priority flexible
    conda install -c phillip404 epta-lite --only-deps -y
    pip install https://github.com/Phillip404/easy_protein_tree_annotating/raw/main/Packaging/Windows/epta-lite-1.0.tar.gz

Standalone Version For Windows 10 or Higher:
--------------------------

Windows 10 and higher supports Linux subsystem, thus a standalone version could be run under such
a subsystem on Windows platform:

    Standalone version **Installation**:
      #. Open **Microsoft Store**
      #. Search **Ubuntu**
      #. Install **Unbuntu**
      #. Type **bash** in Windows search bar and open it
      #. Follow the tutorial above to install the **Standalone version**.

    **Run** Standalone version:
      1. Close all Linux subsystem instance
      2. Download and install **Xserver** as graphic output connector from `vcxsrv Download <https://sourceforge.net/projects/vcxsrv/>`_
      3. Install **Xserver** in **full mode**
      4. Open **Xlaunch** set it as following:

        STEP 1:

        .. image:: ../pics/xs1.png
          :width: 450
          :alt: Alternative text


        STEP 2:

        .. image:: ../pics/xs2.png
          :width: 450
          :alt: Alternative text


        STEP 3:

        .. image:: ../pics/xs3.png
          :width: 450
          :alt: Alternative text
        .. note::
          It is crucial to pick the option **Disable access control** in this step.


        STEP 4:

        .. image:: ../pics/xs4.png
          :width: 450
          :alt: Alternative text

      5. Open **bash** window
      6. Active EPTA environment and run EPTA
