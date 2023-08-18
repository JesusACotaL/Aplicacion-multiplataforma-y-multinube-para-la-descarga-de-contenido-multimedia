call .venv/Scripts/activate
cd mainAPI
start waitress-serve --listen=*:8080 main:app
cd ..

cd mangaInfoAPIs
cd myAnimeList
start waitress-serve --listen=*:5001 myAnimeList:app
cd ..
cd ..

cd mangaAPIs
cd manganelo
start waitress-serve --listen=*:5002 manganelo:app
cd ..
cd mangakakalottv
start waitress-serve --listen=*:5003 mangakakalottv:app
cd ..
cd mangakakalotcom
start waitress-serve --listen=*:5004 mangakakalotcom:app
cd ..
cd ..

exit
