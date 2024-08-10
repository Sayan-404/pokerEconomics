    
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
    gutshot=0
    while(i != len(board)):
        count=1
        start = 0
        for j in range(0,13):
            if ranks[j] == board[i]:
                start = j
                break
        temp = i
        origin = start
        temp_gutshot = 0
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
                if temp_gutshot == 1:
                    break
                if board[(temp+1)%len(board)] == ranks[(start+2)%len(ranks)]:
                    count+=1
                    temp+=1
                    start+=2
                    temp_gutshot = 1
                else:
                    break
        if temp_gutshot == 1:
            gutshot = temp_gutshot
        sequenceCounter.append(count)
        i+=1
    
    return sequenceCounter,gutshot

def straight(board):
    lb = len(board)
    board = sortcards(board)
    sequence, gutshot = getLongestSequence(board)
    print(sequence)
    maxi = max(sequence)
    if gutshot == 1:
        if maxi == 4:
            counter = 0
            for i in sequence:
                if i == maxi:
                    counter+=1
            if counter == 2:
                return 8
            return 4
        return 0
    else:
        if maxi == 5:
            return 0
        if maxi == 4:
            if sequence[-1] == 4 and board[len(board)-1] == 'A':
                return 4
            if sequence[1] == 4 and board[len(board)-1] == 'A':
                return 4
            return 8
        return 0

    # print(maxi)
    
            
if __name__ == "__main__":
    board = ['2h', '5h', '6d', '6h', 'Th']
    print(getLongestSequence(board))
    print(straight(board))




