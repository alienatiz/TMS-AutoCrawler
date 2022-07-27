# TMS_AutoCrawler
Python bot for crawling data from TMS OpenAPI of Cleansys automatically. You can set the scheduled time the bot will be started and, also change the time scheduled for bot.

## Data crawled
[![Cleansys](https://cleansys.or.kr/images/common/logo.png)](https://cleansys.or.kr/)   
Also you can check example data here, [Example data](https://github.com/alienatiz/TMS_AutoCrawler/tree/main/data)

## Libraries MUST needed for crawling data by OpenAPI are below
* urllib
* bs4
* pandas

## Please note
* The crawled data contains Korean. To save this data as csv data, the **encoding format** must be set to '**utf-8-sig**'.
* **OpenAPI server** somtimes **may be unstable**.
* **Handling exception is essential** depending on errors that may occur in OpenAPI.
* **You must get an API Key to use OpenAPI** in the Open Data Portal.

## Open Data Portal
* **KR** [공공데이터포털](https://www.data.go.kr/index.do)
* **EN** [Open Data Portal](https://www.data.go.kr/en/index.do)
<!--- [![한국환경공단](https://cleansys.or.kr/images/common/logo-footer.png)](https://cleansys.or.kr/)-->

## Reference
* [Python (파이썬) 공공데이터 수집 (Open API - XML)](https://greendreamtrre.tistory.com/268)
* [Python. 파일 백그라운드 실행(윈도우즈)](http://drtagkim.blogspot.com/2015/03/python.html)
