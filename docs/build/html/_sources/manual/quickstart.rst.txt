Quick Start
==================

EPTA has a **-test** flag, which allow users test commands and paramters with a build-in
test file. All command of EPTA are usable under test mode, except **-i [Input File]**.

.. note::
  EPTA should be install under an independent Conda environment. Do not forget to activate it before start to run.

Simple Tree
---------------------------

.. image:: ../pics/simple.png
  :width: 600
  :alt: Alternative text

.. code-block:: bash

  epta -test

Annotate Domain
---------------------------

.. image:: ../pics/pfam.png
  :width: 1200
  :alt: Alternative text

.. code-block:: bash

  epta -test -pfam

Annotate Domain and Taxonomy
---------------------------

.. image:: ../pics/tax_marktax_pfam.png
  :width: 1200
  :alt: Alternative text

.. code-block:: bash

  epta -test -pfam -tax -marktax

Annotate Domain, Taxonomy and Branch Information
--------------------------

.. image:: ../pics/full.png
  :width: 1200
  :alt: Alternative text

.. code-block:: bash

  epta -test -pfam -tax -marktax -bif -bl -bs -leg
