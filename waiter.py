from tkinter import Tk, Button, Entry, Label
from threading import Thread
from json import load
from csv import reader
from typing import List, Dict

programIsRunning: bool = True

class table:
    def __init__(self, name: str, severityRating: int, callState: bool) -> None:
        self.tableName = name
        self.severity = severityRating
        if callState: self.col = "red"
        else: self.col = "green"
        self.isCalling = callState

def onClose() -> None:
    pass

def main() -> None:
    def getData() -> None:
        while programIsRunning:
            try: file = open("tables.json", 'r+')
            except FileNotFoundError: print('pussy')
            else:
                fileReader: dict = load(file)
                for key in fileReader.keys(): tables: List[Label] = [table("key", fileReader[key]["severity"], fileReader[key]["isCalling"])]
    app = Tk()
    app.title("waiter software")
    app.resizable(width = False, height = False)
    app.geometry("500x500")
    Label(text = "waiter software", font = ("Arial", 25)).pack()
    Thread(target = getData).start()

    app.mainloop()

if __name__ == "__main__": main()
