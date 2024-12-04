import pandas as pd
import ast  # To parse the string representation of lists
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.database import MorphologyDB
from camel_tools.utils.dediac import dediac_ar

# Load and clean your CSV file
df = pd.read_csv('cleaned_manners.csv')

# Initialize Morphology Analyzer for Lemmatization
db = MorphologyDB.builtin_db()  # Load built-in database for morphology analysis
analyzer = Analyzer(db)

def stem_arabic_tokens(tokens):
    """
    Function to stem a list of Arabic tokens using Camel Tools.
    """
    stemmed_tokens = []
    for token in tokens:
        analysis = analyzer.analyze(token)
        if analysis:  # Check if any analysis exists
            stemmed_token = analysis[0]['stem']  # Use the first stem from the analysis
            stemmed_tokens.append(stemmed_token)
        else:
            stemmed_tokens.append(token)  # If no stem found, keep the original token
    return stemmed_tokens

def process_stemming(row):
    """
    Function to process a string representation of tokenized words,
    parse it into a list, and stem the tokens.
    """
    try:
        # Convert the string representation of the list into an actual list
        tokens = ast.literal_eval(row)
        if isinstance(tokens, list):
            # Apply stemming
            return stem_arabic_tokens(tokens)
        else:
            return []  # Return an empty list if the input is not a valid list
    except (ValueError, SyntaxError):
        return []  # Return an empty list if parsing fails

# Apply stemming to each row
df['Stemmed_tokens'] = df['Cleaned_Citation'].apply(process_stemming)
df['Stemmed_tokens'] = df['Stemmed_tokens'].apply(lambda x: dediac_ar(' '.join(x)))
def tokenize_arabic_text(text):
    """
    Function to tokenize Arabic text.
    """
    # Simple whitespace tokenization
    return text.split()

# Apply tokenization to each row before stemming
df['Tokenized_Citation'] = df['Stemmed_tokens'] .apply(tokenize_arabic_text)

df.to_csv('stemmed_manners.csv', index=False, encoding='utf-8')



