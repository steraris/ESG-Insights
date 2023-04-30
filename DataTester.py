import pandas as pd
import numpy as np
from scipy.stats import shapiro
from scipy.stats import pearsonr


class DataTester:

    def __init__(self, data):
        self.data = data

    def test_null(self):
        null_counts = {}
        for col in self.data.columns:
            null_count = self.data[col].isnull().sum()
            null_counts[col] = null_count
        return null_counts

    def test_data_type(self, col_dtype_dict):
        for col, dtype in col_dtype_dict.items():
            if self.data[col].dtype != dtype:
                print(f"{col} column has incorrect data type: expected {dtype}, got {self.data[col].dtype}")
                return True
        print("All columns have correct data type.")
        return False

    def test_outliers(self, col_list):
        for col in col_list:
            q1, q3 = np.percentile(self.data[col], [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            outliers = self.data[(self.data[col] < lower_bound) | (self.data[col] > upper_bound)]
            if not outliers.empty:
                print(f"{col} column has {len(outliers)} outliers.")
                return True
        print("No outliers found in the data.")
        return False

    def test_data_range(self, col_range_dict):
        for col, (min_val, max_val) in col_range_dict.items():
            if (self.data[col] < min_val).any() or (self.data[col] > max_val).any():
                print(f"{col} column has values outside of the range: [{min_val}, {max_val}].")
                return True
        print("All columns fall within the specified range.")
        return False

    def test_data_distribution(self, alpha=0.05):
        for col in self.data.columns:
            _, p_value = shapiro(self.data[col])
            if p_value < alpha:
                print(f"{col} column does not have a normal distribution.")
                return True
        print("All columns have a normal distribution.")
        return False

    def test_data_correlation(self, col_corr_dict, alpha=0.05):
        for col1, col2 in col_corr_dict.items():
            corr, p_value = pearsonr(self.data[col1], self.data[col2])
            if p_value < alpha:
                print(f"{col1} column has a correlation with {col2} column.")
                return True
        print("No significant correlations found between columns.")
        return False