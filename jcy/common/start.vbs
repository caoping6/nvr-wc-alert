Set WshShell = CreateObject("WScript.Shell")
WshShell.run "cmd /c taskkill /f /t /im python.exe",0, True
WshShell.run "cmd /c python main.py",0

Set WshShell = Nothing
MsgBox "success!", vbInformation, "info"
