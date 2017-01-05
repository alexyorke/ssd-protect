# ssd-protect
Get notified when an app writes a lot of data to your SSD. You can adjust the thresholds as to how much an app has to write in the script file.

Sample notification:

`10000 megabyte(s) have been written since last check, threshold is 1000 mb!`

You can add this line to your crontab file to get a desktop notification if the threshold is reached (be warned, as the desktop notifications may disappear quickly):

`00 00 * * * bash path/to/ssd-protect.sh > /dev/null | notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"`


Or, add this to your crontab file to get notified if you exceed your threshold writes in a day and send the output to email/whatever you have configured for cron:

`00 00 * * * bash path/to/ssd-protect.sh > /dev/null`

##Requirements

I've only tested it on Ubuntu 16.04, but it should work on any *buntu/debian variant  

Requires /proc/diskstats to be available.
