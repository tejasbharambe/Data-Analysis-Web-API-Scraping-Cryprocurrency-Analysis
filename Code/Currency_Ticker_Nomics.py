import requests,pprint
from bs4 import BeautifulSoup
import pandas as pd
import urllib,json,time
import sys
import csv 
from sqlalchemy import create_engine
pd.set_option("display.max_rows", None, "display.max_columns", None)

# Currency Ticker Related Information
def currency_ticker(Symbol_df):
    currency_ticker_dict={'currency':[],'1d_market_cap_change_pct':[],
                         '1d_price_change_pct':[],
                         '1d_volume_change_pct':[],
                         '30d_market_cap_change_pct':[],
                         '30d_price_change_pct':[],
                         '30d_volume_change_pct':[],
                         '365d_market_cap_change_pct':[],
                         '365d_price_change_pct':[],
                         '365d_volume_change_pct':[],
                         'ytd_market_cap_change_pct':[],
                         'ytd_price_change_pct':[],
                         'ytd_volume_change_pct':[],
                         'max_supply':[],
                          'num_exchanges':[],
                          'num_pairs':[]
                         }


    days=['1d','30d','365d','ytd']
    metrics_1=['market_cap_change_pct','price_change_pct','volume_change_pct']
    metrics_2=['max_supply','num_pairs','num_exchanges']
    
    for coin in Symbol_df['Symbol']:
        time.sleep(0.75)
        
        try:
            url = "https://api.nomics.com/v1/currencies/ticker?key=102780b53d3d0aa3a16a88a708cbc193784b6ebc&ids="+coin+"&interval=1d,30d,365d,ytd&convert=USD&per-page=100&page=1"
            currency_ticker=urllib.request.urlopen(url).read().decode('UTF-8')
            responseJson = json.loads(currency_ticker)
    #         pprint.pprint(responseJson)
        except:
            print(coin," Data Not Available")

        for i in responseJson:
            currency_ticker_dict['currency'].append(i['currency'])        
            
            for metric in metrics_1:
                for day in days:
                    if day in i:
                        if metric in i[day]:
                            currency_ticker_dict[day+'_'+metric].append(i[day][metric])
                        else:
                            currency_ticker_dict[day+'_'+metric].append('-')
                    else:
                        currency_ticker_dict[day+'_'+metric].append('-')
            

            for metric in metrics_2:
                if metric in i:  
                    currency_ticker_dict[metric].append(i[metric])
                else:
                    currency_ticker_dict[metric].append('-')

    
    currency_ticker_df=pd.DataFrame.from_dict(currency_ticker_dict,orient='index').transpose()
    return currency_ticker_df
