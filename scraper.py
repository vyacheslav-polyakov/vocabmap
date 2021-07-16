from urllib.request import Request, urlopen
from urllib.parse import quote   
from bs4 import BeautifulSoup as bs
import io
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def findExamples(word):
    # Retrieve the exmples 
    url = 'https://www.purpleculture.net/dictionary-details/?word=' + quote(word)
    request = Request(url, headers=headers)
    response = urlopen(request)
    soup = bs(response, 'html.parser')
    examples = soup.findAll('span', {'class': 'samplesen'})
    meanings = soup.findAll('div', {'class':'sample_en'})

    # Write the exmples to a temporary file to decode it
    file = open(r'vocab\temp.txt', 'w', encoding='utf-8')
    for example in examples:
        file.write(example.text)
    file.close()
        
    # Separate examples into a list 
    file = open(r'vocab\temp.txt', 'r', encoding='utf-8')
    string = file.read()
    file.close()
    examples = re.split("[a-zāáǎàōóǒòēéěèīíìǐūúǔùǖǘǚǜü “”]", string)
    examples = ''.join(examples)
    examples = examples.split('。')
    file = open(r'vocab\temp.txt', 'w', encoding='utf-8')
    examples_cn = []
    examples_en = []
    translations = []
    for m in meanings:
        translations.append(m.text)
    for example in examples:
        if len(example) <= 30 and example.replace(' ', '') != '':
            examples_cn.append(example)
            examples_en.append(translations[examples.index(example)])
            file.write(example+'\n')
    file.close()
    examples_cn.append('') # to know where the list ends
    examples_en.append('') # to know where the list ends
    result = [examples_cn, examples_en]
    return result

findExamples('果然'.encode('utf-8'))