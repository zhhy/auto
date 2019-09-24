from pywinauto import application

app = application.Application().start("notepad.exe")
app.Notepad.MenuSelect('帮助->关于记事本')

# app.