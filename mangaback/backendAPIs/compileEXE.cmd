call .venv/Scripts/activate
cd mainAPI
pyinstaller --noconfirm --add-data "mangafront;mangafront" --add-data "firebase-credentials.json;." productionEXE.py --icon="./mangafront/favicon.ico"
pause