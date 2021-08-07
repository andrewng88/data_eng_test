import pandas as pd

def load_df(file):
    '''
    read of the excel file and subset the columns accordingly
    input an excel file
    '''
    df=pd.read_excel(file)
    cols = ['num_confirmed','num_deaths','num_recovered']
    return df[cols]