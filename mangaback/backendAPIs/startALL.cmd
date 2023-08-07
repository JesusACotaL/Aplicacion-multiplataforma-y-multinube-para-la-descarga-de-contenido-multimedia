call .venv/Scripts/activate
cd mainAPI
start flask --app main run --debug --port 5000 --host=0.0.0.0
cd ..

cd mangaInfoAPIs
cd myAnimeList
start flask --app myAnimeList run --debug --port 5001 --host=0.0.0.0
cd ..
cd ..

cd mangaAPIs
cd manganelo
start flask --app manganelo run --debug --port 5002 --host=0.0.0.0
cd ..
cd mangakakalottv
start flask --app mangakakalottv run --debug --port 5003 --host=0.0.0.0
cd ..
cd mangakakalotcom
start flask --app mangakakalotcom run --debug --port 5004 --host=0.0.0.0
cd ..
cd ..

exit
