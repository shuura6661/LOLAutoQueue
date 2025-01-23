@echo off
REM Change the directory to where your executable is located
cd /d "D:\Games\TFT\Auto Queue\dist"

REM Log message to indicate the script is running in the terminal
echo %date% %time% - Running lolautoqueue.exe

REM Run the executable
lolautoqueue.exe

REM Pause to keep the command prompt window open
pause
