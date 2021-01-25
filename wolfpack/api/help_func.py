"""Some help functions."""
import math
import re
import wolfpack

def Intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


def split_words(query):
    """Split words in the query."""
    query = query.split(' ')
    words = []
    for word in query:
        word = re.sub(r'[^a-zA-Z0-9]+', '', word).lower()
        if word in wolfpack.stopwords or word == '':
            continue
        if word not in words:
            words.append(word)
    return words