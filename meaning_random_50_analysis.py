"""This file extracts the meanings of 50 random compounds from the Duden online dictionary and preprocesses these meaning entries. In addition, it creates a data set that is used for analysis.
"""

import pandas as pd
import re
import duden
import meaning

df = pd.read_csv('Ghost-NN_relations.txt', sep="\t", header=0)

# Creates data set used for data analysis 
random_50 = df.sample(n=50, random_state=21) 

random_50 = random_50.sort_index().reset_index(drop=True)  

# Finds the meaning of compounds in the Duden online dictionary and does not preprocess the found entries
raw_meanings = []
compounds_without_entry_raw = []

for compound in random_50['Compound']:
    delete_umlaut = meaning.delete_umlauts(compound)
    get_meaning = meaning.search_duden_meaning(delete_umlaut)
    if get_meaning == None:
        raw_meanings.append(None)  
        compounds_without_entry_raw.append(compound)
    else:
        raw_meanings.append(str(get_meaning))
                           

random_50['Raw_Meaning'] = raw_meanings
random_50.to_csv('random_50_raw_duden_result.txt', sep='\t', index=False)

no_entry = random_50['Raw_Meaning'].isnull().sum()
print("No entry in the dictionary was found for " + str(no_entry) + " compounds.")


# Finds the meaning of compounds in the Duden online dictionary and creates multiple rows for list entries (multiple meanings)
meanings = []
meaning_lists = {}
compounds_without_entry = []

for compound in random_50['Compound']:
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
                    find_relation = random_50.loc[random_50['Compound'] == compound, 'Relation'].iloc[0]
                    find_raw = random_50.loc[random_50['Compound'] == compound, 'Raw_Meaning'].iloc[0]
                    random_50.loc[index] = compound, find_relation, find_raw
                    random_50 = random_50.sort_index().reset_index(drop=True)
        else:
            first_item = meaning.clean_sentence(str(get_meaning[0]))
            meanings.append(first_item)
        del get_meaning[0]
        for element in get_meaning:
            if isinstance(element, str):
                lentry = meaning.clean_sentence(element)
                meanings.append(lentry)
                index = meanings.index(lentry) - 0.5
                find_relation = random_50.loc[random_50['Compound'] == compound, 'Relation'].iloc[0]
                find_raw = random_50.loc[random_50['Compound'] == compound, 'Raw_Meaning'].iloc[0]
                random_50.loc[index] = compound, find_relation, find_raw
                random_50 = random_50.sort_index().reset_index(drop=True)
            else:
                for list_element in element:
                    if isinstance(list_element, str):
                        lentry = meaning.clean_sentence(list_element)
                        meanings.append(lentry)
                        index = meanings.index(lentry) - 0.5
                        find_relation = random_50.loc[random_50['Compound'] == compound, 'Relation'].iloc[0]
                        find_raw = random_50.loc[random_50['Compound'] == compound, 'Raw_Meaning'].iloc[0]
                        random_50.loc[index] = compound, find_relation, find_raw
                        random_50 = random_50.sort_index().reset_index(drop=True)              

random_50['Meaning'] = meanings 

random_50 = meaning.split_semicolon_including_raw(random_50)
        
random_50 = meaning.remove_one_word_result_multiples(random_50)

# Tries to find a specific linked meaning for compounds with only one word results as a meaning entry
numbers = ["1", "2", "11"]
letters = ["a", "b", "c"]
number_letters = ["1a", "1b", "1c"]
               
for index, row in random_50.iterrows():
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
                    random_50.loc[index, 'Meaning'] = result
        for letter in letters:
            if letter == entry_number:
                position = letters.index(letter)
                del_umlaut = meaning.delete_umlauts(entry)
                new_meaning = meaning.search_duden_meaning(del_umlaut) 
                if new_meaning != None: 
                    result = meaning.clean_sentence(new_meaning[position])
                    random_50.loc[index, 'Meaning'] = result
        for numlet in number_letters:
            if numlet == entry_number:
                position = number_letters.index(numlet)
                del_umlaut = meaning.delete_umlauts(entry)
                new_meaning = meaning.search_duden_meaning(del_umlaut) 
                if new_meaning != None: 
                    result = meaning.clean_sentence(new_meaning[0][position])
                    random_50.loc[index, 'Meaning'] = result

# Tries to find a better definition for compounds with only one word results as meaning entry                   
for index, row in random_50.iterrows():
    if row['Meaning'] != None and len(row['Meaning'].split()) == 1:
        entry = ' '.join(row['Meaning'].split())
        del_umlaut = meaning.delete_umlauts(entry)
        new_meaning = meaning.search_duden_meaning(del_umlaut) 
        compound = row['Compound']
        if new_meaning == None:
            random_50.loc[index, 'Meaning'] = None
        elif isinstance(new_meaning, str):
            new_entry = meaning.clean_sentence(new_meaning)
            random_50.loc[index, 'Meaning'] = new_entry
        else:
            first_item = meaning.clean_sentence(new_meaning[0])
            random_50.loc[index, 'Meaning'] = first_item
            del new_meaning[0]
            find_relation = random_50.loc[random_50['Compound'] == compound, 'Relation'].iloc[0]
            find_raw = random_50.loc[random_50['Compound'] == compound, 'Raw_Meaning'].iloc[0]
            for element in new_meaning:
                if isinstance(element, str):
                    new_lentry = meaning.clean_sentence(element)
                    new_index = index - 0.5
                    random_50.loc[new_index] = compound, find_relation, find_raw, new_lentry
                    
random_50 = meaning.split_semicolon_including_raw(random_50) 

for index, row in random_50.iterrows():
    entry = row['Meaning']
    if isinstance(entry, str):                   
        random_50.loc[index, 'Meaning'] = meaning.remove_brackets_hyphens(entry)

random_50 = meaning.remove_one_word_result_multiples(random_50)

random_50 = random_50.sort_index().reset_index(drop=True)  

# Deletes the rows without a meaning entry
for index, row in random_50.iterrows():
    if row['Meaning'] != None and len(row['Meaning'].split()) == 1:
        random_50.at[index,'Meaning'] = None 

random_50 = random_50.drop_duplicates()

no_entry = random_50['Meaning'].isnull().sum()
print("No entry in the dictionary was found for " + str(no_entry) + " compounds.")



random_50.to_csv('random_50_duden_result.txt', sep='\t', index=False)

# Creates a data set without the unpreprocessed data
without_raw = random_50.drop('Raw_Meaning', axis=1)

without_raw.to_csv('random_50_duden_result_preprocessed.txt', sep='\t', index=False)
