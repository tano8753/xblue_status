# xblue_status

Hello guys,

This project is a python application to display system's status on Retropie.

It's based on [gbz_overlay](https://github.com/d-rez/gbz_overlay) script by [d-rez](https://github.com/d-rez).

I understand that the code is already running well But still want to do something fit with my needs.

# Photo
(photo.png)

---------------------------------------------------------------------------------------------------------------------------------

# Features
The app can show the status:
- Bluetooth (off, on)
- Wifi (off, on, connected)
 
Notice: The icon will only update once the status changes.

You can set the setting for the app on the config.json file.
```json
{
    "icon_size": 24, => If you change this value, You need create a new folder with the name is the size under images folder.
    "margin_top": 5,
    "margin_right": 5,
    "space_between": 5, => It's a space between 2 icons.
	"delay_start": 0, => It's a delay time in seconds to show it after the EmulationStation is started.
    "devices": [ => You can set which device you want to show. The current value is only wifi and bluetooth.
        "wifi",
        "bluetooth"
    ]
}
```
---------------------------------------------------------------------------------------------------------------------------------

# How to setup

## Install pngview by AndrewFromMelbourne
```bash
git clone https://github.com/AndrewFromMelbourne/raspidmx
cd raspidmx/lib
make
cd ../pngview
make
sudo cp pngview /usr/local/bin/
```

## Clone the source
```bash
git clone https://github.com/tano8753/xblue_status.git
```

## Run the app on boot
Use crontab to set it run on boot:
```bash
crontab -e
```
Then add this line to bottom:
```
@reboot python3 /home/pi/xblue_status/main.py
```
At last, Reboot:

```bash
sudo reboot
```
