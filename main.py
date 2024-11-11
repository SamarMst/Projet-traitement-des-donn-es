import re
from camel_tools.sentiment import SentimentAnalyzer 
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.tokenizers.word import simple_word_tokenize
import pandas as pd

data = pd.read_csv('manners.csv')
citation = data['Citation']
##########  Preprocessing the Data ##########
# Function to remove symbols from each word
def clean_words(word_list):
    cleaned_words = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in word_list]
    return cleaned_words
cleaned_list = clean_words(citation)
print(cleaned_list)
