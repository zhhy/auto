from pywinauto import application

app = application.Application().start("notepad.exe")
app.Notepad.MenuSelect('����->���ڼ��±�')

# app.