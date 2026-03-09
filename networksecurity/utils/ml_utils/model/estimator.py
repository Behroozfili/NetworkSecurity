from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os 
import sys
from networksecurity.constant.training_pipeline import SAVE_MODEL_DIR , MODEL_FILE_NAME 

class NetworkModel:
  def __init__(self,preprocessor,model):
    try:
      self.preprocessor = preprocessor
      self.model = model
    except Exception as e:
      raise NetworkSecurityException(e,sys)
  def prediction(self,x):
    try:
      x_transform = self.preprocessor.transform(x)
      y_hat = self.model.predict(x_transform)
      return y_hat
    except Exception as e:
        raise NetworkSecurityException(e,sys)
      
      