# german-noun-compounds

This repository contains the code for my Bachelor thesis project "Automatic extraction of semantic relations in German compounds".

The packages I used for this project can be found in requirements.txt. 
The amrlib model "model_parse_xfm_bart_large-v0_1_0" which is necessary for the Parsing of the AMRs still needs to be installed. 
It can be found here: https://github.com/bjascob/amrlib-models/releases
The model should be extracted in the directory amrlib/data and renamed as model_stog.

The Ghost-NN data set (https://aclanthology.org/L16-1362/) was used for this project. It contains German noun compounds and their semantic relations. 

The Python module duden was used to extract the meanings of the compounds from the Duden online dictionary. https://github.com/radomirbosak/duden
For the extraction of the meanings from Duden meaning_extraction.py needs to be executed.
I analyzed the results of 50 random compounds of the data set. To generate this data set I used meaning_random_50_analysis.py.

The German meaning descriptions were translated into English with DeepL. https://github.com/DeepLcom/deepl-python
This is implemented in translation_to_en.py

The AMRs of these translations were parsed with amrlib. https://github.com/bjascob/amrlib
For this amrlib_sent_to_amr.py has to be executed. 

A data set with features was generated in feature_engineering.py which was then used for multiclass-classification in compound_relation_classification_with_sklearn.ipynb.

Finally, a multiclass-classification with a pretrained transformer model was performed in compound_classification_transformers.ipynb.
