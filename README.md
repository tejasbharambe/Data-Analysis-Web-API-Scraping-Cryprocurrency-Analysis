# Web-Scrapper

### Motivation:
Lately, cryptocurrencies have gained a lot of popularity in the finance sector owing to the massive returns, they have been offering since last few years. There are more than thousands of cryptocurrencies that have been generated.  

This project focuses on the top 25 cryptocurrencies as they constitute more than 90% of the cryptocurrency market capitalization. The idea is to focus on the cryptocurrencies which are currently trending based on the historical returns as well as based on the sentiments across various social media platforms. 

This is an interesting problem to make public aware of the highly trending cryptocurrencies and guide them while doing the investments. The project identifies top 10 cryptocurrencies based on market cap, social media attention on Reddit, Twitter and Cryptocompare. Additionally, based on the current price of the cryptocurrency and the technical indicator, the project also suggests whether a particular cryptocurrency shows a bullish signal or a bearish signal or is neutral.


### Objective:
Performed the following analytics and visualizations based on the data using python concepts like Data structures, Class, Functions, Web scraping websites, File concepts:

1. Identify top 25 cryptocurrencies based on market capitalization and their market capture. Insights and visualizations added using scatter plot and bar plot

2. Compare various cryptocurrencies and identify top 10 based on volume, market cap, price change% for 1 day, 30 days, 365 days, YTD. Insights and visualizations added using the bar charts

3. Compare various cryptocurrencies and identify top 10 cryptocurrencies based on the cryptocompare social media trends like # posts, comments, page views and followers.

4. Compare various cryptocurrencies and identify top 10 cryptocurrencies based on the reddit and twitter social media trends like #comments, posts per day, posts per hour, subscribers, tweets, followers and following.

5. Finally, generated a detailed summary report for 3 cryptocurrencies highlighting all the basic information, historical returns, social media trends and technical indicators suggesting buy/sell of that cryptocurrency


## Requirements to run this entire module:

You may refer to the pdf/ppt shared in the ZIP for all the steps. It is more detailed and has snapshots too.

Things to ensure to run the script:

1. Please don't change the folder structure.

'Code' folder contains all the .py files. There are 5 files there. The HW5_Final_Project.py is the main file and it imports from
	-> scraper.py - This is to scrape the data from API/wesbites and (or) csv files. It uses:
		 -> Coin_Market_Cap.py - This is to scrape the data from website
		 -> Cryptocompare.py - This is to scrape the data from API #1
		 -> Currency_Ticker_Nomics.py - This is to scrape the data from API #2
	-> HW5_Final_Project.py – This contains the code for performing the analytics and insights. This is the only main file which needs to be run. The rest all files are supporting code files. 

'Data' folder contains the scrapped data from APIs and website in csv format
'Data_Generated_For_Processing_Not_Output' contains the intermediate data which is needed for processing of the data


2. Steps to run the code:
2.1 Go to the code folder
2.2 Open command prompt in this folder location i.e. in 'code' folder
2.3 Run either of the following commands:
	--> python3 HW5_Final_Project.py
	--> python3 HW5_Final_Project.py --static
	
You can find these commands along with the snapshots in the shared ppt/pdf file


3.1 Package requirements:
-> Requests
-> Bs4 (Beautiful soup)
-> Pandas
-> Urllib
-> JSON
-> Time
-> Sys
-> CSV
-> SQL Alchemy
-> Seaborn
-> Matplotlib.pyplot
-> Numpy
-> Squarify
-> warnings


3.2 Version Requirements
beautifulsoup4==4.10.0
bs4==0.0.1
certifi==2021.10.8
charset-normalizer==2.0.7
cycler==0.11.0
edx-dl==0.1.13
fonttools==4.28.2
greenlet==1.1.2
html5lib==1.1
idna==3.3
kiwisolver==1.3.2
matplotlib==3.5.0
numpy==1.21.4
packaging==21.3
pandas==1.3.4
Pillow==8.4.0
pyparsing==3.0.6
python-dateutil==2.8.2
pytz==2021.3
requests==2.26.0
ruamel.yaml==0.17.17
ruamel.yaml.clib==0.2.6
scipy==1.7.3
seaborn==0.11.2
setuptools-scm==6.3.2
six==1.16.0
soupsieve==2.3.1
SQLAlchemy==1.4.27
squarify==0.4.3
tabulate==0.8.9
tomli==1.2.2
urllib3==1.26.7
webencodings==0.5.1
youtube-dl==2021.6.6


Note: The pip install commands are already included in the folder. Hence, ideally this shouldn't be a concern.



4. Extensibility of the code:
4.1 The output from this code can be used directly to draw some additional insights, analytics and conclusions from the data
4.2 Some modules of the code can be further used for cleaning, grouping and even extracting the new data from website/API if needed


5. Maintainability of the code:
5.1 The crytocurrency data that my code uses is updated at each second. Hence, there might be some ambiguity which might arise while running the code. However, 
I have done as much exception handling as possible.
5.2 Because the data is based on the current price, the data that you might see may vary in the next run.
5.3 The code is purely dependent on the API and website's information. If website crashes or the website changes its format of storing the data/HTML changes. 
This will further impact the code. As long as the website and APIs are not updated drastically, the code should run correctly
5.4 Code is also dependent on the API Key which is assigned to me. But given this is a public API, it should work
