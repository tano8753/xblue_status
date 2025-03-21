import time
import subprocess
import os
import re
import json

WIFI_CARRIER = "/sys/class/net/wlan0/carrier"
WIFI_LINKMODE = "/sys/class/net/wlan0/link_mode"
BT_CMD = "hciconfig"
APP_PATH = "/usr/local/bin/pngview"

allowDevices = [
    'wifi',
    'bluetooth'
]
devices = []
allProcesses = {}
screenWidth = 1920
imageWidth = 24
marginTop = 5
marginRight = 5
spaceBetween = 5
delayStart = 0
isESStarted = False

folderPath = os.path.dirname(os.path.realpath(__file__))
imagePath = f"{folderPath}/images/{imageWidth}/"

def run():
    loadConfig()
    getScreenWidth()

    if(len(devices) == 0):
        print("The app need at least 1 device to start!")
        exit()
    
    while True:
        if(checkApp("emulationstation") == True):
            i = 0

            for device in devices:
                showStatus(device, i)
                i += 1

        time.sleep(2)

def getScreenWidth():
    try:
        global screenWidth

        cmd = "tvservice -s"
        FB_OUTPUT = subprocess.check_output(cmd.split()).decode().rstrip()
        resolution = re.search(r"(\d{3,}x\d{3,})", FB_OUTPUT).group().split('x')
        screenWidth = int(resolution[0])
    except FileNotFoundError:
        print('Can\'t get the screen width')

def loadConfig():
    global imagePath
    global delayStart
    global marginTop
    global marginRight
    global spaceBetween
    config = {}
    filePath = f"{folderPath}/config.json"
    
    if os.path.exists(filePath) == False:
        print("The setting file does not exist.")
    else:
        with open(filePath) as f:
            config = json.load(f)

            if(config != None):
                ds = config.get('devices')
                if(ds != None and type(ds) == list):
                    for d in ds:
                        check = d in allowDevices
                        if(check == True):
                            devices.append(d)

                imageSize = config.get('image_size')
                if(imageSize != None):
                    imagePath = f"{folderPath}/images/{imageSize}/"

                ds = config.get('delay_start')
                if(ds != None and str(ds).isnumeric()):
                    delayStart = int(ds)

                mt = config.get('margin_top')
                if(mt != None and str(mt).isnumeric()):
                    marginTop = int(mt)

                mr = config.get('margin_right')
                if(mr != None and str(mr).isnumeric()):
                    marginRight = int(mr)

                sb = config.get('space_between')
                if(sb != None and str(sb).isnumeric()):
                    spaceBetween = int(sb)

def checkApp(processName):
    global isESStarted

    if(isESStarted == True):
        return True
    
    str = ""
    try:
        str = subprocess.check_output(["pidof", processName]).decode().rstrip()
    except:
        pass
    
    if(len(str) > 0):
        isESStarted = True

        if(delayStart > 0):
            time.sleep(delayStart)

    return isESStarted

def showStatus(key, index):
    icon = ""
    x = getX(index)

    if(key == "wifi") :
        icon = wifi()

    elif(key == "bluetooth"):
        icon = bluetooth()

    cmd = [APP_PATH, "-d", "0", "-b", "0x0000", "-n", "-l", "15000", "-y", str(marginTop), "-x", str(x), imagePath + icon]
    p = allProcesses.get(key)

    if(p != None):
        currentIcon = p.get("icon")
        if(currentIcon != icon):
            # Create new process
            allProcesses[key] = {
                "icon": icon,
                "process": subprocess.Popen(cmd)
            }

            p.get("process").kill()
    else:
        # Create new process
        allProcesses[key] = {
            "icon": icon,
            "process": subprocess.Popen(cmd)
        }

def getX(index):
    x = 0
    x  = screenWidth - (imageWidth * (index + 1) + marginRight)

    if(index > 0):
        x -= spaceBetween

    return x

def wifi():
    icon = "wifi_off.png"

    try:
        with open(WIFI_CARRIER, "r", encoding="utf-8") as file:
            carrier_state = int(file.read().rstrip())
        if carrier_state == 1:
            # ifup and connected to AP
            icon = "wifi_connected.png"
        elif carrier_state == 0:
            with open(WIFI_LINKMODE, "r", encoding="utf-8") as file:
                linkmode_state = int(file.read().rstrip())
            if linkmode_state == 1:
                # ifup but not connected to any network
                icon = "wifi.png"
                # else - must be ifdown

    except IOError:
        pass

    return icon

def bluetooth():
    icon = "bluetooth_off.png"
    try:
        with subprocess.Popen(BT_CMD, stdout=subprocess.PIPE) as proc1:
            cmd = ['awk', 'FNR == 3 {print tolower($1)}']
            with subprocess.Popen(cmd, stdin=proc1.stdout, stdout=subprocess.PIPE) as proc2:
                state = proc2.communicate()[0].decode().rstrip()
        if state == "up":
            icon = "bluetooth.png"
    except IOError:
        pass

    return icon

run()
