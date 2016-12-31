# ssd-protect
Get notified when an app writes a lot of data to your SSD

Add this to your crontab file to get notified if you exceed your threshold writes in a day:

`00 00 * * * bash path/to/ssd-protect.sh > /dev/null`

The script will only output if the threshold has been exceeded, so you can send the output to your email easily.

You can add this line to your crontab file to get a desktop notification if the threshold is reached (be warned, as the desktop notifications may disappear quickly):

`00 00 * * * bash path/to/ssd-protect.sh > /dev/null | notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')`
