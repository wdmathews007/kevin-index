#from collections import Counter 

def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

text = "12; 3456 124 345 23 45;"

def semicolonFreq(text):
    num = 0
    numList = []
    avg = 0

    for i in splitter(100, text):
        numList.append(i.count(";"))
        num += 1
    
    for i in numList:
        avg += i

    avg = avg/num

    return avg

def commaFreq(text):
        num = 0
        numList = []
        avg = 0

        for i in splitter(100, text):
            numList.append(i.count(","))
            num += 1
    
        for i in numList:
            avg += i

        avg = avg/num

        return avg

def emmdashFreq(text):
    num = 0
    numList = []
    avg = 0

    for i in splitter(100, text):
        numList.append(i.count("—"))
        num += 1
    
    for i in numList:
        avg += i

    avg = avg/num

    return avg    

def ellipsisFreq(text):
    num = 0
    numList = []
    avg = 0

    for i in splitter(100, text):
        numList.append(i.count("..."))
        num += 1
    
    for i in numList:
        avg += i

    avg = avg/num

    return avg  

def exclamationFreq(text):
    num = 0
    numList = []
    avg = 0

    for i in splitter(100, text):
        numList.append(i.count("!"))
        num += 1
    
    for i in numList:
        avg += i

    avg = avg/num

    return avg  

def colonFreq(text):
    num = 0
    numList = []
    avg = 0

    for i in splitter(100, text):
        numList.append(i.count(":"))
        num += 1
    
    for i in numList:
        avg += i

    avg = avg/num

    return avg  

def parenthesesFreq(text):
    num = 0
    numList = []
    avg = 0

    for i in splitter(100, text):
        numList.append(i.count("("))
        num += 1
    
    for i in numList:
        avg += i

    avg = avg/num

    return avg  

    
if __name__ == "__main__":
    number = semicolonFreq(text)
    print(number)
