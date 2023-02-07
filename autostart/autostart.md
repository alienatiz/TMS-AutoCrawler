## Autostart
### Windows
* You can modify the example files from [here](https://github.com/alienatiz/TMS-AutoCrawler/tree/main/autostart/Windows).
* **~.bat**: You must check the path where the **python.exe** or **pythonw.exe** is located and its source code, replace its path.
* **~.vbs**: You must check the path where the **~.bat**(batch executable file) is located and replace its path.
* When all the modifications are done, just run the **~.vbs file once**. It's done!
* To check if it's running in the background, you can see process named as **"Python" in the Background Processes tab in the Task Manager**.'

### Linux
1. Move the **~.service** to **/etc/systemd/service**.
```
sudo mv ./Linux/AutoCrawler.service /etc/systemd/service
```

2. Fill the contents in **~.service** matched your environment.
```
sudo nano /etc/systmd/service/AutoCrawler.service
```

4. Then, you should enable this service on **systemd**.
```
systemctl daemon-reload
systemctl enable AutoCrawler.service
systemctl start AutoCrawler.service
```
