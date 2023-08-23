call .venv/Scripts/activate
cd mainAPI
pyinstaller executable.py --noconfirm --add-data "mangafront;mangafront" --add-data "firebase-credentials.json;." --distpath ../appStarter/mainAPI  --workpath ../appStarter/mainAPI/build
cd ..

cd sourceAPIs
cd mangaInfoAPIs
cd myAnimeList
pyinstaller executable.py --noconfirm --distpath ../../../appStarter/mangaInfoAPIs/myAnimeList  --workpath ../../../appStarter/mangaInfoAPIs/myAnimeList/build
cd ../mangaUpdates
pyinstaller executable.py --noconfirm --distpath ../../../appStarter/mangaInfoAPIs/mangaUpdates  --workpath ../../../appStarter/mangaInfoAPIs/mangaUpdates/build
cd ..
cd ..

cd mangaAPIs
cd manganelo
pyinstaller executable.py --noconfirm --distpath ../../../appStarter/mangaAPIs/manganelo  --workpath ../../../appStarter/mangaAPIs/mangakakalottv/build
cd ../mangakakalottv
pyinstaller executable.py --noconfirm --distpath ../../../appStarter/mangaAPIs/mangakakalottv  --workpath ../../../appStarter/mangaAPIs/mangakakalottv/build
cd ../mangakakalotcom
pyinstaller executable.py --noconfirm --distpath ../../../appStarter/mangaAPIs/mangakakalotcom  --workpath ../../../appStarter/mangaAPIs/mangakakalotcom/build
cd ..
cd ..
cd ..
cd appStarter
pyinstaller appStarter.py --noconfirm --add-data "mainAPI;mainAPI" --add-data "mangaAPIs;mangaAPIs" --add-data "mangaInfoAPIs;mangaInfoAPIs" --add-data "logo.png;."
pause
exit