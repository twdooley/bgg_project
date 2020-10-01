import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


def genre_df(passed_url = ""):
    url = f'https://boardgamegeek.com/browse/boardgame{passed_url}'
    response = requests.get(url)
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
        games[title] = [url] + [i.text.strip('\n\r\t": ') for i in items]

    games_df = pd.DataFrame(games).T
    games_df.columns = ['link', 'rank', 'delete', 'desc', 'geek', 'rating', 'num_voters', 'delete2']
    games_df = games_df.drop(['delete', 'delete2'], axis = 1)

    games_df.geek = games_df.geek.astype(float)
    games_df.rating = games_df.rating.astype(float)
    games_df.num_voters = games_df.num_voters.astype(int)

    dfs = []
    df_dict= {}
    for row in range(len(games_df)):
        #As in get_bgdf, loop through links and read script
        url = f'https://boardgamegeek.com{games_df.link[row]}'
        response = requests.get(url)
        #check if website responds
        if response.status_code != 200:
            raise ValueError("Website unresponsive")
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        script = soup.find_all('script')
        script_str = str(script)
        #Find thematic/genre information 
        stat_dict = {}


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
            print(stat_dict)

        index = soup.find('title').text
        index = index.split('|')[0]
        index = index.strip()


        df_dict[index]=stat_dict
        print(df_dict)
    #stat_df = pd.DataFrame(df_dict).T
    #dfs.append(stat_df)
    df = pd.DataFrame(df_dict).T    
    #concat_dfs = pd.concat(dfs)
    #final = games_df.join(concat_dfs)
    return df