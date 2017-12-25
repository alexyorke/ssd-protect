from datetime import datetime, timedelta
import pickle

# how many entries to show in the overview
amountToShow = 10

# whether the database should be updated or not
writeToDb = True

# how granular to show the summary data (e.g. if the app
# is run multiple times in one day, this can show every entry
# or just an overview of the entries
granularity = timedelta(hours=1)

# the path to the database file
pathToDb = "ssd-protect.pickle"

now = datetime.now()

# get the current data
disks = {}
with open('/proc/diskstats') as fp:
    for cnt, line in enumerate(fp):
        disks[line.split()[2]] = line.split()

database = {}
# read database into file
try:
    pickle_in = open(pathToDb, "rb")
    database = pickle.load(pickle_in)
except FileNotFoundError:
    pass

# add data from right now into the database
database[now] = disks

# write database back to file
if writeToDb:
    pickle_out = open(pathToDb, "wb")
    pickle.dump(database, pickle_out)
    pickle_out.close()

if (len(database) <= 1):
    print("ssd-protect: not enough data available yet.")
    exit()
if (len(database) == 2):
    print("ssd-protect: not enough data available yet for chosen granularity size.")
    exit()


def printDiskEntry(date, megabytesWritten, megabytesRead, displayEstimate=False):
    """Pretty-prints the written and read data, and can display an estimate"""
    print(("\t" + date.ljust(16) + formatSize(megabytesWritten).ljust(15) + " /       " + formatSize(megabytesRead).ljust(8) + "        / " +
           formatSize(float(megabytesRead) + float(megabytesWritten)).rjust(15)), end='')
    if (displayEstimate):
        multiplier = 1 + (31 - int(now.strftime("%d"))) / 31.0
        print("\t/\t" + formatSize((megabytesRead + megabytesWritten) * multiplier))
    else:
        print()


def formatSize(megabytes):
    """Shows the highest integer unit of data if it is greater than or equal to one"""
    kilobytes = float(megabytes) * 1024
    counter = 0
    prefixes = ["B", "KB", "MB", "GB", "TB", "PB"]
    while (kilobytes >= 1024) and counter < len(prefixes) - 1:
        kilobytes = float(kilobytes / 1024)  # TODO: may cause rounding errors
        counter = counter + 1
    return str(round(kilobytes, 2)) + " " + prefixes[counter]


# print header
print("\t\t\t\trx\t\t/\ttx\t\t/\ttotal\t\t/\testimated")

shownSoFar = 0
prevDiskEntry = None

firstEntry = min(database.items(),
                 key=lambda v: v if isinstance(v, datetime) else datetime.min)[1]

for disks in database:
    if (shownSoFar > amountToShow):
        break
    if (prevDiskEntry is not None and (disks - prevDiskEntry) < granularity):
        continue

    prevDiskEntry = disks
    shownSoFar = shownSoFar + 1
    entry = database[disks]
    for disk in entry:
        megabytesWritten = float(entry[disk][6]) / 2 / 1024
        megabytesRead = float(entry[disk][3]) / 2 / 1024
        # subtract very first entry in db from all other entries because
        # it will show how much has been written since then
        megabytesWritten = megabytesWritten - \
            int(float(firstEntry[disk][6]) / 2 / 1024)
        megabytesRead = megabytesRead - \
            int(float(firstEntry[disk][3]) / 2 / 1024)
        print(" " + entry[disk][2] + ": ")
        printDiskEntry(str(disks.strftime("%b %m, %y', %H:%M\t")),
                       megabytesWritten, megabytesRead)
