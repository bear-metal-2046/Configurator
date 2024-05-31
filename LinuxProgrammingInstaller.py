import os
import sys

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print("Python Package 'tqdm' not found.  Installing...")
    os.system("python3 -m pip install tqdm")
    from tqdm import tqdm

try:
    import requests as rq
except ModuleNotFoundError:
    print("Python Package 'requests' not found.  Installing...")
    os.system("python3 -m pip install requests")
    import requests as rq

try:
    import pyautogui as pag
except ModuleNotFoundError:
    print("Python Package 'pyautogui' not found.  Installing...")
    os.system("python3 -m pip install pyautogui")
    import pyautogui as pag


def getJetBrainsPackages():
    print("Using snap to install JetBrains Intellij IDEA...")
    os.system("sudo snap install intellij-idea-community --classic")
    print("JetBrains Intellij IDEA installed!")

def getAmazonCorretto17():
    print("Downloading and installing Amazon Corretto 17 (Java)...")
    # These commands are straight from https://docs.aws.amazon.com/corretto/latest/corretto-17-ug/generic-linux-install.html
    os.system("wget -O - https://apt.corretto.aws/corretto.key | sudo gpg --dearmor -o /usr/share/keyrings/corretto-keyring.gpg && \\")
    os.system('echo "deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main" | sudo tee /etc/apt/sources.list.d/corretto.list')
    os.system('sudo apt-get update; sudo apt-get install -y java-17-amazon-corretto-jdk')
    print("Amazon Corretto 17 installed!")
    print(f"JAVA_HOME is now " + os.environ.get("JAVA_HOME"))

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
    path = input("Download directory: ")
    print("Checking for WPILib ISO...")
    try:  # This is a lengthy download, so this checks to see if we really need to do all the work.
        open(path, 'r')
    except FileNotFoundError:
        print("WPILib Installer ISO not found.")
        print("Downloading WPILib ISO...")
        print("(This might take a while)")
        version="2024.3.2"
        try:
            downloadFileInStream(f"https://packages.wpilib.workers.dev/installer/v{version}/Win64/WPILib_Windows-{version}.iso", path)
        except IOError as e:
            if e.errno == 28:
                # This can happen if something about the streaming goes wrong
                print("Not enough disk space, cancelling installation.")
                os.system(f"rm -f {path}")
            else:
                print("Unknown IOError occurred, raising exception.")
                raise e
            return
    print("Mounting WPILib Disk Image...")
    mountpoint = input("Mount point: ")
    os.system(f"mount {path} {mountpoint}")
    print("Executing installer...")
    print("Careful, this will push buttons on your computer for you.")
    t1 = threading.Thread(target=lambda : runWPILibInstaller(mountpoint))
    t2 = threading.Thread(target=WPILibInstallerInputs)
    t1.start()
    t2.start()
    t2.join()
    print("WPILib Installing")
    print("Attempting to dismount disk image (requires admin privileges)...")
    if os.system(f"") != 0:
        print("\033[1;40m Dismount failed!  Eject disk manually in File Explorer. \033[0m")
        print("Attempting to delete WPILib ISO...")
        os.system(f"rm {path}")

def runWPILibInstaller(mountpoint):
    os.system(f"{mountpoint}/WPILibInstaller.exe")

def WPILibInstallerInputs():
    # We love reliable code |
    #                       v
    import time
    time.sleep(60)
    pag.press("tab")
    pag.press("enter")
    time.sleep(2)
    pag.press("tab")
    pag.press("tab")
    pag.press("enter")
    pag.press("tab")
    pag.press("enter")
    input("Please press enter when install option is chosen.")

def main():
    if (sys.argv.__contains__("-h") or len(sys.argv) == 1):
        print(
"""This is a Python script to install all necessary tools for programming on FRC team 2046 Bear Metal on your computer (if your computer runs on a Linux OS).
(unfortunately, there is no Phoenix Tuner X or FRC Game Tools for Linux)
Run Options:
-a -> install everything this script can install
-w -> install WPILib
-j -> install JetBrains Intellij IDEA (requires WinGet)
-c -> install Amazon Corretto 17 (Java)
-h -> display help info""")
    if (sys.argv.__contains__("-a")):
        print("Beginning computer setup...")
        getAmazonCorretto17()
        getJetBrainsPackages()
        getWPILib()
        print("Assuming nothing went wrong on the way, your computer is now ready to program on!")
    if (sys.argv.__contains__("-w")):
        getWPILib()
    if (sys.argv.__contains__("-j")):
        getJetBrainsPackages()
    if (sys.argv.__contains__("-c")):
        getAmazonCorretto17()

if __name__ == "__main__":
    main()