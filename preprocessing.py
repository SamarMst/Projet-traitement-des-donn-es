import csv
import re
import pandas as pd
from camel_tools.tokenizers.word import simple_word_tokenize
import nltk
from nltk.corpus import stopwords as nltk_stopwords

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords')

# Define Arabic stopwords (if you want to use your own list)
arabic_stopwords = set(nltk_stopwords.words('arabic'))
additional_stopwords = {  "في",
    "على",
    "إلى",
    "من",
    "عن",
    "مع",
    "بـ",
    "لـ",
    "كـ",
    "تحت",
    "فوق",
    "بين",
    "خلال",
    "أمام",
    "وراء",
    "حول",
    "دون",
    "عند",
    "بعد",
    "قبل",
    "بجانب",
    "إزاء",
    "إلى جانب",
    "حيال",
    "نحو",
    "بسبب",
    "بواسطة",
    "رغم",
    "إضافة إلى",
    "وسط",
    "تجاه",
    "خارج",
    "داخل",
    "بينما",
    "مع ذلك",
    "على الرغم من",
    "إلى حد ما",
    "بصورة",
    "حسب",
    "استنادًا إلى",
    "حتى",
    "و",
    "أو",
    "ثم",
    "لكن",
    "بل",
    "إما",
    "لا",
    "ف"
    "ني",
    "كَ",
    "كِ",
    "هُ",
    "هَا",
    "نا",
    "كُمْ",
    "هُمْ",
    "أنا",
    "وأنا",
    "أنتَ",
    "وأنتَ"
    "أنتِ",
    "وأنتِ",
    "هو",
    "هي",
    "نحن",
    "أنتم",
    "هم",
    "إياي",
    "إياكَ",
    "إياكِ",
    "إياهُ",
    "إياها",
    "إيانا",
    "إياكم",
    "إياهم",
    "إياهن",
    "كل",
    "كلا",
    "كلتا",
    "كلا" ,
    "كلما",
     "أو",
    "ثم",
    "لكن",
    "بل",
    "إما",
    "إذا",
    "لأن",
    "بينما",
    "حيث",
    "حتى",
    "كما",
    "لكن",
    "ف",
    "مع أن"}
arabic_stopwords = arabic_stopwords.union(additional_stopwords)

# Read the CSV file
df = pd.read_csv('manners.csv')

# Check for null values in the dataframe
print(df.isnull().sum())

# Drop the rows with null values
df = df.dropna()
print(df.isnull().sum())

# Function to clean text and remove Arabic stopwords
def clean_citation(text):
    # Remove non-Arabic characters except for spaces and periods
    cleaned_text = re.sub(r'[^ء-ي\s.]', '', text)
    # Tokenize the cleaned text
    tokens = simple_word_tokenize(cleaned_text)
    # Remove stopwords using NLTK stopwords
    tokens = [word for word in tokens if word not in arabic_stopwords]
    # Join tokens back into a string
    cleaned_text = ' '.join(tokens)
    return cleaned_text

# Remove duplicate rows based on the 'Citation' column before creating CopyCitation
df = df.drop_duplicates(subset=['Citation'])

# Create a new column 'CopyCitation' with cleaned and tokenized content without stopwords
df['CopyCitation'] = df['Citation'].apply(clean_citation)

# Display the DataFrame with both Citation and CopyCitation
print(df[['CopyCitation']])

# Save the DataFrame with Citation, CopyCitation, and any other existing columns to a new CSV file
df.to_csv('manners_with_copycitation.csv', index=False, encoding='utf-8-sig')
print("Data has been saved to 'manners_with_copycitation.csv'")

""""
# Initialize the Named Entity Recognizer
ner = NERecognizer.pretrained(model_name='arabert')

# Before applying NER
print("Applying NER on cleaned citations...")

test_text = "أريد أن أذهب إلى السوق"
entities = ner.predict(test_text)
print(f"Test entities: {entities}")


# Inside the apply_ner function, print the text being processed
def apply_ner(text):
    print(f"Applying NER to: {text[:50]}...")  # Print the first 50 characters
    entities = ner.predict(text)
    print(f"Entities found: {entities}")  # Show the entities detected
    return entities

# Apply NER to the cleaned citations
df['entities'] = df['Citation'].apply(apply_ner)

# Print the cleaned DataFrame with entities
print(df[['Citation', 'entities']].head())
print(df.head())  # Check the first few rows of your DataFrame
"""
