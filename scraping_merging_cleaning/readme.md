# README: Scraping and merging
## The notebooks were used to build the main scraping module found in get_bgdf.py
`get_bgdf.py` was used to scrape and merge in chunks. 
`project2_boardgames.ipynb` notebook collected these chunks as pickles. `merging_examining.ipynb` was used to explore these individual chunks and then finally collect it into a master .csv file. <br>
`build_genre.ipynb` was used to build another module `get_genre.py`. This was necessary to add genre information to the .csv which could then be dummy variables/features in my final model. <br>
The final file is now in a .csv found in the `data` file. 

