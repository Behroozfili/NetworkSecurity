import os
import sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import read_yaml_file
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
  AdaBoostClassifier,
  GradientBoostingClassifier,
  RandomForestClassifier
  )


from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

class ModelTrainer:
  def __init__(self,model_trainer_config:ModelTrainerConfig,
               data_transformation_artifact:DataTransformationArtifact):
    try:
      self.model_trainer_config = model_trainer_config
      self.data_transformation_artifact=data_transformation_artifact
    except Exception as e :
      NetworkSecurityException(e,sys)
      
      
  def train_model(self,X_train,y_train,X_test,y_test): 
   try:
     hyperparam_file_path = os.path.join(os.getcwd(), "params", "hyperparams.yml")
     model_config =read_yaml_file(hyperparam_file_path)
     params = model_config["model_selection"]["grid_search"]
     models={
       "Random Forest": RandomForestClassifier(verbose=1),
       "Decision Tree": DecisionTreeClassifier(),
       "Gradient Boosting": GradientBoostingClassifier(verbose=1),
       "Logistic Regression": LogisticRegression(verbose=1),
       "AdaBoost":AdaBoostClassifier(),
       
       
     }
     
     model_report,trained_models_dict =evaluate_models(x_train=X_train,
                                       y_train=y_train,
                                       x_test=X_test,
                                       y_test=y_test,
                                       models=models,param=params)  
     # to get best model score from dict
     best_model_score =max(sorted(model_report.values()))
     
     # to get best model name from dict
     best_model_name = list(model_report.keys())[
       list(model_report.values()).index(best_model_score)
     ]
     
     best_model = trained_models_dict[best_model_name]
     
     y_train_pred=best_model.predict(X_train)
     get_classification_score(y_true=y_train,y_pred=y_train_pred)
     classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)
     
     y_test_pred=best_model.predict(X_test)
     get_classification_score(y_true=y_test,y_pred=y_test_pred)
     classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)
     
     preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
     
     model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
     os.makedirs(model_dir_path,exist_ok=True)
     
     Network_Model= NetworkModel(preprocessor=preprocessor,model=best_model)
     
     save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
     
     # Model Trainer Artifact
     model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                         train_metric_artifact=classification_train_metric,
                         test_metric_artifact=classification_test_metric)
     logging.info(f"Model trainer artifact: {model_trainer_artifact}")
     return model_trainer_artifact
     
   except Exception as e:
      raise NetworkSecurityException(e,sys)
    
  def initiate_model_trainer(self) -> ModelTrainerArtifact:
    try:
        train_file_path = self.data_transformation_artifact.transformed_train_file_path
        test_file_path = self.data_transformation_artifact.transformed_test_file_path
        
        
        train_arr = load_numpy_array_data(train_file_path)
        test_arr = load_numpy_array_data(test_file_path)
        
        
        X_train, y_train, X_test, y_test = (
            train_arr[:, :-1],
            train_arr[:, -1],
            test_arr[:, :-1],
            test_arr[:, -1]
        )
        
       
        model_trainer_artifact = self.train_model(X_train, y_train, X_test, y_test)
        return model_trainer_artifact
        
    except Exception as e:
        raise NetworkSecurityException(e, sys) 