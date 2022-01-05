import os

print('------------------------------------------------------------------------------------------------------------------------')
print('Pip installing the required modules to run this program. If already installed, it will upgrade the version of the modules')
print('------------------------------------------------------------------------------------------------------------------------')

os.system('pip install requests --upgrade --quiet --disable-pip-version-check')
os.system('pip install bs4 --upgrade --quiet --disable-pip-version-check')
os.system('pip install pandas --upgrade --quiet --disable-pip-version-check')
os.system('pip install sqlalchemy --upgrade --quiet --disable-pip-version-check')
os.system('pip install squarify --upgrade --quiet --disable-pip-version-check')
os.system('pip install seaborn --upgrade --quiet --disable-pip-version-check --no-warn-script-location')
os.system('pip install numpy --upgrade --quiet --disable-pip-version-check --no-warn-script-location')
os.system('pip install matplotlib --upgrade --quiet --disable-pip-version-check --no-warn-script-location')
os.system('pip install edx-dl --upgrade --quiet --disable-pip-version-check --no-warn-script-location')
os.system('pip install ruamel_yaml --upgrade --quiet --disable-pip-version-check --no-warn-script-location')

print('------------------------------------------------------------------------------------------------------------------------')
print('Modules checked and upgraded (if needed)')
print('------------------------------------------------------------------------------------------------------------------------')

print('------------------------------------------------------------------------------------------------------------------------')
print('Importing Libraries')
print('------------------------------------------------------------------------------------------------------------------------')


import requests,pprint
from bs4 import BeautifulSoup
import pandas as pd
import urllib,json,time
import sys
import csv 
from sqlalchemy import create_engine
import Coin_Market_Cap as cmp
import Currency_Ticker_Nomics as ctn
import Cryptocompare as cc
import warnings
warnings.filterwarnings("ignore")
pd.set_option("display.max_rows", None, "display.max_columns", None)

def normal_scrape(topic,engine):
    print('------------------------------------------------------------------------------------------------------------------------')
    print('\nFetching the ranks of the cryptocurrencies from the website coinmarketcap.com')
    print('\nThis requires pulling the data from various segments of the website. Hence, some time is needed to extract the data\n')
    print('------------------------------------------------------------------------------------------------------------------------')
    final_part1=cmp.final_output(topic)
    final_part2=cmp.get_stat_details(final_part1)
    final_df=pd.concat([final_part1,final_part2], axis=1)
    final_df.to_csv('../Data/Currency_Details_Stats.csv', index=False)
    final_df.to_sql('Currency_Details_Stats', con=engine,if_exists='replace')
    Currency_Details_Stats_SQL_Table=engine.execute("SELECT * FROM Currency_Details_Stats").fetchall()
    Currency_Details_Stats_SQL_Table_columns=engine.execute("SELECT * FROM Currency_Details_Stats").keys()
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Output: ')
    print('------------------------------------------------------------------------------------------------------------------------')
    pprint.pprint(Currency_Details_Stats_SQL_Table_columns)
    pprint.pprint(Currency_Details_Stats_SQL_Table)
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Data stored in the SQL tables using pandas. It created an in-memory SQLite database. \nExtracted the data from the tables using Select * command ')
    print('------------------------------------------------------------------------------------------------------------------------')

    print('------------------------------------------------------------------------------------------------------------------------')
    print('\nFetching the cryptocurrencies details from the Nomics API\n')
    print('------------------------------------------------------------------------------------------------------------------------')
    currency_ticker_df=ctn.currency_ticker(final_df)
    currency_ticker_df.to_csv('../Data/Currency_Ticker.csv', index=False)
    currency_ticker_df.to_sql('Currency_Ticker', con=engine,if_exists='replace')
    Currency_Ticker_SQL_Table=engine.execute("SELECT * FROM Currency_Ticker").fetchall()
    Currency_Ticker_SQL_Table_columns=engine.execute("SELECT * FROM Currency_Ticker").keys()
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Output: ')
    print('------------------------------------------------------------------------------------------------------------------------')
    pprint.pprint(Currency_Ticker_SQL_Table_columns)
    pprint.pprint(Currency_Ticker_SQL_Table)
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Data stored in the SQL tables using pandas. It created an in-memory SQLite database. \nExtracted the data from the tables using Select * command ')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('\nFetching the coin ID to Symbol mapping for primary key (which will be needed for future analytics)\n')
    print('------------------------------------------------------------------------------------------------------------------------')

    coin_dict=cc.coin_mapping(final_df)

    print('------------------------------------------------------------------------------------------------------------------------')
    print('Fetching the social media and sentiment details of cryptocurrencies from the Crytocompare API')
    print('------------------------------------------------------------------------------------------------------------------------')
    sentiment_df=cc.sentiment_analysis_data_combined(final_df,coin_dict)
    sentiment_df.to_csv('../Data/Social_Media_Sentiment_And_Technical.csv', index=False)
    sentiment_df.to_sql('Social_Media_Sentiment_And_Technical', con=engine,if_exists='replace')
    SS_Media_SQL_Table=engine.execute("SELECT * FROM Social_Media_Sentiment_And_Technical").fetchall()
    SS_Media_SQL_Table_columns=engine.execute("SELECT * FROM Social_Media_Sentiment_And_Technical").keys()
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Output: ')
    print('------------------------------------------------------------------------------------------------------------------------')
    pprint.pprint(SS_Media_SQL_Table_columns)
    pprint.pprint(SS_Media_SQL_Table)
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Data stored in the SQL tables using pandas. It created an in-memory SQLite database. \nExtracted the data from the tables using Select * command ')
    print('------------------------------------------------------------------------------------------------------------------------')

    return final_df,currency_ticker_df,sentiment_df

def scrape_part(topic,engine):
    print('------------------------------------------------------------------------------------------------------------------------')
    print('\nFetching the ranks of the cryptocurrencies from the website coinmarketcap.com')
    print('\nThis requires pulling the data from various segments of the website. Hence, some time is needed to extract the data\n')
    print('------------------------------------------------------------------------------------------------------------------------')

    final_part1=cmp.final_output(topic)
    if len(sys.argv)>2:
        final_part1=final_part1[:int(sys.argv[2])]
    else:
        final_part1=final_part1[:5]
    final_part2=cmp.get_stat_details(final_part1)
    final_df=pd.concat([final_part1,final_part2], axis=1)
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Fetching the ranks of the cryptocurrencies from the website coinmarketcap.com')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Output: ')
    print('------------------------------------------------------------------------------------------------------------------------')

    print(final_df)

    currency_ticker_df=ctn.currency_ticker(final_df)
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Fetching the cryptocurrencies details from the Nomics API')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Output: ')
    print('------------------------------------------------------------------------------------------------------------------------')

    print(currency_ticker_df)
    print('------------------------------------------------------------------------------------------------------------------------')
    print('\nFetching the coin ID to Symbol mapping for primary key (which will be needed for future analytics)\n')
    print('------------------------------------------------------------------------------------------------------------------------')

    coin_dict=cc.coin_mapping(final_df)
    sentiment_df=cc.sentiment_analysis_data_combined(final_df,coin_dict)
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Fetching the social media and sentiment details of cryptocurrencies from the Cryptocompare API')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Output: ')
    print('------------------------------------------------------------------------------------------------------------------------')

    print(sentiment_df)

def static_scrape(topic,engine):
    print('------------------------------------------------------------------------------------------------------------------------')
    print('Please note the following:')
    print('Fetched the ranks of the cryptocurrencies from the website coinmarketcap.com')
    print('Fetched the cryptocurrencies details from the Nomics API')
    print('Fetched the social media and sentiment details of cryptocurrencies from the Cryptocompare API')
    print('------------------------------------------------------------------------------------------------------------------------')

    listout=[]
    file_path_list=['../Data/Currency_Details_Stats.csv','../Data/Currency_Ticker.csv','../Data/Social_Media_Sentiment_And_Technical.csv']
    if len(sys.argv)==2 or len(sys.argv)==0:
        for file in file_path_list:
            out_df = pd.read_csv(file)
            print('------------------------------------------------------------------------------------------------------------------------')
            print('Printing the top 20 elements of the file:',file)
            print('------------------------------------------------------------------------------------------------------------------------')
            print(out_df[:20])
            listout.append(out_df)
    else:
        for i in range(len(sys.argv)):
            if i>1:
                out_df = pd.read_csv(sys.argv[i])
                print('------------------------------------------------------------------------------------------------------------------------')
                print('Printing the top 20 elements of the file:',sys.argv[i])
                print('------------------------------------------------------------------------------------------------------------------------')
                print(out_df[:20])
                listout.append(out_df)

    return listout