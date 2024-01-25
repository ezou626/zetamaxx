from containers import DataContainer
import datetime
import pandas as pd
from pandas.testing import assert_frame_equal

datetime_list = [datetime.datetime(2023, 1, i) for i in range(1, 31)]
score_list = [i for i in range(30)]
seconds_list = [120 for _ in range(30)]
ratios_list = [score_list[i]/seconds_list[i] for i in range(30)]
default_list = [i % 2 == 0 for i in range(30)]

def test_constructor_data():
    initial_df = pd.DataFrame({
                'Timestamp': datetime_list,
                'Score': score_list,
                'Seconds': seconds_list,
                'Ratio': ratios_list,
                'Default': default_list
            })
    initial_df.to_csv('test.tsv', sep='\t', index=False)
    
    data_container = DataContainer('test.tsv')
    
    assert_frame_equal(data_container.data, initial_df)
    
#test constructor valid data
def test_constructor_empty():
    with open('test.tsv', 'w') as f: #clear test file
        pass
    data_container = DataContainer('test.tsv')
    initial_df = pd.DataFrame({
                'Timestamp': pd.Series(dtype='datetime64[ns]'),
                'Score': pd.Series(dtype='int'),
                'Seconds': pd.Series(dtype='int'),
                'Ratio': pd.Series(dtype='float'),
                'Default': pd.Series(dtype='bool')
            })
    assert initial_df.equals(data_container.data)