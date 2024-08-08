import requests
import sys
import csv
import time
import datetime
from datetime import date

apikey = "" # Alpha Vantage API Key
filepath = ""

"""
Helper method, returns contents of csv file
as a list of lists
"""
def processcsv(filepath):
    f = open(filepath, "r", encoding="utf-8")
    reader = csv.reader(f, delimiter=",")
    data = list(reader)
    f.close()
    return data


# Get info from file
try:
    print("Please enter the filepath for the csv file you wish to update:")
    filepath = input()
    csvdata = processcsv(filepath)
except FileNotFoundError:
    print("File not found! Please check file name or path.")
    sys.exit()
header = csvdata[0]
data = csvdata[1:]

# Parse data into variables for api call
startdate = data[0][0]
currdate = date.today()
funds = list()
for fund in header[1:]:
    funds.append(fund)
lastfund = funds[-1]

# API call
endpoint = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "apikey": apikey,
}

api_data = dict()
for fund in funds:
    params["symbol"] = fund
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        api_data[fund] = response.json()["Time Series (Daily)"]
    else:
        print("Error: ", response.content)
    if fund != lastfund:
        time.sleep(15)
# End of API call

# Update csv
update = ""
for entry in header:
    update += entry + "," # Adds header as the first line of csv
update = update[:-1] + "\n"
iterator = datetime.datetime.strptime(startdate, "%Y-%m-%d").date()
delta = datetime.timedelta(days=1)
while iterator <= currdate:
    update += str(iterator) + ","
    for fund in funds:
        try:
            update += api_data[fund][str(iterator)]["5. adjusted close"] + ","
        except KeyError:
            update += "-,"
    update = update[:-1] + "\n"
    iterator += delta
update = update[:-1]

f = open(filepath, "w")
f.write(update)
# End of update csv

print("Done")
