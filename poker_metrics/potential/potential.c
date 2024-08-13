#ifdef __cplusplus
extern "C"
{
#endif

    // Function prototypes
    int evaluate_5cards(int a, int b, int c, int d, int e);
    int evaluate_6cards(int a, int b, int c, int d, int e, int f);
    int evaluate_7cards(int a, int b, int c, int d, int e, int f, int g);

    double potential(int *hole_cards, int num_hole_cards, int *community_cards, int num_community_cards);
#ifdef __cplusplus
}
#endif
#include <stdio.h>
#include <stdlib.h>
#include <phevaluator/rank.h>
#include <phevaluator/phevaluator.h>

#define TOTAL_CARDS 52

// Declarations of the previously defined functions
int get_rank_category(int *cards, int noCards);
int evaluate_5cards(int c1, int c2, int c3, int c4, int c5);
int evaluate_6cards(int c1, int c2, int c3, int c4, int c5, int c6);
int evaluate_7cards(int c1, int c2, int c3, int c4, int c5, int c6, int c7);
double potential(int *hole_cards, int hole_count, int *community_cards, int community_count);
void generate_combinations(int *deck, int deck_size, int r, int **combinations, int *num_combinations);

int main()
{
    // Example cards: let's assume these are the indices corresponding to certain cards
    // Here is an example hand with the ranks and suits mapped as explained:
    // Hole cards: Ace of Spades (12*4+3 = 51), King of Hearts (11*4+2 = 46)
    // Community cards: Queen of Diamonds (10*4+1 = 41), Jack of Clubs (9*4+0 = 36), Ten of Spades (8*4+3 = 35)

    int hole_cards[2] = {25, 28};          // Ace of Spades, King of Hearts
    int community_cards[3] = {39, 42, 45}; // Queen of Diamonds, Jack of Clubs, Ten of Spades

    double ahead_fraction;

    // Type lookahead of 1 (simulating turning one more card)
    ahead_fraction = potential(hole_cards, 2, community_cards, 3);

    printf("Ahead Fraction: %.6f\n", ahead_fraction);
    // printf("Inconsequential Fraction: %.6f\n", inconsequential_fraction);

    return 0;
}

// Function definitions...

int get_rank_category(int *cards, int noCards)
{
    int rank;

    if (noCards == 5)
    {
        rank = evaluate_5cards(cards[0], cards[1], cards[2], cards[3], cards[4]);
    }
    else if (noCards == 6)
    {
        rank = evaluate_6cards(cards[0], cards[1], cards[2], cards[3], cards[4], cards[5]);
    }
    else
    {
        rank = evaluate_7cards(cards[0], cards[1], cards[2], cards[3], cards[4], cards[5], cards[6]);
    }

    if (rank > 6185)
        return 8;
    if (rank > 3325)
        return 7;
    if (rank > 2467)
        return 6;
    if (rank > 1609)
        return 5;
    if (rank > 1599)
        return 4;
    if (rank > 322)
        return 3;
    if (rank > 166)
        return 2;
    if (rank > 10)
        return 1;

    return 0;
}

// Definitions of potential and generate_combinations...

double potential(int *hole_cards, int hole_count, int *community_cards, int community_count)
{
    int type_lookahead = (community_count == 3) ? 2 : 1;
    int rank_category, future_rank_category;
    double ahead = 0, inconsequential = 0, total;
    int i, j, combination_size;
    int num_combinations;
    int *combinations;

    // Create a deck excluding hole cards and community cards
    int deck[TOTAL_CARDS];
    int deck_size = 0;
    for (i = 0; i < TOTAL_CARDS; i++)
    {
        int is_in_hand = 0;
        for (j = 0; j < hole_count + community_count; j++)
        {
            if (i == hole_cards[j] || i == community_cards[j])
            {
                is_in_hand = 1;
                break;
            }
        }
        if (!is_in_hand)
        {
            deck[deck_size++] = i;
        }
    }

    // Generate possible combinations
    generate_combinations(deck, deck_size, type_lookahead, &combinations, &num_combinations);

    // Evaluate current rank category
    int hand_size = hole_count + community_count;
    int hand[hand_size];
    for (i = 0; i < hole_count; i++)
        hand[i] = hole_cards[i];
    for (i = 0; i < community_count; i++)
        hand[hole_count + i] = community_cards[i];

    rank_category = get_rank_category(hand, hand_size);

    // Loop through each combination and calculate ahead and inconsequential counts
    for (i = 0; i < num_combinations; i++)
    {
        int full_hand_size = hand_size + type_lookahead;
        int full_hand[full_hand_size];

        // Copy current hand to full_hand
        for (j = 0; j < hand_size; j++)
            full_hand[j] = hand[j];

        // Append the combination to the full hand
        for (j = 0; j < type_lookahead; j++)
            full_hand[hand_size + j] = combinations[i * type_lookahead + j];

        future_rank_category = get_rank_category(full_hand, full_hand_size);

        if (future_rank_category < rank_category)
        {
            ahead++;
        }
        else if (future_rank_category == rank_category)
        {
            inconsequential++;
        }
    }

    total = ahead + inconsequential;

    // Free dynamically allocated memory
    free(combinations);

    return ahead / total;
}

void generate_combinations(int *deck, int deck_size, int r, int **combinations, int *num_combinations)
{
    int i, j, k, index = 0;

    *num_combinations = 1;
    for (i = deck_size - r + 1; i <= deck_size; i++)
    {
        *num_combinations *= i;
    }
    for (i = 1; i <= r; i++)
    {
        *num_combinations /= i;
    }

    *combinations = (int *)malloc(*num_combinations * r * sizeof(int));

    int indices[r];
    for (i = 0; i < r; i++)
    {
        indices[i] = i;
    }

    while (1)
    {
        for (i = 0; i < r; i++)
        {
            (*combinations)[index++] = deck[indices[i]];
        }

        i = r - 1;
        while (i >= 0 && indices[i] == i + deck_size - r)
        {
            i--;
        }

        if (i < 0)
        {
            break;
        }

        indices[i]++;
        for (j = i + 1; j < r; j++)
        {
            indices[j] = indices[j - 1] + 1;
        }
    }
}
