import os 
import pandas as pd 
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger 
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml
from google.oauth2 import service_account

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config['train_ratio']

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info(f'Data Ingestion started with {self.bucket_name} and {self.file_name}')
    
    def download_csv_from_gcp(self):
        try:
            credentials = service_account.Credentials.from_service_account_file('/app/sa-key.json')
            client = storage.Client(credentials=credentials, project=credentials.project_id)
            bucket = client.get_bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)
            logger.info(f'CSV file is successfully downloaded to {RAW_FILE_PATH}')
        except Exception as e:
            logger.error(f'Error while downloading the csv file')
            raise CustomException("Failed to download file from GCP ", e)
        
    def split_data(self):
        try:
            df = pd.read_csv(RAW_FILE_PATH)
            logger.info(f'Starting the splitting process')
            train_data, test_data = train_test_split(df, test_size=1-self.train_test_ratio, random_state=42)
            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)
            logger.info(f'Data is successfully split into train and test')
        except Exception as e:
            logger.error(f'Error while splitting the data')
            raise CustomException('Failed to split the data ', e )
        
    def run(self):
        try:
            logger.info(f'Data Ingestion process started')
            self.download_csv_from_gcp()
            self.split_data()
            logger.info(f'Data Ingestion completed successfully')
        except Exception as e:
            logger.error(f'Error in Data Ingestion')
            raise CustomException('Failed data ingestion ', e)
        finally:
            logger.info(f'Data Ingestion completed')

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()