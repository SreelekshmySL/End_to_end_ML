import sys
from dataclasses import dataclass
import os
from src.utils import save_object

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_tranformer_object(self):
        try:
            num_columns = ['reading_score','writing_score']
            cat_columns = ['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']

            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('encoder',OneHotEncoder()),
                    ('scaler',StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Categorical columns: {cat_columns}")
            logging.info(f"Numerical columns: {num_columns}")
            

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_columns),
                    ("cat_pipeline",cat_pipeline,cat_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read the train and test data')
            logging.info('Obtaining preprocessing objects')

            preprocessing_obj = self.get_data_tranformer_object()

            target_col = 'math_score'

            input_feature_train_df=train_df.drop(columns=[target_col],axis=1)
            target_feature_train_df = train_df[target_col]

            input_feature_test_df=test_df.drop(columns=[target_col],axis=1)
            target_feature_test_df = test_df[target_col]

            logging.info('Applying preprocessing steps on train df and test df')

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)  #fit transform the train data
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)  # the fitting from train data is used to trandform the test data 

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]
            
            logging.info('Saved preprocessing object.')

            save_object(
                file_path = self.data_transformation_config.preprocessor_ob_file_path,
                obj=preprocessing_obj
            )


            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_ob_file_path
                )


        except Exception as e:
            raise CustomException(e,sys)
