# import appropriate libraries

# to pass our secret location
import configparser 

# for api extraction and transformation
import requests 
import json 
import pandas as pd

from datetime import datetime
import dateutil.parser as parser

import logging

# output logging to api.log file
logging.basicConfig(filename='output\covid_api.log',
                    level = logging.DEBUG,
# format based on https://docs.python.org/3/library/logging.html#logrecord-attributes
                    format='%(asctime)s:%(levelname)s:%(message)s')


# Read a config file to get the location of an excel file 
config = configparser.ConfigParser()
config.read('secret_location.ini')
secret_location = config['DEFAULT']['secret_location']
df = pd.read_excel(secret_location)

# we use dictionary to help convert iso(number) to country id used by the API )
# info used https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
iso_to_country = {392 : 'JPN', 840: 'USA'}

# we set the rest of the variables
cols_we_cared_for = ['date','iso','num_confirmed','num_deaths','num_recovered']
url_pattern = 'https://covid-api.com/api/reports?date={}&iso={}'
output_filename = 'output\covid_data.xls'

def extract_from_api(df,url_pattern,iso_to_country,cols_we_cared_for,output_filename):
    
    '''
    this function helps us to extract information from the covid api
    
    inputs:
    
    df is a dataframe
    url_pattern is a string
    iso_to_country is a dictionary
    cols_we_cared for is a list
    output_filename is a string
    
    '''

    #input test for input
    assert isinstance(df, pd.DataFrame),"df with date and iso column"
    assert isinstance(url_pattern, str),"string as https://covid-api.com/api/reports?date={}&iso={}"
    assert isinstance(iso_to_country, dict),"dictionary {392 : 'JPN', 840: 'USA'}"
    assert isinstance(cols_we_cared_for, list),'list'
    assert isinstance(output_filename, str),"string" 
    
    df['cty'] = df.iso.apply(lambda x : iso_to_country[x])
    
    for index,row in df.iterrows():
        date = row['date'].strftime("%Y-%m-%d")
        cty = row['cty']

        # we try to connect to API , else we throw exception error
        try:
            # Create API endpoint
            # Trigger GET request
            url= url_pattern.format(date,cty)
            response = requests.request("GET", url)
            # Convert JSON(dictionary datastructure)
            api_data_dict = response.json()

            #impute values to df based on .loc 
            df.loc[index,'num_confirmed'] = api_data_dict['data'][0]['confirmed'] 
            df.loc[index,'num_deaths'] = api_data_dict['data'][0]['deaths']
            df.loc[index,'num_recovered'] = api_data_dict['data'][0]['recovered']

            #logging data
            input_log = 'inputs are {} ,{}'.format(date,cty)
            output_log = 'extracted from api are confirmed:{}, deaths:{},recovered:{}\n'.format(api_data_dict['data'][0]['confirmed'],api_data_dict['data'][0]['deaths'],api_data_dict['data'][0]['recovered'])

            logging.debug(input_log)
            logging.debug(output_log)

        except:
            error = 'Failed to connect to API\n'
            logging.debug(error)
            logging.debug(input_log)
            raise RuntimeError(error)
    
    #convert to str else xls will treat it as timestamp
    df['date']=df['date'].astype(str)
    
    # extract columns that we cared and save to excel
    df[cols_we_cared_for].to_excel(output_filename,index=False)
    print('Extracted from API and saved to Output folder')
    print('Next step, you may now run python -m unittest test_covid.py')

# run the above function
extract_from_api(df,url_pattern,iso_to_country,cols_we_cared_for,output_filename)