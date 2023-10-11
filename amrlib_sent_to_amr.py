"""This file parses Abstract Meaning Representations from paraphrases of compounds.
"""

import amrlib
import pandas as pd

df = pd.read_csv('dataset_with_translations.txt', sep="\t", header=0)

translations = []
amrs = []

for translation in df['Translation']:
    translations.append(translation)

stog = amrlib.load_stog_model()
graphs = stog.parse_sents(translations)
for graph in graphs:
    amrs.append(graph)
    
df['AMR'] = amrs

df.to_csv('dataset_with_amrs.txt', sep='\t', index=False)

# The following lines are only necessary for the data set created in meaning_random_50_analysis.py since a sorted data set is easier to analyze

# df = df.sort_values(by=['Relation'])

# selection = df[['Compound', 'Relation', 'Meaning', 'Translation']]

# selection.to_csv('sorted.txt', sep='\t', index=False)