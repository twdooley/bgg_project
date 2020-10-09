"""Module to open pickled dfs.
Functions: jar_open(pickles = )"""
import pandas as pd
import pickle 

gerkins = ['1v2', '2v2', '3v2', '4v2', '5v2', '6v2', 
           '7_8v2', '9_15v2']
def jar_open(pickles = gerkins):
    """Takes a list of pickled dfs to open them, clean data, concat into one df
    Param:
        pickles = list; default value gerkins built-in. page_{}.pickle
    Returns:
        concat df with corrected types."""
    dfs=[]
    for dill in pickles :
        with open('page_{}.pickle'.format(dill),'rb') as read_file:
            df = pickle.load(read_file)
            dfs.append(df)
    df = (pd.concat(dfs))
    df.iloc[:,1]=df.iloc[:,1].astype(float)
    df.iloc[:,7:29] = df.iloc[:,7:29].astype(float)
    df.iloc[:,30:34]=df.iloc[:,30:34].astype(float)
    
    return df



