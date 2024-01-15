import tkinter as tk
import pandas as pd

class DataContainer():
    def __init__(self):
        
        self.data = pd.DataFrame({
                'Timestamp': pd.Series(dtype='datetime64[ns]'),
                'Score': pd.Series(dtype='int'),
                'Seconds': pd.Series(dtype='int'),
                'Default': pd.Series(dtype='bool')
            })
        
        try:
            self.data: pd.DataFrame = pd.read_csv('data.tsv', sep='\t')
        except pd.errors.EmptyDataError:
            pass
            
    def add_point(self, timestamp, score, seconds, default):
        new_row = {
            'Timestamp': timestamp,
            'Score': score,
            'Seconds': seconds,
            'Default': default
        }
        self.data: pd.DataFrame = self.data.append(new_row, ignore_index=True)
        self.data.to_csv('data.tsv', sep='\t', index=False)
    
    def get_data(self, default_time, default_settings):
        """
        TODO: Add support for other settings
        Returns:
            (pd.Series, pd.Series): (timestamps, scores)
        """
        return self.data['Timestamp'], self.data['Score']