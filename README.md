# BoardGameGeek Game Rank Analysis
## Contents 
### **Problem**
-------------------------------
BoardGameGeek.com (BGG) is a boardgame database website that includes tens of thousands of entries. The data for each game includes the game's complexity, rating, designer, publisher, among many other points. Games are ranked according to BGG own ranking system. Further, they provide a 'Geek' rating alongside their user provided rating average to evaluate ranking. <br>
***Objective:*** Provide insight to boardgame designers and publishers regarding the prospective ranking of their game through a supervised learning model. 
### **Methods**
----------------------------
I created a scraping solution using BeautifulSoup and Selenium to scrape 10,000 entries in BGG.<br>
The use of Selenium was necessary to collect market price data from dynamic marketplace entries. 
The scraped data can be found in this repo as a .csv file for further analysis. 
In toto: 
``` python
Int64Index: 10018 entries, 0 to 10018
Data columns (total 113 columns):
 #   Column               Non-Null Count  Dtype         
---  ------               --------------  -----         
 0   link                 10018 non-null  object        
 1   rank                 10018 non-null  float64       
 2   desc                 10018 non-null  object        
 3   geek                 10018 non-null  float64       
 4   rating               10018 non-null  float64       
 5   num_voters           10018 non-null  int64         
 6   price                10018 non-null  object        
 7   average              10018 non-null  object        
 8   avgweight            10018 non-null  float64       
 9   baverage             10018 non-null  float64       
 10  maxplayers           10018 non-null  float64       
 11  maxplaytime          10018 non-null  float64       
 12  minage               10018 non-null  float64       
 13  minplayers           10018 non-null  float64       
 14  minplaytime          10018 non-null  float64       
 15  numcomments          10018 non-null  float64       
 16  numfans              10018 non-null  float64       
 17  numgeeklists         10018 non-null  float64       
 18  numhasparts          10018 non-null  float64       
 19  numowned             10018 non-null  float64       
 20  numplays             10018 non-null  float64       
 21  numplays_month       10018 non-null  float64       
 22  numprevowned         10018 non-null  float64       
 23  numtrading           10018 non-null  float64       
 24  numwanting           10018 non-null  float64       
 25  numwantparts         10018 non-null  float64       
 26  numweights           10018 non-null  float64       
 27  numwish              10018 non-null  float64       
 28  numwishlistcomments  10018 non-null  float64       
 29  playmonth            10018 non-null  object        
 30  price_mkt            3332 non-null   float64       
 31  stddev               10018 non-null  float64       
 32  usersrated           10018 non-null  float64       
 33  views                10018 non-null  float64       
 34  walmart_price        260 non-null    object        
 35  yearpublished        10018 non-null  float64       
 36  genres               10009 non-null  object        
 37  designer             9906 non-null   object        
 38  publish              10008 non-null  object        
 39  strategy_war         10018 non-null  int64         
 40  strategy             10018 non-null  int64         
 41  family               10018 non-null  int64         
 42  thematic             10018 non-null  int64         
 43  war                  10018 non-null  int64         
 44  party                10018 non-null  int64         
 45  abstract             10018 non-null  int64         
 46  rank_des             9906 non-null   float64       
 47  geek_des             9906 non-null   float64       
 48  rating_des           9906 non-null   float64       
 49  num_voters_des       9906 non-null   float64       
 50  baverage_des         9906 non-null   float64       
 51  maxplayers_des       9906 non-null   float64       
 52  maxplaytime_des      9906 non-null   float64       
 53  minage_des           9906 non-null   float64       
 54  minplayers_des       9906 non-null   float64       
 55  minplaytime_des      9906 non-null   float64       
 56  numcomments_des      9906 non-null   float64       
 57  numfans_des          9906 non-null   float64       
 58  numgeeklists_des     9906 non-null   float64       
 59  numowned_des         9906 non-null   float64       
 60  numplays_des         9906 non-null   float64       
 61  numplays_month_des   9906 non-null   float64       
 62  numtrading_des       9906 non-null   float64       
 63  numwanting_des       9906 non-null   float64       
 64  numwantparts_des     9906 non-null   float64       
 65  numweights_des       9906 non-null   float64       
 66  numwish_des          9906 non-null   float64       
 67  price_mkt_des        7238 non-null   float64       
 68  views_des            9906 non-null   float64       
 69  strategy_war_des     9906 non-null   float64       
 70  strategy_des         9906 non-null   float64       
 71  family_des           9906 non-null   float64       
 72  thematic_des         9906 non-null   float64       
 73  war_des              9906 non-null   float64       
 74  party_des            9906 non-null   float64       
 75  abstract_des         9906 non-null   float64       
 76  numdes               9906 non-null   float64       
 77  rank_pub             10008 non-null  float64       
 78  geek_pub             10008 non-null  float64       
 79  rating_pub           10008 non-null  float64       
 80  num_voters_pub       10008 non-null  float64       
 81  baverage_pub         10008 non-null  float64       
 82  maxplayers_pub       10008 non-null  float64       
 83  maxplaytime_pub      10008 non-null  float64       
 84  minage_pub           10008 non-null  float64       
 85  minplayers_pub       10008 non-null  float64       
 86  minplaytime_pub      10008 non-null  float64       
 87  numcomments_pub      10008 non-null  float64       
 88  numfans_pub          10008 non-null  float64       
 89  numgeeklists_pub     10008 non-null  float64       
 90  numowned_pub         10008 non-null  float64       
 91  numplays_pub         10008 non-null  float64       
 92  numplays_month_pub   10008 non-null  float64       
 93  numtrading_pub       10008 non-null  float64       
 94  numwanting_pub       10008 non-null  float64       
 95  numwantparts_pub     10008 non-null  float64       
 96  numweights_pub       10008 non-null  float64       
 97  numwish_pub          10008 non-null  float64       
 98  price_mkt_pub        8604 non-null   float64       
 99  views_pub            10008 non-null  float64       
 100 strategy_war_pub     10008 non-null  float64       
 101 strategy_pub         10008 non-null  float64       
 102 family_pub           10008 non-null  float64       
 103 thematic_pub         10008 non-null  float64       
 104 war_pub              10008 non-null  float64       
 105 party_pub            10008 non-null  float64       
 106 abstract_pub         10008 non-null  float64       
 107 numpub               10008 non-null  float64       
 108 yearpublished_dt     9964 non-null   datetime64[ns]
 109 diff_des             9906 non-null   float64       
 110 diff_pub             10008 non-null  float64       
 111 quality_des          10018 non-null  int64         
 112 quality_pub          10018 non-null  int64   
 ```
 
 Columns with suffix `des` represent mean values for a designer appended to each game they designed. Likewise, `pub` represents mean publisher data. <br>
 Genre columns are encoded with dummy variables (0,1). <br>
 `quality` entries include dummy variables with 1 being average or above average for designer/publisher. 
 
### **Results**
----------------------------
The model focuses on the following features : <br>
```python
sub_df[['avgweight', 'strategy','war','family', 'abstract', 'thematic', 'geek_des', 'geek_pub']]
sub_df['log_geek_des'] = np.log(sub_df['geek_des'])
sub_df['log_geek_pub'] = np.log(sub_df['geek_pub'])
```
<br>
Our target/response variable is the ranking on BGG. <br>
The R2 of this model is 0.54.


### **Moving Forward**
----------------------------

### **Appendix** 
----------------------------



