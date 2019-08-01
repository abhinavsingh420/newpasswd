#!/usr/bin/python3

from random import randint, shuffle
import getopt
import sys
import re
import os
import shutil
import urllib.request

STR_LENGTH = 16
UPPERCASE = False
LOWERCASE = False
DIGITS = False
SYMBOLS = False
COUNT = 1
NUMOFWORDS = 2
PREFIX = False
SUFFIX = False
WORD = False
DELIMITER = "-"
PROJECT_FOLDER = os.path.expanduser('~/.newpasswd')

def usage():
    print("Usage: newpasswd [-OPTIONS]")
    print("\t-u, --uppercase\t\t Include UPPERCASE characters (A-Z)")
    print("\t-l, --lowercase\t\t Include lowercase characters (a-z)")
    print("\t-d, --digits\t\t Include digits (0-9)")
    print("\t-s, --symbols\t\t Include symbols (!@#|_-*)")
    print("\t-p, --prefix\t\t Add prefix to password (4 digits)")
    print("\t-x, --suffix\t\t Add suffix to password (4 digits)")
    print("\t-w, --word\t\t Generate sentence (without, a random string will be generated)")
    print("\t-c, --count <num>\t How many passwords to generate")
    print("\t-n, --numOfWords <num>\t How mange words to include. Only works with -w")
    print("\t-b, --between, --delimiter <char>\t A character to seperate words")

def first_run():
    if not os.path.exists(PROJECT_FOLDER):
        os.mkdir(PROJECT_FOLDER)
    
    if not os.path.isfile(os.path.join(PROJECT_FOLDER, 'wordlist.txt')):
        with urllib.request.urlopen('https://raw.githubusercontent.com/madsaune/newpasswd/master/wordlist.txt') as response:
            with open(os.path.join(PROJECT_FOLDER, 'wordlist.txt'), 'wb') as destination:
                shutil.copyfileobj(response, destination)

        destination.close()

first_run()

try:
    opts, args = getopt.getopt(sys.argv[1:], "huldspxwc:n:b:", ['help', 'uppercase', 'lowercase', 'digits', 'symbols', 'prefix', 'suffix', 'word', 'count=', 'numOfWords=', 'between=', 'delimiter='])
    
    if len(opts) < 1:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-u', '--uppercase'):
            UPPERCASE = True
        elif opt in ('-l', '--lowercase'):
            LOWERCASE = True
        elif opt in ('-d', '--digits'):
            DIGITS = True
        elif opt in ('-s', '--symbols'):
            SYMBOLS = True
        elif opt in ('-p', '--prefix'):
            PREFIX = True
        elif opt in ('-x', '--suffix'):
            SUFFIX = True
        elif opt in ('-w', '--word'):
            WORD = True
        elif opt in ('-c', '--count'):
            COUNT = int(arg)
        elif opt in ('-n', '--numOfWords'):
            NUMOFWORDS = int(arg)
        elif opt in ('-b', '--between', '--delimiter'):
            DELIMITER = arg
        else:
            usage()
            sys.exit(2)

except getopt.GetoptError:
    usage()
    sys.exit(2)

def generateKeyspace():
    keyspace = ""

    keyspace += "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if UPPERCASE else ""
    keyspace += "abcdefghijklmnopqrstuvwxyz" if LOWERCASE else ""
    keyspace += "0123456789" if DIGITS else ""
    keyspace += "!@#|_-*" if SYMBOLS else ""

    keyspace = list(keyspace)
    shuffle(keyspace)

    return ''.join(keyspace)

def isValid(str):
    isValid = True

    if UPPERCASE and re.search(r"[A-Z]", str) is None:
        isValid = False
    
    if LOWERCASE and re.search(r"[a-z]", str) is None:
        isValid = False
    
    if DIGITS and re.search(r'[\d]', str) is None:
        isValid = False

    if SYMBOLS and re.search(r'[!@#|_\-*]', str) is None:
        isValid = False

    return isValid

def generateString():
    chars = generateKeyspace()
    global STR_LENGTH

    if PREFIX:
        STR_LENGTH -= 4
    if SUFFIX:
        STR_LENGTH -= 4

    for x in range(COUNT):
        recalc = True
        password = ""

        while not isValid(password):
            password = ""
            prefixData = ""
            suffixData = ""

            if PREFIX:
                prefixData = str(randint(1111, 9999))
            
            if SUFFIX:
                suffixData = str(randint(1111, 9999))
        
            for y in range(STR_LENGTH):
                password += chars[randint(0, len(chars) - 1)]
                
        print(password)
            
def generateSentence():

    f = open(os.path.join(PROJECT_FOLDER, 'wordlist.txt'), 'r')
    wordlist = f.readlines()
    f.close()

    for x in range(0, COUNT):

        list_of_words = []
        password = ""
        
        if PREFIX:
            list_of_words.append(str(randint(1111, 9999)))


        for y in range(0, NUMOFWORDS):
            list_of_words.append(wordlist[randint(0, len(wordlist) - 1)].rstrip().capitalize())
        

        if SUFFIX:
            list_of_words.append(str(randint(1111, 9999)))
        
        password = DELIMITER.join(list_of_words)
        print(password)

def main():
    if WORD:
        generateSentence()
    else:
        generateString()

if __name__ == '__main__':
    main()
