import sys
sys.path.insert(0, '..')

from job_sites_parser.jobs_parser import job_parser
from pymongo import MongoClient
import pymongo
import json
import pandas as pd
from parse_to_mongo.mongo_global_variables import MONGO_URI, MONGO_DB, \
    COLLECTION_NAME
from pymongo.errors import BulkWriteError


def load_jobs_to_mongo(uri = MONGO_URI, db = MONGO_DB, 
                       colletion = COLLECTION_NAME):
    '''
    Function to parse vacancies directly to MongoDB database collection

    Parameters
    ----------
    uri : str, optional
        MongoDB URI. The default is "127.0.0.1:27017".
    
    db : str, optional
        MongoDB database name. The default is "vacancies".
    
    colletion : str, optional
        MongoDB database collection name. The default is "jobs_data".

    '''
    
    with MongoClient(uri) as client:
        db = client[db]
        coll = db[colletion]
        coll.ensure_index("id", unique=True)
        df = job_parser(hh = True, superjobs = True, verbose = True, 
                        save = False)
        df['published_at'] = pd.to_datetime(df['published_at'])
        df.reset_index(drop=True, inplace=True)
        records = json.loads(df.T.to_json()).values()
        try:
            coll.insert_many(records, ordered = False)
        
        except BulkWriteError as bwe:
            print("Batch Inserted with some errors. May be some duplicates "
                  "were found and are skipped.")
            print(f"Count is {coll.count()}.")

        except Exception as e:
            print( { 'error': str(e) })