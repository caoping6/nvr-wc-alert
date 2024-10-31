Set WshShell = CreateObject("WScript.Shell")
WshShell.run "cmd /c taskkill /f /t /im python.exe",0, True

Set WshShell = Nothing
MsgBox "stop!", vbInformation, "info"
