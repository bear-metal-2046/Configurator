import os
import sys

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print("Python Package 'tqdm' not found.  Installing...")
    os.system("cmd /c pip3 install tqdm")
    from tqdm import tqdm

try:
    import requests as rq
except ModuleNotFoundError:
    print("Python Package 'requests' not found.  Installing...")
    os.system("cmd /c pip3 install requests")
    import requests as rq

try:
    import pyautogui as pag
except ModuleNotFoundError:
    print("Python Package 'pyautogui' not found.  Installing...")
    os.system("cmd /c pip3 install pyautogui")
    import pyautogui as pag


def getAppInstaller():
    print("Downloading App Installer MSIX Bundle...")
    path = f'C:/Users/{accountname}/Downloads/wingetInstaller.msixbundle'
    downloadFileInStream("https://github.com/microsoft/winget-cli/releases/latest/download/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle", path)
    os.system(f"cmd /c winget upgrade winget")
    os.system(f"cmd /c {path}")
    pag.press('enter')
    print("App Installer installed!")

def getJetBrainsPackages():
    print("Using winget to download JetBrains software... (Intellij IDEA and Toolbox)")
    os.system(f"cmd /c winget install JetBrains.IntellijIDEA.Community")
    os.system(f"cmd /c winget install JetBrains.Toolbox")
    print("JetBrains Packages installed!")

def getPhoenixTunerX():
    print("Using winget to download Phoenix Tuner X...")
    os.system("cmd /c winget install 'Phoenix Tuner X'")
    print("Pheonix Tuner X installed!")

def getAmazonCorretto17():
    print("Using winget to download Amazon Corretto 17 (Java)...")
    os.system("cmd /c winget install 'Amazon Corretto 17'")
    print("Amazon Corretto 17 installed!")

def downloadFileInStream(url, filepath): # from https://stackoverflow.com/a/37573701
    # Streaming, so we can iterate over the response.
    response = rq.get(url, stream=True)

    # Sizes in bytes.
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(filepath, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError(f"Could not download file: {url}")

def getWPILib():
    import threading
    path = f'C:/Users/{accountname}/Downloads/WPILibDisk.iso'
    print("Checking for WPILib ISO...")
    try:  # This is a lengthy download, so this checks to see if we really need to do all the work.
        open(path, 'r')
    except:
        print("WPILib Installer ISO not found.")
        print("Downloading WPILib ISO...")
        print("This might take a while...")
        version="2024.3.2"
        try:
            downloadFileInStream(f"https://packages.wpilib.workers.dev/installer/v{version}/Win64/WPILib_Windows-{version}.iso", path)
        except IOError as e:
            if e.errno == 28:
                # This can happen if something about the streaming goes wrong
                print("Not enough disk space, cancelling installation.")
                os.system(f"cmd del {path}")
            else:
                print("Unknown IOError occurred, raising exception.")
                raise e
            return
    print("Mounting WPILib Disk Image...")
    os.system(f"powershell Mount-DiskImage -ImagePath {path}")
    print("Executing installer...")
    print("Careful, this will push buttons on your computer for you.")
    t1 = threading.Thread(target=runWPILibInstaller)
    t2 = threading.Thread(target=WPILibInstallerInputs)
    t1.start()
    t2.start()
    t2.join()
    print("WPILib Installing")
    print("Attempting to dismount disk image (requires admin privileges)...")
    if os.system(f'runas /noprofile /user:Administrator "cmd /c Dismount-DiskImage -ImagePath {path}"') != 0:
        print("Dismount failed!  Eject disk manually in File Explorer.")
        print("Attempting to delete WPILib ISO...")
        os.system(f"del {path}")

def getGameTools():
    # year and version are not essential, but useful if you want the right download name.
    year = 2024
    version = 24.0
    path = f"C:\\Users\\{accountname}\\Downloads\\ni-frc-{year}-game-tools_{version}_online.exe"
    print("Downloading FRC Game Tools Package Manager...")
    downloadFileInStream("https://www.ni.com/en/support/downloads/drivers/download/packaged.frc-game-tools.500107.html", path)
    print("Running installer...")
    if (os.system(f"cmd /c {path} --passive --accept-eulas --prevent-activation --prevent-reboot") != 0):
        print(f"Install process failed!  Try running {path} manually (through File Explorer).")

def runWPILibInstaller():
    driveLetters = ["D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    driveLetterNum = 0
    returnNum = 1
    while returnNum != 0:
        driveLetter = driveLetters[driveLetterNum]
        print(f"Checking {driveLetter}:/ for installer")    
        returnNum = os.system(f"cmd /c {driveLetter}:/WPILibInstaller.exe")
        if returnNum == 0:
            print("WPILib Install Process Finished!")
            return
        driveLetterNum += 1
    print("Could not find mounted disk image.")

def WPILibInstallerInputs():
    # We love reliable code |
    #                       v
    import time
    time.sleep(60)
    pag.press("tab")
    pag.press("enter")
    time.sleep(5)
    pag.press("tab")
    pag.press("tab")
    pag.press("enter")
    pag.press("tab")
    pag.press("enter")
    input("Please press enter when install option is chosen.")

def main():
    global accountname
    accountname = os.getlogin()
    if (sys.argv.__contains__("-h") or len(sys.argv) == 1):
        print(
"""This is a Python script to install all necessary tools for programming on FRC team 2046 Bear Metal on your computer (if your computer runs on Windows OS).  
Run Options:
-a -> install everything this script can install
-w -> install WPILib
-i -> install AppInstaller (WinGet)
-j -> install JetBrains Packages (requires WinGet)
-c -> install Amazon Corretto 17 (Java)
-p -> install Phoenix Tuner X
-h -> display help info""")
    if (sys.argv.__contains__("-u")):
        accountname = input("Admin Name Override:")
    if (sys.argv.__contains__("-a")):
        print("Beginning computer setup...")
        if os.system("cmd /c winget -v") != 0:
            getAppInstaller()
        else:
            os.system("cmd /c winget upgrade winget")
        getPhoenixTunerX()
        getAmazonCorretto17()
        getJetBrainsPackages()
        getGameTools()
        getWPILib()
        print("Assuming nothing went wrong on the way, your computer is now ready to program on!")
    if (sys.argv.__contains__("-w")):
        getWPILib()
    if (sys.argv.__contains__("-i")):
        getAppInstaller()
    if (sys.argv.__contains__("-j")):
        getJetBrainsPackages()
    if (sys.argv.__contains__("-c")):
        getAmazonCorretto17()
    if (sys.argv.__contains__("-p")):
        getPhoenixTunerX()

if __name__ == "__main__":
    main()
