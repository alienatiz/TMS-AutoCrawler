## Autostart
### Windows
* You can modify the example files from [/autostart/Windows](https://github.com/alienatiz/TMS-AutoCrawler/tree/main/autostart/Windows).
* **~.bat**: You must check the path where the **python.exe** or **pythonw.exe** is located and its source code, replace its path.
* **~.vbs**: You must check the path where the **~.bat**(batch executable file) is located and replace its path.
* When all the modifications are done, just run the **~.vbs file once**. It's done!
* To check if it's running in the background, you can see process named as **"Python" in the Background Processes tab in the Task Manager**.'

### Linux
* First, you make the **~.service** on **/etc/systemd/service**.
* Fill the contents in **~.service** matched your environment.
* Then, you should enable this service on **systemd**.
1. systemctl daemon-reload
2. systemctl enable ~.service
3. systemctl start ~.service