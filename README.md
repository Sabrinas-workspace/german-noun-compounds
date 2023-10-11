# german-noun-compounds

This repository contains the code for my Bachelor thesis project "Automatic extraction of semantic relations in German compounds".

The packages I used for this project can be found in requirements.txt. 
The amrlib model "model_parse_xfm_bart_large-v0_1_0" which is necessary for the Parsing of the AMRs still needs to be installed. 
It can be found here: https://github.com/bjascob/amrlib-models/releases
The model should be extracted in the directory amrlib/data and renamed as model_stog.

The Ghost-NN data set (https://aclanthology.org/L16-1362/) was used for this project. It contains German noun compounds and their semantic relations. 

The modul duden was used to extract the meanings of the compounds from the Duden online dictionary. https://github.com/radomirbosak/duden

For German meaning descriptions were translated into English with DeepL. https://github.com/DeepLcom/deepl-python

The AMRs were parsed with amrlib. https://github.com/bjascob/amrlib

