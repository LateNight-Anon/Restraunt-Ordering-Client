from tkinter import Tk, Button, Entry, Label, messagebox
from threading import Thread
from json import load, dumps
from csv import reader
from typing import List, Dict
from time import sleep

programIsRunning: bool = True

clearFile = lambda fileName: open(fileName, 'w').close() #abstraction to remove all contents from a specified file

class table:
    def __init__(self, name: str, severityRating: int, callState: bool) -> None:
        self.tableName = name
        self.severity = severityRating
        if callState: self.col = "red"
        else: self.col = "green"
        self.isCalling = callState

def jsonNotFound() -> None:
    global programIsRunning
    print("file tampering detected")
    programIsRunning = False
    exit()

def createError(txt: str) -> None: #shows the error message
    errLabel = Label(text = txt, font = ("Arial", 25), fg = "red")
    errLabel.place(x = 130, y = 750)
    sleep(1.5)
    errLabel.destroy()

def onClose() -> None: #terminates the getData loop and asks for confirmation when the app is closed
    global programIsRunning
    if messagebox.askquestion(title = "Do you really wish to close this window?", message = "Do you wish to close this app") == "yes":
        messagebox.showinfo(title = "App is closing!", message = "App is closing!")
        programIsRunning = False
        exit()

def tickOffCall(tableID: str) -> None: #accepts a tableID, removes a table call once served
    try: file = open("tables.json", 'r')
    except FileNotFoundError: jsonNotFound()
    else:
        with file:
            data: dict = load(file)
            if tableID not in tuple(data.keys()):
                Thread(target = createError, args = ("invalid table ID",)).start()
                return
            data[tableID]["isCalling"] = False
            data[tableID]["severity"] = 0
        clearFile("tables.json")
        with open("tables.json", 'a') as file: file.write(dumps(data))

def getData() -> None: #loads the json file and displays it on the screen
    while programIsRunning:
        try: file = open("tables.json", 'r')
        except FileNotFoundError: jsonNotFound()
        else:
            fileReader: dict = load(file)
            print(fileReader)
            tables: List[table] = [table(key, fileReader[key]["severity"], fileReader[key]["isCalling"]) for key in fileReader.keys()]
        tableLabels: List[Label] = []
        for i, tble in enumerate(tables): #tble is short for table
            print(tble.tableName)
            tableLabels.append(Label(text = "table ID: " + tble.tableName, font = ("Arial", 15), fg = tble.col))
            tableLabels[-1].place(x = 50, y = 50 + i * 95)
            tableLabels.append(Label(text = "severity: " + str(tble.severity), font = ("Arial", 15), fg = tble.col))
            tableLabels[-1].place(x = 50, y = 75 + i * 95)
        sleep(1)
        for i in range(len(tableLabels)): tableLabels[i].destroy()
        del tableLabels, tables, fileReader

app = Tk()
app.title("waiter software")
app.resizable(width = False, height = False)
app.geometry("500x1000")
app.protocol("WM_DELETE_WINDOW", onClose)
Label(text = "waiter software", font = ("Arial", 25)).pack()
Thread(target = getData).start()
enterTableName = Entry(font = ("Arial", 25), bg = "white", borderwidth = 3, relief = "solid")
enterTableName.place(x = 60, y = 800)
Button(text = "submit tick off", font = ("Arial", 20), bg = "tomato", borderwidth = 3, relief = "solid", command = lambda: tickOffCall(enterTableName.get())).place(x = 150, y = 875)

app.mainloop()
