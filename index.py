import requests
from bs4 import BeautifulSoup
from camel_tools.sentiment import SentimentAnalyzer
import xlsxwriter 
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.tokenizers.word import simple_word_tokenize

# Load the built-in language model database
db = MorphologyDB.builtin_db()

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentAnalyzer.pretrained()

# Initialize the morphological analyzer with no backoff
morph_analyzer = Analyzer(db)

# URL of the website to scrape
url = 'https://mawdoo3.com/%D8%A3%D9%85%D8%AB%D8%A7%D9%84_%D9%88%D8%AD%D9%83%D9%85_%D8%B9%D9%86_%D8%A7%D9%84%D8%A3%D8%AE%D9%84%D8%A7%D9%82#:~:text=%D8%A5%D8%B0%D8%A7%20%D8%A3%D8%B1%D8%AF%D8%AA%20%D8%A3%D9%86%20%D8%AA%D8%B7%D8%A7%D8%B9%20%D9%81%D8%A3%D9%85%D8%B1%20%D8%A8%D9%85%D8%A7%20%D9%8A%D8%B3%D8%AA%D8%B7%D8%A7%D8%B9.%20%D9%81%D9%8A,%D8%A3%D9%83%D8%B1%D9%85%D8%AA%20%D8%A7%D9%84%D9%83%D8%B1%D9%8A%D9%85%20%D9%85%D9%8E%D9%84%D9%83%D8%AA%D9%87%20%D9%88%D8%A5%D9%86%20%D8%A3%D9%86%D8%AA%D9%8E%20%D8%A3%D9%83%D8%B1%D9%85%D8%AA%D9%8E%20%D8%A7%D9%84%D9%84%D8%A6%D9%8A%D9%85%20%D8%AA%D9%85%D8%B1%D8%AF%D8%A7.'

# Send a GET request to fetch the page content
response = requests.get(url)

# Set correct encoding for Arabic text
response.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the div with the class 'article-text' that contains the list of proverbs
div = soup.find("div", class_="article-text")

# Find all 'li' elements (assuming proverbs are within list items)
ul = div.find_all('ul')[1]
li_elements = ul.find_all('li')
li_manners = []


for li in li_elements:
    li_manners.append(li.text)


good_Morals = [
    "الاحترامُ والتَّوقِيرُ",
    "الإحسانُ إلى الغَيْرِ",
    "الإصلاح",
    "الاعتِدالُ والوَسَطِيَّةُ",
    "الإعراضُ عن الجاهِلينَ",
    "الألفةُ",
    "الأمانة",
    "الإنصاتُ",
    "الإيثارُ",
    "البر",
    "البشاشة",
    "التَّأْنِّى (الأناةُ)",
    "الْتَّنَبُّتُ",
    "التَّضْحيةُ",
    "الثَّعاوُنُ",
    "الْتَّغَافْلُ",
    "الْتَّفَاؤُلُ",
    "التَّودُّدُ",
    "الْتَّوَاضُعُ",
    "الجِدِّيَّةُ والحَرْمُ",
    "الجُودُ، والكَرَمُ، والسَّخاءُ، والبَدْلُ",
    "الحَدْرُ واليقظة والحيطة"
    "حُسْنُ السَّمْتِ",
    "حُسْنُ الظَّنّ",
    "حُسْنُ العِشْرَةِ والجِوار",
    "حَفْظُ اللِّسَانِ",
    "الحكمة",
    "الحَلْمُ",
    "الحَياءُ",
    "الرحمة",
    "الرِّفْقُ",
    "الزُّهد فيما في أيدي الناسِ",
    "السترُ",
    "السَّكِينَةُ",
    "سلامة الصدر",
    "السماحة",
    "الشجاعة",
    "الشَّفَقَةُ",
    "الشكر",
    "الشَّهامةُ",
    "الصَّبِرُ",
    "الصِّدقُ",
    "الصَّلةُ والتَّواصلُ",
    "الصَّمتُ",
    "العَدلُ والإنصافُ",
    "العِزَّةُ",
    "العَزْمُ والعَزيمةُ وعُلْوُّ الهِمَّةِ",
    "العفّةُ",
    "العَقْوُ والصَّفْحُ",
    "الغَيْرِةُ",
    "الفِراسةُ",
    "الفصاحة",
    "الفِطنةُ والذّكاءُ",
    "القناعة",
    "الْقُوَّةُ",
    "كِتمانُ السِّرِّ",
    "كَظْمُ الغَيظِ",
    "المَحَبَّةَ",
    "المُداراةُ",
    "النَّصْرَةُ",
    "النَّصِيحةُ",
    "النظافةُ",
    "الوَرَعُ",
    "الوفاءُ",
    "الوقار والرزانة"
]

blameworthy_Morals = [
    "الأَثَرةُ والأنانيَّةُ",
    "الاختلاف والتَّنَازُغُ",
    "الإساءة",
    "الإسراف والتَّبذيرُ",
    "الإطراءُ والمدحُ",
    "الافتِراءُ والبُهتانُ",
    "الإفراط",
    "إفشاءُ السِّرّ",
    "الانتقامُ",
    "البُخْلُ والشَّحُ",
    "البَطَرُ",
    "البُغْضُ والكَراهِيَةُ",
    "التَّجَسُّسُ",
    "الْتَّخَادِلُ",
    "التَّسَرُّعُ والتَّهَؤُّرُ والعَجَلةُ",
    "التَّعالى",
    "التَّعسيرُ",
    "التَّعَصُبُ",
    "التَّفرِيطُ",
    "الْتَّقَلَيْدُ والتَّبْعِيَّةُ",
    "التَّنَابُرُ بالألقابِ",
    "الثَّرْثَّرةُ",
    "الجُبْنُ",
    "الجدالُ والْمِرَاءُ",
    "الجَزَعُ",
    "الجُفاءُ",
    "الْحَسَدُ",
    "الحقد",
    "الْخُبْتُ",
    "الخداعُ",
    "الخِدْلانُ",
    "خُلْفُ الوَعْدِ",
    "الخيانةُ",
    "الدّياثةُ",
    "الذّلُّ",
    "رَفعُ الصَّوتِ",
    "السَّبُّ والشَّتَمُ",
    "السُّخْرِيَّةُ والاستهزاءُ",
    "السَّفَهُ والحُمقُ",
    "سُوءُ الجوار",
    "سُوءُ الظَنَّ",
    "الشَّراهةُ",
    "الشَّماتَةُ",
    "الْطَّمَغُ",
    "الظَّلْمُ",
    "الْعُبُوسُ",
    "العُجْبُ",
    "العُدوانُ",
    "الغَدرُ ونقضُ العَهدِ",
    "الغشُّ",
    "الغَضَبُ",
    "الغِلْظَةُ والقَّسوةُ والفظاظةُ",
    "الغِيبةُ",
    "الفُّجورُ",
    "الْفُحْشُ والبَذاءةُ",
    "الكِبْرُ",
    "الْكَذِبُ",
    "الكَسَلُ والْفُتَورُ",
    "اللامبالاةُ",
    "اللّؤْمُ والْخِسَّةُ والدَّناءةُ",
    "المُداهَنة",
    "المَكْرُ والكَيْدُ",
    "المَنَّ",
    "النَّفَاقُ",
    "تُكْرَانُ الجَميلِ",
    "النَّميمةُ",
    "الهَجْرُ",
    "الهَمْزُ واللَّمزُ",
    "الوَهَن",
    "اليأسُ و القُنوطُ و الإحباطُ",
]



# Function to perform stemming
# Dictionary to override specific stems for known problematic words
override_stems = {
    "الوَهَن": "وهن",  # Correct root for الوَهَن
    "المَنَّ": "منّ",  # Correct root for المَنَّ
    # Add more words as needed
}

# Function to perform stemming
def stem_words(words):
    stems = []
    for word in words:
        # Check if the word has an override
        if word in override_stems:
            stems.append(override_stems[word])
        else:
            analyses = morph_analyzer.analyze(word)
            if analyses:
                # Log all analyses for inspection if needed
                if word == "الوَهَن" or word == "المَنَّ":  # Adjust as necessary for other problematic words
                    print(f"Analyses for {word}: {analyses}")
                stems.append(analyses[0]['stem'])
            else:
                stems.append(word)
    return stems


# Stem the good and blameworthy morals lists
good_Morals_stemmed = stem_words(good_Morals)
blameworthy_Morals_stemmed = stem_words(blameworthy_Morals)
good_Morals_stemmed = [moral.strip() for moral in good_Morals_stemmed]
blameworthy_Morals_stemmed = [moral.strip() for moral in blameworthy_Morals_stemmed]





# Function to classify a citation based on the analyzed words
def classify_citation(citation):
    # Check direct match with full phrases first
    for moral in good_Morals:
        if moral in citation:
            return "Good Moral: " + moral
    for moral in blameworthy_Morals:
        if moral in citation:
            return "Blameworthy Moral: " + moral
    
    # If no full phrase matches, tokenize and stem the citation
    words = simple_word_tokenize(citation)
    stems = stem_words(words)

    # Check stems against the stemmed good and blameworthy lists
    for stem in stems:
        if stem in good_Morals_stemmed:
            return "Good Moral: " + stem
        elif stem in blameworthy_Morals_stemmed:
            return "Blameworthy Moral: " + stem

    # Use sentiment analyzer if no specific moral is found
    sentiment = sentiment_analyzer.predict([citation])[0]
    return "Sentiment: " + sentiment


# Create an Excel workbook and worksheet
workbook = xlsxwriter.Workbook('manners.xlsx')
worksheet = workbook.add_worksheet("manners")

# Write the headers
worksheet.write(0, 0, "Citation")
worksheet.write(0, 1, "Manner")

# Write the citations and their classifications to the Excel file
for index, citation in enumerate(li_manners):
    manner = classify_citation(citation)
    worksheet.write(index + 1, 0, citation)
    worksheet.write(index + 1, 1, manner)

# Close the workbook
workbook.close()
