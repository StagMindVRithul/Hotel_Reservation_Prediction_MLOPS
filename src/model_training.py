import os 
import pandas as pd 
import joblib 
from sklearn.model_selection import RandomizedSearchCV
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import logging 
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import * 
from utils.common_functions import read_yaml, load_data 
from scipy.stats import randint 
import mlflow
import mlflow.sklearn

logger = logging.getLogger(__name__)


class ModelTraining:
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        try:
            logger.info("Loading and splitting data...")
            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)

            x_train = train_data.drop(columns=['booking_status'])
            y_train = train_data['booking_status']

            x_test = test_data.drop(columns=['booking_status'])
            y_test = test_data['booking_status']

            logger.info("Data loaded and split successfully.")
            return x_train, y_train, x_test, y_test
        except Exception as e:
            logger.error(f"Error while loading and splitting data")
            raise CustomException("Failed to load and split data ",e) 
    
    def train_model(self, x_train, y_train):
        try:
            logger.info("Training the model...")
            model = LGBMClassifier(random_state=self.random_search_params['random_state'])
            logger.info("Starting the Hyperparameter tuning...")
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.params_dist,
                **self.random_search_params
            )
            random_search.fit(x_train, y_train)
            logger.info("Hyperparameter tuning completed.")
            best_model = random_search.best_estimator_
            logger.info(f"Best parameters found: {random_search.best_params_}")
            logger.info("Model trained successfully.")
            return best_model
        except Exception as e:
            logger.error(f"Error while training the model")
            raise CustomException("Failed to train the model ",e)
    
    def evaluate_model(self, model, x_test, y_test):
        try:
            logger.info("Evaluating the model...")
            y_pred = model.predict(x_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Model evaluation metrics: Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")
            return {
                'Accuracy' : accuracy, 
                'Precision' : precision, 
                'Recall' : recall,
                'F1 Score' : f1
            }
        except Exception as e:
            logger.error(f"Error while evaluating the model")
            raise CustomException("Failed to evaluate the model ",e)
    
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info("Saving the model...")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved at {self.model_output_path}")
        except Exception as e:
            logger.error(f"Error while saving the model")
            raise CustomException("Failed to save the model ",e)
    
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting the model training process...")

                logger.info("Starting the MLflow run...")

                logger.info("Logging the training and testing dataset to MLFLOW")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                x_train, y_train, x_test, y_test = self.load_and_split_data()
                model = self.train_model(x_train, y_train)
                evaluation_metrics  = self.evaluate_model(model, x_test, y_test)
                self.save_model(model)

                logger.info("Logging the model to MLFLOW")
                mlflow.log_artifact(self.model_output_path, artifact_path="models")
                
                logger.info("Logging the model parameters to MLFLOW")
                mlflow.log_params(model.get_params())

                logger.info("Logging the evaluation metrics to MLFLOW")
                mlflow.log_metrics(evaluation_metrics)
                logger.info("Model training process completed successfully.")
        except Exception as e:
            logger.error(f"Error in the model training process")
            raise CustomException("Failed to run the model training process ",e)

if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()
