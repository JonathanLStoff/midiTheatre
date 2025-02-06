@REM where rtmidi >nul 2>&1
@REM if errorlevel 1 (
@REM     echo rtmidi not found, installing with Chocolatey...
@REM     choco install rtmidi -y
@REM ) else (
@REM     echo rtmidi is already installed.
@REM )
poetry run python manage.py makemigrations miditheatre
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runserver