import requests
import re
from bs4 import BeautifulSoup

# Website URL
url4 = 'https://ar.islamway.net/article/76389/%D8%A3%D9%82%D9%88%D8%A7%D9%84-%D8%A7%D9%84%D8%B3%D9%84%D9%81-%D9%88%D8%A7%D9%84%D8%B9%D9%84%D9%85%D8%A7%D8%A1-%D9%81%D9%8A-%D8%A5%D9%81%D8%B4%D8%A7%D8%A1-%D8%A7%D9%84%D8%B3%D8%B1'
response4 = requests.get(url4)

# Set correct encoding for Arabic text
response4.encoding = 'utf-8'

# Parse the page content using BeautifulSoup
soup4 = BeautifulSoup(response4.content, 'html.parser')

# Extract the text from the <h4> element
h4_text = soup4.find('h4').get_text(separator="")  # Using space as separator

# Split the text at dashes ("-")
sentences = h4_text.split("()")

# Clean up the sentences (remove leading/trailing spaces and empty entries)
sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
print(sentences)
