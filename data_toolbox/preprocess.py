import datetime as dt
import os

import pandas as pd

# Set the default variables
file_path = './data/'
area_code = 'nowon' + '_'


# Updating the original .csv file
def preprocess():
    date_obj = dt.datetime.now().strftime('%Y-%m-%d')
    datetime_obj = dt.datetime.strptime(date_obj, '%Y-%m-%d')
    yesterday_obj = datetime_obj - dt.timedelta(days=1)
    yesterday = yesterday_obj.strftime('%Y-%m-%d')

    old_file_nm = file_path + area_code + str(yesterday) + '.csv'
    df = pd.read_csv(old_file_nm, header=None)
    boolean = not df[0].is_unique

    if boolean is True:
        if os.path.isdir(old_file_nm) is True:
            update_df = pd.read_csv(old_file_nm, header=None)
            update_df.drop_duplicates(keep='first', inplace=True)
            update_df.to_csv(old_file_nm, encoding='utf-8-sig', index=False, header=False, mode='w')

        else:
            pass

    else:
        pass


if __name__ == '__main__':
    preprocess()
