call .venv/Scripts/activate
cd mainAPI
pyinstaller --add-data "firebase-credentials.json;." --noconfirm productionEXE.py
pause