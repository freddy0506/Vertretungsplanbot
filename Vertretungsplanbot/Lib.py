import requests
import os
from bs4 import BeautifulSoup as bs
import csv
from datetime import date
from datetime import datetime

today = date.today()
now = datetime.now()

global skip
skip = False

def Download():
    i = 0
    ErrorPa = False
    while(i < 10 and ErrorPa == False):
        i = i + 1
        #print(i)
        url = "http://www.inc-crm.de/typo3/fileadmin/1/subst_00" + str(i) + ".htm"
        r = requests.get(url, allow_redirects=True)
        wbstring = r.content
    
        open("Vertretungsplan" + str(i) + ".html", 'wb').write(r.content)
        if "leider ist ein Fehler aufgetreten" in str(wbstring):
            #print("n " + str(url))
            ErrorPa = True
            os.remove("Vertretungsplan" + str(i) + ".html")
        else:

            soup = bs(r.content, "html.parser")
            tdList = soup.find_all("td")
            #print(tdList)
            #for td in tdList:
                #print(td.get_text())

    return i


def HtmltoCsv(i, Year): 
    csvfile = open("Vertetungen.csv", "w")
    writer = csv.writer(csvfile, delimiter = ";")

    ReadFiles = 1

    
    while ReadFiles < (i):

        doc = open("Vertretungsplan" + str(ReadFiles) + ".html", "r", 1, "latin1").read()
        soup = bs(doc, "html.parser")

        DateHtml = soup.find_all("div")

        DateList = (DateHtml[0].get_text()).split("(")
        FullDate = DateList[0]

        DateList = DateList[0].split(str(Year))

        ShortDate = DateList[0]


        #OrdDatePath = "C:/Users/Frede/OneDrive/Dokumente/Vertretungspläne" + str(FullDate)
        #if not os.path.exists(OrdDatePath):
        #    os.mkdir(OrdDatePath)


        tdList = soup.find_all("td")

        Vertretung = []
        Vertretungen = []

        tdText = ""
        VertretungenExist = True
        DatePos = 0
        
        while(tdList[DatePos].get_text() != ShortDate):
            DatePos += 1
            if len(tdList) <= (DatePos + 5):
                VertretungenExist = False
                break

        if VertretungenExist:
            #print(doc)
            for td in tdList[DatePos:]:
                tdText = td.get_text()
    
                if tdText == ShortDate:
                    writer.writerow(Vertretung)
        
                    Vertretung.clear()

                    Vertretung.append(tdText)
                else:
                    Vertretung.append(tdText)
    
            writer.writerow(Vertretung)

        ReadFiles += 1



def classswitcher(Klasse):
    options = {
        "5a" : "05a",
        "5b" : "05b",
        "5c" : "05c",
        "5d" : "05d",
        "5e" : "05e",
        "6a" : "06a",
        "6b" : "06b",
        "6c" : "06c",
        "6d" : "06d",
        "6e" : "06e",
        "7a" : "07a",
        "7b" : "07b",
        "7c" : "07c",
        "7d" : "07d",
        "7e" : "07e",
        "8a" : "08a",
        "8b" : "08b",
        "8c" : "08c",
        "8d" : "08d",
        "8e" : "08e",
        "9a" : "09a",
        "9b" : "09b",
        "9c" : "09c",
        "9d" : "09d",
        "9e" : "09e",
        "ef" : "EF",
        "q1" : "Q1",
        "q2" : "Q2"
    }
    return options.get(Klasse, "Invalid Klasse")


def AskClass():
        print("In welcher Klasse sind sie? (5a/5b/5c/5d/6a/6b/6c/6d/7a/7b/7c/7d/8a/8b/8c/8d/9a/9b/9c/9d/EF/Q1/Q2)")
        Schoolclass = input("Klasse: ")
        Schoolclass = Schoolclass.lower()
        Schoolclass = classswitcher(Schoolclass)
    
        while Schoolclass == "Invalid Klasse":
            
            print("Diese Klasse existiert nicht")

            print("In welcher Klasse sind sie? (5a/5b/5c/5d/6a/6b/6c/6d/7a/7b/7c/7d/8a/8b/8c/8d/9a/9b/9c/9d/EF/Q1/Q2)")
            Schoolclass = input("Klasse: ")
            Schoolclass = Schoolclass.lower()
            Schoolclass = classswitcher(Schoolclass)
            
    
        Schoolclass = Schoolclass.upper()
        return Schoolclass


def NumWeekday (WeekdayNum):
    switcher = {
        0 : "Montag",
        1 : "Dienstag",
        2 : "Mittwoch",
        3 : "Donnerstag",
        4 : "Freitag",
        5 : "Samstag",
        6 : "Sonntag"
        }
    return switcher.get(WeekdayNum, "Why is it invalid????? Dafuq")

def monthDays(month):
    switcher = {
        0 : 31,
        1 : 28,
        2 : 31,
        3 : 30,
        4 : 31,
        5 : 30,
        6 : 31,
        7 : 31,
        8 : 30,
        9 : 31,
        10 : 30,
        11 : 31,
        }
    return switcher.get(month, -1)


def getDate():
    WeekdayNum = today.weekday()
    
    Weekday = NumWeekday(WeekdayNum)

    Date = today.strftime("%d.%m.")

    Year = "20" + today.strftime("%y")

    return Date, Weekday, Year

def reloadtime(Break):


    current_minute = now.strftime("%M")
    if int(current_minute)%Break == 0:
        return True
    else:
        return False

def checkday(nextdayTime):
    curhour = int(now.strftime("%H"))
    weekday = today.weekday()
    print(weekday)

    if curhour >= nextdayTime:
        return True
    elif weekday >= 4:
        return True
    else:
        return False

def addDay(Date):
    weekday = today.weekday()
    dateList = Date.split(".")
    daymonth = monthDays(int(dateList[1]))
    
    if weekday == 4:
        daytoAdd = 3
    elif weekday == 5:
        daytoAdd = 2
    else:
        daytoAdd = 1

    dateList[0] = int(dateList[0]) + daytoAdd

    if int(dateList[0]) > daymonth:
        dateList[0] = int(dateList[0]) - daymonth
        dateList[1] = int(dateList[1]) + 1
    Date = str(dateList[0]) + "." + str(dateList[1]) + "."
    return Date
    

def isDateReal(Date):
    wrongDate = False
    dateList = Date.split(".")
    if int(dateList[0]) > 31:
        wrongDate = True
    if int(dateList[1]) > 12:
        wrongDate = True
    return wrongDate

def readInfofile(path):

    Error = False

    infoFile = open(path + "Informationen.csv", "r")
    infoReader = csv.reader(infoFile, delimiter = ";")

    for row in infoReader:
        if len(row) > 0:
            #print(row)
            if row[0] == "Klasse" and row[1] != "":
                Schoolclass = row[1].lower()
                Schoolclass = classswitcher(Schoolclass)
            
                if Schoolclass == "Invalid Klasse":
                    print("Die Klasse sie du aufgeschriebern hast existiert nicht")
                    Error = True

                Schoolclass = Schoolclass.upper()

            elif row[0] == "Tag" and row[1] != "":
                if row[1] == "Heute":
                    FormDate = today.strftime("%d.%m.")
                else:
                    FormDate = row[1]
            elif row[0] == "Kurse" and row[1] != "":
                kursList = row

    infoFile.close()

    while isDateReal(FormDate):
        print("Das Datum das sie angegeben hat existiert nicht!")
        FormDate = input("Bitte geben sie ein anderes Datum an: ")

    if Error == True:
        AskClass()

    return Schoolclass, FormDate


#print("Vertretungen für den " + FormDate + today.strftime("%y"))
#print("")

def searchVertretungen(Schoolclass, FormDate, path):
    global skip
    csvfile = open("Vertetungen.csv", "r")
    reader = csv.reader(csvfile, delimiter = ";")
    
        if skip == True:
            os.mkdir(classPath)

        while skip == False:
            create = input("Create New Directory in " + path + " (y/n)")
            if create == "y" or create == "Y":
                os.mkdir(classPath)
                skip = True
            elif create == "n" or create == "N":
                print("Stopping...")
                skip = True
            else:
                print("invalid answer")
                skip = False
    
    verToday = open(path + Schoolclass + "/" + "Vertetungen_Heute.csv", "w")
    todaywriter = csv.writer(verToday, delimiter = ";")

    Schoolclass = Schoolclass.lower()
    Schoolclass = classswitcher(Schoolclass)
    Schoolclass = Schoolclass.upper()

    for row in reader:
        if len(row) > 0:
            item = 0
            while item < len(row):
                if row[item] == "\xa0":
                    row[item] = ""
                item += 1
            if Schoolclass != "EF" and Schoolclass != "Q1" and Schoolclass != "Q2":
                isyear = row[1].find(Schoolclass[0:2])
                isclass = row[1].find(Schoolclass[2])
            else:
                isyear = isclass = row[1].find(Schoolclass)
            #print(str(isyear) + "  " + str(isclass))
            if(row[0] == FormDate and isclass >= 0 and isyear >= 0):
                print(row)
                todaywriter.writerow(row)

    csvfile.close()
    verToday.close()


def writeInHtml(Schoolclass, FormDate, Weekday, path):

    csvfile = open(path + Schoolclass + "/" + "Vertetungen_Heute.csv", "r", 1, "latin1")
    todayReader = csv.reader(csvfile, delimiter = ";")

    writetabelle = False

    with open(path + Schoolclass + "/" + "index.html", "w", 1, "latin1") as htmlF:
        with open("Vertretungvorlage.html", "r", 1, "latin1") as htmlVorlage:
                todayReader = csv.reader(csvfile, delimiter = ";")
                lineNum = 0
                for line in htmlVorlage:
            
                    if line[0:11] == '<div </div>':
                        htmlF.write('<div class="mon_title">' + FormDate + '2020 ' + Weekday + '</div>')

                    if line[0:66] == '<th class="list" align="center"><b>Klasse</b></th><th class="list"':
                        htmlF.write(line)
                        writetabelle = True
                    elif writetabelle == True:
                        for row in todayReader:
                            if row != []:
                                #print(row[8])
                                if row[8] == "eigenv. Arbeiten" or row[8] == "Entfall":
                                    htmlF.write('<tr style = "background: #ec2c2c" >')
                                    #print("Rot")
                                elif row[8] == "Vertretung":
                                    htmlF.write('<tr style = "background: #fbff00" >')
                                    #print("Gelb")
                                elif row[8] == "Sondereins.":
                                    htmlF.write('<tr style = "background: #faaf2d" >')
                                    #print("Orange")
                                elif row[8] == "Raum-Vtr.":
                                    htmlF.write('<tr style = "background: #5356fc" >')
                                    #print("Gelb")
                                else:
                                    htmlF.write('<tr style = "background: #ffffff" >')
                                    #print("Weiß")
    

                                itemNum = 0

            
                                for item in row:
                                    if itemNum >= 10:
                                        newrow = False
                                        break

                                    itemNum += 1
                                    htmlF.write('<td class="list" align="center"><strong>' + str(item) + '</strong></td>')
                                    #htmlF.write('<td class="list" align="center"><strong>' + item + '</strong></td>')
                                    #print(item)
                                    newrow = True
    
    
                                htmlF.write("</tr>")

                                #print("")
                            
                                lineNum += 1
                        writetabelle = False
                    else:
                        htmlF.write(line)
                        #print(line)
                        lineNum += 1
    csvfile.close()

def sortAllClass(posClasses, FormDate, path):

    for Class in posClasses:
        searchVertretungen(Class, FormDate, path)

def writeAll( Date, Weekday, posClasses, path):
    for Class in posClasses:
        writeInHtml(Class, Date, Weekday, path)

