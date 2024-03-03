import pandas as pd
import datetime
from typing import Optional
import os

datatypes = {
                'Timestamp': pd.Series(dtype='datetime64[ns]'),
                'Score': pd.Series(dtype='int'),
                'Seconds': pd.Series(dtype='int'),
                'Ratio': pd.Series(dtype='float'),
                'Default': pd.Series(dtype='bool')
            }

class DataContainer():
    """Wrapper for pandas dataframe involving the data"""
    
    def __init__(self, data_file: str = 'data.tsv'):
        """Reads data from storage file and loads it into a dataframe variable"""
        
        self.data_file = data_file
        
        self.data = pd.DataFrame(datatypes)
        
        standard_columns = datatypes.keys()
        if not os.path.exists('data.tsv'):
            return
        try:
            data = pd.read_csv(self.data_file, sep='\t')
            
            #check correct columns
            if len(set(data.columns.values).union(standard_columns)) == 5:
                data['Timestamp'] = data['Timestamp'].astype('datetime64[ns]')
                self.data = data
        except pd.errors.EmptyDataError:
            print("No historical data")
        except pd.errors.ParserError:
            print("Error parsing data; please check validity of file")
            
    def add_point(self, timestamp: datetime.datetime, score: int, seconds: int, default: bool):
        """Adds a datapoint to the dataframe representing a test result

        Args:
            timestamp (datetime.datetime): Time of result
            score (int): Score achieved
            seconds (int): Number of seconds in time limit
            default (bool): True if default settings, False otherwise
        """
        
        new_row = pd.DataFrame([[timestamp, score, seconds, score/seconds, default]], 
                                columns = self.data.columns)
        for column, example in datatypes.items():
            new_row[column] = new_row[column].astype(example.dtype)
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.data.to_csv(self.data_file, sep='\t', index=False)
        
    def has_last(self) -> bool:
        """Checks if data container is empty

        Returns:
            bool: True if there are more elements, False otherwise
        """
        return len(self.data) != 0
                
    def remove_last(self) -> Optional[pd.DataFrame]:
        """Removes last row from dataframe

        Returns:
            pd.DataFrame, None: last row from dataframe, none if original is empty
            
        Raises:
            ValueError: if no elements are remaining
        """
        
        if not self.has_last():
            raise ValueError('No more elements in dataframe')
        last_row = self.data.iloc[:-1]
        self.data: pd.DataFrame = self.data.iloc[:-1]
        self.data.to_csv(self.data_file, sep='\t', index=False)
        return last_row
    
    #TODO: remove default values
    def get_data(self, default_time: Optional[bool], default_settings: Optional[bool], 
                 ratio: bool) -> tuple[Optional[pd.Series], 
                                         Optional[pd.Series], 
                                         Optional[tuple[datetime.datetime, 
                                                        datetime.datetime]]]:
        """Get data for display on chart widget based on query
        
        Args:
            default_time (Optional[bool], optional): If time is standard 120 seconds, None if no restrictions. Defaults to True.
            default_settings (Optional[bool], optional): If problem settings are standard, None if no restrictions. Defaults to True.
            ratio (bool, optional): If data is returned as ratio. Defaults to False.

        Returns:
            tuple[pd.Series, pd.Series, list[datetime.datetime, datetime.datetime]]:
                x series, y series, time range
        """
        selected_data: pd.DataFrame = None
        match (default_settings, default_time): # definitely smells
            case (True, True):
                selected_data = self.data[(self.data['Default'] == True) & 
                                      (self.data['Seconds'] == 120)]
            case (True, False):
                selected_data = self.data[(self.data['Default'] == True) & 
                                      (self.data['Seconds'] != 120)]
            case (True, None):
                selected_data = self.data[(self.data['Default'] == True)]
            case (False, True):
                selected_data = self.data[(self.data['Default'] != True) & 
                                      (self.data['Seconds'] == 120)]
            case (False, False):
                selected_data = self.data[(self.data['Default'] != True) & 
                                      (self.data['Seconds'] != 120)]
            case (False, None):
                selected_data = self.data[(self.data['Default'] != True)]
            case (None, True):
                selected_data = self.data[(self.data['Seconds'] == 120)]
            case (None, False):
                selected_data = self.data[(self.data['Seconds'] != 120)]
            case (None, None):
                selected_data = self.data
            case _:
                raise ValueError
        return self.format_output(selected_data, ratio)
    
    @staticmethod
    def format_output(df: pd.DataFrame, ratio):
        """Formats output of dataframe

        Args:
            df (pd.DataFrame): Dataframe to extract series from

        Returns:
            tuple[pd.Series, pd.Series, list[datetime.datetime, datetime.datetime]]:
                x series, y series, time range
        """
        if len(df) == 0:
            return [], [], [datetime.date(2007, 12, 5), datetime.date(2007, 12, 7)]
        x = pd.to_datetime(df['Timestamp'])
        y = df['Score'] if not ratio else df['Ratio']
        timeframe = df.iloc[-1]['Timestamp'] - df.iloc[0]['Timestamp']
        if len(df) == 1:
            timeframe = datetime.timedelta(seconds=1)
        limits = (df.iloc[0]['Timestamp'] - timeframe / 4, 
                  df.iloc[-1]['Timestamp'] + timeframe / 4)
        return x, y, limits