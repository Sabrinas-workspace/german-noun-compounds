"""This file extracts the meanings of the compounds from the Duden online dictionary and preprocesses these meaning entries.
"""

import pandas as pd
import re
import duden
import meaning

df = pd.read_csv('Ghost-NN_relations.txt', sep="\t", header=0)

meanings = []
meaning_lists = {}
compounds_without_entry = []

# Finds the meaning of compounds in the Duden online dictionary and creates multiple rows for list entries (multiple meanings)
for compound in df['Compound']:
    delete_umlaut = meaning.delete_umlauts(compound)
    get_meaning = meaning.search_duden_meaning(delete_umlaut)
    if get_meaning == None:
        meanings.append(None)  
        compounds_without_entry.append(compound)
    elif isinstance(get_meaning, str):
        entry = meaning.clean_sentence(get_meaning)
        meanings.append(entry)   
    else:
        if isinstance(get_meaning[0], list):
            list_in_list = get_meaning[0]
            first_item = meaning.clean_sentence(list_in_list[0])
            meanings.append(first_item)
            del list_in_list[0]
            for element in list_in_list:
                if isinstance(element, str):
                    lentry = meaning.clean_sentence(element)
                    meanings.append(lentry)
                    index = meanings.index(lentry) - 0.5
                    find_relation = df.loc[df['Compound'] == compound, 'Relation'].iloc[0]
                    df.loc[index] = compound, find_relation
                    df = df.sort_index().reset_index(drop=True)
        else:
            first_item = meaning.clean_sentence(get_meaning[0])
            meanings.append(first_item)
        del get_meaning[0]
        for element in get_meaning:
            if isinstance(element, str):
                lentry = meaning.clean_sentence(element)
                meanings.append(lentry)
                index = meanings.index(lentry) - 0.5
                find_relation = df.loc[df['Compound'] == compound, 'Relation'].iloc[0]
                df.loc[index] = compound, find_relation
                df = df.sort_index().reset_index(drop=True)
            else:
                for list_element in element:
                    if isinstance(list_element, str):
                        lentry = meaning.clean_sentence(list_element)
                        meanings.append(lentry)
                        index = meanings.index(lentry) - 0.5
                        find_relation = df.loc[df['Compound'] == compound, 'Relation'].iloc[0]
                        df.loc[index] = compound, find_relation
                        df = df.sort_index().reset_index(drop=True)                          

df['Meaning'] = meanings

df = meaning.split_semicolon(df)      

df = meaning.remove_one_word_result_multiples(df)

# Tries to find a specific linked meaning for compounds with only one word results as a meaning entry
numbers = ["1", "2", "11"]
letters = ["a", "b", "c"]
number_letters = ["1a", "1b", "1c"]
               
for index, row in df.iterrows():
    if row['Meaning'] != None and len(row['Meaning'].split()) == 2:
        entry = (row['Meaning'].split()[0])
        entry_number = re.sub("\(|\)", "", row['Meaning'].split()[1])
        for number in numbers:
            if number == entry_number:
                del_umlaut = meaning.delete_umlauts(entry)
                new_meaning = meaning.search_duden_meaning(del_umlaut) 
                if new_meaning != None: 
                    entry_number = int(entry_number) - 1
                    result = meaning.clean_sentence(new_meaning[entry_number])
                    df.loc[index, 'Meaning'] = result
        for letter in letters:
            if letter == entry_number:
                position = letters.index(letter)
                del_umlaut = meaning.delete_umlauts(entry)
                new_meaning = meaning.search_duden_meaning(del_umlaut) 
                if new_meaning != None: 
                    result = meaning.clean_sentence(new_meaning[position])
                    df.loc[index, 'Meaning'] = result
        for numlet in number_letters:
            if numlet == entry_number:
                position = number_letters.index(numlet)
                del_umlaut = meaning.delete_umlauts(entry)
                new_meaning = meaning.search_duden_meaning(del_umlaut) 
                if new_meaning != None: 
                    result = meaning.clean_sentence(new_meaning[0][position])
                    df.loc[index, 'Meaning'] = result

# Tries to find a better definition for compounds with only one word results as meaning entry
for index, row in df.iterrows():
    if row['Meaning'] != None and len(row['Meaning'].split()) == 1: 
        entry = ' '.join(row['Meaning'].split())
        del_umlaut = meaning.delete_umlauts(entry)
        new_meaning = meaning.search_duden_meaning(del_umlaut) 
        compound = row['Compound']
        if new_meaning == None:
            df.loc[index, 'Meaning'] = None
        elif isinstance(new_meaning, str):
            new_entry = meaning.clean_sentence(new_meaning)
            df.loc[index, 'Meaning'] = new_entry
        else:
            first_item = meaning.clean_sentence(new_meaning[0])
            df.loc[index, 'Meaning'] = first_item
            del new_meaning[0]
            find_relation = df.loc[df['Compound'] == compound, 'Relation'].iloc[0]
            for element in new_meaning:
                if isinstance(element, str):
                    new_lentry = meaning.clean_sentence(element)
                    new_index = index - 0.5
                    df.loc[new_index] = compound, find_relation, new_lentry

df = meaning.split_semicolon(df) 

for index, row in df.iterrows():
    entry = row['Meaning']
    if isinstance(entry, str):                   
        df.loc[index, 'Meaning'] = meaning.remove_brackets_hyphens(entry)

df = meaning.remove_one_word_result_multiples(df)

df = df.sort_index().reset_index(drop=True)  

# Deletes the rows without a meaning entry
for index, row in df.iterrows():
    if row['Meaning'] != None and len(row['Meaning'].split()) == 1:
        df.at[index,'Meaning'] = None 

df = df.drop_duplicates()

no_entry = df['Meaning'].isnull().sum()
print("No entry in the dictionary was found for " + str(no_entry) + " compounds.")

df = df.dropna()

df.to_csv('dataset_with_meanings.txt', sep='\t', index=False)