pushd %~dp0
set script_dir=%CD%
popd

SET PROJECT_DIR=%script_dir%\..
SET ISCC="C:\Program Files (x86)\Inno Setup 5\iscc"

cd %PROJECT_DIR%
pyinstaller citest\w32\console.py
pyinstaller citest\w32\service.py
%ISCC% building\w32installer.iss /DMyAppVersion=%1
