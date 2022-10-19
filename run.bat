@echo off

SET token=

for /f "delims=" %%i in (%~dp0\bot-token.txt) do call :setToken %%i
if defined token (
    python %~dp0\src\main.py %token%
)
goto finish

:setToken
set token=%token% %1%
goto :eof

:finish
pause