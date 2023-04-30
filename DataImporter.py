import pandas as pd
import requests

class DataImporter:

    @staticmethod
    def read_csv(file_path):
        return pd.read_csv(file_path)

    @staticmethod
    def read_excel(file_path):
        return pd.read_excel(file_path)

    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as f:
            json_data = f.read()
        return pd.read_json(json_data)

    @staticmethod
    def read_html(file_path):
        return pd.read_html(file_path)[0]

    @staticmethod
    def fetch_data(url):
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data)