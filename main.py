from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig





if __name__=='__main__':
  try:
    trainingpiplineconfig=TrainingPipelineConfig()
    dataingestionconfig=DataIngestionConfig(trainingpiplineconfig)
    data_ingestion=DataIngestion(dataingestionconfig)
    dataingestionartifact=data_ingestion.initiate_data_ingestion()
    
    logging.info("initiate the data ingestion")
  except Exception as e:
    raise NetworkSecurityException(e,sys)
  