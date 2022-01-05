import requests,pprint
from bs4 import BeautifulSoup
import pandas as pd
import urllib,json,time
import sys
import csv 
from sqlalchemy import create_engine
pd.set_option("display.max_rows", None, "display.max_columns", None)

def final_output(topic, page_number = 1):    
    doc = get_topic_page1(topic, page_number)
    tr_tags = doc.tbody.find_all('tr')
    top_100_cryptocurrenices = [complete_cryptocurrencies_list1(tr_tags[i], doc) for i in range(100)]
    write_csv1(top_100_cryptocurrenices, '../Data_Generated_For_Processing_Not_Output/top_100_cryptocurrenices.csv')
    rank_number = rank_list(page_number)  
    y1 = pd.read_csv('../Data_Generated_For_Processing_Not_Output/rank.csv')
    y2 = pd.read_csv('../Data_Generated_For_Processing_Not_Output/top_100_cryptocurrenices.csv')
    Final_Output= pd.DataFrame.join(y1, y2)
    #print('The output file is stored as Final_Output.csv')
    #Final_Output.to_csv('Final_Output.csv', index=False)
    return Final_Output

def get_topic_page1(topic, page):
    topic_with_page= topic + '/?page=' + str(page)
    response = requests.get(topic_with_page)
    with open('../Data_Generated_For_Processing_Not_Output/Cryptocurrency_test.html', 'w') as f:
        f.write(response.text)
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page' + topic)
    return BeautifulSoup(response.text, 'html.parser')


def complete_cryptocurrencies_list1(tr_tag, document):
    tr_tags = document.tbody.find_all('tr')
    base_url = 'https://coinmarketcap.com'
    td_tags = tr_tag.find_all('td')
    
    if tr_tags.index(tr_tag)<10:
        td_tag=td_tags[2]
        div_in_td = td_tag.find_all('div', class_='sc-16r8icm-0 sc-1teo54s-1 dNOTPP') 
        name2 = div_in_td[0].find_all('p', class_='sc-1eb5slv-0 iworPT')
        name = name2[0].text
        symbol2 = div_in_td[0].find_all('p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol')
        symbol= symbol2[0].text
        price_in_USD1 = td_tags[3].text
        price_in_USD = price_in_USD1.replace(',','')
        url_Cryptocurrency = td_tag.a['href'].strip()
        URL = base_url + url_Cryptocurrency
    else:
        span=td_tags[2].a.find_all('span')
        name = span[1].text
        symbol= span[2].text
        price_in_USD1 = td_tags[3].text
        price_in_USD = price_in_USD1.replace(',','')
        url_Cryptocurrency = td_tags[2].a['href'].strip()
        URL = base_url + url_Cryptocurrency
    return{
    'Name' : name,
    'Symbol': symbol, 
    'Price_in_USD' : price_in_USD,
    'URL':URL,
        
        }

def rank_list(page_number):
    with open('../Data_Generated_For_Processing_Not_Output/rank.csv', 'w') as f:
        f.write('Rank' + '\n')
        if page_number == 0: 
            page_number = 1
        rank_range = [(((page_number-1)*100)+i) for i in range(1,101)]
        for rank_number in rank_range:
            f.write(str(rank_number) + '\n')
    return rank_range
        
def write_csv1(items, path):
    """Write a list of dictionaries to a CSV file"""
    with open(path, 'w') as f:
        if len(items) == 0:
            return
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, "")))
            f.write(','.join(values) + "\n")
            
def get_stat_details(base_data):
    stats_out={'Market Cap':[],'Diluted Market Cap':[],'Volume':[],'Volume Per Market Cap':[],'Circulating Supply':[]}
    
    for url in base_data.loc[:,'URL']:
        mainpage = requests.get(url)
        soup = BeautifulSoup(mainpage.content, 'html.parser')        
        statsContainer = soup.find_all("div", {"class" : "hide statsContainer"})
        statsValues = statsContainer[0].find_all("div", {"class" : "statsValue"})

        statsValue_marketcap = statsValues[0].text.strip()
        stats_out['Market Cap'].append(statsValue_marketcap)
        statsValue_fully_diluted_marketcap = statsValues[1].text.strip()
        stats_out['Diluted Market Cap'].append(statsValue_fully_diluted_marketcap)
        statsValue_volume = statsValues[2].text.strip()
        stats_out['Volume'].append(statsValue_volume)
        statsValue_volume_per_marketcap = statsValues[3].text.strip()
        stats_out['Volume Per Market Cap'].append(statsValue_volume_per_marketcap)
        statsValue_circulating_supply = statsValues[4].text.strip()
        stats_out['Circulating Supply'].append(statsValue_circulating_supply)
    df= pd.DataFrame(stats_out)
    return df
