# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from periodictable import *
from periodicDict import periodicMasses
from ui_moleConvert import Ui_MainWindow

# checks if a number can be made a float
def checkFloat(num):
    print "checkFloat triggered"
    num = eval(num)
    try:
        float(num)
        return True
    except ValueError:
        return False

# Checks if a character is an int
def checkInt(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


components = []
unitList = []
totalMass = 0
elementNum = 0

grams = 0
moles = 0
units = 0
atoms = 0
amount = 0
mass = 0

# Breaks up formula into elements and subscripts
def allClear():
    global components
    global unitList
    global totalMass
    global elementNum
    global amount
    global mass
    components = []
    unitList = []
    totalMass = 0
    elementNum = 0
    amount = 0
    mass = 0


# parses the formula into separate elements
def formulaParse(formula):
    global components
    checkNum = ''
    element = ''
    # Separates the element symbols and subscripts
    for x in range(0, len(formula)):
        i = formula[x]
        # Finds subscripts and appends them to the components list
        if checkInt(i):
            components.append(i)
            element = ''
        # Finds element symbols and appends them to the components list
        else:
            # Checks if current character is uppercase; if so, do necessary actions
            if i == i.upper():
                element += str(i)
                if len(formula) == 1:
                    components.append(i)
                elif x + 1 >= len(formula):
                    components.append(i)
                # Checks to see if the next character is a number or lowercase letter
                elif not checkInt(i):
                    if checkInt(formula[x + 1]) or formula[x + 1] == formula[x + 1].upper():
                        components.append(i)
                    else:
                        pass
                else:
                    pass
            # If the current character is lowercase, append it to element and append element to components list
            elif i == i.lower():
                element += str(i)
                components.append(element)
                element = ''
            else:
                pass
    # Checks for invalid element symbols
    for i in components:
        if checkInt(i):
            pass
        elif i not in periodicMasses.keys():
            components = []
            return False
        else:
            pass
    # Stores the formula in checkNum
    for i in components:
        checkNum += i
    # Checks if the formula entered is only numbers and invalid
    if checkInt(checkNum):
        components = []
        return False
    else:
        pass
    # Checks for blank formula input
    if formula == '':
        return False
    else: pass
    print components


# Properly splits up element symbols and subscripts
def componentsParse():
    global unitList
    numLength = 0
    num = ''
    correctIndex = 0
    repeat = False
    for x in range(0, len(components)):
        print("correctIndex: " + str(correctIndex))
        # Ensures no repeated numbers are appended to the list
        if repeat == True and x < len(components):
            correctIndex += numLength
            numLength = 0
            repeat = False
        else:
            if correctIndex < len(components):
                i = components[correctIndex]
            else:
                print unitList
                return
            # Appends symbols and subscripts as separate units into unitList
            if not checkInt(i):
                unitList.append(i)
            elif checkInt(i):
                num += i
                if correctIndex + 1 >= len(components):
                    unitList.append(num)
                    num = ''
                    #Assists in preventing double appending of certain numbers
                elif checkInt(components[correctIndex + 1]):
                    oneMore = correctIndex + 1
                    while oneMore < len(components) and checkInt(components[oneMore]):
                        num += components[oneMore]
                        numLength += 1
                        oneMore += 1
                    unitList.append(num)
                    repeat = True
                    num = ''
                elif not checkInt(components[correctIndex + 1]):
                    unitList.append(num)
                    num = ''
                else:
                    pass
            else:
                pass
            correctIndex += 1
    print unitList


# Calculates the atomic mass of the formula
def massCalc():
    global totalMass
    # Calculates the mass of the formula
    for x in range(0, len(unitList)):
        i = unitList[x]
        if checkInt(i):
            pass
        else:
            if x + 1 >= len(unitList):
                mass = periodicMasses[i]
                totalMass += mass
            else:
                mass = periodicMasses[i]
                if checkInt(unitList[x + 1]):
                    mass *= int(unitList[x + 1])
                else:
                    pass
                totalMass += mass


# Counts the total number of elements
def elementCount():
    global elementNum
    for x in range(0, len(unitList)):
        i = unitList[x]
        if checkInt(i):
            elementNum += int(i)
        else:
            if x + 1 >= len(unitList):
                elementNum += 1
            else:
                if not checkInt(i):
                    if checkInt(unitList[x + 1]):
                        pass
                    else:
                        elementNum += 1


# Converts a given gram value to mole value
def gramsToMoles():
    global amount
    global mass
    global moles
    moles = float(amount) / mass


# Converts given mole value to gram value
def molesToGrams():
    global amount
    global mass
    global grams
    global moles
    grams = float(moles) * mass


# Converts given mole value to unit value
def molesToUnits():
    global units
    units = float(moles) * (6.022 * 10 ** 23)


# Converts given unit value to Mole value
def unitsToMoles():
    global amount
    global moles
    moles = float(units) / (6.022 * 10 ** 23)


# Converts given unit value to atom value
def unitsToAtoms():
    global atoms
    print elementNum
    atoms = float(units) * elementNum
    print atoms


# Converts given atom value to unit value
def atomsToUnits():
    global amount
    global units
    units = float(amount) / elementNum


# Solves for all cases when a gram value is given
def gramsSolver(unit, chemFormula):
    # Ensures no same-value conversions
    if unit == 'Grams':
        return "Can't convert to same unit"
    elif unit == 'Moles':
        gramsToMoles()
        print mass
        return str(moles) + ' moles of ' + str(chemFormula)
    elif unit == 'Molecules':
        gramsToMoles()
        molesToUnits()
        return str(units) + ' units/molecules of ' + str(chemFormula)
    elif unit == 'Atoms':
        gramsToMoles()
        molesToUnits()
        unitsToAtoms()
        return str(atoms) +' atoms in ' + str(chemFormula)
    else:
        pass


# Solves for all cases when a mole value is given
def molesSolver(unit, chemFormula):
    global amount
    global grams
    global moles
    global units
    global atoms
    # Ensures no same-value conversions
    if unit == "Moles":
        return "Can't convert to same unit"
    elif unit == "Grams":
        moles = amount
        molesToGrams()
        return str(grams) + ' grams of ' + str(chemFormula)
    elif unit == "Molecules":
        moles = amount
        molesToUnits()
        return str(units) + ' units/molecules of ' + str(chemFormula)
    elif unit == "Atoms":
        moles = amount
        molesToUnits()
        unitsToAtoms()
        return str(atoms) + " atoms of " + str(chemFormula)
    else:
        pass


# Solves for all cases when a unit value is given
def unitsSolver(unit, chemFormula):
    global amount
    global grams
    global moles
    global units
    global atoms
    # Ensures no same-value conversions
    if unit == "Molecules":
        return "Can't convert to same unit"
    elif unit == "Grams":
        units = amount
        unitsToMoles()
        molesToGrams()
        return str(grams) + " grams of " + str(chemFormula)
    elif unit == "Moles":
        units = amount
        unitsToMoles()
        return str(moles) + " moles of " + str(chemFormula)
    elif unit == "Atoms":
        units = amount
        unitsToAtoms()
        return str(atoms) + " atoms of " + str(chemFormula)
    else:
        pass


# Solves for all cases when a atom value is given
def atomsSolver(unit, chemFormula):
    # Ensures no same-value conversions
    if unit == "Atoms":
        return "Can't convert to same unit"
    elif unit == "Molecules":
        atomsToUnits()
        return str(units) + " units of " + str(chemFormula)
    elif unit == "Moles":
        atomsToUnits()
        unitsToMoles()
        return str(moles) + " moles of " + str(chemFormula)
    elif unit == "Grams":
        atomsToUnits()
        unitsToMoles()
        molesToGrams()
        return str(grams) + " grams of " + str(chemFormula)
    else:
        pass

# Calls appropriate functions to derive final answer
def solve(amt, chemFormula, unitOne, unitTwo):
    global components
    global unitList
    global totalMass
    global elementNum
    global amount
    global mass
    if checkFloat(amt):
        if formulaParse(chemFormula) == False:
            allClear()
            return "Check your elements"
        else:
            componentsParse()
            massCalc()
            elementCount()
            amount = eval(amt)
            mass = totalMass
            if unitOne == 'Grams':
                answer = gramsSolver(unitTwo, chemFormula)
                allClear()
                return answer
            elif unitOne == 'Moles':
                answer = molesSolver(unitTwo, chemFormula)
                allClear()
                return answer
            elif unitOne == 'Molecules':
                answer = unitsSolver(unitTwo, chemFormula)
                allClear()
                return answer
            elif unitOne == 'Atoms':
                answer = atomsSolver(unitTwo, chemFormula)
                allClear()
                return answer
            else:
                pass
    else:
        allClear()
        return "Check your numbers"



# Qt GUI handling
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pressGo()

    def pressGo(self):
        self.pushButton.clicked.connect(self.solveConn)

    def solveConn(self):
        finalAns = solve(self.amountEdit.text(), self.formulaEdit.text(),
              self.unitSel_1.currentText(), self.unitSel_2.currentText())
        self.textBrowser.append(finalAns)


# Program main module
if __name__ == "__main__":
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()