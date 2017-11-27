# Adam Calabrigo 2017

# This script is used to scrape Futurama scripts from online and write to the 
# futurama_scripts.txt file. 

from bs4 import BeautifulSoup
import sys
from urllib.request import Request, urlopen
import re

# open corpus file
f = open('futurama_scripts.txt', 'w')
script_list_url = 'https://theinfosphere.org/Episode_Transcript_Listing'

num_scripts = 0
num_lines = 0

def add_script(script_url):
    ''' Pulls the relevant script text from a given
        online script. '''

    req = Request('https://theinfosphere.org' + script_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    i = 0
    soup = BeautifulSoup(html, 'lxml')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        if p.find('b') is not None:
            if p.find('b').find('a') is not None:
                name = str(p.find('b').find('a').contents[0])
            else:
                name = str(p.find('b').contents[0])
            f.write(name + re.sub(r'\[.+?\]\s*', '', str(p.contents[len(p.contents) - 1])))
            i += 1
    print(script_url, str(i))
    return i

def get_script_urls():
    ''' Goes through the web page that contains the script links and
        creates a list of links to parse. '''
    
    req = Request(script_list_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    script_urls = []

    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a')
    for l in links:
        if len(l.contents) > 0 and len(l.contents[0]) > 10:
            if str(l.contents[0])[:11] == 'Transcript:':
                script_urls.append(l.get('href'))
    return script_urls

# create the corpus

script_urls = get_script_urls()
for script_url in script_urls[:-4]:
    lines = add_script(script_url)
    num_lines += lines
    if lines > 0:
        num_scripts += 1
print('Scraping complete: {} scripts {} lines scraped'.format(num_scripts, num_lines))
f.close()
