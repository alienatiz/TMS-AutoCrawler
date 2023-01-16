# TMS-AutoCrawler
[![Cleansys](https://cleansys.or.kr/images/common/logo.png)](https://cleansys.or.kr/)   
Python bot for crawling data from TMS OpenAPI of CleanSYS automatically. You can set the scheduled time the bot will be started and, also change the time scheduled for bot.


# Features
## Crawling
* You can check example in [/data](https://github.com/alienatiz/TMS_AutoCrawler/tree/main/data).

 **mesure_dt**      | **area_nm** | **fact_manage_nm** | **stack_code** | **nh3_exhst_perm_stdr_value** | **nh3_mesure_value** | **\.\.\.** 
--------------------|---------|----------|---------|----------------|---------------|------------
 2023\-01\-16 15:00 | 서울특별시   | 노원자원회수시설 | 1       | NaN            | NaN           | \.\.\.    
 2023\-01\-16 15:00 | 서울특별시   | 노원자원회수시설 | 2       | NaN            | NaN           | \.\.\.    

## Autostart
### Windows
* You can modify the example files from [/autostart/Windows](https://github.com/alienatiz/TMS-AutoCrawler/tree/main/autostart/Windows).
* **~.bat**: You must check the path where the **python.exe** or **pythonw.exe** is located and its source code, replace its path.
* **~.vbs**: You must check the path where the **~.bat**(batch executable file) is located and replace its path.
* When all the modifications are done, just run the **~.vbs file once**. It's done!
* To check if it's running in the background, you can see process named as **"Python" in the Background Processes tab in the Task Manager**.'

### Linux
* First, you make the **~.service** on **/etc/systemd/service**.
* Fill the contents in **~.service** are below:

[Unit]<br/>
Description={service name}<br/>

[Service]<br/>
User={user name}<br/>
WorkingDirectory={Working directory}<br/>
ExecStart=/bin/bash -c 'cd {Project directory} && source {Your virtualenv activation} && python3 {Project script}'<br/>

[Install]<br/>
WantedBy=multi-user.target<br/>

* Then, you should enable this service on **systemd**.
1) systemctl daemon-reload
2) systemctl enable ~.service
3) systemctl start ~.service


## Libraries
Libraries MUST needed for crawling data by OpenAPI are below:
* urllib3
* bs4
* pandas
* schedule
* datetime
* time
* lxml

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
