
REM @echo off

REM The autobuild directory
set SCRIPT_DIR=C:\Users\caret\autobuild\wb_autobuild
set WINDOWS_SCRIPT_DIR=%SCRIPT_DIR%\windows64

REM Go to script repository
cd %WINDOWS_SCRIPT_DIR% || exit/b %ERRORLEVEL%

REM Update build script repository
../update.bat || exit/b %ERRORLEVEL%

REM Run the build
./build_helper.bat || exit/b %ERRORLEVEL%
