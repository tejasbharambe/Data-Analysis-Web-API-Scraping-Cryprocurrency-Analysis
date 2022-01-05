import scraper
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:.2f}'.format
import squarify
import matplotlib
import sys
import time


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def move_figure(f):
    """Move figure's upper left corner to pixel (x, y)"""
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        #f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        mng = plt.get_current_fig_manager()
        ### works on Ubuntu??? >> did NOT working on windows
        # mng.resize(*mng.window.maxsize())
        mng.window.state('zoomed')
    elif backend == 'WXAgg':
        #f.canvas.manager.window.SetPosition((x, y))
        mng = plt.get_current_fig_manager()
        mng.frame.Maximize(True)
    
def plot_market_cap(topn_crypto,marketcap):

    #plt.axis([-50,50,0,10000])
    #plt.ion()
    #plt.show()
    #plt.pause(0.001)
    data = marketcap.loc[:topn_crypto,['Name','Price_in_USD','Market Cap','% MC','Cumm. % MC']]
    f,ax=plt.subplots()
    
    plt.rcParams['figure.figsize'] = [20, 10]

    # use the scatterplot function to build the bubble map
    sns.scatterplot(data=data, x="Name", y="% MC", size="Market Cap", legend=False, sizes=(200, 2000),alpha=0.5)
    # plt.ticklabel_format(useOffset=False)

    plt.title('Top '+str(topn_crypto)+' crytocurrencies market cap distribution\n The size of each circle depends on the market cap of that crypto\n\n For eg. Bitcoin captures >40% of the total cryptocurrency market capitalization',fontsize=20)
    plt.xlabel('Crytocurrencies',fontsize=15)
    plt.ylabel('Market Cap Portion (in %)',fontsize=15)


    plt.xticks(rotation=40, ha="right")
    plt.yticks(fontsize=15)
    plt.tight_layout()
    plt.grid()
    move_figure(f)
    plt.subplots_adjust(left=0.105, bottom=0.35, right=0.71, top=0.808, wspace=0.2, hspace=0.2)
    
    # show the graph
    plt.show()

    #plt.pause(0.001)
    print("Dynamically Generated Insights:")
    print('--------------------------------')
    print("The most market of cryptocurrency is captured by",
          marketcap.loc[0,['Name']].iloc[0],'-',marketcap.loc[0,['Market Cap']].iloc[0],'USD (',
          round(marketcap.loc[0,['% MC']].iloc[0],2),'% )')
    print('The second most market of cryptocurrency is captured by',
          marketcap.loc[1,['Name']].iloc[0],'-',marketcap.loc[1,['Market Cap']].iloc[0],'USD (',
          round(marketcap.loc[1,['% MC']].iloc[0],2),'% )')
    print('The third most market of cryptocurrency is captured by',
          marketcap.loc[2,['Name']].iloc[0],'-',marketcap.loc[2,['Market Cap']].iloc[0],'USD (',
          round(marketcap.loc[2,['% MC']].iloc[0],2),'% )')
    print("\nThe top 3 cyrptocurrencies capture",round(marketcap.loc[2,['Cumm. % MC']].iloc[0],2),'% of the market')
    print("The top 5 cyrptocurrencies capture",round(marketcap.loc[4,['Cumm. % MC']].iloc[0],2),'% of the market')
    print("The top 10 cyrptocurrencies capture",round(marketcap.loc[9,['Cumm. % MC']].iloc[0],2),'% of the market')
    print("The top 15 cyrptocurrencies capture",round(marketcap.loc[14,['Cumm. % MC']].iloc[0],2),'% of the market')
    print("The top 25 cyrptocurrencies capture",round(marketcap.loc[24,['Cumm. % MC']].iloc[0],2),'% of the market')
    time.sleep(2)

def get_crypto_details(coin_symbol,marketcap,final_df,currency_ticker_df2,sentiment_df2):
    time.sleep(2)
    print('\n\n\n\n\n\n\n\nX--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
    print('X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
    
    print('--------------------------------------------------------------------------------------------------------------')
    print('Detailed Report of the Cryptocurrency for',coin_symbol)
    print('--------------------------------------------------------------------------------------------------------------')
    
    print('\n--------------------------------------------------------------------------------------------------------------')
    print('Basic Information')
    print('--------------------------------------------------------------------------------------------------------------')
    
    marketcap_rank=final_df.loc[:,['Name','Symbol','Market Cap','Price_in_USD','URL','Circulating Supply']]
    marketcap_rank['% MC']=marketcap_rank['Market Cap']/sum(marketcap_rank['Market Cap'])*100
    marketcap_rank['Cumm. % MC']=marketcap_rank['% MC'].cumsum()
    mc_rank=marketcap_rank[marketcap_rank['Symbol']==coin_symbol]
    
    print('Name                               :',mc_rank.loc[:,'Name'].iloc[0])
    print('Symbol                             :',mc_rank.loc[:,'Symbol'].iloc[0])
    print('Current Price(USD)                 :',mc_rank.loc[:,'Price_in_USD'].iloc[0])
    print('Total Market Cap(USD)              :',mc_rank.loc[:,'Market Cap'].iloc[0])
    print('% of crytocurrency market captured :',round(mc_rank.loc[:,'% MC'].iloc[0],2),'%')
    print('Circulating Supply                 :',mc_rank.loc[:,'Circulating Supply'].iloc[0])
    print('URL                                :',mc_rank.loc[:,'URL'].iloc[0])
    
    print('\n--------------------------------------------------------------------------------------------------------------')
    print('Historical Data/Returns for',coin_symbol)
    print('--------------------------------------------------------------------------------------------------------------')
    
    columns=currency_ticker_df2.columns
    columns=columns[1:]
    count_1=0
    count_2=0
    count_3=0
    count_4=0
    for i,col in enumerate(columns):
        data=currency_ticker_df2.loc[:,['currency',col]].sort_values(col,ascending=False).reset_index()
        data=data[data['currency']==coin_symbol]
        
        if int(i/3)==0:
            count_1+=1
            if count_1==1:
                print('\nBased on the changes in the last 1 day:')
                print('-----------------------------------------')
        elif int(i/3)==1:
            count_2+=1
            if count_2==1:
                print('\nBased on the changes in the last 30 days:')
                print('-----------------------------------------')
        elif int(i/3)==2:
            count_3+=1
            if count_3==1:
                print('\nBased on the changes in the last 365 days:')
                print('-----------------------------------------')
        elif int(i/3)==3:
            count_4+=1
            if count_4==1:
                print('\nBased on the changes in the last YTD:')
                print('-----------------------------------------')
        if int(i/3)==4:
            if col=='max_supply':
                print('\nThe maximum supply of ',coin_symbol,': ',data.loc[:,col].iloc[0])
            elif col=='num_exchanges':
                print('The number of exchanges for ',coin_symbol,': ',data.loc[:,col].iloc[0])
            elif col=='num_pairs':
                print('The number of pairs for ',coin_symbol,': ',data.loc[:,col].iloc[0],'\n')
                
                
        else:
            if i%3==0:
                print('Change in Market Cap :',data.loc[:,col].iloc[0],'% and is ranked at',data.index[0]+1)
            if i%3==1:
                print('Change in Price      :',data.loc[:,col].iloc[0],'% and is ranked at',data.index[0]+1)
            if i%3==2:
                print('Change in Volume     :',data.loc[:,col].iloc[0],'% and is ranked at',data.index[0]+1)
        
    
    print('\n--------------------------------------------------------------------------------------------------------------')
    print('Social Media Trends for',coin_symbol)
    print('--------------------------------------------------------------------------------------------------------------')
    
    columns=sentiment_df2.columns
    columns_1=columns[1:-4]
    columns_2=columns[-4:]

    columns_1=columns_1.drop('REDDIT_community_creation')

    count_1=0
    count_2=0
    count_3=0
    
    for j,col in enumerate(columns_1):
        try:
            data=sentiment_df2.loc[:,['Coin',col]].sort_values(col,ascending=False).reset_index()
            data=data[data['Coin']==coin_symbol]

            if(data[col].iloc[0]==0):
                print(col,': Data Not Available')
            else:
                if j<4:
                    count_1+=1
                    if count_1==1:
                        print('\nBased on Cryptocompare Social Media data:')
                        print('-----------------------------------------')
                    print('Cryptocompare',col,':',data.loc[:,col].iloc[0],' and is ranked at',data.index[0]+1)
                elif j<10:
                    count_2+=1
                    if count_2==1:
                        print('\nBased on Reddit Social Media data:')
                        print('-----------------------------------------')
                    print(col,':',data.loc[:,col].iloc[0],' and is ranked at',data.index[0]+1)
                else:
                    count_3+=1
                    if count_3==1:
                        print('\nBased on Twitter Social Media :')
                        print('-----------------------------------------')
                    print(col,':',data.loc[:,col].iloc[0],' and is ranked at',data.index[0]+1)

        except:
            print("EXCEPTION:",col)

    print('\n--------------------------------------------------------------------------------------------------------------')
    print('Technical Analysis Indicators for ',coin_symbol)
    print('--------------------------------------------------------------------------------------------------------------')
            
    for j,col in enumerate(columns_2):
        try:
            data=sentiment_df2.loc[:,['Coin',col]]
            data=data[data['Coin']==coin_symbol]
            if(data[col].iloc[0]==0):
                print(col,': Data Not Available')
            else:
                if j==0:
                    print('\nBased on Addresses Net Growth Signal')
                    print('-----------------------------------------')
                    print('Momentum signal that gives an indication of the tokens underlying network health by measuring the amount of new addresses minus the addresses that have their balances emptied. It is bullish when more addresses are being created than emptied.')
                elif j==1:
                    print('\nBased on Concentration Signal:')
                    print('-----------------------------------------')
                    print('The Concentration signal is based on the accumulation (bullish) or reduction (bearish) of addresses with more than 0.1% of the circulating supply.')
                elif j==2:
                    print('\nBased on In Out Signal:')
                    print('-----------------------------------------')
                    print('This momentum signal calculates the net change of in/out of the money addresses, if the number of "In the Money" addresses is increasing this would be a bullish signal. In the money means addresses that would make a profit on the tokens they hold because they acquired the tokens at a lower price.')
                elif j==3:
                    print('\nBased on Large Tokens Signal:')
                    print('-----------------------------------------')
                    print('Momentum signal that is bullish when the short term trend of the number of txs > $100k is greater than the long term average.')
                
                print('\n',col,':',data.loc[:,col].iloc[0])
                
        except:
            print("EXCEPTION:",col)

    print('\nX--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
    print('X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
    time.sleep(2)
# Sorted by reddit comments per day
def returns_stats(no_of_crypto,currency_ticker_df2,sym2name):
    d365_mc_pct=currency_ticker_df2.loc[:,['currency','365d_market_cap_change_pct']].sort_values('365d_market_cap_change_pct',ascending=False)
    ytd_mc_pct=currency_ticker_df2.loc[:,['currency','ytd_market_cap_change_pct']].sort_values('ytd_market_cap_change_pct',ascending=False)
    d30_mc_pct=currency_ticker_df2.loc[:,['currency','30d_market_cap_change_pct']].sort_values('30d_market_cap_change_pct',ascending=False)

    d365_pc_pct=currency_ticker_df2.loc[:,['currency','365d_price_change_pct']].sort_values('365d_price_change_pct',ascending=False)
    ytd_pc_pct=currency_ticker_df2.loc[:,['currency','ytd_price_change_pct']].sort_values('ytd_price_change_pct',ascending=False)
    d30_pc_pct=currency_ticker_df2.loc[:,['currency','30d_price_change_pct']].sort_values('30d_price_change_pct',ascending=False)

    d365_vc_pct=currency_ticker_df2.loc[:,['currency','365d_volume_change_pct']].sort_values('365d_volume_change_pct',ascending=False)
    ytd_vc_pct=currency_ticker_df2.loc[:,['currency','ytd_volume_change_pct']].sort_values('ytd_volume_change_pct',ascending=False)
    d30_vc_pct=currency_ticker_df2.loc[:,['currency','30d_volume_change_pct']].sort_values('30d_volume_change_pct',ascending=False)

    ##### Write a SQL query and then pull the output.

    for i,data in enumerate([d365_mc_pct,ytd_mc_pct,d30_mc_pct,d365_pc_pct,ytd_pc_pct,d30_pc_pct,d365_vc_pct,ytd_vc_pct,d30_vc_pct]):
        
        f=plt.figure(figsize=(30,10))

        plt.ticklabel_format(useOffset=False)
        plt.ticklabel_format(useOffset=False, style='plain')

        height=data.iloc[:,1].iloc[:no_of_crypto]
        bars=data['currency'].iloc[:no_of_crypto]
        # patches,texts=plt.pie(height,labels=bars,labeldistance=1.15)

        x_pos=np.arange(len(bars))

        plt.bar(x_pos,height,alpha=0.5)
        plt.xticks(x_pos,bars,fontsize=10,rotation=40, ha="right")
        plt.yticks(fontsize=10)
        plt.tight_layout()

        rank1=sym2name[sym2name['Symbol']==bars.iloc[0]].loc[:,['Name']].iloc[0][0]
        rank2=sym2name[sym2name['Symbol']==bars.iloc[1]].loc[:,['Name']].iloc[0][0]
        rank3=sym2name[sym2name['Symbol']==bars.iloc[2]].loc[:,['Name']].iloc[0][0]

        if i<3:
            label_header='Market Capitalization Change'
        elif i<6:
            label_header='Price Change'
        else:
            label_header='Volume Change'

        if i%3==0:
            day_header='365 days'
        elif i%3==1:
            day_header='YTD'
        else:
            day_header='30 days'

        title_graph='Top '+str(no_of_crypto)+' Crytocurrencies based on '+label_header+' in the latest '+day_header
        plt.title(title_graph,fontsize=15)
        plt.xlabel('Crytocurrencies',fontsize=15)
        plt.ylabel('% '+label_header,size=15)
        print('\n')
        move_figure(f)
        plt.subplots_adjust(left=0.105, bottom=0.35, right=0.71, top=0.808, wspace=0.2, hspace=0.2)
    
        plt.show()
        #plt.pause(0.001)
        print("Dynamically Generated Insights:")
        print('--------------------------------')
        print("Rank 1: ",rank1," with ",label_header," of",round(height.iloc[0],2),'%',"in the last",day_header)
        print("Rank 2: ",rank2," with ",label_header," of",round(height.iloc[1],2),'%',"in the last",day_header)
        print("Rank 3: ",rank3," with ",label_header," of",round(height.iloc[2],2),'%',"in the last",day_header)
        print('\nX--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
        time.sleep(2)

##### Write a SQL query and then pull the output.
def cryptocompare_social_media(no_of_cryptos,sentiment_df2,sym2name):
    for j,data_header in enumerate(['Posts','Comments','PageViews','Followers']):

        f=plt.figure(figsize=(30,10))

        plt.ticklabel_format(useOffset=False)
        plt.ticklabel_format(useOffset=False, style='plain')

        data_extract=sentiment_df2.iloc[:no_of_cryptos,:].sort_values(data_header,ascending=False)
        height=data_extract[data_header]
        bars=data_extract['Coin']

        # patches,texts=plt.pie(height,labels=bars,labeldistance=1.15)
        patches,texts,_=plt.pie(height,autopct='%1.2f%%',shadow=True, radius=0.75,textprops=dict(color="w"))
        plt.legend(patches, bars, loc="right")

        title_graph='Top '+str(no_of_cryptos)+' Crytocurrencies based on number of '+data_header+ ' in CryptoCompare social media portal'
        plt.title(title_graph,fontsize=15)
        print('\n\n')
        move_figure(f)
        plt.subplots_adjust(left=0.105, bottom=0.35, right=0.71, top=0.808, wspace=0.2, hspace=0.2)

        plt.show()
        #plt.pause(0.001)
        rank1=sym2name[sym2name['Symbol']==bars.iloc[0]].loc[:,['Name']].iloc[0][0]
        rank2=sym2name[sym2name['Symbol']==bars.iloc[1]].loc[:,['Name']].iloc[0][0]
        rank3=sym2name[sym2name['Symbol']==bars.iloc[2]].loc[:,['Name']].iloc[0][0]

        print('Cryto Compare Social Media Platform - #',data_header," (Dynamically Generated Insights):")
        print('-------------------------------------------------------------------------------------')
        print("Rank 1: ",rank1," with a total of",round(height.iloc[0],2),data_header,' on cryptocompare')
        print("Rank 2: ",rank2," with a total of",round(height.iloc[1],2),data_header,' on cryptocompare')
        print("Rank 3: ",rank3," with a total of",round(height.iloc[2],2),data_header,' on cryptocompare')
        print('\nX--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
        time.sleep(2)

def reddit_stats(no_of_crypto,sentiment_df2,sym2name):
    
    for j in ['REDDIT_comments_per_day','REDDIT_posts_per_day','REDDIT_posts_per_hour','REDDIT_subscribers']:
        data_extract=sentiment_df2.sort_values(j,ascending=False).iloc[:no_of_crypto,:]
        height=data_extract[j]
        bars=data_extract['Coin']

        cmap = matplotlib.cm.Blues
        mini=min(data_extract[j])
        maxi=max(data_extract[j])
        norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
        colors = [cmap(norm(value)) for value in data_extract[j]]
        
        fig1 = plt.figure(figsize=(30,10))
        ax = fig1.add_subplot()
        labels = [f'{coin_}\n{value_}' for coin_,value_ in zip(data_extract['Coin'], data_extract[j])]

        squarify.plot(sizes=data_extract[j], label=labels,color=colors,
                      alpha=.7, bar_kwargs=dict(linewidth=0.5, edgecolor="#222222"),text_kwargs={'fontsize':10,'wrap':True},pad=False)

        title_graph='Treemap: Top '+str(no_of_crypto)+' Crytocurrencies based on number of '+j+ ' in Reddit social media portal'
        plt.title(title_graph,fontsize=15)
        plt.axis('off')
        move_figure(fig1)
        plt.subplots_adjust(left=0.105, bottom=0.35, right=0.71, top=0.808, wspace=0.2, hspace=0.2)
    
        plt.show()
        #plt.pause(0.001)
        rank1=sym2name[sym2name['Symbol']==bars.iloc[0]].loc[:,['Name']].iloc[0][0]
        rank2=sym2name[sym2name['Symbol']==bars.iloc[1]].loc[:,['Name']].iloc[0][0]
        rank3=sym2name[sym2name['Symbol']==bars.iloc[2]].loc[:,['Name']].iloc[0][0]

        print(j," (Dynamically Generated Insights):")
        print('--------------------------------------------------------')
        print("Rank 1: ",rank1," with a total of",round(height.iloc[0],2),j)
        print("Rank 2: ",rank2," with a total of",round(height.iloc[1],2),j)
        print("Rank 3: ",rank3," with a total of",round(height.iloc[2],2),j)
        print('\nX--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
        time.sleep(2)

def twitter_stats(no_of_crypto,sentiment_df2,sym2name):
    for j in ['TWITTER_favourites','TWITTER_followers','TWITTER_following', 'TWITTER_statuses']:    
        data_extract=sentiment_df2.sort_values(j,ascending=False).iloc[:no_of_crypto,:]
        # set figure size
        height=data_extract[j]
        bars=data_extract['Coin']

        cmap = matplotlib.cm.Blues
        mini=min(data_extract[j])
        maxi=max(data_extract[j])
        norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
        colors = [cmap(norm(value)) for value in data_extract[j]]
        
        fig1 = plt.figure(figsize=(30,10))
        ax = fig1.add_subplot()

        labels = [f'{coin_}\n{value_}' for coin_,value_ in zip(data_extract['Coin'], data_extract[j])]
        squarify.plot(sizes=data_extract[j], label=labels,color=colors,
                      alpha=.7, bar_kwargs=dict(linewidth=0.5, edgecolor="#222222"),text_kwargs={'fontsize':10,'wrap':True} )

        title_graph='Treemap: Top '+str(no_of_crypto)+' Crytocurrencies based on number of '+j+ ' in Twitter social media portal'
        plt.title(title_graph,fontsize=15)

        plt.axis('off')
        plt.subplots_adjust(left=0.105, bottom=0.35, right=0.71, top=0.808, wspace=0.2, hspace=0.2)
        move_figure(fig1)
        plt.subplots_adjust(left=0.105, bottom=0.35, right=0.71, top=0.808, wspace=0.2, hspace=0.2)
    
        plt.show()
        #plt.pause(0.001)
        rank1=sym2name[sym2name['Symbol']==bars.iloc[0]].loc[:,['Name']].iloc[0][0]
        rank2=sym2name[sym2name['Symbol']==bars.iloc[1]].loc[:,['Name']].iloc[0][0]
        rank3=sym2name[sym2name['Symbol']==bars.iloc[2]].loc[:,['Name']].iloc[0][0]

        print(j," (Dynamically Generated Insights):")
        print('--------------------------------------------------------')
        print("Rank 1: ",rank1," with a total of",round(height.iloc[0],2),j)
        print("Rank 2: ",rank2," with a total of",round(height.iloc[1],2),j)
        print("Rank 3: ",rank3," with a total of",round(height.iloc[2],2),j)
        print('\nX--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X--X')
        time.sleep(2)

def main():
    topic= 'https://coinmarketcap.com/'
    engine = scraper.create_engine('sqlite://', echo=False)

    if len(sys.argv)==1:
        final_df,currency_ticker_df,sentiment_df=scraper.normal_scrape(topic,engine)

    elif sys.argv[1]=='--static':
        listout=scraper.static_scrape(topic,engine)
        final_df,currency_ticker_df,sentiment_df=listout[0],listout[1],listout[2]

    final_df[final_df.columns[[3,5,6]]] = final_df[final_df.columns[[3,5,6]]].replace('[\$,]', '', regex=True).astype(float)

    currency_ticker_df2=currency_ticker_df.replace(r'^-*$', np.nan, regex=True)
    currency_ticker_df2=currency_ticker_df2.fillna(0.0)
    for i in range(len(currency_ticker_df2.columns)):
        if i>0:
            currency_ticker_df2.iloc[:,i]=currency_ticker_df2.iloc[:,i].astype(float).round(4)

    sym2name=final_df.loc[:,['Name','Symbol']]
    
    sentiment_df=sentiment_df.replace(r'^-*$', np.nan, regex=True)
    sentiment_df2=sentiment_df.fillna(0.0)
    for i in range(len(sentiment_df2.columns)):
        if i>0 and i<16:
            sentiment_df2.iloc[:,i]=sentiment_df2.iloc[:,i].astype(float).round(4)

    marketcap=final_df.loc[:,['Name','Market Cap','Price_in_USD']]
    marketcap['% MC']=marketcap['Market Cap']/sum(marketcap['Market Cap'])*100
    marketcap['Cumm. % MC']=marketcap['% MC'].cumsum()
    
    
    plot_market_cap(25,marketcap)
    returns_stats(10,currency_ticker_df2,sym2name)
    cryptocompare_social_media(10,sentiment_df2,sym2name)
    reddit_stats(10,sentiment_df2,sym2name)
    twitter_stats(10,sentiment_df2,sym2name)    

    get_crypto_details('BTC',marketcap,final_df,currency_ticker_df2,sentiment_df2)
    get_crypto_details('ETH',marketcap,final_df,currency_ticker_df2,sentiment_df2)
    get_crypto_details('XRP',marketcap,final_df,currency_ticker_df2,sentiment_df2)

if __name__ == '__main__':
    main()
