import requests,pprint
from bs4 import BeautifulSoup
import pandas as pd
import urllib,json,time
import sys
import csv 
from sqlalchemy import create_engine
pd.set_option("display.max_rows", None, "display.max_columns", None)


def coin_mapping(Symbol_df):

    U='https://min-api.cryptocompare.com/data/all/coinlist?summary=true&api_key=6013d40887f97ef57ac70f3540ea90e4d9739a63480492c2f9516b57c82102d0'
    # Available Coin List
    coin_dict={}
    coin_list=urllib.request.urlopen(U).read().decode('UTF-8')
    responseJson = json.loads(coin_list)
    
    for coin_data in Symbol_df['Symbol']:
        time.sleep(0.75)
        if coin_data in responseJson['Data']:
            coin_dict[coin_data]=responseJson['Data'][coin_data]['Id']
        else:
            coin_dict[coin_data]=None
    print(coin_dict)
    return coin_dict


def sentiment_analysis_data_combined(Symbol_df,coin_dict):
# statuses - The number of tweets posted by the requested coin’s Twitter account.

    sentiment_dict={'Coin':[],'Comments':[],'Followers':[],'PageViews':[],'Posts':[],'REDDIT_active_users': [],
                    'REDDIT_comments_per_day': [],'REDDIT_comments_per_hour':[],'REDDIT_community_creation':[] ,
                    'REDDIT_posts_per_day':[],'REDDIT_posts_per_hour':[],'REDDIT_subscribers':[],
                    'TWITTER_favourites': [],'TWITTER_followers': [],'TWITTER_following':[],'TWITTER_statuses':[],
                    'Sentiment_addressesNetGrowth':[],'Sentiment_concentrationVar':[],'Sentiment_inOutVar':[],
                    'Sentiment_largetxsVar':[]}
    
    for coin in Symbol_df['Symbol']:
        time.sleep(0.75)

        try:

            U1="https://min-api.cryptocompare.com/data/social/coin/latest?coinId="+coin_dict[coin]+"&api_key=6013d40887f97ef57ac70f3540ea90e4d9739a63480492c2f9516b57c82102d0"
            sentiment=urllib.request.urlopen(U1).read().decode('UTF-8')
            responseJson_senti = json.loads(sentiment)
        except:
            print(coin,' Not Available')

        sentiment_dict['Coin'].append(coin)
        
            
        metrics=['Comments','Followers','PageViews','Posts']
        for metric in metrics:
            
            if metric in responseJson_senti['Data']['CryptoCompare']:
                sentiment_dict[metric].append(responseJson_senti['Data']['CryptoCompare'][metric])
            else:
                sentiment_dict[metric].append('-')

                
        metrics=['active_users','comments_per_day','comments_per_hour','community_creation','posts_per_day','posts_per_hour','subscribers']
        for metric in metrics:
            if metric in responseJson_senti['Data']['Reddit']:
                sentiment_dict['REDDIT_'+metric].append(responseJson_senti['Data']['Reddit'][metric])
            else:
                sentiment_dict['REDDIT_'+metric].append('-')

                
        metrics=['favourites','followers','following','statuses']
        for metric in metrics:
            if metric in responseJson_senti['Data']['Twitter']:
                sentiment_dict['TWITTER_'+metric].append(responseJson_senti['Data']['Twitter'][metric])
            else:
                sentiment_dict['TWITTER_'+metric].append('-')
        
        
        try:
            U2="https://min-api.cryptocompare.com/data/tradingsignals/intotheblock/latest?fsym="+coin+"&api_key=6013d40887f97ef57ac70f3540ea90e4d9739a63480492c2f9516b57c82102d0"

            sentiment_scores=urllib.request.urlopen(U2).read().decode('UTF-8')
            responseJson_ss = json.loads(sentiment_scores)

        except:
            print(coin,' Not Available')

        
        
        metrics=['addressesNetGrowth','concentrationVar','inOutVar','largetxsVar']
        for metric in metrics:
            if metric in responseJson_ss['Data']:
                if 'sentiment' in responseJson_ss['Data'][metric]:
                    sentiment_dict['Sentiment_'+metric].append(responseJson_ss['Data'][metric]['sentiment'])
                else:
                    sentiment_dict['Sentiment_'+metric].append('-')
            else:
                    sentiment_dict['Sentiment_'+metric].append('-')

            ##############################################################################################################

    sentiment_df=pd.DataFrame.from_dict(sentiment_dict)
    
    return sentiment_df
