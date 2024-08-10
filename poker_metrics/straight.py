    
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["s","c","h","d"]
def sortcards(board):
    order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    reverse_order = {v: k for k, v in order.items()}
    newcards=[]
    for i in board:
        newcards.append(order[i[0]])
    newcards = sorted(set(newcards))
    board = []
    for i in newcards:
        board.append(reverse_order[i])
    return board  

def getLongestSequence(board):
    i=0
    board = sortcards(board)
    sequenceCounter = []
    gutshot=1
    while(i != len(board)):
        count=1
        start = 0
        for j in range(0,13):
            if ranks[j] == board[i]:
                start = j
                break
        temp = i
        origin = start
        while(1):
            _temp = (temp+1)%len(board) if origin == 12 else temp+1
            _start = (start+1)%len(ranks) if origin == 12 else start+1
            if _temp > len(board) - 1:
                break
            if board[_temp] == ranks[_start]:
                count+=1
                temp+=1
                start+=1
            else:
                break
        sequenceCounter.append(count)
        i+=1
    
    return sequenceCounter,gutshot

def longestGutshot(newboard):
    max_count = 0
    i=0
    while(i != len(newboard)):
        count=1
        start = 0
        for j in range(0,13):
            if ranks[j] == newboard[i]:
                start = j
                break
        temp = i
        origin = start
        while(1):
            _temp = (temp+1)%len(newboard) 
            _start = (start+1)%len(ranks)
            if _temp > len(newboard) - 1:
                break
            if newboard[_temp] == ranks[_start]:
                count+=1
                temp+=1
                start+=1
            else:
                if newboard[(temp+1)%len(newboard)] == ranks[(start+2)%len(ranks)]:
                    count+=1
                    temp+=1
                    start+=2
                else:
                    break
        if count > max_count:
            max_count = count
        i+=1
    return max_count

def gutshotAnalyser(board,sequence):
    maxi = max(sequence)
    newboard = []
    gutshot=0
    if(maxi == 2):
        for i in range(0,len(sequence)):
            if sequence[i] == 2:
                newboard.append(board[i])
                newboard.append(board[(i+1)%len(board)])
                gutshot = longestGutshot(newboard)
    if(maxi == 3 or sequence[-1] == 4):
        for i in range(0,len(sequence)):
            if sequence[i] == 3:
                newboard.append(board[i])
                newboard.append(board[(i+1)%len(board)])
                newboard.append(board[(i+2)%len(board)])
                gutshot = longestGutshot(newboard)
                if board[-1] == 'A':
                    newboard.append('A')
                    c1 = longestGutshot(newboard)
                    newboard[-1] = board[(i+3)%len(board)]
                    c2 = longestGutshot(newboard)
                    gutshot = 8 if c1 == c2 else max(c1,c2)
                else:
                    newboard.append(board[(i+3)%len(board)])
                    gutshot = longestGutshot(newboard)

    return gutshot
    # if(ranks[newboard[1]+1] == board[newboard[2]]):
    #     print(1)

def straight(board):
    lb = len(board)
    board = sortcards(board)
    
    sequence, gutshot = getLongestSequence(board)
    maxi = max(sequence)
    counter = 0
    # print(maxi)
    gutshot = gutshotAnalyser(board,sequence)
    if(gutshot >= 4):
        return gutshot
    
    for i in sequence:
        if i == maxi:
            counter+=1
    
    if maxi == 4:
        if sequence[-1] == 4 or board[len(board)-1] == 'A':
            return 4
        if sequence[2] == 4 
        return 8
    return 0
        
    
            
if __name__ == "__main__":
    board = ['6s', '7d', '8s', '9d', 'Td']
    # print(getLongestSequence(board))
    print(straight(board))




