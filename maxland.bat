@echo off
set projects_dir=C:\maxland_VR-01
set main_dir=C:\maxland

echo Activating conda environment...
call activate maxland %*



echo Finding pybpod folder...
chdir /D %projects_dir%

echo Launching pybpod...
call start-pybpod

chdir /D %main_dir%

echo done