# ssd-protect
Get notified when an app writes a lot of data to your SSD. You can adjust the thresholds as to how much an app has to write in the script file.

You can run it like this:

`bash path/to/ssd-protect.sh disktype megabytesThreshold /path/to/savefile.txt`

Where `disktype` is the name of the disk (after /dev/) and `megabytesThreshold` is how many megabytes can be written before you should be notified, and `/path/to/savefile.txt` is a text file which stores how many megabytes have been written since the last check. This file must be different for every disk you intend to monitor. 

Sample notification:

`10000 megabyte(s) have been written since last check, threshold is 1000 mb!`

You can add this line to your crontab file to get a desktop notification if the threshold is reached (be warned, as the desktop notifications may disappear quickly):

`00 00 * * * bash path/to/ssd-protect.sh > /dev/null | xargs notify-send --urgency=low` 


Or, add this to your crontab file to get notified if you exceed your threshold writes in a day and send the output to email/whatever you have configured for cron:

`00 00 * * * bash path/to/ssd-protect.sh > /dev/null`

## Roadmap

ssd-protect is currently being ported to Python 3 to allow for more features to be added. You can run ssd-protect in your cron as often as you'd like to have data for. In your crontab, just add `00 00 * * * python3 /path/to/ssd-protect.py --daemon > /dev/null` to update the database every day at 12am. The new interface will look extremely similar to vnstat. This is the proposed interface:
```
decagon@server:~$ python3 ssd-protect.py
                        rx              /       tx              /       total           /       estimated
 sdb:
        Dec 12, 17'     24.0 KB         /       819.0 KB        /        843.0 KB
 vda1:
        Dec 12, 17'     664.0 KB        /       673.0 KB        /         1.31 MB
 vda:
        Dec 12, 17'     667.0 KB        /       688.5 KB        /         1.32 MB
   ```     
        
In this example, it will show you how much has been written to every disk every day. The ssd-protect daemon can be run as often as you like, and the granularity for displaying the data can be adjusted down to the second, or up to the year. Unfortunately, the previous data files will not be compatible with version 2.0 of ssd-protect.

## Requirements

Requires /proc/diskstats to be available, and Python 3.



