import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

class DataIngestionConfig:
    # specifying paths for train,test outputs from this file as well as for raw data
    # artifacts is the folder to be created
    train_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')
    raw_data_path = os.path.join('artifacts','data.csv')

class DataIngestion:

    # initialize all the paths mentioned above into a single variable
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    # reading the dataset (try except method)
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")

        try:
            df = pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            #making the folder artifacts in above class for train,test and raw data
            #os.path.dirname --> for combining directory path name
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)   #exist_ok - so that if it exist then don't create it again

            # send the df to raw_data_path as csv
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info('Train test split initiated.')
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of data completed.")

            # returning elements for next step: transformation

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )



        except Exception as e:
            raise CustomException(e,sys)
        
# testing this file
if __name__=="__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()

