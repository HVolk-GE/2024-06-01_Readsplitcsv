# Python 3.11.3 Windows env.
# Need tkinter for File Open Dialog.
################################################################################################################
# Appl. Version:
#   Version     Date            Comments
#   1.0.1       03.06.2024      Initial Verion, simple shell application
# 
################################################################################################################
# depentencies : 
#
# pip3 install progress progressbar2 alive-progress tqdm
# 
# (pip install ini-parser / for python < 3.12 - atm not coded!)
#
# For create py to exe file:
# pip install pyinstaller
# find afterwards exe file under "\dist\*filename*\"
################################################################################################################
################################################################################################################
# Don't touch this area, when you not know what it is !
################################################################################################################
################################################################################################################
# import depentencies:
import csv, os, os.path, configparser, time, ctypes
from progress.bar import Bar
from datetime import datetime
import tkinter as tk
import tkinter.messagebox as tkMessageBox
from tkinter import *
from tkinter.filedialog import askopenfilename
from functools import partial
################################################################################################################
# Define messagesbox:
WS_EX_TOPMOST = 0x40000
MessageBox = ctypes.windll.user32.MessageBoxExW

# Read config.ini file for default settings outside the scource code:
config = configparser.ConfigParser()
config.read('config.ini')
dirName = config['defaults']['DataFoldername']
columnStr = config['defaults']['SearchString']
delaytTime = config['defaults']['EndDelayTime']
delimmer = config['defaults']['delimiter']
distanceChar = config['defaults']['DistanceChar']

if delaytTime == "":
    delaytTime = 0
else:
    delaytTime = float(delaytTime)

################################################################################################################
# Fileopen Dialog :
tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
filename = askopenfilename()
if filename =="": 
    exit(0)
if os.path.exists(dirName) == False:
    print("Folder not exits !")
    exit(1)
################################################################################################################
# Distance split in km input
DistanceKM = input(distanceChar + "-Eingabe : ")
if DistanceKM == "":
    print('Keine Eingabe, Application wird beendet !')
    exit(1)
else:
    DistanceKM = int(DistanceKM)
    print('Your choice of distance : ', DistanceKM, " " + distanceChar)
################################################################################################################
################################################################################################################
# initializing variables:
basename_without_ext = os.path.splitext(os.path.basename(filename))[0]
# rewrite the path name to the subfolder inside the source data path
dirName = os.path.dirname(filename) + dirName
writefilename = ""
fields = []
rows = []
count = 0
discountcolm = 0
columnscount = 0
# m * multiplier = km
distanecsrec = int(DistanceKM) * 1000
distancesrec2 = distanecsrec
distancevalue = 0
distancecompare = 0
header = ""
################################################################################################################
# Start the application.
# create the subfolder, when not exists
if os.path.exists(dirName) == False:
   os.mkdir(dirName) 

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter = delimmer)
    # extracting field names through first row
    fields = next(csvreader)
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
    
    # get total number of rows
    print("Total no. of rows: %d" % (csvreader.line_num - 1))
# Read date now - start time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Start Time =", current_time)
# init. Process bar
bar = Bar('Processing', max=csvreader.line_num - 1)

# reading the columns-fields - from the headerline:
for field in fields:
    # Point it out, when the header row -> column includes the "search string", define upper!
    if fields[count] == columnStr:
        # set count result to const variable
        discountcolm = count
    count += 1
    columnscount = count - 1

# Distance calculation m to km
distanecsrec3 = int(distanecsrec / 1000)
# initial file1 variable
file1 = False
# Write resultat file name to the variable
writefilename = dirName + basename_without_ext + "_till_" + str(distanecsrec3) + "-" + distanceChar + ".csv"

# Reading rows
for row in rows:
    if os.path.isfile(writefilename) == False:
        # resultat file not exits - create file
        # and add headerline + first data row
        file1 = open(writefilename, 'a', newline='')
        if header == "":
           header = fields
           wirter = csv.writer(file1)
           wirter.writerow(fields)
           wirter.writerow(row)
    elif os.path.isfile(writefilename) == True: 
        # add data rows to resultat file
        wirter.writerow(row)
    # Read Value from search column (Header row), value in the row
    distancevalue = row[discountcolm]
    distancevalue = int(distancevalue)
    # When the reading value > than the steps value close the file within all lines before
    if distancevalue > distanecsrec:
       distancecompare = distancevalue / distanecsrec
       if distancecompare >= 1:
        distanecsrec = distanecsrec + distancesrec2
        file1.close()
        distanecsrec3 = int(distanecsrec / 1000)
        writefilename = dirName + basename_without_ext + "_till_" + str(distanecsrec3) + "-" + distanceChar + ".csv"
        header = ""
    # Process bar steps up
    bar.next()

bar.finish()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("End Time = ", current_time)
print("")

print("Done !", "You will finde the data-files in ", dirName)

MessageBox(None, 'Done, You will find the data-files in : ' + dirName + ' !', 'Information', WS_EX_TOPMOST)

print(delaytTime, ' seconds waiting for close !')
time.sleep(delaytTime)

exit(0)
