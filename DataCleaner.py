import pandas as pd
import numpy as np

class DataCleaner:

    def __init__(self, df):
        self.df = df

    def replace_null(self, column):
        self.df[column].fillna((self.df[column].shift() + self.df[column].shift(-1)) / 2, inplace = True)

    def convert_to_int(self, column):
        self.df[column] = self.df[column].astype(int)

    def drop_columns(self, *columns):
        self.df.drop(list(columns), axis = 1, inplace = True)
        return self.df

    def check_outliers(self, column):
        q1, q3 = np.percentile(self.df[column], [25,75])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        return outliers

    def deal_outliers(self, column):
        q1, q3 = np.percentile(self.df[column], [25,75])
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        self.df[column] = np.where(self.df[column] < lower_bound, lower_bound, self.df[column])
        self.df[column] = np.where(self.df[column] > upper_bound, upper_bound, self.df[column])

    def save_cleaned_data(self, file_name):
        self.data.to_csv(file_name, index = False)