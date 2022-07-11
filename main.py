import requests, bs4
import pandas as pd
from pandas import DataFrame
from lxml import html
import numpy as np
import datetime
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote


url = "http://apis.data.go.kr/B552584/cleansys/rltmMesureResult"
api_key = unquote('')

filePath = "./TMS데이터"
todayDate = ""
ft_name = ""

queryParams = '?' + urlencode(
    {
        quote_plus('ServiceKey'): api_key,
        quote_plus('areaNm'): '전라남도',
        quote_plus('factManageNm'): '㈜포스코%20광양제철소',
        quote_plus('stackCode'): '1',
        quote_plus('type'): 'xml'
    }
)

result = urlopen(url + queryParams)
print("디버깅 URL 출력\n", url + queryParams)
xmlObj = bs4.BeautifulSoup(result, 'lxml-xml')

print("\n데이터 출력")
data = xmlObj.find_all('item')
print(data)

dataList = []

for i in range(len(data)):

    mesure_dt = data[i].mesure_dt.string.strip()
    area_nm = data[i].area_nm.string.strip()
    fact_manage_nm = data[i].fact_manage_nm.string.strip()
    stack_code = data[i].stack_code.string
    nh3_exhst_perm_stdr_value = data[i].nh3_exhst_perm_stdr_value.string
    nh3_mesure_value = data[i].nh3_mesure_value.string
    nox_exhst_perm_stdr_value = data[i].nox_exhst_perm_stdr_value.string
    nox_mesure_value = data[i].nox_mesure_value.string
    sox_exhst_perm_stdr_value = data[i].sox_exhst_perm_stdr_value.string
    sox_mesure_value = data[i].sox_mesure_value.string
    tsp_exhst_perm_stdr_value = data[i].tsp_exhst_perm_stdr_value.string
    tsp_mesure_value = data[i].tsp_mesure_value.string
    hf_exhst_perm_stdr_value = data[i].hf_exhst_perm_stdr_value.string
    hf_mesure_value = data[i].hf_mesure_value.string
    hcl_exhst_perm_stdr_value = data[i].hcl_exhst_perm_stdr_value.string
    hcl_mesure_value = data[i].hcl_mesure_value.string
    co_exhst_perm_stdr_value = data[i].co_exhst_perm_stdr_value.string
    co_mesure_value = data[i].co_mesure_value.string

    data = [mesure_dt, area_nm, fact_manage_nm, stack_code, nh3_exhst_perm_stdr_value, nh3_mesure_value,
            nox_exhst_perm_stdr_value, nox_mesure_value, sox_exhst_perm_stdr_value, sox_mesure_value,
            tsp_exhst_perm_stdr_value, tsp_mesure_value, hf_exhst_perm_stdr_value, hf_mesure_value,
            hcl_exhst_perm_stdr_value, hcl_mesure_value, co_exhst_perm_stdr_value, co_mesure_value]
    todayDate = mesure_dt
    ft_name = fact_manage_nm
print(data)
dataList.append(data)


print(dataList)

df = pd.DataFrame(dataList, columns=['측정시간', '지역명', '사업장명', '배출구', '암모니아 허용기준', '암모니아 측정값',
                                     '질소산화물 허용기준', '질소산화물 측정값', '황산화물_허용기준', '황산화물_측정값',
                                     '먼지_허용기준', '먼지_측정값', '불화수소 허용기준', '불화수소 측정값', '염화수소 허용기준',
                                     '염화수소 측정값', '일산화탄소 허용기준', '일산화탄소 측정값'])

print(df)

filename = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
df.to_csv("./㈜포스코 광양제철소/" + filename + ".csv",
          sep=',',
          na_rep='NaN',
          float_format='%.2f',
          index=False,
          header=True,
          line_terminator="\n",
          encoding='utf-8-sig')
