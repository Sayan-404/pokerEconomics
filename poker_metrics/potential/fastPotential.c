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
#include <string.h>

#define NUM_RANKS 13
#define NUM_SUITS 4
#define DECK_SIZE (NUM_RANKS * NUM_SUITS)

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

void get_deck(int *deck)
{
    for (int rank = 0; rank < NUM_RANKS; rank++)
    {
        for (int suit = 0; suit < NUM_SUITS; suit++)
        {
            deck[rank * NUM_SUITS + suit] = rank * NUM_SUITS + suit;
        }
    }
}

double potential(int *hole_cards, int num_hole_cards, int *community_cards, int num_community_cards)
{
    int deck[DECK_SIZE];
    get_deck(deck);

    int type_lookahead = (num_community_cards == 3)? 2 : 1;

    int hand_size = num_hole_cards + num_community_cards;
    int hand[hand_size];
    memcpy(hand, hole_cards, num_hole_cards * sizeof(int));
    memcpy(hand + num_hole_cards, community_cards, num_community_cards * sizeof(int));

    // Remove cards in hand from the deck
    int deck_size = DECK_SIZE;
    for (int i = 0; i < hand_size; i++)
    {
        for (int j = 0; j < deck_size; j++)
        {
            if (deck[j] == hand[i])
            {
                deck[j] = deck[--deck_size];
                break;
            }
        }
    }

    int current_rank_category = get_rank_category(hand, hand_size);

    double ahead = 0;
    double inconsequential = 0;

    // Iterate over possible combinations
    for (int i = 0; i < deck_size; i++)
    {
        if (type_lookahead == 1)
        {
            int full_hand[hand_size + 1];
            memcpy(full_hand, hand, hand_size * sizeof(int));
            full_hand[hand_size] = deck[i];
            int future_rank_category = get_rank_category(full_hand, hand_size + 1);

            if (future_rank_category < current_rank_category)
            {
                ahead++;
            }
            else if (future_rank_category == current_rank_category)
            {
                inconsequential++;
            }
        }
        else if (type_lookahead == 2 && num_community_cards == 3)
        {
            for (int j = i + 1; j < deck_size; j++)
            {
                int full_hand[hand_size + 2];
                memcpy(full_hand, hand, hand_size * sizeof(int));
                full_hand[hand_size] = deck[i];
                full_hand[hand_size + 1] = deck[j];
                int future_rank_category = get_rank_category(full_hand, hand_size + 2);

                if (future_rank_category < current_rank_category)
                {
                    ahead++;
                }
                else if (future_rank_category == current_rank_category)
                {
                    inconsequential++;
                }
            }
        }
    }

    double total = ahead + inconsequential;
    return total == 0 ? 0 : ahead / total;
}

int main()
{
    int hole_cards[] = {0, 1};         // Example: Deuce of clubs and trey of clubs
    int community_cards[] = {4, 5, 6}; // Example: Six of clubs, seven of clubs, eight of clubs
    int type_lookahead = 2;

    double result = potential(hole_cards, 2, community_cards, 3);
    printf("Potential: %f\n", result);

    return 0;
}
