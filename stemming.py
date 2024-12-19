import re 
import pandas as pd
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from nltk.corpus import stopwords as nltk_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize Morphology Analyzer for Lemmatization
db = MorphologyDB.builtin_db()  # Load built-in database for morphology analysis
analyzer = Analyzer(db)
# Load and clean your CSV file
df2 = pd.read_csv('diacritics_manners.csv')
df2 = df2.drop_duplicates(subset=['DiacriticsManners']).dropna()

""" # Function to remove diacritics from text
def remove_diacritics(text):
    diacritics_pattern = re.compile(r'[\u064B-\u0652\u0670]')
    return diacritics_pattern.sub('', text)

# Function to perform stemming
def stem_words(words):
    stems = []
    for word in words:
        analyses = analyzer.analyze(word)
        if analyses:
            stem = analyses[0]['stem']  # Get the stem of the word
            stems.append(remove_diacritics(stem))  # Remove diacritics from the stem
        else:
            stems.append(word)  # If no analysis found, keep the word as is
    return stems

# Function to clean, lemmatize, and stem text
def clean_lemmatize_and_stem_citation(text):
    # Tokenize the text
    tokens = simple_word_tokenize(text)
    # Apply stemming
    stemmed_tokens = stem_words(tokens)
    # Join tokens back into a string
    return ' '.join(stemmed_tokens)



# Define the character replacement function
def remplacer_caracteres(texte):
    return texte.replace('ء','ا').replace( 'ؤ','ا')

# Define Arabic stopwords (if you want to use your own list)
arabic_stopwords = set(nltk_stopwords.words('arabic'))
additional_stopwords = { 
    "في", "على", "إلى", "من", "عن", "مع", "بـ", "لـ", "كـ", "تحت",
    "فوق", "بين", "خلال", "أمام", "وراء", "حول", "دون", "عند", "بعد",
    "قبل", "بجانب", "إزاء", "إلى جانب", "حيال", "نحو", "بسبب", 
    "بواسطة", "رغم", "إضافة إلى", "وسط", "تجاه", "خارج", "داخل",
    "بينما", "مع ذلك", "على الرغم من", "إلى حد ما", "بصورة", "حسب",
    "استنادًا إلى", "حتى", "و", "أو", "ثم", "لكن", "بل"
}
arabic_stopwordss = arabic_stopwords.union(additional_stopwords)
df2['DiacriticsManners'] = df2['DiacriticsManners'].apply(lambda x: ' '.join([word for word in x.split() if word not in arabic_stopwordss]))

# Apply the function to process citations
df2['Stemming'] = df2['DiacriticsManners'].apply(clean_lemmatize_and_stem_citation)
df2['Stemming'] = df2['Stemming'].apply(clean_lemmatize_and_stem_citation)
df2['Stemming'] = df2['Stemming'].apply(remplacer_caracteres)
 """
def normalize_arabic_sentence(sentence):
    # Fonction pour supprimer les diacritiques
    def remove_diacritics(text):
        arabic_diacritics = re.compile("""
             ّ    | # Shadda
             َ    | # Fatha
             ً    | # Tanwin Fath
             ُ    | # Damma
             ٌ    | # Tanwin Damm
             ِ    | # Kasra
             ٍ    | # Tanwin Kasr
             ْ    | # Sukun
             ـ     # Tatweel
         """, re.VERBOSE)
        return re.sub(arabic_diacritics, '', text)

    # Fonction de stemming/racinisation
    def stem_arabic_word(word):
        # Suppression des préfixes courants
        word = re.sub(r'^(ال|و|ف|ب|ك|ل|لل|س)', '', word)  # Préfixes
        word = re.sub(r'^(ان|يت|مت|من|است|سي|لل)', '', word)  # Préfixes complexes
        
        # Suppression des suffixes courants
        word = re.sub(r'(ون|ات|ين|ة|ي|ا|ه|ها|هم|نا|ك|كم|كن|ت)$', '', word)  # Suffixes

        # Suppression des doublons de lettres (comme "كرّر" → "كر")
        word = re.sub(r'(.)\1+', r'\1', word)  # Simplification des répétitions

        return word

    # Nettoyage général de la phrase
    sentence = remove_diacritics(sentence)
    sentence = re.sub(r'[^\w\s]', '', sentence)  # Supprimer ponctuation
    sentence = re.sub(r'[إأآاؤء]', 'ا', sentence)  # Normaliser Alif
    sentence = re.sub(r'ى', 'ي', sentence)      # Normaliser Ya
    sentence = re.sub(r'ئ', 'ي', sentence)      # Normaliser Hamza sur Ya

    # Découper en mots et appliquer stemming
    words = sentence.split()
    normalized_words = [stem_arabic_word(word) for word in words]

    # Reconstruire la phrase normalisée
    return ' '.join(normalized_words)

df2['Stemming'] = df2['DiacriticsManners'].apply(normalize_arabic_sentence)

# Save the results to a new CSV file
df2['Stemming'].to_csv('stemming_manners.csv', index=False, encoding='utf-8-sig')

# Vectorization using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df2['Stemming'])

# Convert the matrix to a DataFrame for easy manipulation
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
tfidf_df.index = df2.index  # Ensure indices match the original DataFrame

# Concatenate TF-IDF results with the original DataFrame
df_with_tfidf = pd.concat([df2, tfidf_df], axis=1)
df_with_tfidf.drop(columns=['DiacriticsManners','Stemming'], inplace=True)  # Drop the original citation column

df_with_tfidf.to_csv('stemming_tfidf_manners.csv', index=False, encoding='utf-8-sig')
print(df_with_tfidf)  # Display the DataFrame with TF-IDF results



