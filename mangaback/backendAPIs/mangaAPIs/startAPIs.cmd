call ./.venv/Scripts/activate.bat
cd manganelo
start flask --app manganelo run --debug --port 5002
cd ..
cd mangakakalottv
start flask --app mangakakalottv run --debug --port 5003