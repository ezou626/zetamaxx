from datacontainer import DataContainer
import datetime
import pandas as pd

datetime_list = [datetime.datetime(2023, 1, i) for i in range(30)]
score_list = [i for i in range(30)]
seconds_list = [120 for _ in range(30)]
ratios_list = [score_list[i]/seconds_list[i] for i in range(30)]
default_list = [i % 2 == 0 for i in range(30)]

#test the constructor
def test_constructor_empty():
    with open('test.tsv', 'w'): #clear test file
        pass
    data_container = DataContainer('test.tsv')
    initial_df = pd.DataFrame({
                'Timestamp': pd.Series(dtype='datetime64[ns]'),
                'Score': pd.Series(dtype='int'),
                'Seconds': pd.Series(dtype='int'),
                'Ratio': pd.Series(dtype='float'),
                'Default': pd.Series(dtype='bool')
            })
    assert initial_df == data_container.data