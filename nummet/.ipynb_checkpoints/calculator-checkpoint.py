from socket import *
import re
import math


# A pattern problem must follow
problemPattern = re.compile(r'[\d. +\-*\/\^()a-z]')
# A pattern any sign must follow
signPattern = re.compile(r'[+\- ]')
# A pattern any number in problem must follow
numberPattern = re.compile(r'[\d. ]')
# A pattern to find if operator implies multiplication or division
multiplyOrDividePattern = re.compile(r'[*(a-z\d\/]')
# A pattern to find if operator implies multiplication
multiplyPattern = re.compile(r'[*(a-z\d]')
# A pattern to find if operator is '*' or '/'
multiplicativeOperatorPattern = re.compile(r'[*\/]')
# A pattern used to look for operators in layer 2 or upwards
layer2UpPattern = re.compile(r'[*(a-z\d\/\^]')
# A pattern used to look for math method's, (pi, sqrt(), ln(), etc)
mathMethodPattern = re.compile(r'[a-z]')



# The calculator, calls layer 1 with stop set to 0 and upper set to False

def calc(problem):
    
    # Simple syntax check of problem, won't catch everything
    if not problemPattern.match(problem): raise Exception

    problemLength = len(problem)
    return calcLayer1(problem, problemLength, 0, False)
    


# Layer 1: addition and subtraction

def calcLayer1(problem, problemLength, stop, upper):

    operator = '+'
    
    number = newNumber = 0

    start = stop

    
    # When start is larger than strLength all of problem has been read and calculated
    while start < problemLength:
        
        # If operator has been set to ')' and function not bottom, special return takes place
        if upper and operator == ')':

            stop += 1   # moves stop out of ')'
            # if stop is not outside problem, stop iterates to next operator
            while stop < problemLength and problem[stop] == ' ': 
                stop += 1

            return number, stop     # number and stop is returned to lower function
        
        
        # decides start, stop and sign of new number
        start, stop, sign = newNumberInitials(problem, problemLength, stop)


        # Operator before the next number if there is one
        if stop < problemLength: operator = problem[stop]
        # calculates initial newNumber. Also finds possible new stop value and operator
        newNumber, stop, operator = newNumberInitializer(problem, problemLength, start, stop, operator)


        # Checks if operator before new number is '^'
        if operator == '^':
            # If operator is '^' Layer 3 calculator is run
            newNumber, stop = calcLayer3(problem, problemLength, newNumber, stop)
            # operator is updated if possible
            if stop < problemLength: operator = problem[stop]

        # Checks if operator before new number is '*' or '/'
        if multiplyOrDividePattern.match(operator):
            # If operator is '*' or '/' Layer 2 calculator is run
            newNumber, stop = calcLayer2(problem, problemLength, newNumber, stop)
            # operator is updated if possible
            if stop < problemLength: operator = problem[stop]

        

        # Adds newNumber times sign to previous number
        number += newNumber * sign

        # start is updated
        start = stop

    return number



# Layer 2: multiplication and division

def calcLayer2(problem, problemLength, number, stop):
    
    operator = problem[stop]
    multiply = multiplyPattern.match(operator)
    
    newNumber = 0
    
    if multiplicativeOperatorPattern.match(operator): stop += 1
    start = stop
    
    
    # When start is larger than strLength or operator is from below layer 2, calculations are finished
    while start < problemLength and layer2UpPattern.match(operator):
        
        # decides start, stop and sign of new number
        start, stop, sign = newNumberInitials(problem, problemLength, stop)
        

        # operator before next number if there is one
        if stop < problemLength: operator = problem[stop]

        newNumber, stop, operator = newNumberInitializer(problem, problemLength, start, stop, operator)
        

        # Checks if operator before new number is from layer 3 or upwards
        if operator == '^':
            # If operator is '^' layer 3 calculator is run
            newNumber, stop = calcLayer3(problem, problemLength, newNumber, stop)
            # operator is updated if possible
            if stop < problemLength: operator = problem[stop]


        # multiplies number to or divides number by newNumber times sign
        if multiply:
            number *= (newNumber * sign)
        else:
            number /= (newNumber * sign)
        

        # Cheks if next operation is multiplication
        multiply = multiplyPattern.match(operator)

        # stop is moved from operator if necessary and start is updated
        if multiplicativeOperatorPattern.match(operator): stop += 1
        start = stop


    #stop -= 1
    return number, stop



# Layer 3: exponents

def calcLayer3(problem, problemLength, number, stop):
    
    operator = problem[stop]
    
    newNumber = 0
    
    stop += 1
    start = stop
    

    while start < problemLength and operator == '^':
        
        # decides start, stop and sign of new number
        start, stop, sign = newNumberInitials(problem, problemLength, stop)


        # operator before next number if there is one
        if stop < problemLength: operator = problem[stop]

        newNumber, stop, operator = newNumberInitializer(problem, problemLength, start, stop, operator)


        # raises number to newNumber times sign
        number **= (newNumber * sign)


        # stop is moved from operator and start is updated
        stop += 1
        start = stop
    

    stop -= 1
    return number, stop       




# Finds start, stop and sign of new number

def newNumberInitials(problem, problemLength, stop):

    sign = 1

    # stop iterates to beginning of new number
    while signPattern.match(problem[stop]):
        # if negative sign is discovered, sign variable is changed
        if problem[stop] == '-': 
            sign *= -1
        stop += 1

    start = stop    # start moves so problem[start:stop] won't include operators

    # stop iterates to the next operator or the end of problem
    while stop < problemLength and numberPattern.match(problem[stop]):
        stop += 1

    return start, stop, sign



# Finds newNumber and possible following operator wether it's from parentheses, a math method or can be read directly
def newNumberInitializer(problem, problemLength, start, stop, operator):

    # if problem[start] is a number, newNumber can be read directly
    if numberPattern.match(problem[start]): 
        # Next number are characters from start to stop
        newNumber = float(problem[start:stop])
        
    # Checks if operator is start of parentheses
    elif operator == '(':
        stop += 1   # moves stop out of '('
        # layer 1 calculator is run with stop = stop and upper set to True
        newNumber, stop = calcLayer1(problem, problemLength, stop, True)
        
        # operator is updated if possible
        if stop < problemLength: operator = problem[stop]
        # if not possible, operator is set to '' to prevent issues with pattern variables
        else: operator = ''
    
    # Checks if operator is start of math method
    elif mathMethodPattern.match(operator):
        # method calculator is run from stop
        newNumber, stop = calcMethod(problem, problemLength, stop)
        
        # operator is updated if possible
        if stop < problemLength: operator = problem[stop]
        # if not possible, operator is set to '' to prevent issues with pattern variables
        else: operator = ''
    
    return newNumber, stop, operator



# Functions for various math methods: (e, sqrt(), ln(), etc.)

# Method for solivng e
def e(problem, problemLength, stop):
    # stop is moved to next operator if possible
    while stop < problemLength and problem[stop] == ' ':
        stop += 1 
    return math.e, stop


# Method for solving pi
def pi(problem, problemLength, stop):
    # stop is moved to next operator if possible  
    while stop < problemLength and problem[stop] == ' ':
        stop += 1  
    return math.pi, stop


# Method for solving sqrt(number)
def sqrt(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True 
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.sqrt(number), stop


# Method for solving ln(number)
def ln(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.log(number), stop


# Method for solving log(number)
def log(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.log10(number), stop


# Method for solving cos(number)
def cos(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.cos(number), stop


# Method for solving arccos(number)
def arccos(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.acos(number), stop


# Method for solving sin(number)
def sin(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.sin(number), stop


# Method for solving arcsin(number)
def arcsin(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.asin(number), stop


# Method for solving tan(number)
def tan(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.tan(number), stop


# Method for solving arctan(number)
def arctan(problem, problemLength, stop):
    
    stop += 1   # moves stop out of '('
    # layer 1 calculator is run with stop = stop and upper set to True
    number, stop = calcLayer1(problem, problemLength, stop, True)
    return math.atan(number), stop



# Dictionary of math methods, (e, sqrt(), ln(), etc.)
methodDictionary = {
    'e': e,
    'pi': pi,
    'sqrt': sqrt,
    'ln': ln,
    'log': log,
    'cos': cos,
    'arccos': arccos,
    'sin': sin,
    'arcsin': arcsin,
    'tan': tan,
    'arctan': arctan
}


# Method calculator 
# reads method from problem, then runs and returns corresponding function from dictionary

def calcMethod(problem, problemLength, stop):

    start = stop    # start initialized as stop
    # stop is moved forward so long as character on index stop is within a-z
    while stop < problemLength and mathMethodPattern.match(problem[stop]):
        stop += 1
    method = problem[start:stop]    # string from start to stop is extracted

    # math method function is retreived from methodDictionary and run
    number, stop = methodDictionary[method](problem, problemLength, stop)
    
    return number, stop



if __name__ == '__main__':
    
    # Code to ask for inputs and run calculator until user breaks it
    try:
        while True:
            try:
                problem = input('Write a problem: ')
                if problem == 'exit': 
                    print('Exiting')
                    break
                print(calc(problem))
            except Exception:
                print('Bitch')
    
    except KeyboardInterrupt:
        print('\nExiting')