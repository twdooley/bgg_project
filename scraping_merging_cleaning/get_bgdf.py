import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

ua = UserAgent()
user_agent = {'User-agent': ua.random}
print(user_agent)


chromedriver = "/Applications/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


def make_bgdf(passed_url=""):
    """Makes a DataFrame for one page (100 entries) of BoardGameGeek.
    Params: 
        url = '' by default. pass '/page/2' et c. 
    Returns:
        a merged DF of overall list with individual stats."""
    url = f'https://boardgamegeek.com/browse/boardgame{passed_url}'
    response = requests.get(url, headers = user_agent)
    response.status_code

    page = response.text 
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table')
    rows = [row for row in table.find_all('tr')]

    games = {}

    for row in rows[1:101]:
        items = row.find_all('td')
        title = items[2].find('a').text
        url = items[2].find('a')['href']
        price = items[-1].find('a')['href']
        #url, name = link['href'], link.get('title')
        games[title] = [url] + [i.text.strip('\n\r\t": ') for i in items] + [price]

    games_df = pd.DataFrame(games).T
    games_df.columns = ['link', 'rank', 'delete', 'desc', 'geek', 'rating', 'num_voters', 'delete2', 'price']
    games_df = games_df.drop(['delete', 'delete2'], axis = 1)

    games_df.geek = games_df.geek.astype(float)
    games_df.rating = games_df.rating.astype(float)
    games_df.num_voters = games_df.num_voters.astype(int)

    dfs = []

    for row in range(len(games_df)):
        driver.get(url = f'https://boardgamegeek.com{games_df.link[row]}')
        metal_soup = BeautifulSoup(driver.page_source, 'lxml')
        url = f'https://boardgamegeek.com{games_df.link[row]}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Website unresponsive")
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        script = soup.find_all('script')
        script_str = str(script)
        start = script_str.index('"stats":')
        end = script_str.index(',"relatedcounts')
        stats = script_str[int(start+9): int(end-1)]
        remove_comma = stats.split(",")

        stat_dict = {}
        for string in remove_comma:
            key,value = string.split(':')
            key = key.strip('"')
            value = value.strip('"')
            stat_dict[key] = value
        
        #Need stats from another area. Get index and split again as above. 
        try:    
            another_start = script_str.index('"yearpublished":')
            another_end = script_str.index('"override_rankable":')
            more_stats = script_str[int(another_start): int(another_end-1)]
            new_remove_comma = more_stats.split(",")
        
            for string in new_remove_comma:
                key,value = string.split(':')
                key = key.strip('"')
                value = value.strip('"')
                stat_dict[key] = value
        except:
            pass # pass if not, continue
        
        #see if Walmart pricing is available 
        try:
            wal_start = script_str.index('"walmart_price":')
            wal_end = script_str.index('"media":')
            wal_stats = script_str[int(wal_start): int(wal_end-3)]
            wal_remove_comma = wal_stats.split(",")
            wal_remove_comma

            for string in wal_remove_comma:
                key,value = string.split(':')
                key = key.strip('"')
                value = value.strip('"')
                stat_dict[key] = value
        except:
            pass #pass if not, continue
        
        #Get theme/genres if available
        
        try:

            theme_start = script_str.index('"prettyname":')
            theme_end = script_str.index('}],"polls":{"')
            theme_str = script_str[int(theme_start):int(theme_end)]

            theme_dict = {}
            theme_remove_comma = theme_str.split(",")
            for string in theme_remove_comma:
                key,value = string.split(':')
                key = key.strip('"')
                value = value.strip('"')
                if key not in theme_dict.keys():
                    theme_dict[key] = value
                else:
                    theme_dict[key] += ", "+ value

            #find genres by unique index
            genres = theme_dict['veryshortprettyname']
            #clean genre information, remove Overall rank, strip, split. 
            genres = genres.replace("Overall, ", "")
            genres = genres.strip()
            split_genres = genres.split(',')

            for item in split_genres:
                if 'genres' not in stat_dict.keys():
                    stat_dict['genres'] = item
                else:
                    stat_dict['genres'] += "," +item
        except:
            pass
        #see if designer is available, append to stats_dict
        try:  
            
            designer_start = script_str.index('"boardgamedesigner":[{"name":')
            designer_end = script_str.index(',"objecttype":"person"')
            designer_str = script_str[int(designer_start + 22):int(designer_end)]

            key, value = designer_str.split(':')
            value = value.strip('"')
            stat_dict['designer'] = value
        except:
            pass  # pass if not, continue

        try:  #see if publisher is available. Append to stats_dict
            publisher_start = script_str.index('"boardgamepublisher":[{"name":')
            publisher_end = script_str.index('"objecttype":"company"')
            publisher_str = script_str[int(publisher_start + 23):int(publisher_end - 1)]

            key, value = publisher_str.split(':')
            value = value.strip('"')
            stat_dict['publish'] = value
        except:
            pass  # pass if not, continue
        
        #Get top pricing on BGG, except and pass if not available. Need Selenium
        try:
            price_txt = metal_soup.find_all('strong', class_="ng-binding")
            #check position 1&2 for dollar amount, if none, return none and convert to be equal
            #to other amount (i.e. price1 = None, price1= price2)
            #then get average price
            price1 = price_txt[1].text
            try:
                price1 = float(price1[1:])
            except:
                price1 = None
            price2 = price_txt[2].text
            try:
                price2 = float(price2[1:])
            except:
                price2 = None
            if price1 == None:
                price1 = price2
            if price2 == None:
                price2 = price1
            mean_price = (price1 + price2)/2
            stat_dict['price_mkt'] = mean_price
        except:
            pass #pass if nothing
        
        #Get index/Title to add as key for dictionary to build new DataFrame
        index = soup.find('title').text
        index = index.split('|')[0]
        index = index.strip()

        df_dict= {}
        df_dict[index]=stat_dict
        stat_df = pd.DataFrame(df_dict).T
        dfs.append(stat_df)
    
    concat_dfs = pd.concat(dfs)
    
    final = games_df.join(concat_dfs)
    return final

