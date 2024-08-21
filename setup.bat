SETX Path ""
mkdir garbage
cd garbage
curl --output pythonInstaller.exe https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe
PAUSE
pythonInstaller.exe /passive /quiet /log log.txt TargetDir="C:\Python_3_12_5"
SETX Path "C:\Python_3_12_5;C:\Python_3_12_5\Scripts;"
PAUSE