RMDIR /S /Q .\dist
RMDIR /S /Q .\build
call .\venv\Scripts\activate.bat
pyinstaller --add-binary main_window.ui;. --name="mcs2pdf" --noconsole main.py