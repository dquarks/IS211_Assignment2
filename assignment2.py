import re
import csv
import sys
import logging
import argparse
import urllib2
import datetime

def errorL(text):
    logger = logging.getLogger('assignment2')
    logger.error(text)

def downloadData(url):
    f = urllib2.urlopen(url)
    return f

def processData(data):
    r = csv.reader(data, delimiter=',', dialect=csv.excel_tab)
    db = {}
    for x, row in enumerate(r,start=1):
        uid     = row[0]
        uname   = row[1]
        ubday   = row[2]
        res = re.split('/|-', ubday)
        if(len(res) == 3):
            if((int(res[0]) < 12 and int(res[0]) > 1) and int(res[1]) < 31 and (int(res[2]) > 0 and int(res[2]) < datetime.date.today().year)):
                t = datetime.datetime(year=int(res[2]), month=int(res[0]), day=int(res[1])).date()
                if(uid not in db.keys()): db[int(uid)] = {'name' : uname, 'bday' : t}
            else:
                errorL('Error processing line ' + str(x) + ' for ID# ' + uid)
        else:
            errorL('Error processing line ' + str(x) + ' for ID# ' + uid)
    return db

def displayPerson(id, personData):
    if(id not in personData.keys()):
        print('No user found with that id')
    else:
        print('Person #' + str(id) + ' is ' + personData[id].get('name') + ', with a birthday of ' + str(personData[id].get('bday')))


def main():
    logging.basicConfig(filename='erorr.log', filemode='w', level=logging.ERROR, format='%(message)s')
    if len(sys.argv) <= 2:
        exit()
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Enter a URL whose data we will access')
    arg = parser.parse_args()
    try:
        csvData = downloadData(arg.url)
        personData = processData(csvData)
        while True:
            input = int(raw_input('Please enter an ID#: '))
            if(input <= 0):
                exit()
            else:
                displayPerson(int(input), personData)
    except Exception as exception:
        errorL('Invalid URL: ' + str(exception))
main()
