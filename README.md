# Easy Protein Tree Annotating

Introduction：
---------------

EPTA, the abbreviation of Easy Protein Tree Annotating, is a user-friendly protein tree generation and annotating tool. EPTA takes the FASTA file as input and outputs a protein phylogenetic tree with annotated taxonomy and domain of each sequence automatically. EPTA has 40 parameters to ensure users can run it more flexibly, and it is also capable of running on Windows, Linux, and Mac operating systems.

Installation：
---------------
EPTA has been packaged and distributed as a Conda package. For more information, check the [**Manual Pgae**](https://easy-protein-tree-annotating.readthedocs.io/en/latest/download/download.html#install-epta).

**Conda channel:** https://anaconda.org/phillip404/repo


Features and Functionality:
---------------

**Protein Sequence Input:** PhyloTreeAnnotator accepts protein sequence data in FASTA formats. It supports single or multiple sequence inputs, allowing for comprehensive phylogenetic analysis.

**Multiple Alignment:** The tool performs sequence alignment using  MAFFT and MUSCLE to generate high-quality multiple sequence alignments.

**Phylogenetic Tree Generation:** EPTA introduced IQ-TREE to generate phylogenetic trees. IQ-TREE employs robust algorithms and tests a reasonable amount of models to find the best fit to construct phylogenetic trees from the aligned protein sequences. The tool provides options to select the most appropriate algorithm based on the user's requirements.

**Tree Visualization:** The generated phylogenetic tree can be visualized using various levels of tree-viewing options, such as annotated trees with taxonomy information, trees with annotated domains, etc. This allows users to explore and analyze the evolutionary relationships in a visually appealing manner.

**Annotation and Customization:** EPTA offers extensive annotation capabilities to enhance the interpretation of the phylogenetic tree. Users can label branches with taxonomic information, display bootstrap support values, and color-code branches based on specific characteristics or attributes.

**Export and Sharing:** The tool allows users to save the tree as an image (e.g., PNG, SVG).

**Advanced Analysis Options:** EPTA includes advanced features such as relocate root bifurcation, branch length optimization, and statistical tests for branch support assessment. These options enable users to conduct in-depth evolutionary analyses and refine their understanding of phylogenetic relationships.

**User-Friendly Interface:** The tool offers an intuitive and user-friendly command-line-based interface, making it accessible to researchers and bioinformaticians with varying levels of expertise. The interface provides clear instructions, tooltips, and example datasets to assist users throughout the analysis process.

**Compatibility and Performance:** EPTA is designed to run efficiently on different performance platforms and operating systems. It utilizes web server computing capabilities to handle large datasets, ensuring optimal performance on low-performance platforms.

**Documentation and Support:** The tool provides comprehensive documentation, including tutorials, FAQs, and user guides, to assist users in utilizing its features effectively. 
**Manual Page:** https://easy-protein-tree-annotating.readthedocs.io/en/latest/
