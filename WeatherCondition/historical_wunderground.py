import requests
import csv
import os
from dateutil.rrule import *
from dateutil.parser import *

# Variables
daySt = "20160601"  # state date
dayEnd = "20160701"  # end date
outPath = os.path.abspath(os.curdir) + \
    '/historical_data/weather/'  # output path
station = 'ZBAA'  # weather station ID
api = '0f93224c89292602'  # developer API key

# Create list of dates between start and end
days = list(rrule(DAILY, dtstart=parse(daySt), until=parse(dayEnd)))

# Create daily url, fetch json file, write to disk
for day in days:
    # format day as YYYYMMDD
    r = requests.get('http://api.wunderground.com/api/' + api +
                     '/history_' + day.strftime("%Y%m%d") + '/q/' + station + '.json')
    data = r.json()['history']['observations']
    file_name = station + '_' + day.strftime("%Y%m%d") + '.csv'
    file_path = os.path.join(outPath, file_name)
    print "Save history data into file: " + file_name
    with open(file_path, 'w+') as csvfile:
        f = csv.writer(csvfile)
        f.writerow(["datetime", "tempm", "tempi", "dewptm", "dewpti", "hum", "wspdm", "wspdi", "wgustm", "wgusti", "wdird", "wdire", "vism", "visi", "pressurem",
                    "pressurei", "windchillm", "windchilli", "heatindexm", "heatindexi", "precipm", "precipi", "conds", "fog", "rain", "snow", "hail", "thunder", "tornado"])
        for elem in data:
            f.writerow([elem["utcdate"]["year"] + elem["utcdate"]["mon"] + elem["utcdate"]["mday"] + 'T' + elem["utcdate"]["hour"] + elem["utcdate"]["min"], elem["tempm"], elem["tempi"], elem["dewptm"], elem["dewpti"], elem["hum"], elem["wspdm"], elem["wspdi"], elem["wgustm"], elem["wgusti"], elem["wdird"],
                        elem["wdire"], elem["vism"], elem["visi"], elem["pressurem"], elem["pressurei"], elem["windchillm"], elem["windchilli"], elem["heatindexm"], elem["heatindexi"], elem["precipm"], elem["precipi"], elem["conds"], elem["fog"], elem["rain"], elem["snow"], elem["hail"], elem["thunder"], elem["tornado"]])
