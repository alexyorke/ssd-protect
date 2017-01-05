# grep for your hd (e.g. sda1) assumes 512kb blocks
# based on http://serverfault.com/questions/238033/measuring-total-bytes-written-under-linux

# Configuration

# the name after /dev/ for your hdd (e.g. sda1) for the hardrive that you want to monitor
# you can use the "disks" app in ubuntu to find this information or by running df -h
hdd="$1"

# where to store ssd protect information
prevMbDb="$3"

# how many mb can be written before you should be notified that something is up (must be a positive integer)
warningThreshold="$2"

# End configuration

# create database if it doesn't exist
touch "$prevMbDb"

# get new and prev stats
prevMb=$(cat "$prevMbDb")
currMbRaw=$( awk '/sd/ {print $3"\t"$10 / 2 / 1024}' /proc/diskstats | sed 's/\s\+/ /g' | grep $hdd )
mbWritten=$(echo $currMbRaw | cut -d " " -f 2)

# save current stats
echo "$mbWritten" > "$prevMbDb"

deltaMb=$(($mbWritten-$prevMb))

# check to see if threshold is exceeded
echo "$deltaMb megabyte(s) have been written since last check, threshold is $warningThreshold mb"

if [[ "$deltaMb" -gt "$warningThreshold" ]]
then
	# http://stackoverflow.com/questions/2990414/echo-that-outputs-to-stderr
	(>&2 echo "Threshold disk writes has been exceeded on $(date)! Megabytes written: $deltaMb")
fi

# exercise for the reader: save value to file, and compare it to tomorrow to see how many mb's were written
# if there is more than, say, 1024 * 40 then you might want to track down the app that's writing too much
