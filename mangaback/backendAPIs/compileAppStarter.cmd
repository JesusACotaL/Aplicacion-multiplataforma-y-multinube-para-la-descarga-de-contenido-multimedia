CALL .venv/Scripts/activate

SET root=%CD%
SET appstarter=%CD%\appStarter

CD %root%\mainAPI
ECHO "Compiling mainAPI..."
pyinstaller executable.py --noconfirm --add-data "mangafront;mangafront" --add-data "firebase-credentials.json;." --distpath ../appStarter/mainAPI  --workpath ../appStarter/mainAPI/build

CD %root%\sourceAPIs
rem https://stackoverflow.com/questions/12118810/arithmetic-inside-a-for-loop-batch-file
setlocal enableDelayedExpansion
FOR /F %%a IN ('dir /b /a:d "mangaInfoAPIs"') DO IF EXIST "%root%\sourceAPIs\mangaInfoAPIs\%%a\executable.py" (
CD %root%\sourceAPIs\mangaInfoAPIs\%%a
ECHO "Compiling %%a..."
pyinstaller executable.py --noconfirm --distpath %appstarter%\mangaInfoAPIs\%%a --workpath %appstarter%\%%a_BUILD
CD ..
)
FOR /F %%a IN ('dir /b /a:d "mangaAPIs"') DO IF EXIST "%root%\sourceAPIs\mangaAPIs\%%a\executable.py" (
CD %root%\sourceAPIs\mangaInfoAPIs\%%a
ECHO "Compiling %%a..."
pyinstaller executable.py --noconfirm --distpath %appstarter%\mangaAPIs\%%a --workpath %appstarter%\%%a_BUILD
CD ..
)
CD %appstarter%
ECHO "Compiling appStarter..."
pyinstaller appStarter.py --noconfirm --add-data "mainAPI;mainAPI" --add-data "mangaAPIs;mangaAPIs" --add-data "mangaInfoAPIs;mangaInfoAPIs" --add-data "logo.png;." --workpath %appstarter%\mainAPI_BUILD
PAUSE