from collections import Counter 

def splitter(n, s):
    pieces = s.split()
    return (" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n))

text = "12; 3456 124 345 23 45;"

def instance_of_semicolon(text):
    num = 0
    freq = Counter(text)

    for i in splitter(100, text):
        num += i.count(';')

    return num 
        
        

if __name__ == "__main__":
    number = instance_of_semicolon(text)
    print(number)
