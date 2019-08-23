"""
PoetryFoundation Scraper

Simple web scraper that scrapes a poet's poems from the PoetryFoundation
website into a single txt file.

Eric Li
"""

from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
import html

poet = input('Enter a poet: ')

poet = poet.lower()
poet = re.sub('[^a-z]+','-',poet)

fileout = poet + ".txt"
output = open(fileout,'w')

url = "http://www.poetryfoundation.org/bio/"+poet+"#about"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
parser = html.parser.HTMLParser()

poems = soup.find_all('a',href=re.compile('.*/poems/[0-9]+/.*'))
poems2 = soup.find_all('a',href=re.compile('.*/poem/.*'))

poems.extend(poems2)

for poem in poems:

    poemURL = poem.get('href')
    poemPage = requests.get(poemURL)
    poemSoup = BeautifulSoup(poemPage.text, 'html.parser')
    
    poemTitle = poemSoup.find('h1')
    
    if poemTitle:
        print(html.unescape(poemTitle.text).encode('utf-8').decode('utf-8'),file=output)
        
        poemContent = poemSoup.find('div',{'class':'o-poem'})
        poemLines = poemContent.findAll('div')
        for line in poemLines:
            text = html.unescape(line.text)
            out = text.encode('utf-8').decode("utf-8") 
            print(out,file=output)
        
