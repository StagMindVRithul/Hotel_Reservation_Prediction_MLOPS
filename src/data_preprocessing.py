import os 
import pandas as pd 
import numpy as np 
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data 
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def preprocess_data(self,df):
        try:
            logger.info("Starting data preprocessing")

            logger.info("Dropping the columns")
            df.drop(columns=['Booking_ID'],axis=1,inplace=True)
            logger.info("Dropping the duplicates")
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Applying Label Encoding")
            mappings = {}
            for col in cat_cols:
                label_encoder = LabelEncoder()
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
            logger.info("Lable Mappings are: ")
            for col, mapping in mappings.items():
                logger.info(f"{col}: {mapping}")
            
            logger.info("Applying Skewness Transformation")
            skewness_threshold = self.config['data_processing']['skewness_threshold']
            for col in num_cols:
                skewness = df[col].skew()
                if abs(skewness) > skewness_threshold:
                    df[col] = np.log1p(df[col])
                    logger.info(f"Applied log transformation on {col} with skewness {skewness}")
                else:
                    logger.info(f"No transformation needed for {col} with skewness {skewness}")
            logger.info("Data Preprocessing completed successfully")
            return df
        except Exception as e:
            logger.error("Error while data preprocessing")
            raise CustomException("Error in data preprocessing", e)   
    
    def handle_imbalance(self, df):
        try:
            logger.info("Handling Imbalance in the data")
            x = df.drop(columns=['booking_status'])
            y = df['booking_status']
            smote = SMOTE(random_state=42)
            x_res, y_res = smote.fit_resample(x,y)
            df_res = pd.DataFrame(x_res, columns=x.columns)
            df_res['booking_status'] = y_res
            logger.info("Imbalance handled successfully")
            return df_res
        except Exception as e:
            logger.error("Error while handling imbalance in the data")
            raise CustomException("Error in handling imbalance", e)

    def feature_selection(self, df):
        try:
            logger.info("Starting feature selection")
            x = df.drop(['booking_status'], axis=1)
            y = df['booking_status']
            model = RandomForestClassifier(random_state=42)
            model.fit(x,y)
            feature_importances = model.feature_importances_
            feature_importances_df = pd.DataFrame({'Feature': x.columns, 'Importance': feature_importances})
            feature_importances_df = feature_importances_df.sort_values(by='Importance', ascending=False)
            num_of_features_select = self.config['data_processing']['no_of_features']
            top_10_features = feature_importances_df.head(num_of_features_select)['Feature'].tolist()
            df = df[top_10_features + ['booking_status']]
            logger.info("Feature selection completed successfully")
            return df 
        except Exception as e:
            logger.error("Error while feature selection")
            raise CustomException("Error in feature selection", e)
    
    def save_process_data(self, df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info("Processed data saved successfully")
        except Exception as e:
            logger.error("Error while saving processed data")
            raise CustomException("Error in saving processed data ", e)
        
    def process(self):
        try:
            logger.info("Loading data from RAW directory")
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.handle_imbalance(train_df)
            test_df = self.handle_imbalance(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_process_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_process_data(test_df, PROCESSED_TEST_DATA_PATH)
            logger.info("All Data processing completed successfully")
        except Exception as e:
            logger.error("Error in data processing pipeline")
            raise CustomException("Error during the data processing ", e)
    
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()

    






