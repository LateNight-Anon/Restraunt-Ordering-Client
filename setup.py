from typing import List, Tuple
from csv import reader
from json import dump

#custom error classes
class userMisinputError(Exception): pass
class numCantBeFloatError(Exception): pass

def minAndMax() -> None:
    pass

def tablenumber() -> None:
    with open("tableNumber.csv", 'w') as file:
        num: int = None
        while True:
            try:
                num = input("input a table number: ")
                if '.' in num: raise numCantBeFloatError()
                if num < 0:
                    while True:
                        inp: str = input("do you really want to set a negative value: ").lower()
                        match inp:
                            case "yes": break
                            case "no": raise userMisinputError
            except ValueError: print("invalid input, input has to be an integer")
            except numCantBeFloatError: print("invalid input, number cant be a float")
            except userMisinputError: print("retrying input due to user error")
            else: break
        

def menu() -> None:
    pass

def main() -> None:
    userEntry: str = None
    while userEntry != "exit":
        userEntry = input("what values do you want to modify: ").lower()
        match userEntry:
            case "min/max": minAndMax()
            case "tablenumber": tablenumber()
            case "menu": menu()
            case "exit": print("goodbye")
            case _: print("invalid option")

if __name__ == "__main__":
    main()