import datetime as dt

import pandas as pd

file_path = './data/'
area_code = 'nowon' + '_'
str_dt = dt.datetime.now().strftime('%Y-%m-%d')


# Updating the original .csv file
def preprocess():
    date_obj = str_dt
    datetime_obj = dt.datetime.strptime(date_obj, '%Y-%m-%d')
    yesterday_obj = datetime_obj - dt.timedelta(days=1)
    yesterday = yesterday_obj.strftime('%Y-%m-%d')

    old_file_nm = file_path + area_code + str(yesterday) + '.csv'
    df = pd.read_csv(old_file_nm, header=None)
    boolean = not df[0].is_unique

    if boolean is True:
        update_df = pd.read_csv(old_file_nm, header=None)
        update_df.drop_duplicates(keep='first', inplace=True)
        update_df.to_csv(old_file_nm, encoding='utf-8-sig', index=False, header=False, mode='w')

    else:
        pass
