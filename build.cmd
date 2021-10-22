call .\venv\Scripts\activate.bat
pyinstaller --add-binary main_window.ui;. --name="mcs2pdf" --noconsole main.py