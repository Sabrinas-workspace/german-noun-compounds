"""This file translates German paraphrases of compounds into English by using the DeepL API.
"""

import deepl
import pandas as pd

auth_key = "key"  # Replace "key" with your authentication key, more info: https://support.deepl.com/hc/en-us/articles/360020695820-Authentication-Key
translator = deepl.Translator(auth_key)

df = pd.read_csv('dataset_with_meanings.txt', sep="\t", header=0)

# For the analysis data set from meaning_random_50_analysis.py use the following line instead
# df = pd.read_csv('random_50_duden_result_preprocessed.txt', sep='\t', header=0)

en_translation = []

for meaning in df['Meaning']:
    result = translator.translate_text(meaning, source_lang="DE", target_lang="EN-US")
    en_translation.append(result.text)   
    
df['Translation'] = en_translation

df.to_csv('dataset_with_translations.txt', sep='\t', index=False)

# For the analysis data set from meaning_random_50_analysis.py use the following line instead
# df.to_csv('random_50_dataset_with_translations.txt', sep='\t', index=False)


# Creates the data set which is used for the classification with transfomers (not needed for data set analysis)
df_transformers = df[['Translation', 'Relation']]

# Deletes all rows with LEX compounds
df_transformers  = df_transformers.loc[df["Relation"] != "LEX"]

df_transformers.to_csv('only_translation_relation.txt', sep=';', header=None, index=False)
