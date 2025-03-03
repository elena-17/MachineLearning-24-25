

######################################## IMPORTS ########################################
import pandas as pd
import configparser
from sklearn.preprocessing import OneHotEncoder

#########################################################################################


################################## Global Configurations ################################
# Load configuration fileconfig["data"]["targets"]
CONFIG_FILE_PATH = "mlflow/test.conf"

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
DATASET_PATH = config["data"]["dataset_path"]
TEST_DATASET_PATH = config["data"]["dataset_test_path"]
print(DATASET_PATH)
DATASET_INDEX_FEATURE = config["data"]["dataset_index"]
DATASET_TARGET_FEATURES = ["h1n1_vaccine", "seasonal_vaccine"]

#########################################################################################
class Dataset:
    '''
    ## Dataset
    
    This class represents a dataset. It handles dataset loading and splitting.
    
    ### Attributes
    
    - test: The test dataset.
    
    '''
    def __init__(self):
        '''
        Constructor for the Dataset class.
        '''
        data = pd.read_csv(DATASET_PATH)
        target = DATASET_TARGET_FEATURES
        data.set_index(DATASET_INDEX_FEATURE, inplace=True)
        self._y = data[target]
        self._X = data.drop(columns=target)
        test_data =  pd.read_csv(TEST_DATASET_PATH)
        test_data.set_index(DATASET_INDEX_FEATURE, inplace=True)
        self.test = test_data
    
    def with_correlation(self):
        '''
        ## with_correlation
        Method that returns a copy of the dataset features and targets.
        
        ### Returns
        (X, y): A tuple containing the dataset features and targets.
        '''
        
        return self._X.copy(), self._y.copy()

    def with_onehot(self):
        '''
        ## with_onehot
        Method that returns a copy of the dataset features and targets with one-hot encoding.

        ### Returns
        (X, y, test): A tuple containing the dataset features, targets and test dataset with one-hot encoding.
        '''
        encoder = OneHotEncoder()
        all_features = pd.concat([self._X, self.test])
        encoder.fit(all_features)
        X = encoder.transform(self._X)
        y = self._y
        test_transformed = encoder.transform(self.test)
        test_df = pd.DataFrame(test_transformed.toarray(), index=self.test.index)
        return X, y, test_df
    
    def with_division(self):
        ''''
        ## with_division
        Method that returns a tuple containing the dataset features and targets divided into two datasets, one for each target.
        
        ### Returns
        ((h1n1, h1n1_y, test_h1n1), (seasonal, seasonal_y, test_seasonal)): A tuple containing two tuples, each containing the dataset features, targets and test dataset for each target.'''
        
        h1_n1 = self._X.copy()
        seasonal = self._X.copy()
        h1_columns = ['doctor_recc_seasonal','opinion_seas_vacc_effective','opinion_seas_risk','opinion_seas_sick_from_vacc']
        seasonal_columns = ['h1n1_concern','h1n1_knowledge','doctor_recc_h1n1','opinion_h1n1_vacc_effective','opinion_h1n1_risk','opinion_h1n1_sick_from_vacc']
        h1_n1.drop(columns=h1_columns, inplace=True)
        seasonal.drop(columns=seasonal_columns, inplace=True)
        h1_n1_y = self._y['h1n1_vaccine']
        seasonal_y = self._y['seasonal_vaccine']
        test_h1_n1 = self.test.copy()
        test_seasonal = self.test.copy()
        test_h1_n1.drop(columns=h1_columns, inplace=True)
        test_seasonal.drop(columns=seasonal_columns, inplace=True)
        return (h1_n1, h1_n1_y, test_h1_n1), (seasonal, seasonal_y, test_seasonal)

    def all_features(self):
        '''
        ## all_features
        Method that returns the dataset encoded with all the features without dropping the ones with random values.

        ### Returns
        X, y, test
        '''
        X = pd.read_csv(config["data"]["dataset_all_path"], index_col="respondent_id")
        target = ["h1n1_vaccine","seasonal_vaccine"]
        y = X[target]
        X = X.drop(columns=target)
        test = pd.read_csv(config["data"]["dataset_test_all_path"], index_col="respondent_id")
        return X, y, test
    
    def no_outliers(self):
        '''
        ## no_outliers
        Method that returns the dataset encoded with all the features removing some outliers.

        ### Returns
        X, y, test
        '''
        X = pd.read_csv(config["data"]["dataset_no_outliers_path"], index_col="respondent_id")
        target = ["h1n1_vaccine","seasonal_vaccine"]
        y = X[target]
        X = X.drop(columns=target)
        return X, y, self.test.copy()

    def no_outliers_onehot(self):
        '''
        ## no_outliers_onehot
        Method that returns the dataset encoded with all the features removing some outliers and one-hot encoding.

        ### Returns
        X, y, test
        '''
        X = pd.read_csv(config["data"]["dataset_no_outliers_path"], index_col="respondent_id")
        target = ["h1n1_vaccine","seasonal_vaccine"]
        y = X[target]
        X = X.drop(columns=target)
        encoder = OneHotEncoder()
        all_features = pd.concat([X, self.test])
        encoder.fit(all_features)
        encoder.fit(X)
        X = encoder.transform(X)
        test_transformed = encoder.transform(self.test)
        test_df = pd.DataFrame(test_transformed.toarray(), index=self.test.index)
        return X, y, test_df
    
    def all_onehot(self):
        X,y,test = self.all_features()
        encoder = OneHotEncoder()
        all_features = pd.concat([X, test])
        encoder.fit(all_features)
        encoder.fit(X)
        X_transformed = encoder.transform(X)
        X_df = pd.DataFrame(X_transformed.toarray(), index=X.index)
        test_transformed = encoder.transform(test)
        test_df = pd.DataFrame(test_transformed.toarray(), index=test.index)
        return X, y, test_df
    
    def original_dataset(self):
        '''
        ## original_dataset
        Method that returns the original dataset without NaN values.

        ### Returns
        X, y, test
        '''
        X = pd.read_csv(config["data"]["dataset_no_nulls_path"], index_col="respondent_id")
        target = ["h1n1_vaccine","seasonal_vaccine"]
        y = X[target]
        X = X.drop(columns=target)
        test = pd.read_csv(config["data"]["dataset_test_no_nulls_path"], index_col="respondent_id")
        return X, y, test
