#whole file is post-mvp leaderboard, login info, and recipeSaved information
#function to set up leaderboard
#CITATION: FILE FUNCTIONS FROM https://www.geeksforgeeks.org/reading-writing-text-files-python/
def leaderboard(file):
    board = dict()
    f = open(file, 'r')
    for line in f.readlines():
        line = line.replace('\n','')
        line = line.strip()
        name = ''
        num = 0
        for char in line:
            if not char == '\n' and not char == ' ':
                if char.isdigit():
                    char = int(char)
                    num*=10
                    num += char
                elif char != ':':
                    name = name + char
        if not name=='':
            board[name] = num
    return board #return dictionary of person: score

#https://www.kite.com/python/answers/how-to-edit-a-file-in-python file function documentation
#function to set up passuser
def passUser(file):
    login = dict()
    f = open(file, 'r')
    for line in f.readlines():
        line = line.replace('\n','')
        line = line.strip()
        user = ''
        password = ''
        isBeforeColon = True
        for char in line:
            if not char == '\n' and not char == ' ':
                if char == ':':
                    isBeforeColon = False
                else:
                    if isBeforeColon:
                        user = user + char
                    else:
                        password = password + char
                    

        if not user=='':
            login[user] = password
    return login #return login board of pass:user

#update leaderboard dict given ur curent score
def updateLeaderboard(file, currentUser, currentScore): #boad is a dict
    board = leaderboard(file)
    board[currentUser] = currentScore 
    updatedFile = open(file, "a") #go into append mode, handle at the end
    updatedFile.write(f"{currentUser}: {currentScore} \n") 
    updatedFile.close() 
    return board

#return sorted leaderboard list given a dictionary 
def sortLeaderboard(file, board):
    boardList = list()
    for item, value in board.items():
        if not (isinstance(value, int)):
            board[item] = 30 #default number to avoid bugs
        boardList.append(value)
    boardList.sort(reverse = True)
    return boardList
#CITATION: https://www.kite.com/python/answers/how-to-edit-a-file-in-python referenced to overwrite files to add recipes 
#function to add current created dish to current User's list of overal recipes created
def addRecipe(file, curruser, finalDish):
    f = open(file, 'r')
    listOfStrings = f.readlines()

    f.close()
    linecounter = 0
    lineToChange = 0
    lineText = ''
    for line in listOfStrings:
        
        isBeforeColon = True
        firstSpace = True
        recipe =''
        user = ''
        for char in line:
            if not char == '\n':
                if char == ':':
                    isBeforeColon = False
                else:
                    if isBeforeColon:
                        user = user + char
                    else:
                        if not char == ' ':
                            recipe = recipe + char
            #after getting all the nifo check if this is current user
        if curruser == user:
            recipe = recipe + f', {finalDish} ' #string of all the lists
            lineText = f'{curruser}:{recipe}'
            lineToChange = linecounter

        linecounter+=1 
    listOfStrings[lineToChange] = lineText + '\n'
    f = open(file, 'w')
    newContents = ''.join(listOfStrings)
    f.write(newContents)
    f.close() 

    readFile = open(file)
