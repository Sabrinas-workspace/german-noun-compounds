"""This file parses Abstract Meaning Representations from paraphrases of compounds.
"""

# The model "model_parse_xfm_bart_large-v0_1_0" needs to be installed to execute the code in this file, it can be found here : https://github.com/bjascob/amrlib-models/releases

import amrlib
import pandas as pd

df = pd.read_csv('dataset_with_translations.txt', sep="\t", header=0)

# For the analysis data set from meaning_random_50_analysis.py use the following line instead
# df = pd.read_csv('random_50_dataset_with_translations.txt', sep='\t', header=0)

translations = []
amrs = []

for translation in df['Translation']:
    translations.append(translation)

stog = amrlib.load_stog_model()
graphs = stog.parse_sents(translations)
for graph in graphs:
    amrs.append(graph)
    
df['AMR'] = amrs

for index, row in df.iterrows():
    amr = row['AMR']
    start = amr.find('\n(')
    clean_entry = amr[start:]
    df.at[index,'AMR'] = clean_entry

df.to_csv('dataset_with_amrs.txt', sep='\t', index=False)


# The following lines are only necessary for the data set created in meaning_random_50_analysis.py since a sorted data set is easier to analyze

# df = df.sort_values(by=['Relation'])

# df.to_csv('random_50_dataset_with_amrs_sorted.txt', sep='\t', index=False)