import datetime as dt
import os
import time
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode, quote_plus, unquote
from urllib.request import urlopen

import bs4
import pandas as pd
import schedule

# Defualt variables
url = 'http://apis.data.go.kr/B552584/cleansys/rltmMesureResult'
api_key = unquote('your_api_key')
todayDate = ''
file_path = './data/'
factoryName = ''
measureTime = ''
area_code = 'nowon' + '_'
stackCode = ['1', '2']
str_dt = dt.datetime.now().strftime('%Y-%m-%d')

# Disclaimer: Set the 'dataList' as global variable.
# Can stack the data into dataList (type: List)
# dataList = []


# Feature: Crawling
def crawling():
    global todayDate, factoryName, measureTime
    str_mesure_dt = ''
    executeTime = dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    column_nm = ['mesure_dt', 'area_nm', 'fact_manage_nm', 'stack_code',
                 'nh3_exhst_perm_stdr_value', 'nh3_mesure_value', 'nox_exhst_perm_stdr_value', 'nox_mesure_value',
                 'sox_exhst_perm_stdr_value', 'sox_mesure_value', 'tsp_exhst_perm_stdr_value', 'tsp_mesure_value',
                 'hf_exhst_perm_stdr_value', 'hf_mesure_value', 'hcl_exhst_perm_stdr_value', 'hcl_mesure_value',
                 'co_exhst_perm_stdr_value', 'co_mesure_value']

    # Problem: When DataFrame is saved to .csv file, the next list was appended at previous list. 
    # Then .csv file has the bigger file size.
    # 
    # Workaround: Initialize dataList
    dataList = []

    print('Running time: ', executeTime)
    print('Exhaust connected successfully: ')

    for i in range(len(stackCode)):
        queryParams = '?' + urlencode(
            {
                quote_plus('serviceKey'): api_key,
                quote_plus('areaNm'): '서울특별시',
                quote_plus('factManageNm'): '노원자원회수시설',
                quote_plus('stackCode'): str(stackCode[i]),
                quote_plus('type'): 'xml'
            }
        )

        # Fix the problem that couldn't retry to get data.
        try:
            result = urlopen(url + queryParams)
            # Only for debugging the link log for checking the connections
            # print("Link connected successfully: ", url + queryParams)
            print(str(stackCode[i]), end='_OK ')

            xmlObj = bs4.BeautifulSoup(result, 'lxml-xml')
            data = xmlObj.find_all('item')

            for k in range(len(data)):
                mesure_dt = data[k].mesure_dt.string.strip()
                area_nm = data[k].area_nm.string.strip()
                fact_manage_nm = data[k].fact_manage_nm.string.strip()
                stack_code = data[k].stack_code.string
                nh3_exhst_perm_stdr_value = data[k].nh3_exhst_perm_stdr_value.string
                nh3_mesure_value = data[k].nh3_mesure_value.string
                nox_exhst_perm_stdr_value = data[k].nox_exhst_perm_stdr_value.string
                nox_mesure_value = data[k].nox_mesure_value.string
                sox_exhst_perm_stdr_value = data[k].sox_exhst_perm_stdr_value.string
                sox_mesure_value = data[k].sox_mesure_value.string
                tsp_exhst_perm_stdr_value = data[k].tsp_exhst_perm_stdr_value.string
                tsp_mesure_value = data[k].tsp_mesure_value.string
                hf_exhst_perm_stdr_value = data[k].hf_exhst_perm_stdr_value.string
                hf_mesure_value = data[k].hf_mesure_value.string
                hcl_exhst_perm_stdr_value = data[k].hcl_exhst_perm_stdr_value.string
                hcl_mesure_value = data[k].hcl_mesure_value.string
                co_exhst_perm_stdr_value = data[k].co_exhst_perm_stdr_value.string
                co_mesure_value = data[k].co_mesure_value.string

                data = [mesure_dt, area_nm, fact_manage_nm, stack_code, nh3_exhst_perm_stdr_value, nh3_mesure_value,
                        nox_exhst_perm_stdr_value, nox_mesure_value, sox_exhst_perm_stdr_value, sox_mesure_value,
                        tsp_exhst_perm_stdr_value, tsp_mesure_value, hf_exhst_perm_stdr_value, hf_mesure_value,
                        hcl_exhst_perm_stdr_value, hcl_mesure_value, co_exhst_perm_stdr_value, co_mesure_value]
                measureTime = mesure_dt.replace(":", "-")
                str_mesure_dt = str(mesure_dt)
                factoryName = fact_manage_nm
                dataList.append(data)

        # HTTPError should be declared at first.
        except HTTPError as e:
            print('error code: ', e.code)
            print(e, '\nHTTPError is occurred. It will be restarted soon.')
            time.sleep(15)
            crawling()
            return

        except ConnectionError as e:
            print(e, '\nConnectionError is occurred. It will be restarted soon.')
            print('Reason: ', e)
            time.sleep(15)
            crawling()
            return

        except TimeoutError as e:
            print('\nTimeoutError is occurred. Failed to get the request.')
            print('Reason: ', e)
            time.sleep(15)
            crawling()
            return

        except URLError as e:
            print('\nURLError is occurred. Failed to connect a server.')
            print('Reason: ', e.reason)
            time.sleep(15)
            crawling()
            return

    # Debug: Check the measure time and generate the pandas.DataFrame
    print('mesure_dt: ', measureTime)

    # Set the file_name
    nm_Struct = area_code + str_mesure_dt[0:10]
    file_nm = file_path + nm_Struct

    print('The data is saving now.')

    # Save the data (changed daily)
    if str(dataList[0][0][11:16]) == '0:00':

        # Create the new .csv file
        new_df = pd.DataFrame(dataList, columns=column_nm)
        new_df.to_csv(file_nm + '.csv', sep=',', na_rep='NaN', float_format='%.2f',
                      index=False, header=True, lineterminator='\n', encoding='utf-8-sig', mode='w')

    else:
        update_df = pd.DataFrame(dataList, columns=column_nm)
        update_df.to_csv(file_nm + '.csv', sep=',', na_rep='NaN', float_format='%.2f',
                         index=False, header=True, lineterminator='\n', encoding='utf-8-sig', mode='a')

    print('Done (' + str(dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + ')')
    dataList.clear()


# This function is just for debugging process
def show_rerunning_time():
    rerunningTime = dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print("Re-running time: " + rerunningTime)


def updating():
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


# To run this code as a process on Windows/Linux, you need to configure this syntax as below.
if __name__ == '__main__':

    # First running
    print('AutoCrawler is starting...')
    crawling()

    # Automation - to set time to re-run this script.
    # You can change the time you want.
    # 15 minutes every hour
    # schedule.every().hour.at(":15").do(show_rerunning_time)
    schedule.every().hour.at(":15").do(crawling)

    # 45 minutes every hour
    # schedule.every().hour.at(":45").do(show_rerunning_time)
    schedule.every().hour.at(":45").do(crawling)

    while True:
        schedule.run_pending()
        time.sleep(1)
