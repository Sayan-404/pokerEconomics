#ifdef __cplusplus
extern "C" {
#endif

// Function prototypes
int evaluate_5cards(int a, int b, int c, int d, int e);
int evaluate_6cards(int a, int b, int c, int d, int e, int f);
int evaluate_7cards(int a, int b, int c, int d, int e, int f, int g);

double handStrength(int *hole, int hole_size, int *board, int board_size);

#ifdef __cplusplus
}
#endif

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <phevaluator/phevaluator.h>
#include <phevaluator/rank.h>
#include <math.h>

#define NUM_CARDS 52
#define MAX_HAND_SIZE 7 // Max 2 cards + 5 board cards
#define MAX_COMBINATIONS (NUM_CARDS * (NUM_CARDS - 1) / 2)

// Function prototypes
int evaluate_5cards(int a, int b, int c, int d, int e);
int evaluate_6cards(int a, int b, int c, int d, int e, int f);
int evaluate_7cards(int a, int b, int c, int d, int e, int f, int g);

// Function to calculate the card value based on rank and suit
int calculate_card_value(int rank, int suit)
{
    return rank * 4 + suit;
}

// Function to generate a deck of 52 cards, excluding the player's hand (hole + board) if provided
void generate_deck(uint64_t exclusion_mask, int deck[], int *deck_size)
{
    int index = 0;
    for (int card = 0; card < NUM_CARDS; card++)
    {
        if (!(exclusion_mask & ((uint64_t)1 << card)))
        {
            deck[index++] = card;
        }
    }
    *deck_size = index;
}

// Function to create a bitmask for the cards to be excluded (hole + board)
uint64_t create_exclusion_mask(int *hand, int hand_size, int *board, int board_size)
{
    uint64_t mask = 0;
    for (int i = 0; i < hand_size; i++)
    {
        mask |= (uint64_t)1 << hand[i];
    }
    for (int i = 0; i < board_size; i++)
    {
        mask |= (uint64_t)1 << board[i];
    }
    return mask;
}

// Function to generate all possible hands by combining the deck and board cards
void generate_hands(int deck[], int deck_size, int *board, int board_size, int **hands, int *num_hands)
{
    int index = 0;
    int hand_size = 2 + board_size; // 2 cards from the deck + board_size cards

    for (int i = 0; i < deck_size - 1; i++)
    {
        for (int j = i + 1; j < deck_size; j++)
        {
            int *hand = hands[index++];
            hand[0] = deck[i];
            hand[1] = deck[j];
            for (int k = 0; k < board_size; k++)
            {
                hand[2 + k] = board[k];
            }
        }
    }

    *num_hands = index;
}

// Function to compute the probabilistic score
double handStrength(int *hole, int hole_size, int *board, int board_size)
{
    int deck[NUM_CARDS];
    int deck_size;

    uint64_t exclusion_mask = create_exclusion_mask(hole, hole_size, board, board_size);
    generate_deck(exclusion_mask, deck, &deck_size);

    int *hands[MAX_COMBINATIONS];
    for (int i = 0; i < MAX_COMBINATIONS; i++)
    {
        hands[i] = (int *)malloc(MAX_HAND_SIZE * sizeof(int));
    }

    int num_hands;
    generate_hands(deck, deck_size, board, board_size, hands, &num_hands);

    double w = 1.0 / num_hands; // Weight for each hand

    double ahead = 0.0;
    double tied = 0.0;
    double behind = 0.0;

    int pRank;

    // Generating player's rank
    if (board_size == 3)
    {
        pRank = evaluate_5cards(hole[0], hole[1], board[0], board[1], board[2]);
    }
    else if (board_size == 4)
    {
        pRank = evaluate_6cards(hole[0], hole[1], board[0], board[1], board[2], board[3]);
    }
    else if (board_size == 5)
    {
        pRank = evaluate_7cards(hole[0], hole[1], board[0], board[1], board[2], board[3], board[4]);
    }

    for (int i = 0; i < num_hands; i++)
    {
        int rank;

        // Generating opponent's rank
        if (board_size == 3)
        {
            rank = evaluate_5cards(hands[i][0], hands[i][1], board[0], board[1], board[2]);
        }
        else if (board_size == 4)
        {
            rank = evaluate_6cards(hands[i][0], hands[i][1], board[0], board[1], board[2], board[3]);
        }
        else if (board_size == 5)
        {
            rank = evaluate_7cards(hands[i][0], hands[i][1], board[0], board[1], board[2], board[3], board[4]);
        }

        if (rank < pRank)
        {
            ahead += w;
        }
        else if (rank == pRank)
        {
            tied += w;
        }
        else
        {
            behind += w;
        }
    }

    // Free allocated memory
    for (int i = 0; i < MAX_COMBINATIONS; i++)
    {
        free(hands[i]);
    }

    // printf("Ahead: %d\n", ahead);
    // printf("Tied: %d\n", tied);
    // printf("Behind: %d\n", behind);

    // *100 is the percentage of hands that we beat or at least tie given the input
    return 1 - ((ahead + tied / 2) / (ahead + tied + behind));
}

// Example usage
int main()
{
    int hole[] = {calculate_card_value(12, 3), calculate_card_value(11, 3)};                                                         // Example hole cards: Ace of Spades and King of Hearts
    int board[] = {calculate_card_value(10, 3), calculate_card_value(9, 3), calculate_card_value(8, 3), calculate_card_value(2, 3)}; // Example board: 4 cards

    int board_size = 4; // You can change this value to anything between 0 and 5

    double strength = handStrength(hole, 2, board, board_size);
    printf("Strength: %lf\n", strength);

    return 0;
}
