"""This module preprocesses the data that can be extracted from the Duden online dictionary.

   Functions:
   delete_umlauts(string) -> string
   remove_brackets_hyphens(string) -> string
   remove_nonessential_words_symbols(string) -> string
   remove_abbreviations(string) -> string
   remove_dot(string) -> string
   clean_sentence(string) -> string
   remove_one_word_result_multiples(pandas.DataFrame) -> pandas.DataFrame
   split_semicolon(pandas.DataFrame) -> pandas.DataFrame
   split_semicolon_including_raw(pandas.DataFrame) -> pandas.DataFrame
"""

import re
import duden

def delete_umlauts(text: str):
    """Converts German diacritics to the respective non-diacritic equivalent.

    Args:
        text: A string.

    Returns:
        The string without diacritics.
    """   
    umlauts = {ord('ä'):'ae', ord('ö'):'oe', ord('ü'):'ue', ord('ß'):'sz'}
    return text.translate(umlauts)

def remove_brackets_hyphens(text: str):
    """Removes square brackets, hyphens and curved brackets including the text inside them.

    Args:
        text: A string.

    Returns:
        The string without square brackets, hyphens and curved brackets and the text that was inside the curved brackets.
    """   
    return re.sub(" \(.*?\)|\(.*?\) |\[|\]|–[^–]+– ", "", text)

def remove_nonessential_words_symbols(sentence: str):
    """Removes symbols and phrases that are not part of the definition of a word.

    Args:
        sentence: A string.

    Returns:
        The string without these symbols and phrases.
    """ 
    if '💡' in sentence:
        index = sentence.find('\n\n💡')
        sentence = sentence[:index]
    if 'Kurzform für' in sentence:
        index = sentence.find('\n')
        index = index + 2
        sentence = sentence[index:]   
    if 'Kurzform' in sentence:
        index = sentence.find('\nKurzform')
        sentence = sentence[:index]
    if 'Abkürzung' in sentence:
        index = sentence.find('\nAbkürzung')
        sentence = sentence[:index]
    if 'Kurzwort für' in sentence:
        index = sentence.find('\n')
        index = index + 2
        sentence = sentence[index:]   
    if 'Kurzwort' in sentence:
        index = sentence.find('\nKurzwort')
        sentence = sentence[:index]
    if '\n\nHerkunft' in sentence:
        index = sentence.find('\n\nHerkunft')
        sentence = sentence[:index]
    if '\nHerkunft' in sentence:
        index = sentence.find('\nHerkunft')
        sentence = sentence[:index]
    return sentence

def remove_abbreviations(sentence: str):
    """Removes the abbreviations "o. Ä.", "o. ä.", "u.a.", and "u. Ä.".
    Args:
        sentence: A string.

    Returns:
        The string without the abbreviations.
    """ 
    abbreviations = [" o. Ä.", " o. ä.", " u. a.", " u. Ä."]
    for word in abbreviations:
        sentence = sentence.replace(word, "")
    return sentence

def remove_dot(sentence: str):
    """Removes dots from a string if it does not contain "bzw.".

    Args:
        sentence: A string.

    Returns:
        The string without dots.
    """ 
    if "bzw." not in sentence:
        return re.sub("\.", "", sentence)
    else:
        return sentence
    
def clean_sentence(sentence: str):
    """Applies the functions del_abbreviations, del_dots and clean_sentence to a string.

    Args:
        sentence: A string.

    Returns:
        The string after those functions were applied.
    """ 
    del_abbreviations = remove_abbreviations(sentence)
    del_dots = remove_dot(del_abbreviations)
    clean_sentence = remove_nonessential_words_symbols(del_dots)
    return clean_sentence

def search_duden_meaning(word: str):
    """Extracts the meaning of a word from the Duden online dictionary.

    Args:
        word: A string containing one word.

    Returns:
        The meaning of a word or None if no entry can be found in the dictionary.
    """ 
    without_umlauts = delete_umlauts(word)
    search_word = duden.get(without_umlauts)
    if search_word != None:
        meaning = search_word.meaning_overview
        if meaning == "":
            return None
        else:
            return meaning
    else:
        return None 


def remove_one_word_result_multiples(df):
    """Removes meanings containing only one word for compounds that have multiple entries in the data frame.

    Args:
        df: A pandas.DataFrame with the columns Meaning and Compound.

    Returns:
        The pandas.DataFrame without the one word results for compounds that have multiple meaning entries.
    """ 
    for index, row in df.iterrows():
        if row['Meaning'] != None and len(row['Meaning'].split()) == 1: #only synonym as meaning
            if df['Compound'].value_counts()[row['Compound']] > 1:
                word = row['Compound']
                count = df['Compound'].value_counts()[word]
                number = 0
                multiple = []
                while number < count:
                    find_meaning = df.loc[df['Compound'] == word, 'Meaning'].iloc[number]
                    multiple.append(find_meaning)
                    number = number + 1
                for result in multiple:
                    delete = False
                    if len(result.split()) > 1: 
                        delete = True
                        for result in multiple:
                            if len(result.split()) == 1 and delete is True:
                                if row['Meaning'] == result:
                                    df = df[df.Meaning != result]           
    return df

def split_semicolon(df):
    """Creates a new row in the data frame if the meanings of a compound are seperated by a semicolon.

    Args:
        df: A pandas.DataFrame with the columns Meaning, Relation and Compound.

    Returns:
        The pandas.DataFrame with a row for each meaning of a compound that has multiple meanings that were seperated by a semicolon.
    """ 
    for index, row in df.iterrows():
        if row['Meaning'] != None and ";" in row['Meaning']: 
            compound = row['Compound']
            result_list = row['Meaning'].split("; ")
            find_relation = df.loc[df['Compound'] == compound, 'Relation'].iloc[0]
            df.loc[index] = compound, find_relation, result_list[0]
            del result_list[0]
            index = index - 0.5
            for result in result_list:
                df.loc[index] = compound, find_relation, result    
    return df

def split_semicolon_including_raw(df):
    """Creates a new row in the data frame if the meanings of a compound are seperated by a semicolon.

    Args:
        df: A pandas.DataFrame with the columns Meaning, Raw_Meaning, Relation and Compound.

    Returns:
        The pandas.DataFrame with a row for each meaning of a compound that has multiple meanings that were separated by a semicolon.
    """ 
    for index, row in df.iterrows():
        if row['Meaning'] != None and ";" in row['Meaning']: 
            compound = row['Compound']
            result_list = row['Meaning'].split("; ")
            find_relation = df.loc[df['Compound'] == compound, 'Relation'].iloc[0]
            find_raw = df.loc[df['Compound'] == compound, 'Raw_Meaning'].iloc[0]
            df.loc[index] = compound, find_relation, find_raw, result_list[0]
            del result_list[0]
            for result in result_list:
                index = index - 0.5
                df.loc[index] = compound, find_relation, find_raw, result    
    return df