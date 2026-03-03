import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


from dotenv import load_dotenv
load_dotenv()

MANGO_DB_URL=os.getenv("MANGO_DB_URL")

ca=certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
           
            self.mongo_client = pymongo.MongoClient(MANGO_DB_URL, tlsCAFile=ca)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def cv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            
            records = list(json.loads(data.to_json(orient='records')))
            return records   
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mangodb(self, records, database_name, collection_name):
        try:
           
            db = self.mongo_client[database_name]
            col = db[collection_name]
            
            result = col.insert_many(records)
            return len(result.inserted_ids)
      
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    
if __name__=='__main__':
  FILE_PATH='Network_Data\phisingData.csv'
  DATABASE="BEHROOZ"
  Collection="NetworkData"
  networkobj=NetworkDataExtract()
  records=networkobj.cv_to_json_convertor(file_path=FILE_PATH)
  print(records)
  no_of_records=networkobj.insert_data_mangodb(records,DATABASE,Collection)
  print(no_of_records)