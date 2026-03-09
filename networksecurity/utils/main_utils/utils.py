from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import yaml
import os , sys 
import numpy as np
import dill
import pickle
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path:str)->dict:
  try:
    with open(file_path,"r") as yaml_file:
      return yaml.safe_load(yaml_file)
  except Exception as e :
    raise NetworkSecurityException(e,sys)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w") as file:
            yaml.dump(content, file, default_flow_style=False)
            
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path: str, array:np.array):
    """
    Save numpy arry data to file 
    file_path : str location of file to save 
    arry: np.array data to save 
    """
    try:
       dir_path = os.path.dirname(file_path)
       os.makedirs(dir_path,exist_ok= True)
       with open(file_path,"wb") as file_obj:
           np.save(file_obj,array)
    except Exception as e :
        raise NetworkSecurityException(e, sys)
def save_object(file_path: str,obj : object) ->None:
    try:
        logging.info("Entered the save_object method of maiUtils clss")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb")as file_obj:
            pickle.dump(obj,file_obj)
            logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
         raise NetworkSecurityException(e, sys)
     
     
def read_data(file_path)->pd.DataFrame:
    try:
      return pd.read_csv(file_path)
       
    except Exception as e:
      raise  NetworkSecurityException(e,sys)
  
def load_object(file_path):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file : {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load numpy array data from file 
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
            
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
            
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def evaluate_models(x_train, y_train, x_test, y_test, models, param):
    try:
        report = {}
        trained_models = {}

        for model_name, model in models.items():
            para = param.get(model_name, {})

            logging.info(f"Started Grid Search for: {model_name}")
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(x_train, y_train)
            trained_models[model_name] = gs.best_estimator_
            best_model = gs.best_estimator_
            y_test_pred = best_model.predict(x_test)
            test_model_score = r2_score(y_test, y_test_pred)
            report[model_name] = test_model_score
        
            logging.info(f"Finished {model_name}. Best Score: {test_model_score}")

        return report,trained_models

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e