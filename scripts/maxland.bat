@echo on
rem set dir
set CONDAPATH=C:\Users\%USERNAME%\anaconda3
rem set environment
set ENVNAME=maxland
set ENVPATH=%CONDAPATH%\envs\%ENVNAME% 
rem set maxland root dir
set ROOTDIR=C:\maxland\maxland_%COMPUTERNAME%

rem check if all dirs and envs exist
if not exist %CONDAPATH% (
    echo Please install anaconda for your local Users
    pause
)
if not exist %ENVPATH% (
    echo Please install maxland and maxland environment
    pause
)
if not exist %ROOTDIR% (
    echo Please install maxland or specify a correct root path
    pause
)




rem activate anaconda prompt
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%

cd %ROOTDIR%
start-pybpod
