import requests
from bs4 import BeautifulSoup
from camel_tools.sentiment import SentimentAnalyzer
import xlsxwriter 
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.tokenizers.word import simple_word_tokenize
import csv


# Load the built-in language model database
db = MorphologyDB.builtin_db()

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentAnalyzer.pretrained()

# Initialize the morphological analyzer with no backoff
morph_analyzer = Analyzer(db)

#Website 1
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

# Website 2
url1 = 'https://tweet.gulffalcons.net/%D8%A7%D8%AC%D9%85%D9%84-%D9%85%D8%A7-%D9%82%D9%8A%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%B5%D8%A8%D8%B1-%D8%B9%D9%84%D9%89-%D8%A7%D9%84%D8%A8%D9%84%D8%A7%D8%A1-%D9%88%D8%A7%D9%84%D8%AD%D8%A8-%D9%83%D9%84/'
response1 = requests.get(url1)

# Set correct encoding for Arabic text
response1.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response1.content, 'html.parser')
div1 = soup.find("div", id="article-body")

# Find all 'li' elements (assuming proverbs are within list items)

for ul in div1.find_all('ul')[1:5]:  # Adjust range based on the number of <ul> elements
    li_elements = ul.find_all('li')
    for li in li_elements:
        li_manners.append(li.text.strip())


# Website 3
url2 = 'https://tweet.gulffalcons.net/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%B5%D8%A8%D8%B1-%D9%88%D8%A7%D9%84%D8%AA%D8%AD%D9%85%D9%84-%D8%A3%D8%AC%D9%85%D9%84-%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%B5%D8%A8/'
response2 = requests.get(url2)

# Set correct encoding for Arabic text
response2.encoding = 'utf-8'
# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response2.content, 'html.parser')
div2 = soup.find("div", id="article-body")

# Find all 'li' elements (assuming proverbs are within list items)

for ul in div2.find_all('ul')[1:7]:  # Adjust range based on the number of <ul> elements
    li_elements = ul.find_all('li')
    for li in li_elements:
        li_manners.append(li.text.strip())

# Function to recursively extract text from <li> and nested <ul> elements
def extract_li_text(ul_element):
    li_items = ul_element.find_all('li', recursive=False)  # Get all direct <li> children
    extracted_text = []

    for li in li_items:
        # Extract the text from the current <li> item
        text = li.get_text(strip=True)
        extracted_text.append(text)

        # If there is a nested <ul> inside this <li>, extract its text as well
        nested_ul = li.find('ul')
        if nested_ul:
            extracted_text.extend(extract_li_text(nested_ul))  # Recursively extract from nested <ul>

    return extracted_text

# Process ul_element5
ul_element6 = div2.find_all('ul')[8]  # Adjust based on the correct index of the <ul>
li_manners6 = extract_li_text(ul_element6)  # Recursively extract text from <ul> and <li> elements
li_manners.extend(li_manners6)  # Add extracted text to the manners list


#Website  4
url4 = 'https://qaoul.com/m/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D9%85%D8%AF%D8%AD'
response4 = requests.get(url4)

# Set correct encoding for Arabic text
response4.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup4 = BeautifulSoup(response4.content, 'html.parser')
#div4 = soup4.find("div", attrs={"class": ["article-text", "links-color"]})
# Find all divs with class 'quote-content'
# Find all quote-content divs
quote_contents = soup4.find_all("div", class_="quote-content")

# List to store the extracted text


# Iterate through each quote-content div and extract the <p> text
for quote in quote_contents:
    # Find all blockquote elements within each quote-content div
    blockquotes = quote.find_all("blockquote")
    
    for blockquote in blockquotes:
        # Find all <p> elements within the blockquote
        paragraphs = blockquote.find_all("p")
        
        # Check if there is a valid second <p> and extract its text
        if len(paragraphs) > 1:
            p_text = paragraphs[1].get_text(strip=True)  # Get the text of the second <p>
            if p_text:  # Append to the list if the text is not empty
                li_manners.append(p_text)

# Find all divs with the specified style (you can also use a class if available)
divs = soup4.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")
# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    li_manners.append(combined_phrase)  # Append the combined string to the list

#Website 5
url5 = 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%AD%D8%B3%D8%AF'
response5 = requests.get(url5)

# Set correct encoding for Arabic text
response5.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup5 = BeautifulSoup(response5.content, 'html.parser')
# Find all divs with class 'quote-content'
# Find all quote-content divs
quote_contents = soup5.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract the <p> text
for quote in quote_contents:
    # Find all blockquote elements within each quote-content div
    blockquotes = quote.find_all("blockquote")
    
    for blockquote in blockquotes:
        # Find all <p> elements within the blockquote
        paragraphs = blockquote.find_all("p")
        
        # Check if there is a valid second <p> and extract its text
        if len(paragraphs) > 1:
            p_text = paragraphs[1].get_text(strip=True)  # Get the text of the second <p>
            if p_text:  # Append to the list if the text is not empty
                li_manners.append(p_text)

# Find all divs with the specified style (you can also use a class if available)
divs = soup5.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")


# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    li_manners.append(combined_phrase)  # Append the combined string to the list

#Website 6
url6 = 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%B9%D8%B2%D8%A9-%D8%A7%D9%84%D9%86%D9%81%D8%B3'
response6 = requests.get(url6)

# Set correct encoding for Arabic text
response6.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup5 = BeautifulSoup(response6.content, 'html.parser')
# Find all quote-content divs
quote_contents = soup5.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract the <p> text
for quote in quote_contents:
    # Find all blockquote elements within each quote-content div
    blockquotes = quote.find_all("blockquote")
    
    for blockquote in blockquotes:
        # Find all <p> elements within the blockquote
        paragraphs = blockquote.find_all("p")
        
        # Check if there is a valid second <p> and extract its text
        if len(paragraphs) > 1:
            p_text = paragraphs[1].get_text(strip=True)  # Get the text of the second <p>
            if p_text:  # Append to the list if the text is not empty
                li_manners.append(p_text)

# Find all divs with the specified style (you can also use a class if available)
divs = soup5.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")

# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    li_manners.append(combined_phrase)  # Append the combined string to the list


#Website 7
url7 = 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%B9%D8%AF%D8%A7%D9%84%D8%A9'
response7 = requests.get(url7)

# Set correct encoding for Arabic text
response7.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup7 = BeautifulSoup(response7.content, 'html.parser')
# Find all quote-content divs
quote_contents = soup7.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract the <p> text
for quote in quote_contents:
    # Find all blockquote elements within each quote-content div
    blockquotes = quote.find_all("blockquote")
    
    for blockquote in blockquotes:
        # Find all <p> elements within the blockquote
        paragraphs = blockquote.find_all("p")
        
        # Check if there is a valid second <p> and extract its text
        if len(paragraphs) > 1:
            p_text = paragraphs[1].get_text(strip=True)  # Get the text of the second <p>
            if p_text:  # Append to the list if the text is not empty
                li_manners.append(p_text)

# Find all divs with the specified style (you can also use a class if available)
divs = soup7.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")

# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    li_manners.append(combined_phrase)  # Append the combined string to the list

#Website 8
url8 = 'https://qaoul.com/m/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D9%83%D8%B0%D8%A8'
response8 = requests.get(url8)

# Set correct encoding for Arabic text
response8.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup8 = BeautifulSoup(response8.content, 'html.parser')
# Find all quote-content divs
quote_contents = soup8.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract the <p> text
for quote in quote_contents:
    # Find all blockquote elements within each quote-content div
    blockquotes = quote.find_all("blockquote")
    
    for blockquote in blockquotes:
        # Find all <p> elements within the blockquote
        paragraphs = blockquote.find_all("p")
        
        # Check if there is a valid second <p> and extract its text
        if len(paragraphs) > 1:
            p_text = paragraphs[1].get_text(strip=True)  # Get the text of the second <p>
            if p_text:  # Append to the list if the text is not empty
                li_manners.append(p_text)

# Find all <li> elements
li_elements = soup8.find_all('li')

for li in li_elements:
    spans = li.find_all('span')
    if len(spans) > 1:  # Ensure there's more than one <span> to avoid index errors
        li_manners.append(spans[1].get_text(strip=True))  # Get the text from the second <span>


# Find all divs with the specified style
divs = soup8.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")

# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    
    # Remove duplicated phrases
    words = combined_phrase.split()  # Split into words
    unique_words = list(dict.fromkeys(words))  # Remove duplicates while preserving order
    final_phrase = ' '.join(unique_words)  # Join back the unique words
    
    li_manners.append(final_phrase)  # Add the deduplicated phrase




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

# Create a CSV file
with open('manners.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ["Citation", "Manner"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the headers
    writer.writeheader()

    # Write the citations and their classifications to the CSV file
    for citation in li_manners:
        manner = classify_citation(citation)
        writer.writerow({"Citation": citation, "Manner": manner})



"""
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
"""