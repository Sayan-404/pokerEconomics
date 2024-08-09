#include <stdio.h>

// Function to generate a board value based on rank and suit
int generateBoardValue(char rank, char suit) {
    int suitsInInt;
    int ranksInInt;

    // Map suit to integer
    switch (suit) {
        case 's': suitsInInt = 0; break;
        case 'c': suitsInInt = 1; break;
        case 'd': suitsInInt = 2; break;
        case 'h': suitsInInt = 3; break;
        default: return -1; // Invalid suit
    }

    // Map rank to integer
    if (rank >= '2' && rank <= '9') {
        ranksInInt = rank - '0'; // Convert char '2' to '9' to integer 2 to 9
    } else {
        switch (rank) {
            case 'T': ranksInInt = 10; break;
            case 'J': ranksInInt = 11; break;
            case 'Q': ranksInInt = 12; break;
            case 'K': ranksInInt = 13; break;
            case 'A': ranksInInt = 14; break;
            default: return -1; // Invalid rank
        }
    }

    // Calculate and return the board value
    return ranksInInt * 10 + suitsInInt;
}

int main() {
    // Example usage
    char rank = 'A';
    char suit = 'h';
    int boardValue = generateBoardValue(rank, suit);

    if (boardValue != -1) {
        printf("Board value: %d\n", boardValue);
    } else {
        printf("Invalid rank or suit\n");
    }

    return 0;
}
