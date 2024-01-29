# Bioclear_earth

## Overview

The data provided by Bioclear Earth. This data is the result from Next Generation Sequencing data, also known as NGS. The data contains 6 different files. To start off, there is a txt file that explains the content of 4 of the other files.
The file that is anonymized is the Mapping.txt file. This file contains anonymised data with the sample id's, 4 unknown variables and per variable there are multiple unexplained abbrevations.
The first explained file is is ASV.fa, this fasta file contains the unique amplicon sequence variant sequences for the samples.
The second explained file is ASV_counts.txt, in this file is an abundance table created by mapping the found asv's to the sequences of the samples.
The third explained file is ASV_taxonomy.txt, this file has the taxonomy for the found asv's. The taxonomy is split up in 7 taxonomic ranks. The ranks are Domain, Phylum, Class, Order, Family, Genus and Species.
The fourth explained file is Blast_results.txt, this file is used to double check the taxonomy using only species. This is done because of taxonomy classification errors.

## Files and Directories

Explain the organization of your project's files and directories.

- `/scripts`: Includes any scripts or code used for data processing.
- `/analyse`: Includes the EDA that analyses the data.
- `/docs`: Documentation files, including this README.

## Usage

To use the data a couple of steps have to be taken. In order to continue the research on this data,
permission will have to be asked from Bioclear Earth. For any questions regarding the used data, please contact Bioclear 
Earth, which can be done via the link at the bottom of the readme.

### Installation

To be able to run the code, certain tools have to be installed.

* Python version 3.10
* Jupyter Notebook

### Imports

Multiple import statements have been used to be able to produce the code. In some cases, the use of a pip command might
be necessary if the system does not have the library yet.
This can look like: pip install dash-bio==1.0.1

```python
# Load data using Python
import pandas as pd
import panel as pn
import plotly.graph_objects as go
pd.options.plotting.backend = 'holoviews'
from bokeh.plotting import figure
import plotly.express as px
import numpy as np
from dash import Dash, html
import dash_bio as dashbio
from Bio import SeqIO
```

## References
Bioclear Earth: https://bioclearearth.nl/

## Contact
For direct contact with Bioclear Earth, the link to the website can be used: https://bioclearearth.nl/

Cheyenne Brouwer: e.h.b.brouwer@st.hanze.nl
