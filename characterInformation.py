#function to set up leaderboad
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
    return board #return dictionary board
#https://www.kite.com/python/answers/how-to-edit-a-file-in-python file function documentation

#print(leaderboard('leaderboard.txt'))   
#update leaderboard dict given ur curent core
def updateLeaderboard(file, currentUser, currentScore): #boad is a dict
    board = leaderboard(file)
    board[currentUser] = currentScore 
    updatedFile = open(file, "a") #go into append mode, handle at the end
    updatedFile.write(f"{currentUser}: {currentScore} \n") 
    updatedFile.close() 
    return board


def sortLeaderboard(file, board):
    boardList = list()
    for item, value in board.items():
        if not (isinstance(value, int)):
            board[item] = 30 #default number to avoid bugs
        boardList.append(value)
        print(value)
        print(type(value))
    boardList.sort(reverse = True)
    return boardList