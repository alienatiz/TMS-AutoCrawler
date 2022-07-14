import datetime as dt
import time
from urllib.parse import urlencode, quote_plus, unquote
from urllib.request import urlopen

import bs4
import pandas as pd
import schedule

# Defualt variables
url = "http://apis.data.go.kr/B552584/cleansys/rltmMesureResult"
api_key = unquote('')
todayDate = ""
filePath = "./TMS데이터"
factoryName = ""
measureDate = ""
stackCode = ['1', '123', '132', '15', '153', '154', '155', '156', '16', '17', '18', '2', '20', '24', '25',
             '26', '27', '28', '29', '3', '30', '31', '32', '45', '47', '49', '51', '52', '53', '54', '92', '93']


# Feature: Crawling
def crawling():
    global todayDate, factoryName, measureDate
    saveDate = dt.datetime.now().strftime('%H-%M-%S')
    executeDate = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Problem: When DataFrame is saved to .csv file, the next list was appended at previous list. 
    # Then .csv file has the bigger file size.
    # 
    # Workaround: Initialize dataList
    dataList = []
    
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
        print("Exhaust connected successfully: #" + str(stackCode[i]))
        xmlObj = bs4.BeautifulSoup(result, 'lxml-xml')
        data = xmlObj.find_all('item')
        
        # Added exception handling when an ConnectionError is occurred
        try:
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
                measureDate = mesure_dt.replace(":", "-")
                factoryName = fact_manage_nm
                dataList.append(data)

        except ConnectionError as e:
            print(e, "\nConnectionError is occurred. It will be restarted soon.")
            time.sleep(10)
            crawling()
            return
  
    print("\nChecking the measure date: ", measureDate)
    print("\nExecuted: data -> df(DataFrame)")

    df = pd.DataFrame(dataList, columns=['측정시간', '지역명', '사업장명', '배출구', '암모니아_허용기준', '암모니아_측정값',
                                         '질소산화물_허용기준', '질소산화물_측정값', '황산화물_허용기준', '황산화물_측정값',
                                         '먼지_허용기준', '먼지_측정값', '불화수소_허용기준', '불화수소_측정값', '염화수소_허용기준',
                                         '염화수소_측정값', '일산화탄소_허용기준', '일산화탄소_측정값'])

    print("Completed: data -> df(DataFrame)")
    print("\nChecking: The length of df row/col: " + str(df.shape[0]) + " rows/" + str(df.shape[1]) + " cols")
    print("Checking: The contents of df: \n", df)

    fileName = str(factoryName) + " " + str(measureDate) + " " + saveDate

    print("\nExecuted: df(DataFrame) -> .csv")
    df.to_csv(fileName + ".csv",
              sep=',',
              na_rep='NaN',
              float_format='%.2f',
              index=False,
              header=True,
              line_terminator="\n",
              encoding='utf-8-sig',
              mode='w')
    
    print("Completed: df(DataFrame) -> " + fileName + ".csv")
    print("Completed: Saved successfully", str(saveDate.replace("-", ":")))


def show_rerunning_time():
    rerunningTime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\nRe-Running time: " + rerunningTime)


# First running
print("------------------------------")
print("# AutoCrawler is starting... #")
print("------------------------------")
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
