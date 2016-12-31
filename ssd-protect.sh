# grep for your hd (e.g. sda1) assumes 512kb blocks
# based on http://serverfault.com/questions/238033/measuring-total-bytes-written-under-linux

stat=$( awk '/sd/ {print $3"\t"$10 / 2 / 1024}' /proc/diskstats | sed 's/\s\+/ /g' | grep sda1 )

mbWritten=$(echo $stat | cut -d " " -f 2)

echo "Megabytes written (all time): $mbWritten"

# exercise for the reader: save value to file, and compare it to tomorrow to see how many mb's were written
# if there is more than, say, 1024 * 40 then you might want to track down the app that's writing too much
