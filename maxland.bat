@echo off
set projects_dir=C:\maxland_VR-01

echo Activating conda environment...
call activate maxland %*



echo Finding pybpod folder...
chdir /D %projects_dir%

echo Launching pybpod...
call start-pybpod

echo done