import requests, bs4
import pandas as pd
from pandas import DataFrame
from lxml import html
import numpy as np
import datetime as dt
import time
import schedule
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote


# Defualt variables
url = "http://apis.data.go.kr/B552584/cleansys/rltmMesureResult"
api_key = unquote('')
todayDate = ""
filePath = "./TMS데이터"
ft_name = ""
stackCode = ['1', '123', '132', '15', '153', '154', '155', '156', '16', '17', '18', '2', '20', '24', '25',
             '26', '27', '28', '29', '3', '30', '31', '32', '45', '47', '49', '51', '52', '53', '54', '92', '93']
dataList = []
mergedList = []


# Feature: Crawling
def crawling():
    global todayDate, ft_name
    for i in range(len(stackCode)):
        queryParams = '?' + urlencode(
            {
                quote_plus('ServiceKey'): api_key,
                quote_plus('areaNm'): '전라남도',
                quote_plus('factManageNm'): '㈜포스코%20광양제철소',
                quote_plus('stackCode'): str(stackCode[i]),
                quote_plus('type'): 'xml'
            }
        )

        result = urlopen(url + queryParams)
        
        # This code is for debugging
        # print("디버깅 URL 출력\n", url + queryParams)
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
            todayDate = mesure_dt.replace(":", "-")
            ft_name = fact_manage_nm
            dataList.append(data)
        
        # This code is for debugging
        print(todayDate)

    df = pd.DataFrame(dataList, columns=['측정시간', '지역명', '사업장명', '배출구', '암모니아_허용기준', '암모니아_측정값',
                                         '질소산화물_허용기준', '질소산화물_측정값', '황산화물_허용기준', '황산화물_측정값',
                                         '먼지_허용기준', '먼지_측정값', '불화수소_허용기준', '불화수소_측정값', '염화수소_허용기준',
                                         '염화수소_측정값', '일산화탄소_허용기준', '일산화탄소_측정값'])
    
    # This code is for debugging
    print(df)
    
    
    # Added crawling time to distinguish whether crawled data is the same data according to server status
    thisDate = dt.datetime.now().strftime('%H-%M-%S')
    filename = str(ft_name) + " " + str(todayDate) + " " + thisDate
    df.to_csv(filename + ".csv",
              sep=',',
              na_rep='NaN',
              float_format='%.2f',
              index=False,
              header=True,
              line_terminator="\n",
              encoding='utf-8-sig')


# Crawled every 25 minutes
schedule.every(25).minutes.do(crawling)

while True:
    schedule.run_pending()
    time.sleep(1)
