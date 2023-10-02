CALL .venv/Scripts/activate

SET root=%CD%
SET appstarter=%CD%\appStarter

CD %root%\mainAPI
ECHO ====================Compiling MainAPI...====================
pyinstaller executable.py --noconfirm --add-data "mangafront;mangafront" --add-data "firebase-credentials.json;." --distpath %appstarter%\mainAPI  --workpath %appstarter%\mainAPI_BUILD

CD %root%\sourceAPIs
FOR /F %%a IN ('dir /b /a:d "mangaInfoAPIs"') DO IF EXIST "%root%\sourceAPIs\mangaInfoAPIs\%%a\executable.py" (
CD %root%\sourceAPIs\mangaInfoAPIs\%%a
ECHO ====================Compiling %%a...====================
pyinstaller executable.py --noconfirm --distpath %appstarter%\mangaInfoAPIs\%%a --workpath %appstarter%\%%a_BUILD
)

CD %root%\sourceAPIs
FOR /F %%a IN ('dir /b /a:d "mangaAPIs"') DO IF EXIST "%root%\sourceAPIs\mangaAPIs\%%a\executable.py" (
CD %root%\sourceAPIs\mangaAPIs\%%a
ECHO ====================Compiling %%a...====================
pyinstaller executable.py --noconfirm --distpath %appstarter%\mangaAPIs\%%a --workpath %appstarter%\%%a_BUILD
)

CD %appstarter%
ECHO ====================Compiling AppStarter...====================
pyinstaller appStarter.py --noconfirm --add-data "mainAPI;mainAPI" --add-data "mangaAPIs;mangaAPIs" --add-data "mangaInfoAPIs;mangaInfoAPIs" --add-data "logo.png;." --workpath %appstarter%\appstarter_BUILD
PAUSE