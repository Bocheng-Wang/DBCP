@echo off

REM There is no setting to make a DOS script exit when a command
REM fails.  However, the variable %ERRORLEVEL% is set to the value
REM returned by each command.  Following most commands is the code
REM "|| exit/b %ERRORLEVEL%".  The code on the right of the
REM "||" is executed when the command on the left returns a non-zero
REM value and this code will exit the script with the return value
REM from the command that failed.
REM Another, way instead of using "||" is to check the 
REM %ERRORLEVEL% in a IF statement after each command.
REM    "if %ERRORLEVEL% NEQ 0 exit/b %ERRORLEVEL%"


REM The autobuild directory
set AUTOBUILD_DIR=C:\Users\caret\autobuild\autobuild_dir

REM Type of build (release | debug)
set DEV_BUILD_TYPE=release

REM Directory in which the build takes place
set BUILD_DIR=%AUTOBUILD_DIR%\%DEV_BUILD_TYPE%
set SOURCE_DIR=%AUTOBUILD_DIR%\workbench

REM Directory to which executables and libraries
REM are copied and windeployqt is run
set BUILD_OUTPUT_DIR=%AUTOBUILD_DIR%\bin_%DEV_BUILD_TYPE%

REM Update PATH for compiler and Qt
call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" AMD64
set PATH=C:\dev64_msvc2014\install\qt-5.7.0\bin;%PATH%

REM Go source directory
cd %SOURCE_DIR% || exit/b %ERRORLEVEL%

REM Update source code
c:\cygwin\bin\git.exe fetch origin || exit/b %ERRORLEVEL%
c:\cygwin\bin\git.exe reset --hard origin/master --  || exit/b %ERRORLEVEL%

REM Go to build directory
cd %BUILD_DIR% || exit/b %ERRORLEVEL%

REM Run CMake
cmake ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DWORKBENCH_FREETYPE_DIR=C:\dev64_msvc2014\install\FreeType-2.7 ^
    -DWORKBENCH_USE_QT5=TRUE ^
    -DOPENSSL_ROOT_DIR=C:\dev64_msvc2014\install\openssl-1.0.1t ^
    -DZLIB_ROOT=C:\dev64_msvc2014\install\zlib-1.2.8 ^
    -G "NMake Makefiles JOM" ^
    ..\workbench\src ^
	|| exit/b %ERRORLEVEL%
  
REM Build source.  "jom" is a program from Qt that builds in parallel (nmake does not)
jom -j8 || exit/b %ERRORLEVEL%

REM Go to the output directory, copy libraries
REM and run windeployqt on the executables
cd %BUILD_OUTPUT_DIR% || exit/b %ERRORLEVEL%
copy %BUILD_DIR%\Desktop\wb_view.exe . || exit/b %ERRORLEVEL%
copy %BUILD_DIR%\CommandLine\wb_command.exe .  || exit/b %ERRORLEVEL%
windeployqt wb_view.exe  || exit/b %ERRORLEVEL%
windeployqt wb_command.exe || exit/b %ERRORLEVEL%
copy C:\dev64_msvc2014\install\openssl-1.0.1t\bin\libeay32.dll . || exit/b %ERRORLEVEL%
copy C:\dev64_msvc2014\install\openssl-1.0.1t\bin\ssleay32.dll . || exit/b %ERRORLEVEL%
copy C:\dev64_msvc2014\install\zlib-1.2.8\bin\zlib.dll . || exit/b %ERRORLEVEL%

set MYELIN_DEST_DIR=caret@myelin1:/mainpool/storage/distribution/caret7_distribution/workbench/bin_windows64
REM Copy to myelin
REM c:\cygwin\bin\scp .\*  %MYELIN_DEST_DIR%   || exit/b %ERRORLEVEL%

copy %AUTOBUILD_DIR%\..  || exit/b %ERRORLEVEL%

exit/b 0
