from bs4 import BeautifulSoup
import bs4
import requests as req
import time
import random
import re

headers = {
    'referer': 'https://na.op.gg/',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
html_doc = req.get('https://na.op.gg/champion/statistics', headers=headers)
soup = BeautifulSoup(html_doc.content, 'html.parser')

def get_champ_info(url, name):
    req_headers = {
        'referer': 'https://na.op.gg/',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }  
    champ_page_req = req.get(url, headers=req_headers)
    champ_page = BeautifulSoup(champ_page_req.content, 'html.parser')
    print('url: ', url)
    f = open(name + '.html', "w")
    f.write(str(champ_page.prettify()))
    f.close()
    #print('champ_page')
    champ_page_body = champ_page.body

    #print('regex:', champ_page(text=re.compile('champion-matchup-champion-list')))

    for div in champ_page.find_all('div', attrs={'class': True}):
        if div.has_attr('class') and 'champion-matchup-champion-list' in div['class']:
            print('div: ', div['class'])
    #champ_page.find(name='div', class_='champion-matchup-champion-list')
    return {}

def main():
    body = soup.body
    res = body.find_all('div', {'data-champion-name': True})
    index = 0
    champs = {}

    for r in res:
        #print('index: ', index)
        champ_info = {}
        name = r['data-champion-name']
        url = 'https://na.op.gg'
        if r.a:
            #print('r.a: ', r.a)
            #print('r.a.attrs["href"]: ', r.a.attrs["href"])
            url += r.a['href']
            #print('url: ', url)
            champ_info = get_champ_info(url, name)
            input('press a key to continue')
            #time.sleep(1  + random.random()/2) #sleep for half a second as to not get flagged as a scraping tool
        else:
            print('r does not have attr a')
        
        index += 1


if __name__ == "__main__":
    main()
