import sys
sys.path.insert(0, '..')
from pymongo import MongoClient
import pandas as pd
import numpy as np
from parse_to_mongo.mongo_global_variables import MONGO_URI, MONGO_DB, \
    COLLECTION_NAME

def filter_on_salary(threshold = 10000, bounds = 'min', 
                     uri = MONGO_URI, db = MONGO_DB, 
                     colletion = COLLECTION_NAME):
    '''
    Return vacancies with salary greater than specified threshold. 

    Parameters
    ----------
    threshold : float, optional
        Threshold to search job posts with salary greater than this value.
        The default is 10000.
    
    bounds : str, optional
        Which bound to use for filtering. Eiter of the following:
            - 'min' - filter on the lower bound of salaries
            - 'max' - filter on the upper bound of salaries
            - 'no' - select vacancies without salary specified.
        The default is 'min'.
    
    uri : str, optional
        MongoDB URI. The default is "127.0.0.1:27017".
    
    db : str, optional
        MongoDB database name. The default is "vacancies".
    
    colletion : str, optional
        MongoDB database collection name. The default is "jobs_data".

    Returns
    -------
    df : pandas DataFrame
        Filtered dataframe.
    '''
    with MongoClient(uri) as client:
        db = client[db]
        coll = db[colletion]
       
        if bounds == 'min':
            result = coll.find(
            {"payment_from": {"$gte": threshold}},
        )
            
        elif bounds == 'max':
            result = coll.find(
            {"payment_to": {"$gte": threshold}},
        )
            
        elif bounds == 'no':
            result = coll.find({
            '$and':[
                {"payment_from": None},
                {'payment_to': None}
                ]}
        )
        
        df =  pd.DataFrame(list(result))
    
    return df





