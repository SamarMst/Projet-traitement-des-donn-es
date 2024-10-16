import requests
import re
from bs4 import BeautifulSoup
#Website 
url5 = 'https://qaoul.com/m/%D8%AD%D9%83%D9%85-%D8%B9%D9%86-%D8%A7%D9%84%D8%AD%D8%B3%D8%AF'
response5 = requests.get(url5)

# Set correct encoding for Arabic text
response5.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup5 = BeautifulSoup(response5.content, 'html.parser')
#div4 = soup5.find("div", attrs={"class": ["article-text", "links-color"]})
# Find all divs with class 'quote-content'
# Find all quote-content divs
quote_contents = soup5.find_all("div", class_="quote-content")

# List to store the extracted text
paragraph_texts = []

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
                paragraph_texts.append(p_text)

print(paragraph_texts)
print(len(paragraph_texts))
# Find all divs with the specified style (you can also use a class if available)
divs = soup5.find_all("div", style="display: inline-grid;grid-template-columns: max-content max-content;column-gap: 50px")


# List to store the combined text from each div
combined_phrases = []

# Iterate through each div and combine the text of the spans
for div in divs:
    spans = div.find_all("span")
    combined_phrase = ' '.join(span.get_text(strip=True) for span in spans)  # Combine span texts into a single string
    combined_phrases.append(combined_phrase)  # Append the combined string to the list

# Print the list of combined phrases
print(combined_phrases)
print(len(combined_phrases))