SET /A counter=5000
CALL .venv\Scripts\activate
CD mainAPI
START flask --app main run --debug --port %counter% --host=0.0.0.0
SET /A counter+=1

CD ../sourceAPIs
rem https://stackoverflow.com/questions/12118810/arithmetic-inside-a-for-loop-batch-file
setlocal enableDelayedExpansion
FOR /F %%a IN ('dir /b /s /a:d "mangaInfoAPIs"') DO IF EXIST "%%a\main.py" (
CD %%a 
START flask --app main run --debug --port %%counter%% --host=0.0.0.0 
SET /A counter+=1
CD ..
)
CD ..
FOR /F %%a IN ('dir /b /s /a:d "mangaAPIs"') DO IF EXIST "%%a\main.py" (
CD %%a 
START flask --app main run --debug --port %%counter%% --host=0.0.0.0
SET /A counter+=1
CD ..
)
pause
