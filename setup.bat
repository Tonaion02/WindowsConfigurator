SETX Path ""
mkdir garbage
cd garbage
curl --output pythonInstaller.exe https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe
PAUSE
pythonInstaller.exe /passive /quiet /log log.txt TargetDir="C:\Python_3_12_5" | Out-Null
SETX Path "C:\Python_3_12_5;C:\Python_3_12_5\Scripts;" | Out-Null
pip install python-magic-bin | Out-Null
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1')) | Out-Null
PAUSE
