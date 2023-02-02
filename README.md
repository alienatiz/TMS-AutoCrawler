# TMS-AutoCrawler
[![CleanSYS](https://cleansys.or.kr/images/common/logo.png)](https://cleansys.or.kr/)   
Python bot for crawling data from TMS OpenAPI of CleanSYS automatically. You can set the scheduled time the bot will be started and, also change the time scheduled for bot.


## Features: Crawling data automatically
* You can check example in [/data](https://github.com/alienatiz/TMS_AutoCrawler/tree/main/data).

| **mesure_dt**      | **area_nm** | **fact_manage_nm** | **stack_code** | **nh3_exhst_perm_stdr_value** | **nh3_mesure_value** | **\.\.\.** |
|--------------------|-------------|--------------------|----------------|-------------------------------|----------------------|------------|
| 2023\-01\-16 15:00 | 서울특별시       | 노원자원회수시설           | 1              | NaN                           | NaN                  | \.\.\.     |
| 2023\-01\-16 15:00 | 서울특별시       | 노원자원회수시설           | 2              | NaN                           | NaN                  | \.\.\.     |

## Getting Started
1) Download this code in your directory.
2) Write the auto starting script matched by your environment. Check [autostart.md](https://github.com/alienatiz/TMS-AutoCrawler/tree/main/autostart/autostart.md)
3) Run the script in background on your system.
4) Check the data collected by script.

```git
git clone git@github.com:alienatiz/TMS-AutoCrawler.git
```

## Libraries
Libraries MUST be needed for crawling data by OpenAPI are explained in requirements.txt.  <br />
Check them here. > [requirements.txt](https://github.com/alienatiz/TMS-AutoCrawler/blob/main/requirements.txt)

## Please note
* The crawled data contains Korean. To save this data as csv data, the **encoding format** must be set to '**utf-8-sig**'.
* **OpenAPI server** somtimes **may be unstable**.
* **Handling exception is essential** depending on errors that may occur in OpenAPI.
* **You must get an API Key to use OpenAPI** in the Open Data Portal.

## Links
### Open Data Portal
* **KR** [공공데이터포털](https://www.data.go.kr/index.do)
* **EN** [Open Data Portal](https://www.data.go.kr/en/index.do)
<!--- [![한국환경공단](https://cleansys.or.kr/images/common/logo-footer.png)](https://cleansys.or.kr/)-->

### Reference
* [Python (파이썬) 공공데이터 수집 (Open API - XML)](https://greendreamtrre.tistory.com/268)
* [Python. 파일 백그라운드 실행(윈도우즈)](http://drtagkim.blogspot.com/2015/03/python.html)
