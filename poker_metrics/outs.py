

ranks = ["A","2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["s","c","h","d"]
def pair(hole,board):
    hand = hole + board
    # print(len(hand))
    count=0
    for i in range(len(hand)):
        for j in range(i+1,len(hand)):
            if (hand[i][0] == hand[j][0]):
                count += 1
    
    if count >=1:
        return 0
    else:
        if len(hand) == 5:
            return 15
        else:
            return 16 

def twopair(hole,board):
    hand = hole + board
    # print(len(hand))
    count=0
    for i in range(len(hand)):
        for j in range(i+1,len(hand)):
            if (hand[i][0] == hand[j][0]):
                count += 1
    
    if count >= 2:
        return 0
    if count == 0:
        return 0
    if count == 1:
        if len(hand) == 5:
            return 9 
        else:
            return 12

def trips(hole,board):
    hand = hole+board
    count=0
    for i in range(len(hand)):
        for j in range(i+1,len(hand)):
            if (hand[i][0] == hand[j][0]):
                count += 1
    
    if count == 3:
        return 0
    else:
        if count == 1:
            if len(hand) == 5:
                return 2
            else:
                return 2
        else:
            return 0
        
def boat(hole,board):
    hand=hole+board
    count=0
    for i in range(len(hand)):
        for j in range(i+1,len(hand)):
            if (hand[i][0] == hand[j][0]):
                count += 1
    
    if count == 5:
        return 0
    else:
        if count == 2:
            if len(hand) == 5:
                return 4
            else:
                return 4
        if count == 3:
                if len(hand)==5:
                    return 6
                else:
                    return 9
        else:
            return 0

def quads(hole,board):
    hand=hole+board
    count=0
    for i in range(len(hand)):
        for j in range(i+1,len(hand)):
            if (hand[i][0] == hand[j][0]):
                count += 1

    if count == 4:
        return 0
    if count == 3:
        if len(hand) == 5:
            return 1
        else:
            return 1
    else:
        return 0
    
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
    gutshot=0
    while(i != len(board)):
        count=1
        start = 0
        for j in range(0,13):
            if ranks[j] == board[i]:
                start = j
                break
        temp = i
        while(1):
            if board[(temp+1)%len(board)] == ranks[(start + 1)%len(ranks)]:
                count+=1
                temp+=1
                start+=1
            else:
                if board[(temp+1)%len(board)] == ranks[(start+2)%len(ranks)]:
                    gutshot = 1
                break
        sequenceCounter.append(count)
        i+=1
    return sequenceCounter,gutshot

def straight(board):
    lb = len(board)
    board = sortcards(board)
    
    sequence, gutshot = getLongestSequence(board)
    max = 0
    for i in sequence:
        if i > max:
            max = i
    if gutshot:
        counter = 0
        for i in sequence:
            if (i == 3):
                if(lb == 5):
                    return 4
                else:
                    return 4
            if (i==2):
                counter+=1
        if (counter == 2):
            if(lb == 5):
                return 4
            else:
                return 4
        else:
            return 0
    
    else:
            if(sequence[len(sequence)-1] == 4):
                if(lb == 5):
                    return 4
                else:
                    return 4
            if (max == 4):
                if(lb == 5):
                    return 8
                else:
                    return 8
            if(max == 5):
                return 0 
            else:
                return 0
            

def flush(board):
    lb = len(board)
    prev = board[0][1]
    count = 1
    max = 0
    for i in range(0,lb):
        index = board[i][1]
        for j in range(0,lb):
            if i!=j:
                if board[j][1] == index:
                    count+=1
        if count>max:
            max = count
        count = 1

    if (max == 5):
        return 0
    if (max == 4):
        if lb == 5:
            return 9
        else:
            return  9
    else:
        return 0

def straightflush(board):
    if(straight(board) == 8 and flush(board) == 9):
        return 2
    if(straight(board) == 4 and flush(board) == 9):
        return 1
    return 0

def pairFlush(hole,board):
    if(pair(hole,board) != -1 and flush(hole+board) == 9):
        return 1
    return 0
 
def equity(hole, board):
    if len(hole) != 2 or len(board) < 3:
        raise 'Invalid number of input cards.'
    outs = 0
    outs += pair(hole,board) + twopair(hole,board) + trips(hole,board) + boat(hole,board) + quads(hole,board) + straight(hole+board) + flush(hole+board) - straightflush(hole+board) - pairFlush(hole,board)
    prob = 0
    if len(hole+board) == 5:
        prob = outs/47 + ((52-outs)/47) * (outs/46)
    else:
        prob = outs/46
    return prob

if __name__ == "__main__":
    hole=['2s', '4h']
    board = ['5h', 'Jh', 'Ah']
    outs = 0
    outs += pair(hole,board) + twopair(hole,board) + trips(hole,board) + boat(hole,board) + quads(hole,board) + straight(hole+board) + flush(hole+board) - straightflush(hole+board) - pairFlush(hole,board)
    # _pair = pair(hole,board) if pair(hole,board) != -1 else 0
    # if pair(hole,board) == -1:
    #     if twopair(hole,board) != -1:
    #         outs += twopair(hole,board)
    #     if trips(hole,board) != -1:
    #         outs += trips(hole,board)
    #     if boat(hole,board) > 0 and boat(hole,board)<1:
    #         outs += boat(hole,board) - trips(hole,board)
    #     if quads(hole,board) != 1:
    #         outs += quads(hole,board)
    # else:
    #     outs += pair(hole,board)

    # if straight(hole+board) != 1:
    #     outs += straight(hole+board)
    # if flush(hole+board) != 1:
    #     outs += flush(hole+board)
    prob = 0
    if len(hole+board) == 5:
        prob = outs/47 + ((52-outs)/47) * (outs/46)
    else:
        prob = outs/46
    # print(flush(hole+board))
    print(f"Ahead/total:{prob} Inconsequential/Total:{1 - prob}")

    