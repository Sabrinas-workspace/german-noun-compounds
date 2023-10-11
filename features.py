"""This module generates features from Abstract Meaning Representations and saves the results for each AMR (0 (the AMR does not have this feature) or 1 (the AMR does have this feature).

   Functions:
   focus_numbers(pandas.DataFrame) -> list
   focus_and_or(string, pandas.DataFrame) -> list
   focus_entity(pandas.DataFrame) -> list
   focus_word(string, pandas.DataFrame) -> list
   part_of_AMR(string, pandas.DataFrame) -> list
   first_role(string, pandas.DataFrame) -> list
   count_lower(string, integer, pandas.DataFrame) -> list
   count_higher(string, integer, pandas.DataFrame) -> list
   relation_in_amr(pandas.DataFrame) -> list
   end_brackets(string, integer, pandas.DataFrame) -> list
   POS_occurance(string, integer, pandas.DataFrame) -> list
   first_POS(string, pandas.DataFrame) -> list
"""

import pandas as pd
import re
from collections import Counter
import spacy

def focus_numbers(df):
    """Checks if the root of an AMR contains a number.

    Args:
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if its root contains a number or not.
    """   
    feature_list = []
    for index, row in df.iterrows():
        amr = row['AMR']
        focus = amr.find('/') + 1
        word = amr[focus:].split()[0]
        num = re.compile('\d')
        if num.search(word) != None:
            feature_list.append(1)
        else:
            feature_list.append(0)
    return feature_list

def focus_and_or(and_or: str, df):
    """Checks if the root of an AMR contains "and" or "or".

    Args:
        and_or: A string containg either "and" or "or".
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if its root contains "and"/ "or" or not.
    """  
    feature_list = []
    for index, row in df.iterrows():
        amr = row['AMR']
        focus = amr.find('/') + 1
        word = amr[focus:].split()[0]
        if word == and_or:
            feature_list.append(1)
        else:
            feature_list.append(0)
    return feature_list

def focus_entity(df): 
    """Checks if the root of an AMR does not contain numbers, "and" or "or".

    Args:
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if its root does not contain numbers, "and" or "or" or not.
    """ 
    feature_list = []
    for index, row in df.iterrows():
        amr = row['AMR']
        focus = amr.find('/') + 1
        word = amr[focus:].split()[0]
        num = re.compile('\d') 
        if word != 'and' and word != 'or' and num.search(word) == None:
            feature_list.append(1)
        else:
            feature_list.append(0)
    return feature_list

def focus_word(concept: str, df): 
    """Checks if the root of an AMR contains a specific AMR concept.

    Args:
        concept: An AMR concept.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if its root contains the concept or not.
    """ 
    feature_list = []
    for index, row in df.iterrows():
        amr = row['AMR']
        focus = amr.find('/') + 1
        word = amr[focus:].split()[0]
        if word == 'and' or word == 'or':
            word = amr[focus:].split()[4] 
        word = re.sub("\)", "", word)
        if word == concept:
            feature_list.append(1)
        else:
            feature_list.append(0)
    return feature_list

def part_of_AMR(word: str, df):
    """Checks if an AMR contains a specific AMR relation or a specific word.

    Args:
        word: An AMR relation or a specific word.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if it does contain the AMR relation/the word.
    """ 
    in_AMR = []
    for index, row in df.iterrows():
        amr = row['AMR']
        if word in amr:
            in_AMR.append(1)
        else:
            in_AMR.append(0)
    return in_AMR 

def first_role(role: str, df):
    """Checks if a specific PropBank argument or :mod is the first AMR relation that occurs in an AMR.

    Args:
        role: A PropBank argument :ARGX or :mod.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if the argument/mod is the first AMR relation that occurs in an AMR.
    """ 
    first_roles = []
    for index, row in df.iterrows():
        amr = row['AMR']
        first_role = ""
        focus = amr.find("/") + 1
        if len(amr[focus:].split()) > 1:
            first_role = amr[focus:].split()[1]
            if ":op" in first_role:
                first_role = amr[focus:].split()[5]
                if ":op" in first_role and len(amr[focus:].split()) > 9:
                    first_role = amr[focus:].split()[9]
                    if ":op" in first_role and len(amr[focus:].split()) > 13:
                        first_role = amr[focus:].split()[13]
                        if ":op" in first_role and len(amr[focus:].split()) > 17:
                            first_role = amr[focus:].split()[17]
        if role == first_role:
            first_roles.append(1)
        else:
            first_roles.append(0)
    return first_roles      

def count_lower(countOfWhat: str, number: int, df):
    """Checks if an AMR contains less than a specific number of nodes or line breaks.

    Args:
        countOfWhat: A string containing what should be counted.
        number: An integer to check if the count of nodes/line breaks is lower than this number.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if it does contain less nodes/line breaks than the specific number.
    """ 
    counts = []
    for index, row in df.iterrows():
        amr = row['AMR']
        nodes_count = amr.count(countOfWhat)
        if nodes_count < number:
            counts.append(1)
        else:
            counts.append(0)
    return counts

def count_higher(countOfWhat: str, number: int, df):
    """Checks if an AMR contains more than a specific number of nodes or line breaks.

    Args:
        countOfWhat: A string containing what should be counted.
        number: An integer to check if the count of nodes/line breaks is higher than this number.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if it does contain more nodes/line breaks than the specific number.
    """ 
    counts = []
    for index, row in df.iterrows():
        amr = row['AMR']
        nodes_count = amr.count(countOfWhat)
        if nodes_count > number:
            counts.append(1)
        else:
            counts.append(0)
    return counts

def relation_in_amr(df):
    """Checks if the semantic relation occurs literally in an AMR.

    Args:
        df: A pandas.DataFrame with the columns AMR and Relation.

    Returns:
        A list of 0s and 1s indicating for each AMR if it does contain the AMR relation/the word.
    """ 
    relationAMR = []
    for index, row in df.iterrows():
        amr = row['AMR']
        rel = " " + row['Relation'] + "-"
        if rel.lower() in amr:
            relationAMR.append(1)
        else:
            relationAMR.append(0)
    return relationAMR

def end_brackets(operator: str, number: int, df):
    """Checks if an AMR has more than or equal to a specific number of closing brackets at the end.

    Args:
        operator: This string indicates if an equal or greater count should be checked.
        number: An integer to check if the count of closing brackets is equal to or higher than this number.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if it does end with more/equal closing brackets than the specific number.
    """ 
    closing_brackets = []
    for index, row in df.iterrows():
        amr = row['AMR']
        focus = amr.find("/") + 1
        last_word = amr[focus:].split()[-1]
        count_brackets = last_word.count(')')
        if operator == "equal":
            if count_brackets == number:
                closing_brackets.append(1)
            else:
                closing_brackets.append(0)
        if operator == "greater":
            if count_brackets > number:
                closing_brackets.append(1)
            else:
                closing_brackets.append(0)    
    return closing_brackets

def POS_occurance(pos_type: str, number: int, df):
    """Checks how often a specific part of speech occurs in an AMR.

    Args:
        pos_type: A string indicating which part of speech should be counted.
        number: An integer to check if the count of occurances of a specific part of speech is higher than this number.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if it does have more occurances of a specific part of speech than the specific number.
    """ 
    pos_tag = []
    nlp = spacy.load("en_core_web_sm")
    for index, row in df.iterrows():
        amr = row['AMR']
        if "-" in amr:
            amr = re.sub("-(0[1-9]|[1-9][0-9])", "", amr)
        doc = nlp(amr)
        count = 0
        for token in doc:
            if token.pos_ == pos_type:
                count = count + 1
        if count > number:
            pos_tag.append(1)      
        else:
            pos_tag.append(0)
    return pos_tag

def first_POS(pos_type: str, df):
    """Checks if the first occuring concept in an AMR is a specific part of speech.

    Args:
        pos_type: A string indicating which part of speech should be checked.
        df: A pandas.DataFrame with the column AMR.

    Returns:
        A list of 0s and 1s indicating for each AMR if the first concept is a specific part of speech or not.
    """ 
    first_pos_tag = []
    nlp = spacy.load("en_core_web_sm")
    for index, row in df.iterrows():
        amr = row['AMR']
        if "-" in amr:
            index = amr.find('-')
            amr = amr[:index]
        focus = amr.find("/") + 1
        word = amr[focus:].split()[0]
        word = re.sub("\)", "", word)
        doc = nlp(word)
        for token in doc:
            if token.pos_ == pos_type:
                first_pos_tag.append(1)
            else: 
                first_pos_tag.append(0)
    return first_pos_tag