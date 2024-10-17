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



# Website 9
url9 = 'https://qaoul.com/m/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%B4%D8%AC%D8%A7%D8%B9%D8%A9'
response9 = requests.get(url9)

# Set correct encoding for Arabic text
response9.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup9 = BeautifulSoup(response9.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup9.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract the <p> text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find the first <p> element within the blockquote
        p = blockquote.find("p")
        
        if p:
            # Extract the text from the <span> inside the <p>
            p_text = p.get_text(strip=True)  # Get the text of the <p>
            if p_text:  # Append to the list if the text is not empty
                li_manners.append(p_text)

# Find all divs with the specified style
divs = soup9.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px") 
# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    
    li_manners.append(combined_phrase)  # Add the deduplicated phrase



# Website 10
url10 = 'https://qaoul.com/m/%D9%83%D9%84%D9%85%D8%A7%D8%AA-%D8%B9%D9%86-%D8%A7%D9%84%D9%88%D9%81%D8%A7%D8%A1'
response10 = requests.get(url10)

# Set correct encoding for Arabic text
response10.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup10 = BeautifulSoup(response10.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup10.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Find all divs with the specified style
divs = soup10.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")
  
# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    
    # Remove duplicated phrases
    words = combined_phrase.split()  # Split into words
    unique_words = list(dict.fromkeys(words))  # Remove duplicates while preserving order
    final_phrase = ' '.join(unique_words)  # Join back the unique words
    
    li_manners.append(final_phrase)  # Add the deduplicated phrase


#Website 11

url11 = 'https://tweet.gulffalcons.net/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D9%83%D8%AA%D9%85%D8%A7%D9%86-%D8%A7%D9%84%D8%B3%D8%B1-%D9%83%D8%AA%D9%85%D8%A7%D9%86-%D8%A7%D9%84%D8%B3%D8%B1-%D9%88%D8%AD%D9%81%D8%B8-%D8%A7%D9%84/?fbclid=IwZXh0bgNhZW0CMTEAAR1Q7VZyFeVi08JcMVdi0NwBSuuA8095tMIcw8dQT3TTJQLktQ72nwogC58_aem_WbLiv5Ve_ShIWg3IiYQ_mQ' 
response11 = requests.get(url11)
soup11 = BeautifulSoup(response11.content, 'html.parser')

# Find the article body
article_body = soup.find("div", id="article-body")

if article_body is None:
    print("Could not find the div with id 'article-body'. Check the page structure.")
else:
    # Find all <li> elements
    li_elements = article_body.find_all("li")

    # Flag to start collecting from the specified <li>
    collect = False

    for li in li_elements:
        # Check if the text starts with the specific phrase
        if li.get_text(strip=True) == "ثلاث خلاصات؛  تقوى الله في السر والعلن، والقصد في الفقر والغنى، والعدل في الغضب والرضا.":
            collect = True  # Start collecting from this point
        if collect:
            # Get the text directly from the <li> without including <a> text
            li_text = ''.join([str(content).strip() for content in li.contents if isinstance(content, str)])
            if li_text:
                li_manners.append(li_text)


#Website 12
url12 = 'https://qaoul.com/m/%D9%82%D8%A7%D9%84%D9%88%D8%A7-%D8%B9%D9%86-%D8%A7%D9%84%D8%B1%D8%AD%D9%85%D8%A9'
response12 = requests.get(url12)

# Set correct encoding for Arabic text
response12.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup12 = BeautifulSoup(response12.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup12.find_all("div", class_="quote-content")


# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote: 
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 13
url13 = 'https://qaoul.com/m/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D9%82%D9%86%D8%A7%D8%B9%D8%A9'
response13 = requests.get(url13)

# Set correct encoding for Arabic text
response13.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup13 = BeautifulSoup(response13.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup13.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Find all divs with the specified style
divs = soup13.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")

# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    li_manners.append(combined_phrase)  # Add the deduplicated phrase


# Website 14
url14 = 'https://qaoul.com/m/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%B5%D8%A8%D8%B1'
response14 = requests.get(url14)

# Set correct encoding for Arabic text
response14.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup14 = BeautifulSoup(response14.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup14.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 15
url15 = 'https://qaoul.com/m/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%AE%D9%8A%D8%A7%D9%86%D8%A9'
response15 = requests.get(url15)

# Set correct encoding for Arabic text
response15.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup15 = BeautifulSoup(response15.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup15.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 16
url16 = 'https://qaoul.com/m/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%AA%D9%83%D8%A8%D8%B1'
response16 = requests.get(url16)

# Set correct encoding for Arabic text
response16.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup16 = BeautifulSoup(response16.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup16.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 17
url17 = 'https://qaoul.com/m/%D8%A3%D8%AC%D9%85%D9%84-%D9%85%D8%A7-%D9%82%D9%8A%D9%84-%D9%81%D9%8A-%D8%A7%D9%84%D9%83%D8%B1%D9%85'
response17 = requests.get(url17)

# Set correct encoding for Arabic text
response17.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup17 = BeautifulSoup(response17.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup17.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 18
url18= 'https://qaoul.com/m/%D9%82%D8%A7%D9%84%D9%88%D8%A7-%D8%B9%D9%86-%D8%A7%D9%84%D9%83%D9%84%D8%A7%D9%85-%D8%A7%D9%84%D8%AC%D8%A7%D8%B1%D8%AD'
response18= requests.get(url18)

# Set correct encoding for Arabic text
response18.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup18= BeautifulSoup(response18.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup18.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 19
url19= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D9%88%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%AD%D9%85%D9%82%D9%89'
response19= requests.get(url19)

# Set correct encoding for Arabic text
response19.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup19= BeautifulSoup(response19.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup19.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 20
url20= 'https://qaoul.com/m/%D8%A3%D8%AC%D9%85%D9%84-%D9%85%D8%A7-%D9%82%D9%8A%D9%84-%D8%B9%D9%86-%D8%A7%D9%84%D8%B3%D8%B1'
response20= requests.get(url20)

# Set correct encoding for Arabic text
response20.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup20= BeautifulSoup(response20.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup20.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 21
url21= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D9%85%D9%86-%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%A7%D9%84%D8%AD%D9%83%D9%85%D8%A7%D8%A1'
response21= requests.get(url21)

# Set correct encoding for Arabic text
response21.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup21= BeautifulSoup(response21.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup21.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 22
url22= 'https://qaoul.com/m/%D9%82%D8%A7%D9%84%D9%88%D8%A7-%D8%B9%D9%86-%D8%A7%D9%84%D8%A8%D8%AE%D9%84'
response22= requests.get(url22)

# Set correct encoding for Arabic text
response22.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup22= BeautifulSoup(response22.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup22.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 23
url23= 'https://qaoul.com/m/%D9%83%D9%84%D8%A7%D9%85-%D8%B9%D9%86-%D8%A5%D8%AE%D9%84%D8%A7%D9%81-%D8%A7%D9%84%D9%88%D8%B9%D8%AF'
response23= requests.get(url23)

# Set correct encoding for Arabic text
response23.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup23= BeautifulSoup(response23.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup23.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 24
url24= 'https://qaoul.com/m/%D9%83%D9%84%D8%A7%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%B7%D9%85%D8%B9'
response24= requests.get(url24)

# Set correct encoding for Arabic text
response24.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup24= BeautifulSoup(response24.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup24.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 25
url25= 'https://qaoul.com/m/%D9%83%D9%84%D8%A7%D9%85-%D9%81%D9%8A-%D8%A7%D9%84%D8%B5%D9%85%D9%8A%D9%85-%D9%84%D9%84%D8%AE%D8%A7%D8%A6%D9%86%D9%8A%D9%86'
response25= requests.get(url25)

# Set correct encoding for Arabic text
response25.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup25= BeautifulSoup(response25.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup25.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 26
url26= 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%BA%D8%AF%D8%B1'
response26= requests.get(url26)

# Set correct encoding for Arabic text
response26.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup26= BeautifulSoup(response26.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup26.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 28
url28= 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%B8%D9%86-%D8%A8%D9%84%D8%B3%D9%88%D8%A1'
response28= requests.get(url28)

# Set correct encoding for Arabic text
response28.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup28= BeautifulSoup(response28.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup28.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 29
url29= 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D9%84%D9%84%D9%8A%D8%A7%D8%A6%D8%B3%D9%8A%D9%86'
response29= requests.get(url29)

# Set correct encoding for Arabic text
response29.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup29= BeautifulSoup(response29.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup29.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 30
url30= 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%A8%D8%AE%D9%8A%D9%84'
response30= requests.get(url30)

# Set correct encoding for Arabic text
response30.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup30= BeautifulSoup(response30.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup30.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 31
url31= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B4%D9%83%D8%B1-%D9%88%D8%AB%D9%86%D8%A7%D8%A1'
response31= requests.get(url31)

# Set correct encoding for Arabic text
response31.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup31= BeautifulSoup(response31.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup31.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 32
url32= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B4%D9%83%D8%B1-%D9%88%D8%AA%D9%82%D8%AF%D9%8A%D8%B1-%D9%84%D9%84%D8%A3%D8%AD%D8%A8%D8%A9'
response32= requests.get(url32)

# Set correct encoding for Arabic text
response32.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup32= BeautifulSoup(response32.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup32.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 33
url33= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%A3%D8%B5%D8%AD%D8%A7%D8%A8-%D8%A7%D9%84%D9%88%D8%AC%D9%87%D9%8A%D9%86'
response33= requests.get(url33)

# Set correct encoding for Arabic text
response33.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup33= BeautifulSoup(response33.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup33.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 34
url34= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D8%A3%D9%88%D9%81%D9%8A%D8%A7%D8%A1'
response34= requests.get(url34)

# Set correct encoding for Arabic text
response34.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup34= BeautifulSoup(response34.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup34.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 35
url35= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D8%BA%D9%8A%D9%88%D8%B1%D9%8A%D9%86'
response35= requests.get(url35)

# Set correct encoding for Arabic text
response35.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup35= BeautifulSoup(response35.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup35.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 36
url36= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D8%AC%D9%87%D9%84%D8%A7%D8%A1'
response36= requests.get(url36)

# Set correct encoding for Arabic text
response36.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup36= BeautifulSoup(response36.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup36.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 37
url37= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%A7%D9%84%D9%85%D8%AA%D9%83%D8%A8%D8%B1%D9%8A%D9%86'
response37= requests.get(url37)

# Set correct encoding for Arabic text
response37.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup37= BeautifulSoup(response37.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup37.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 38
url38= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%A7%D9%84%D8%AE%D8%B0%D9%84%D8%A7%D9%86'
response38= requests.get(url38)

# Set correct encoding for Arabic text
response38.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup38= BeautifulSoup(response38.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup38.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 39
url39= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%A7%D9%84%D8%AA%D8%B3%D8%A7%D9%85%D8%AD'
response39= requests.get(url39)

# Set correct encoding for Arabic text
response39.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup39= BeautifulSoup(response39.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup39.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 40
url40= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D9%85%D8%A4%D8%AB%D8%B1%D8%A9-%D8%B9%D9%86-%D8%A7%D9%84%D8%B8%D9%84%D9%85'
response40= requests.get(url40)

# Set correct encoding for Arabic text
response40.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup40= BeautifulSoup(response40.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup40.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 41
url41= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%B3%D9%88%D8%A1-%D8%A7%D9%84%D8%B8%D9%86'
response41= requests.get(url41)

# Set correct encoding for Arabic text
response41.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup41= BeautifulSoup(response41.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup41.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 42
url42= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%A7%D9%84%D8%B1%D9%81%D9%82'
response42= requests.get(url42)

# Set correct encoding for Arabic text
response42.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup42= BeautifulSoup(response42.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup42.find_all("div", class_="quote-content")

# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 43
url43= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D9%82%D9%88%D9%84-%D8%A7%D9%84%D8%AD%D9%82'
response43= requests.get(url43)

# Set correct encoding for Arabic text
response43.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup43= BeautifulSoup(response43.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup43.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 44
url44= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%AB%D9%82%D9%8A%D9%84-%D8%A7%D9%84%D8%B8%D9%84'
response44= requests.get(url44)

# Set correct encoding for Arabic text
response44.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup44= BeautifulSoup(response44.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup44.find_all("div", class_="quote-content")
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)

# Website 45
url45= 'https://qaoul.com/m/%D8%B9%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-%D8%B9%D9%86-%D8%AD%D9%83%D9%85%D8%A9-%D8%A7%D9%84%D9%8A%D9%88%D9%85'
response45= requests.get(url45)

# Set correct encoding for Arabic text
response45.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup45= BeautifulSoup(response45.content, 'html.parser')

# Find all quote-content divs
quote_contents = soup45.find_all("div", class_="quote-content")
phrases = [] 
# Iterate through each quote-content div and extract text
for quote in quote_contents:
    # Find the blockquote element within each quote-content div
    blockquote = quote.find("blockquote")
    
    if blockquote:
        # Find all <p> and <div> elements within the blockquote
        paragraphs_and_divs = blockquote.find_all('p')
        
        # Iterate through found elements and get the text
        for elem in paragraphs_and_divs:
            text = elem.get_text(strip=True)
            if text:  # Append the non-empty text to the list
                li_manners.append(text)


# Website 46
url46 = 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%AE%D9%8A%D8%A7%D9%86%D8%A9-%D9%88%D8%A7%D9%84%D8%AE%D8%A7%D8%A6%D9%86%D9%8A%D9%86'
response46 = requests.get(url46)

# Set correct encoding for Arabic text
response46.encoding = 'utf-8'
phrases = [] 
# Parse the page content using BeautifulSoup
soup46 = BeautifulSoup(response46.content, 'html.parser')
# Find the <h2> element with the specific id
h2_element = soup46.find('h2', {'id': '.COT-أقوال_عن_الخيانة_والخائنين_6236c26fdf388'})

# Find the next <ul> element following the <h2>
ul_element = h2_element.find_next('ul')

# Find all <li> items within this <ul>
list_items = ul_element.find_all('li')

# Extract the text from each <li> element (or from <span> if you prefer)
li_texts = [li.get_text(strip=True) for li in list_items]
li_manners.extend(li_texts)

# Website 47

url47 = 'https://7ekam.com/praise/'
response47 = requests.get(url47)
soup47 = BeautifulSoup(response47.content, 'html.parser')

# Find all <p> elements that do NOT contain <strong> tags
p_elements = soup47.find_all('p', style=True)  # Get all <p> elements with inline styles

for p in p_elements:
    if not p.find('strong'):  # Filter out any <p> that contains a <strong> tag
        li_manners.append(p.get_text())




# Website 48
url48 = 'https://www.edarabia.com/ar/%D8%A7%D9%84%D9%85%D8%AF%D8%AD-%D9%88-%D8%A3%D9%87%D9%85-49-%D8%B9%D8%A8%D8%A7%D8%B1%D8%A9-%D9%81%D9%8A-%D9%85%D8%AF%D8%AD-%D8%B4%D8%AE%D8%B5/'
response48 = requests.get(url48)

# Set correct encoding for Arabic text
response48.encoding = 'utf-8'

phrases = [] 

# Parse the page content using BeautifulSoup
soup48 = BeautifulSoup(response48.content, 'html.parser')

# Find the h3 tag with id="2"
h3_tag = soup48.find('h3', id='2')

# Find the next ul after the h3 tag
ul_tag = h3_tag.find_next('ul')

# Extract the text from all <li> elements in this <ul>
li_texts = [li.get_text(strip=True) for li in ul_tag.find_all('li')]
li_manners.extend(li_texts)



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