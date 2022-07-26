import datetime as dt
import time
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode, quote_plus, unquote
from urllib.request import urlopen

import bs4
import pandas as pd
import schedule

# Defualt variables
url = "http://apis.data.go.kr/B552584/cleansys/rltmMesureResult"
api_key = unquote('')
todayDate = ""
filePath = "./TMS_data"
factoryName = ""
measureTime = ""
stackCode = ['1']


# Feature: Crawling
def crawling():
    global todayDate, factoryName, measureTime
    executeTime = dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    saveTime = dt.datetime.now().strftime('%H-%M-%S')
    
    # Problem: When DataFrame is saved to .csv file, the next list was appended at previous list. 
    # Then .csv file has the bigger file size.
    # 
    # Workaround: Initialize dataList
    dataList = []
    
    print('----------------------------------------------------')
    print('Running time: ', executeTime)
    print('----------------------------------------------------')
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
  
    print('\n----------------------------------------------------')
    print('Checking the measure time: ', measureTime)
    print('----------------------------------------------------')
    print('Executed: data -> df(DataFrame)')

    df = pd.DataFrame(dataList, columns=['측정시간', '지역명', '사업장명', '배출구', '암모니아_허용기준', '암모니아_측정값',
                                         '질소산화물_허용기준', '질소산화물_측정값', '황산화물_허용기준', '황산화물_측정값',
                                         '먼지_허용기준', '먼지_측정값', '불화수소_허용기준', '불화수소_측정값', '염화수소_허용기준',
                                         '염화수소_측정값', '일산화탄소_허용기준', '일산화탄소_측정값'])

    print('Completed: data -> df(DataFrame)')
    print('----------------------------------------------------')
    print('Checking: The length of df row/col: ' + str(df.shape[0]) + ' rows/' + str(df.shape[1]) + ' cols')
    print('Checking: The contents of df.head(5): \n\n', df.head(5))

    nameStructure = str(factoryName) + " " + str(measureTime) + " " + saveTime
    fileName = filePath + nameStructure

    print('----------------------------------------------------')
    print('Executed: df(DataFrame) -> ' + fileName + '.csv is saving')
    df.to_csv(fileName + '.csv',
              sep=',',
              na_rep='NaN',
              float_format='%.2f',
              index=False,
              header=True,
              line_terminator="\n",
              encoding='utf-8-sig',
              mode='w')
    
    print('Completed: Done (time: ' + str(dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + ')')


def show_rerunning_time():
    rerunningTime = dt.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print('****************************************************')
    print("Re-running time: " + rerunningTime)


# First running
print('AutoCrawler is starting...')
crawling()

# Automation - to set time to re-run
# 15 minutes every hour
schedule.every().hour.at(":15").do(show_rerunning_time)
schedule.every().hour.at(":15").do(crawling)

# 45 minutes every hour
schedule.every().hour.at(":45").do(show_rerunning_time)
schedule.every().hour.at(":45").do(crawling)

while True:
    schedule.run_pending()
    time.sleep(1)
