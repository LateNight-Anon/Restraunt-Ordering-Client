from tkinter import Tk, Label, Button, Entry, Text, Canvas, PhotoImage, NW, Frame, BOTH, messagebox
from threading import Thread
from multiprocessing import Process
from typing import List, Tuple, Dict
from csv import reader
from json import *
from time import sleep
from PIL import Image, ImageTk
from os import environ #os is exclusively used for stopping the pygame welcome message
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #stops the pygame welcome message from printing
from pygame import mixer

class cartItem: #this class is the template for how items are stored in the users cart list
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price

class menuItem: #this class is the template for the sections where you add items to your cart
    def __init__(self, name: str, ingredients: Tuple[str], price: int) -> None: #price as integer of cents
        self.count = 0
        self.name = name
        self.ingredients = ingredients
        self.price = price

class tempButton(Button): #this exists because winfo_rootx gives me the wrong values constantly
    realX: int = None
    realY: int = None

    def assignRealPosition(self, x: int, y: int) -> None:
        self.realX = x
        self.realY = y
    
    def grabRealPos(self) -> List[int]: return [self.realX, self.realY]

class tempLabel(Label): #this exists because winfo_rootx gives me the wrong values constantly
    realX: int = None
    realY: int = None

    def assignRealPosition(self, x: int, y: int) -> None:
        self.realX = x
        self.realY = y
    
    def grabRealPos(self) -> List[int]: return [self.realX, self.realY]

#one liner abstractions over dumb function / methods
playSound = lambda: mixer.music.play() #abstraction over mixer.music.play that turns it into a simple playSound() function
clearFile = lambda fileName: open(fileName, 'w').close() #abstraction to remove all contents from a specified file

tableNumber: int = None

def fatalError(errorID: str) -> None:
    messagebox.showinfo(title = "fatal error", message = "fatal error detected\ncontact admins with error code\nerrorCode: " + errorID)
    exit()

def closeMainWindow() -> None: #function that runs when window is closed that adds a confirmation box
    messageBoxText: str = ""
    try: file = open("closeMessage.txt", 'r')
    except FileNotFoundError: messageBoxText = "[INVALID / MISSING FILE DETECTED]"
    else: messageBoxText = "".join((item if item not in ('{', '}') else '') for item in next(reader(file)))
    if messagebox.askquestion(title = "Do you really wish to close this window?", message = messageBoxText) == "yes":
        messagebox.showinfo(title = "App is closing!", message = "App is closing!")
        exit()

def createErrorMessage(master: Tk, msg: str, fontSize: int, xPos: int, yPos: int) -> None:
    errLabel = Label(master, text = msg, font = ("Arial", fontSize), fg = "red")
    errLabel.place(x = xPos, y = yPos)
    [playSound(), sleep(2), errLabel.destroy()]

def deleteItem(name: str, cart: List[str]) -> None: #removes item from users cart
    for i, item in enumerate(cart):
        if item.name == name: 
            userCart.pop(i)
            return
    Thread(target = createErrorMessage, args = (app, "you dont have any of this item", 25, 0, 130)).start()

def getTotalOfCartAndAssign(cart: List[cartItem]) -> None:
    value: float = sum(item.price for item in cart) / 100
    cartTotalLabel.configure(text = '$' + str(value))
    if value > 0: payTabButton.configure(bg = "SeaGreen2")
    else: payTabButton.configure(bg = "tomato")

getTotalOfCart = lambda cart: sum(item.price for item in cart) / 100 #returns sum of all items in the users cart

def parseArrToStr(item: List[str]) -> List[str]: #turns a list of items into a string of text i.e inputting [1, 2, 3] returns "1, 2, 3"
    endResult: str = ""
    for i, string in enumerate(item): 
        if i == len(item) - 1: endResult += string
        else: endResult += string + ', '
    return endResult

countOfXItemsInArrY = lambda X, Y: sum(1 for i in Y if i == X)

def createPayWindow(cost: float) -> None:
    global cardLabel, cashLabel, soulLabel, addPaymentButton
    listOfPaymentTypes: List[chr] = [] #c = credit / debit card. p = physical cash. b = babies souls 

    def assignAddPaymentButton() -> None:
        global addPaymentButton
        addPaymentButton = Button(payWindow, text = "add payment method", font = ("Arial", 25), bg = "grey77", borderwidth = 3, relief = "solid", command = createPaymentMethodSelection)
        addPaymentButton.place(x = 90, y = 200)

    def addPaymentSplitLabels() -> None:
        def addCardLabel(col: str) -> None:
            global cardLabel
            cardLabel = Label(payWindow, text = "amount of credit / debit cards used:  " + str(countOfXItemsInArrY('c', listOfPaymentTypes)), font = ("Arial", 15), fg = col)
            cardLabel.place(x = 75, y = 400)
        
        def addCashLabel(col: str) -> None:
            global cashLabel
            cashLabel = Label(payWindow, text = "amount of seperate sums of cash used:  " + str(countOfXItemsInArrY('p', listOfPaymentTypes)), font = ("Arial", 15), fg = col)
            cashLabel.place(x = 75, y = 450)

        def addSoulLabel(col: str) -> None:
            global soulLabel
            soulLabel = Label(payWindow, text = "amount of baby souls used: " + str(countOfXItemsInArrY('b', listOfPaymentTypes)), font = ("Arial", 15), fg = col)
            soulLabel.place(x = 75, y = 500)

        if 'c' in listOfPaymentTypes: addCardLabel("red")
        else: addCardLabel("green")
        if 'p' in listOfPaymentTypes: addCashLabel("red")
        else: addCashLabel("green")
        if 'b' in listOfPaymentTypes: addSoulLabel("red")
        else: addSoulLabel("green")

    def createPaymentMethodSelection() -> None:
        global cardLabel, cashLabel, soulLabel
        def addPaymentMethod(method: chr) -> None:
            listOfPaymentTypes.append(method)
            [addCreditCard.destroy(), addCash.destroy(), addTheSoulsOfInfants.destroy()]
            [assignAddPaymentButton(), addPaymentSplitLabels()]

        [cardLabel.destroy(), cashLabel.destroy(), soulLabel.destroy()]
        addPaymentButton.destroy()
        addCreditCard = Button(payWindow, text = "add a credit / debit card", font = ("Arial", 25), bg = "LavenderBlush2", borderwidth = 3, relief = "solid", command = lambda: addPaymentMethod('c'))
        addCreditCard.place(x = 75, y = 200)
        addCash = Button(payWindow, text = "add a blob of dollars", font = ("Arial", 25), bg = "LavenderBlush2", borderwidth = 3, relief = "solid", command = lambda: addPaymentMethod('p'))
        addCash.place(x = 100, y = 300)
        addTheSoulsOfInfants = Button(payWindow, text = "add an infants soul", font = ("Arial", 25), bg = "LavenderBlush2", borderwidth = 3, relief = "solid", command = lambda: addPaymentMethod('b'))
        addTheSoulsOfInfants.place(x = 107, y = 400)

    def onWindowClose() -> None:
        global payWindowIsOpen
        payWindowIsOpen = False
        payWindow.destroy()

    global payWindowIsOpen
    if not payWindowIsOpen:
        if cost > 0:
            payWindowIsOpen = True
            payWindow = Tk()
            payWindow.title("pay for your meal")
            payWindow.geometry("500x800")
            payWindow.resizable(width = False, height = False)
            payWindow.protocol('WM_DELETE_WINDOW', onWindowClose)
            Label(payWindow, text = "pay your bill", font = ("Arial", 25)).pack()    
            costLabel = Label(payWindow, text = 'you need to pay $' + str(cost / 100), font = ("Arial", 25))
            costLabel.place(x = 150 - 12 * len(str(cost)), y = 120) #math is used to center text
            [assignAddPaymentButton(), addPaymentSplitLabels()]
            submitPaymentButton = Button(text = "submit payment", bg = "tomato", font = ("Arial", 15))
            submitPaymentButton

            payWindow.mainloop()
        else: Thread(target = createErrorMessage, args = (app, "you cant pay for an empty cart", 20, 0, 130)).start()
    else: Thread(target = createErrorMessage, args = (app, "this window is already open", 20, 0, 130)).start()

def createCallWindow() -> None: #creates and contains functionality for the menu that lets you call a window
    def submitCall(severity: int, table: int) -> None: 
        try: 
            file = open("tables.json", 'r')
            #open file containing the minimum an maximum severity ratings and assigns them to vars
            minAndMaxReader = next(reader(open("MinAndMaxSev.csv", 'r')))
            minSev: int = int(minAndMaxReader[0])
            maxSev: int = int(minAndMaxReader[1])
            del minAndMaxReader
            if int(severity) < minSev or int(severity) > maxSev: raise ValueError()
        except FileNotFoundError: fatalError("001")
        except ValueError: Thread(target = createErrorMessage, args = (callApp, "input a severity rating between " + str(minSev) + " and " + str(maxSev), 15, 75, 300)).start()
        else:
            with file:
                fileReader = load(file)
                fileReader["table" + str(table)]["severity"] = severity
                fileReader["table" + str(table)]["isCalling"] = True
                #for some reason it is strictly neccesary to remove all data from tables.json then append to it instead of writing as that creates an error
                clearFile("tables.json")
            with open("tables.json", 'a') as file: file.write(dumps(fileReader))

    def readNumberFromCsv() -> int: #reads the softwares assigned table number
        try: file = open("tableNumber.csv", 'r')
        except FileNotFoundError: fatalError("002")
        except ValueError: fatalError("003")
        else:
            with file: return int(next(reader(file))[0])

    def onWindowClose() -> None:
        global waiterWindowIsOpen
        waiterWindowIsOpen = False
        callApp.destroy()

    global waiterWindowIsOpen
    if not waiterWindowIsOpen:
        waiterWindowIsOpen = True
        callApp = Tk()
        callApp.title("call a waiter to your table")
        callApp.geometry("500x800")
        callApp.protocol('WM_DELETE_WINDOW', onWindowClose)
        Label(callApp, text = "call a waiter", font = ("Arial", 25)).pack()
        tableNumber: int = readNumberFromCsv()
        Label(callApp, text = "you're on table " + str(tableNumber), font = ("Arial", 10)).place(x = 200, y = 60)
        severityEntry = Entry(callApp, font = ("Arial", 35), borderwidth = 3, relief = "solid", width = 6)
        severityEntry.place(x = 165, y = 230)
        Button(callApp, text = "call a waiter", font = ("Arial", 25), bg = "grey", borderwidth = 3, relief = "solid", command = lambda: submitCall(severityEntry.get(), tableNumber)).place(x = 150, y = 120)
        
        callApp.mainloop()
    else: Thread(target = createErrorMessage, args = (app, "this window is already open", 20, 0, 130)).start()

def createBathroomWindow() -> None:
    def onWindowClose() -> None:
        global bathroomWindowIsOpen
        bathroomWindowIsOpenWindow = False
        bathroomApp.destroy()

    global bathroomWindowIsOpen
    if not bathroomWindowIsOpen:
        bathroomApp = Tk()
        bathroomApp.title("Map to the Bathroom")
        bathroomApp.geometry("800x800")
        bathroomApp.resizable(width = False, height = False)
        canvas = Canvas(bathroomApp, width = 800, height = 800)
        Label(bathroomApp, text = "bathroom map", font = ("Arial", 25)).place(x = 330, y = 40)
        canvas.create_rectangle(100, 100, 250, 150, fill = "grey76")
        canvas.create_rectangle(450, 450, 550, 550, fill = "grey76")
        canvas.create_line(150, 170, 505, 430, dash = (5, 2))
        Label(bathroomApp, text = "YOU!!1", font = ("Arial", 15), bg = "grey76").place(x = 120, y = 120)
        Label(bathroomApp, text = "barthroomba!", font = ("Arial", 15), bg = "grey76").place(x = 435, y = 470)

        bathroomApp.mainloop()
    else: Thread(target = createErrorMessage, args = (app, "this window is already open", 20, 0, 130)).start()

def moveObjectsOnCanvas(canvValue: int, widValue: int) -> None:
    def moveStandardWidget(index: int) -> None:
        cords: List[int] = listOfObjectsOnCanvas[index].grabRealPos()
        xPos: int = cords[0]
        yPos: int = cords[1]
        del cords
        listOfObjectsOnCanvas[index].place(x = xPos, y = yPos + widValue)
        listOfObjectsOnCanvas[index].assignRealPosition(xPos, yPos + widValue)

    for i in range(len(listOfObjectsOnCanvas)):
        match str(type(listOfObjectsOnCanvas[i])):
            case "<class 'int'>": 
                cords: List[float] = canvas.coords(listOfObjectsOnCanvas[i])
                canvas.moveto(listOfObjectsOnCanvas[i], 100, cords[1] + canvValue)
            case "<class '__main__.tempLabel'>": moveStandardWidget(i)
            case "<class '__main__.tempButton'>": moveStandardWidget(i)
            case _: [fatalError("004"), exit()]

#create boolean values that represent if a window is open

global payWindowIsOpen, bathroomWindowIsOpen, waiterWindowIsOpen
payWindowIsOpen = bathroomWindowIsOpen = waiterWindowIsOpen = False

#create window basics

app = Tk()
app.title("Restraunt Ordering Terminal")
app.geometry("800x800")
app.resizable(width = False, height = False)
app.protocol("WM_DELETE_WINDOW", closeMainWindow)
Button(text = 'X', font = ("Arial", 25), borderwidth = 3, relief = "solid", bg = "red", command = closeMainWindow).place(x = 745, y = 729)
canvas = Canvas(width = 800, height = 800)
Label(text = "$               $", font = ("Arial", 25), fg = "green").place(x = 305, y = 60)
Label(text = "welcome", font = ("Arial", 35)).pack()
Button(text = "bathroom", font = ("Arial", 25), borderwidth = 3, relief = "solid", bg = "grey", command = createBathroomWindow).place(x = 10, y = 10)
Button(text = "call a waiter", font = ("Arial", 25), borderwidth = 3, relief = "solid", bg = "grey", command = createCallWindow).place(x = 580, y = 10)
payTabButton = Button(text = "pay your tab", font = ("Arial", 15), borderwidth = 3, relief = "solid", bg = "tomato", command = lambda: createPayWindow(sum(item.price for item in userCart)))
payTabButton.place(x = 332, y = 60)
cartTotalLabel = Label(text = "$0.00", font = ("Arial", 25))
cartTotalLabel.place(x = 10, y = 80)

cartTotal: int = 0
userCart: List[cartItem] = []

#open menu list

try: file = open("foodItems.json", 'r')
except FileNotFoundError: fatalError("005")
else:
    with file:
        fileReader = load(file)
        listOfItems: Tuple[Dict[List[str] , int | str]] = (fileReader[key] for key in fileReader.keys())

#use menu list to generate odering UI

interactiveItems: List[Dict[str, list | str]] = [menuItem(fileReader[key]["name"], fileReader[key]["ingredients"], fileReader[key]["price"]) for key in fileReader.keys()]
listOfObjectsOnCanvas : List[Label | Button] = [] #this exists so that all the objects can be moved

def placeButton() -> None: #made its own function for readability
    def addButtons(pos: int, itemName: str, itemPrice: int, userCart: List[cartItem]) -> None: #split into a function as directly making them in the loop created errors possibly from pointers
        listOfObjectsOnCanvas.append(tempButton(text = '+', font = ("Arial", 10), bg = "green", borderwidth = 1, relief = "solid", command = lambda: [userCart.append(cartItem(itemName, itemPrice)), getTotalOfCartAndAssign(userCart)]))
        listOfObjectsOnCanvas[-1].place(x = 370, y = drawCanvasYPos + 180)
        listOfObjectsOnCanvas[-1].assignRealPosition(370, drawCanvasYPos + 180)
        listOfObjectsOnCanvas.append(tempButton(text = '-', font = ("Arial", 10), bg = "red", borderwidth = 1, relief = "solid", command = lambda: Thread(target = lambda: [deleteItem(itemName, userCart), getTotalOfCartAndAssign(userCart)]).start()))
        listOfObjectsOnCanvas[-1].place(x = 340, y = drawCanvasYPos + 180)
        listOfObjectsOnCanvas[-1].assignRealPosition(340, drawCanvasYPos + 180)

    def addIngredientsLabel(wrapVar: int) -> None:
        listOfObjectsOnCanvas.append(tempLabel(text = ingredientsAsStr, font = ("Arial", 10), wraplength = 235))
        listOfObjectsOnCanvas[-1].place(x = 110, y = drawCanvasYPos + 155)
        listOfObjectsOnCanvas[-1].assignRealPosition(110, drawCanvasYPos + 155)

    drawCanvasYPos: int = 50
    for i, item in enumerate(interactiveItems):
        drawCanvasYPos += 100
        listOfObjectsOnCanvas.append(canvas.create_rectangle(100, drawCanvasYPos, 400, drawCanvasYPos + 100, outline = "black"))
        listOfObjectsOnCanvas.append(tempLabel(text = item.name, font = ("Arial", 15)))
        listOfObjectsOnCanvas[-1].place(x = 110, y = drawCanvasYPos + 125)
        listOfObjectsOnCanvas[-1].assignRealPosition(110, drawCanvasYPos + 125)
        ingredientsAsStr: str = parseArrToStr(item.ingredients)
        if len(ingredientsAsStr) < 25: addIngredientsLabel(800)
        else: addIngredientsLabel(235)
        listOfObjectsOnCanvas.append(tempLabel(text = str(item.price / 100) + " $", font = ("Arial", 10)))
        listOfObjectsOnCanvas[-1].place(x = 400 - len(str(item.price / 100)) * 10, y = drawCanvasYPos + 130)
        listOfObjectsOnCanvas[-1].assignRealPosition(400 - len(str(item.price / 100) * 10), drawCanvasYPos + 130)
        addButtons(drawCanvasYPos, item.name, item.price, userCart)
        drawCanvasYPos += 10
    canvas.place(x = 0, y = 120)
placeButton()

#add scroll buttons

Button(text = "↑", font = ("Arial", 35), bg = "grey", borderwidth = 3, relief = "solid", command = lambda: moveObjectsOnCanvas(-10, -9)).place(x = 500, y = 380)
Button(text = "↓", font = ("Arial", 35), bg = "grey", borderwidth = 3, relief = "solid", command = lambda: moveObjectsOnCanvas(10, 11)).place(x = 500, y = 520)

#load audio with pygames mixer object

[mixer.init(), mixer.music.load("bleep.mp3")]

#setup keybindings for scrolling

app.bind("<Up>", lambda event: moveObjectsOnCanvas(-10, -9))
app.bind("<Down>", lambda event: moveObjectsOnCanvas(10, 11)) 

app.mainloop()
