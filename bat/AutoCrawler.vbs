Set WinScriptHost = CreateObject( "WScript.shell" )
WinScriptHost.Run Chr(34) & "C:\Users\{USER_NAME}\TMS-AutoCrawler\AutoCrawler.bat" & Chr(34), 0
Set WinScriptHost = Nothing