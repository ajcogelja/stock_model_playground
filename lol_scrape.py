from typing import Union
from bs4 import BeautifulSoup
import bs4
from bs4.element import Script, Tag
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

def get_counter_champs(counter_url):
    print(counter_url)
    req_headers = {
        'referer': 'https://na.op.gg/',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }  
    champ_page_req = req.get(counter_url, headers=req_headers)
    champ_page = BeautifulSoup(champ_page_req.content, 'html.parser')
    attributes = {
        'class': True,
        'data-champion-name': True, 
        'data-value-winrate' : True,
    }
    counter_list = champ_page.find_all('div', attrs=attributes)
    counters = {} #dict
    for counter in counter_list:
        game_div = counter.find('div', class_='champion-matchup-list__totalplayed')
        c_attrs = counter.attrs
        #print('game_div', game_div)
        #print('c', c_attrs)
        counters[c_attrs['data-champion-name']] = {
            'winrate': c_attrs['data-value-winrate'],
            'pickrate': float(game_div.span.text.replace('%', '')),
            'games': int(c_attrs['data-value-totalplayed'])
        }
    return counters

def contains_id_indicator(tag: Tag):
    id_str = 'championId:'
    if id_str in str(tag.prettify()):
        return True
    return False

def find_champ_id(page : Union[Tag, BeautifulSoup]):
    id_str = 'championId:'
    found = page.find_all(lambda tag: (tag.name == 'script' and contains_id_indicator(tag)))  
    for f in found:
        found_string = str(f.prettify())
        index = found_string.index(id_str)# + len(id_str)
        end_index = found_string.index('\n', index)
        other_end = found_string.index('}', index + len(id_str))
        newline_champ_val = found_string[index + len(id_str):end_index].strip()
        curly_champ_val = found_string[index + + len(id_str):other_end].strip()
        # print('newline end index ', newline_champ_val)
        # print('curly bracket end index', curly_champ_val)
        # print('newline num: ', int(newline_champ_val))
        # print('curly num:', int(curly_champ_val))

        return int(curly_champ_val)
        
        #print('f: ', f.__dict__.keys())
        #print('script vars: ', len(vars(script)) )#script.__dict__.keys())
        #print('script.string:', script.__dict__.keys())

    return -1

def find_tier(page):
    found = page.find(lambda tag : (tag.name == 'b' and tag.text and 'Tier ' in tag.text))
    #print('find:', found.text.replace('Tier ', ''))
    return int(found.text.replace('Tier ', ''))

def get_champ_info(url, name):
    req_headers = {
        'referer': 'https://na.op.gg/',
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }  
    champ_page_req = req.get(url, headers=req_headers)
    champ_page = BeautifulSoup(champ_page_req.content, 'html.parser')
    champ_page_body = champ_page.body
    info = {}
    #print('regex:', champ_page(text=re.compile('counters'))) -- exaple on string parsing
    info['id'] = find_champ_id(champ_page_body)
    info['tier'] = find_tier(champ_page_body)
    found_anchors = champ_page_body.find_all('a', attrs={'href': True}, text='Counters')
    for a in found_anchors:
        print('a', a)
        print('a.attrs: ', a.attrs)
        print('a.text: ', a.text)
        counter_url = 'https://na.op.gg' + a.attrs['href']
        counters = get_counter_champs(counter_url)
        info['counters'] = counters


    return info

def main():
    body = soup.body
    res = body.find_all('div', {'data-champion-name': True})
    index = 0
    champs = {}

    for r in res:
        if index == 4:
            break
        #print('index: ', index)
        champ_info = {}
        name = r['data-champion-name']
        url = 'https://na.op.gg'
        if r.a:
            url += r.a['href']
            champ_info = get_champ_info(url, name)
            champs[name] = champ_info
            input('press a key to continue')
            #time.sleep(1  + random.random()/2) #sleep for half a second as to not get flagged as a scraping tool
        else:
            print('r does not have attr a')
        
        index += 1
    print('champs: ', champs)


if __name__ == "__main__":
    main()
