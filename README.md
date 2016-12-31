# ssd-protect
Get notified when an app writes a lot of data to your SSD

Add this to your crontab file to get notified if you exceed your threshold writes in a day:

`00 00 * * * bash path/to/ssd-protect.sh > /dev/null`

The script will only output if the threshold has been exceeded, so you can send the output to your email easily.
