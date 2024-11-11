<<<<<<< HEAD
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

words = ['يا ابن آدم',
'وقال عمر بن الخطاب (رضي الله عنه)','قال عمر بن الخطاب (رضي الله عنه)','قال عمر بن الخطاب','رضي الله عنه','و كما قال الحسن البصري','كما قال الحسن البصري','قال الحسن البصري','وقال علي بن أبي طالب',
'وقال علي بن أبي طالب','قال علي بن أبي طالب','فقال','وكما قال عبد الله بن مسعود','كما قال عبد الله بن مسعود','قال أبو علي الدقاق','وقال أبو علي الدقاق','وكما قال عمر بن عبد العزيز','قال عمر بن عبد العزيز','وكما قال أبو محمد الجريري','قال أبو محمد الجريري','قال الحسن','الحِرمان. (الورّاق)','قال: الطَّمع فيها ثُمَّ لا ينالها','(الإمام جَعفر الصَّادق)',
'(أناتول فرانس)','(بوبليليوس سيروس)','(نابليون بونابرت)','(علي الطنطاوي)','(نبال قندس)','(عوف الكلبي)','(باولو كويلّو)','(مثل هولندي)','(ابن الأحمر)','(قول عربي)','(حديث صحيح)','(كاليماكوس)','(مثل فرنسي)','(سلفستر دوساسي)','(مثل إسباني)','(توماس بين)','(هاروكي موراكامي)','(جان جاك روسّو)','(حديث شريف- صحيح البخاري)','(شارلز ديكينز)','(باولو كويلّو)','(كوفي أنان)','(فوفنارغ)','(أكثم بن صيفي التَّميمي)','(عبد الله بن عمر)','(الإمام الشَّافعي','علي الطّنطاوي','روبرت سيرفس',
'مارلين فوس زافانت','علي بِن أبي طالِب','دعبل الخُزاعي','عمر أبو الغارات','عُمر بن الخطّاب','أبو العتاهية','ابن خُبيق الأنطاكي','الحرّالي','ابن القيّم','وَهب بن منبه','الحسن البصري','عُمر بن عبد العزيز','أبو العطاء السّندي','ابن عبّاس','خليل مطران','بكر بن عبدالله','هزّال القُريعي','مريد البرغوثي','الحرّالي','علي ين أبي طالب','لُقمان الحكيم','الإمام الشّافعي','هارون الرّشيد','ابن المقري','علي بن عبد العزيز القاضي الجرجاني','الحادرة الذبياني','ثابت بن قطنة','أبو حامٍ الغزالي','حديث نبوي - رواه مُسلم',
'العتبي الرشيد','يوهان دينه','أندريه موروا','فؤاد زكريَّا','عبّاس محمود العقّاد','أمين مَعلوف','وليَم شكسبير','ابن عاشور','حديث نبوي/ رواه البُخاريّ','المهاتما غاندي','فرانكلين روزفلت','مُنذِر القبَّاني','فريدريك نيتشه','فولتير','نِزار قبّاني','وليام شكسبير','روجر فريتس','مُصطفى مَحمود','مُحمَّد الرَّطبان','مارك توين','حديث شريف/ رواه أبو داود','[U+200F]','[9438] رواه ابنُ المبارك في   ((الزهد)) (2/19)، وأبو نعيم في ((حلية الأولياء)) (1/212) واللفظ له، وابن عساكر   في ((تاريخ دمشق)) (47/160).',
'رَضِيَ اللهُ عنه','قال أبو الدَّرداءِ','[9439] ((الدر المنثور)) للسيوطي   (1/61).','- وقال الحَسَنُ:)','- وقال الثَّوريُّ','[9440] ((الدر المنثور)) للسيوطي   (1/61)، ((حلية الأولياء)) لأبي نعيم (7/284) وفيه عن سفيانَ بنِ عُيَينةَ رحمه   اللهُ.','[9441] رواه أحمد في ((الورع))   (178).','- ورُويَ عن','ابنِ عُمَرَ','رَضِيَ اللهُ عنهما قال:','[9441] رواه أحمد في ((الورع))   (178).','وقال ميمونُ بنُ مِهرانَ:','[9442] ((الورع)) لأحمد بن حنبل   (ص: 53)، ((حلية الأولياء)) لأبي نعيم (4/84).','- وقال','سُفيانُ بنُ عُيَينةَ','[9443] ((الورع)) لأحمد بن حنبل   (ص: 146).',
'إبراهيمُ بنُ أدهَمَ','[9444] ((الرسالة القشيرية))   (1/233).','وقال إسحاقُ بنُ خَلَفٍ:','[9445] ((الزهد الكبير)) للبيهقي   (ص: 319)، ((تاريخ دمشق)) لابن عساكر (8/205).',
' وقال أبو سُلَيمانَ الدَّارانيُّ:','[9446] ((الزهد)) لابن أبي الدنيا   (ص: 159).','[9447] ((الزهد الكبير)) للبيهقي   (ص: 316).','وقال يحيى بنُ مُعاذٍ:','وقال: (الوَرَعُ على وجهينِ:','[9448] ((الزهد الكبير)) للبيهقي   (ص: 318).','[9449] ((الرسالة القشيرية))   (1/234).','[9450] ((الرسالة القشيرية))   (1/235).','يونُسُ بنُ عُبيدٍ:','[9450] ((الرسالة القشيرية))   (1/235).','سُفيانُ'
'الثَّوريُّ','[9451] ((الرسالة القشيرية))   (1/235).','وقال الحَسَنُ:','[9452] ((الرسالة القشيرية))   (1/236).','وقال أبو هُرَيرةَ رَضِيَ اللهُ عنه:','[9453] ذكره القشيري في ((الرسالة   القشيرية)) (1/236).','وقال بعضُ الصَّحابةِ:','[9454] ((إحياء علوم الدين))   للغزالي (4/490)، ((مدارج السالكين)) لابن القيم (2/25).','[9455] ((مدارج السالكين)) لابن   القيم (2/25).','وقال الهَرَويُّ:','وقال ابنُ مِسكَوَيهِ:','[9456] ((تهذيب الأخلاق)) (ص:   29).','وقال سُفيانُ:','[9457] ((الورع)) لابن أبي الدنيا   (ص: 112).'
]

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
arabic_stopwords = arabic_stopwords.union(additional_stopwords)

# Load and clean your CSV file
df = pd.read_csv('manners.csv')
df = df.drop_duplicates(subset=['Citation']).dropna()

# Function to perform stemming
def stem_words(words, override_stems=None):
    stems = []
    for word in words:
        # Check if the word has an override
        if override_stems and word in override_stems:
            stems.append(override_stems[word])
        else:
            analyses = analyzer.analyze(word)
            if analyses:
                stems.append(analyses[0]['stem'])  # Get the stem of the word
            else:
                stems.append(word)  # If no analysis found, keep the word as is
    return stems

# Function to remove specified phrases from text
def remove_phrases(text, phrases):
    for phrase in phrases:
        text = text.replace(phrase, '')  # Remove each phrase
    return text

# Function to clean, lemmatize, and stem text
def clean_lemmatize_and_stem_citation(text, phrases, override_stems=None):
    # Remove specified phrases
    text = remove_phrases(text, phrases)
    
    # Replace multiple consecutive periods with a single space
    text = re.sub(r'\.\s*\.', ' ', text)
    
    # Remove single periods
    if text.count('.') <= 1:
        text = text.replace('.', '')
    
    # Remove non-Arabic characters except spaces
    cleaned_text = re.sub(r'[^ء-ي\s]', '', text)
    
    # Tokenize the cleaned text
    tokens = simple_word_tokenize(cleaned_text)
    
    # Lemmatize and remove stopwords
    lemmatized_tokens = []
    for token in tokens:
        if token not in arabic_stopwords:
            analysis = analyzer.analyze(token)
            if analysis:
                lemma = analysis[0].get('lemma', token)
                lemmatized_tokens.append(lemma)
            else:
                lemmatized_tokens.append(token)
    
    # Apply stemming
    stemmed_tokens = stem_words(lemmatized_tokens, override_stems)
    
    return stemmed_tokens

# Override stems for specific words
override_stems = {
    'أكل': 'أكْل',  
    'شرب': 'شَرْب'   
}

# Apply the function to process citations
df['ProcessedCitation'] = df['Citation'].apply(lambda text: ' '.join(clean_lemmatize_and_stem_citation(text, words, override_stems)))

# Vectorization using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['ProcessedCitation'])

# Convert the matrix to a DataFrame for easy manipulation
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
tfidf_df.index = df.index  # Ensure indices match the original DataFrame

# Concatenate TF-IDF results with the original DataFrame
df_with_tfidf = pd.concat([df, tfidf_df], axis=1)
df_with_tfidf.drop(columns=['Citation','ProcessedCitation','Manner'], inplace=True)  # Drop the original citation column

print(df_with_tfidf)  # Display the DataFrame with TF-IDF results
=======
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
>>>>>>> 0156625bb6ec254f41cc21926ddeb6dc7ed4e1f4
