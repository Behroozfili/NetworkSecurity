from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig





if __name__=='__main__':
  try:
    trainingpiplineconfig=TrainingPipelineConfig()
    dataingestionconfig=DataIngestionConfig(trainingpiplineconfig)
    data_ingestion=DataIngestion(dataingestionconfig)
    logging.info("initiate the data ingestion")
    dataingestionartifact=data_ingestion.initiate_data_ingestion()
    print(dataingestionartifact)
    logging.info("data ingestion completed")
    datavalidationconfig=DataValidationConfig(trainingpiplineconfig)
    data_validation=DataValidation(dataingestionconfig,datavalidationconfig)
    logging.info("initiate the data validation")
    datavalidationartifact=data_validation.initiate_data_validation()
    print(datavalidationartifact)
    logging.info("data validation completed")
    datatransformationconfig=DataTransformationConfig(trainingpiplineconfig)
    logging.info("data transformation started")
    data_transformation=DataTransformation(datavalidationartifact,datatransformationconfig)
    data_transformation_artifact=data_transformation.initiate_data_transformation()
    print( data_transformation_artifact)
    logging.info("data transformation completed")
    
    
  except Exception as e:
    raise NetworkSecurityException(e,sys)
  