"""This file translates German paraphrases of compounds into English by using the DeepL API.
"""

import deepl
import pandas as pd

auth_key = "key"  # Replace "key" with your key
translator = deepl.Translator(auth_key)

df = pd.read_csv('dataset_with_meanings.txt', sep="\t", header=0)

en_translation = []

for meaning in df['Meaning']:
    result = translator.translate_text(meaning, source_lang="DE", target_lang="EN-US")
    en_translation.append(result.text)   
    
df['Translation'] = en_translation

df.to_csv('dataset_with_translations.txt', sep='\t', index=False)